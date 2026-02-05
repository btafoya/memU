# Production Ollama Deployment Design

**Date:** 2026-02-05
**Status:** Approved
**Deployment Tool:** podman-compose

## Overview & Architecture

### Current State
The docker-compose.yml has two services: `memu` (the application) and `db` (PostgreSQL with pgvector). Currently configured for development with placeholder credentials and `host.docker.internal` for Ollama access.

### Target State
Production-ready setup for podman-compose with:
- Ollama endpoint pointing to `http://192.168.25.165:11434/api`
- Secrets managed via `.env` file (excluded from git)
- `.env.example` template for documentation
- Hardened configuration with restart policies, healthchecks, and resource limits

### Deployment Context
- Running on the same host as Ollama (192.168.25.165)
- Using podman-compose for container orchestration
- Production environment with security hardening

### Key Changes
1. **Environment Management**: Move all secrets to `.env` file, reference via `${VAR}` syntax
2. **Ollama Configuration**: Update `OLLAMA_API_BASE_URL` to production endpoint
3. **Production Hardening**: Add restart policies (`unless-stopped`), healthchecks for both services, memory/CPU limits
4. **Security**: Remove volume mount of current directory in production, use stronger database credentials

## Environment Configuration

### `.env` File Structure
Create a `.env` file with all sensitive configuration. This file will be added to `.gitignore` to prevent accidental commits.

```bash
# API Keys
OPENAI_API_KEY=sk-your-actual-key-here
OPENROUTER_API_KEY=your-openrouter-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Ollama Configuration
OLLAMA_API_BASE_URL=http://192.168.25.165:11434/api

# Database Configuration
POSTGRES_DB=memu_db
POSTGRES_USER=memu_production_user
POSTGRES_PASSWORD=your-strong-password-here
MEMU_DB_URL=postgresql+psycopg://memu_production_user:your-strong-password-here@db:5432/memu_db

# Resource Limits (optional)
MEMU_MEMORY_LIMIT=2g
DB_MEMORY_LIMIT=1g
```

### `.env.example` Template
A committed template file with placeholder values and comments explaining what each variable does. This serves as documentation for anyone deploying the system.

### `.gitignore` Update
Add `.env` if not already present to prevent credential leaks.

## Docker-Compose Updates

### Service: memu
- Replace hardcoded environment variables with `${VAR}` references to `.env`
- Update `OLLAMA_API_BASE_URL` to use `${OLLAMA_API_BASE_URL}`
- Remove the `.:/app` volume mount (production shouldn't mount source code)
- Add restart policy: `restart: unless-stopped`
- Add memory limit: `mem_limit: ${MEMU_MEMORY_LIMIT:-2g}`
- Add healthcheck: HTTP check on port 8000
- Add logging configuration for log rotation

### Service: db
- Replace hardcoded credentials with `${POSTGRES_*}` variables
- Add restart policy: `restart: unless-stopped`
- Add memory limit: `mem_limit: ${DB_MEMORY_LIMIT:-1g}`
- Add healthcheck: PostgreSQL connection check using `pg_isready`
- Keep the data volume for persistence
- Add logging configuration for log rotation

### Podman Compatibility
The configuration will work with both `docker-compose` and `podman-compose` - no special syntax needed. The main difference is podman uses `host.containers.internal` instead of `host.docker.internal`, but since we're using an explicit IP (192.168.25.165), this doesn't matter.

## Production Hardening

### Restart Policies
- `restart: unless-stopped` on both services ensures they survive host reboots and crashes, but won't restart if manually stopped (good for maintenance)

### Healthchecks
- **memu service**: HTTP GET to `http://localhost:8000/health` (or root endpoint) every 30s, 3 retries, 10s timeout
- **db service**: `pg_isready -U ${POSTGRES_USER}` command every 10s, starts checking after 10s initial delay

### Resource Limits
- Memory limits prevent OOM scenarios from affecting the host
- Defaults: 2GB for memu, 1GB for database (configurable via .env)
- CPU limits optional - can add `cpus: '1.0'` if needed

### Dependency Management
- Keep `depends_on` but note: healthchecks don't affect startup order in compose v3 (would need v2.1 or orchestrator like Kubernetes for true health-based dependencies)

### Logging
- Add log rotation: `max-size: "10m"`, `max-file: "3"` to prevent disk filling

## Security Improvements

### Volume Security
- **Remove development volume mount**: The `.:/app` mount in the memu service will be removed. Production containers should run from the built image, not mount source code
- **Database volume**: Keep `postgres_data` volume for data persistence, but it's isolated and managed by the container

### Network Isolation
- Both services communicate over Docker's internal network (default bridge)
- Only expose necessary ports: 8000 (memu API) and 5432 (database)
- Consider: Remove port 5432 exposure if database access is only needed internally

### Credential Security
- All secrets in `.env` file (mode 600 recommended: `chmod 600 .env`)
- `.env` in `.gitignore` prevents accidental commits
- Use strong passwords for `POSTGRES_PASSWORD` (recommend 32+ character random string)

### Read-Only Filesystem (Optional)
- Could add `read_only: true` to containers with `tmpfs` mounts for writable areas
- May require application testing to ensure compatibility
- **Decision**: Not implementing in initial production setup; can be added later if needed

## Deployment Steps

### Files to Create/Modify

1. **`.env`** - Production environment file with your actual secrets (user fills in actual values)
2. **`.env.example`** - Template with documentation for each variable
3. **`docker-compose.yml`** - Updated with all the hardening and environment variable references
4. **`.gitignore`** - Add `.env` if not already present

### Execution Steps

1. Update `docker-compose.yml` with production configuration
2. Create `.env.example` template
3. Create `.env` file (user edits with actual API keys and passwords)
4. Update `.gitignore` to exclude `.env`
5. Stop any running containers: `podman-compose down`
6. Build fresh images: `podman-compose build`
7. Start production setup: `podman-compose up -d`
8. Verify healthchecks: `podman-compose ps` (should show "healthy" status)
9. Test Ollama connectivity from within the memu container
10. Check logs for any errors: `podman-compose logs -f`

### Validation Criteria
- Healthchecks passing for both services
- Application can reach Ollama at the production endpoint (http://192.168.25.165:11434/api)
- Database connection working
- No errors in logs
- Services restart automatically after system reboot
