# Rocket.Chat Bot with Ollama: Complete Guide

Deploy a privacy-focused, memory-enabled Rocket.Chat bot using MemU and Ollama for local LLM inference.

## Overview

This guide demonstrates how to build and deploy a production-ready Rocket.Chat bot with:
- **Long-term memory**: Remembers user preferences and conversation history
- **Local LLM inference**: Runs completely offline using Ollama
- **User-scoped memory**: Each user has their own isolated memory context
- **Privacy-first**: All data stays on your infrastructure

## Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  Rocket.Chat    │ ◄────── │   MemU Bot      │ ◄────── │     Ollama      │
│   Server        │         │  (Python)       │         │  (Local LLM)    │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   PostgreSQL    │
                            │  (Memory Store) │
                            └─────────────────┘
```

## Prerequisites

### Required Components

1. **Rocket.Chat Server**
   - Self-hosted instance or cloud subscription
   - Version 3.0+ recommended
   - Admin access to create bot user

2. **Ollama**
   - Local LLM inference engine
   - 8GB+ RAM for llama2
   - Optional: GPU for faster inference

3. **Python 3.13+**
   - With pip or uv package manager

4. **PostgreSQL** (recommended for production)
   - Version 12+ with pgvector extension
   - Optional: Use in-memory storage for testing

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8GB | 16GB |
| Storage | 10GB | 50GB |
| Network | 10 Mbps | 100 Mbps |

## Step-by-Step Setup

### Step 1: Install Ollama

**Linux / macOS:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the llama2 model (7B parameters)
ollama pull llama2

# Verify installation
ollama list
```

**Windows:**
1. Download installer from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Open PowerShell and run:
```powershell
ollama pull llama2
ollama list
```

**Verify Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

Expected output: JSON list of installed models.

### Step 2: Set Up Rocket.Chat Bot User

1. **Log in to Rocket.Chat as admin**

2. **Create a new user**:
   - Go to **Administration** → **Users** → **New**
   - Username: `membot` (or your choice)
   - Email: `membot@example.com`
   - Password: Create a strong password
   - Roles: Select **bot**
   - Enable: ✅ Verified

3. **Grant bot permissions**:
   - Go to **Administration** → **Permissions**
   - Search for "bot" role
   - Ensure these permissions are enabled:
     - `view-c-room` (view channel messages)
     - `post-readonly` (post to channels)
     - `view-history` (read message history)

4. **Add bot to channels**:
   - Go to each channel where you want the bot
   - Click channel settings → **Members** → **Add**
   - Add `membot` user

### Step 3: Install MemU with Dependencies

```bash
# Clone the repository
git clone https://github.com/btafoya/MemU.git
cd MemU

# Install with Rocket.Chat support
pip install ".[rocketchat]"

# Or for full features (PostgreSQL + Rocket.Chat)
pip install ".[postgres,rocketchat]"
```

### Step 4: Configure Environment Variables

Create a `.env` file in your project directory:

```bash
# Rocket.Chat Configuration
ROCKETCHAT_URL=https://chat.example.com
ROCKETCHAT_USER=membot
ROCKETCHAT_PASSWORD=your_secure_password

# Ollama Configuration (local inference)
OLLAMA_API_BASE_URL=http://localhost:11434/api

# Optional: PostgreSQL for persistent memory
MEMU_DB_URL=postgresql+psycopg://user:password@localhost:5432/memu_db

# Optional: Use OpenAI instead of Ollama
# OPENAI_API_KEY=sk-your-api-key
```

**Load environment variables:**
```bash
# Linux / macOS
export $(cat .env | xargs)

# Windows PowerShell
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    Set-Content env:\$name $value
}
```

### Step 5: Run the Bot

```bash
# From the examples directory
cd examples
python rocketchat_bot_ollama.py
```

Expected output:
```
============================================================
MemU Rocket.Chat Bot with Ollama Support
============================================================
2024-01-15 10:30:00 - memu.rocketchat_bot - INFO - 🏠 Using Ollama (local) for LLM inference
2024-01-15 10:30:00 - memu.rocketchat_bot - INFO -    Endpoint: http://localhost:11434/api
2024-01-15 10:30:01 - memu.rocketchat_bot - INFO - 🧠 Initializing MemoryService...
2024-01-15 10:30:02 - memu.rocketchat_bot - INFO - ✅ MemoryService initialized
2024-01-15 10:30:02 - memu.rocketchat_bot - INFO - 🤖 Bot connected to https://chat.example.com as @membot
2024-01-15 10:30:02 - memu.rocketchat_bot - INFO - 💬 Ready to receive messages!
2024-01-15 10:30:02 - memu.rocketchat_bot - INFO - 🚀 Bot polling started (interval: 5 seconds)
```

### Step 6: Test the Bot

1. **Send a message to the bot** in any channel where it's present:
   ```
   @membot Hello! I'm interested in Python programming.
   ```

2. **Bot response** (first interaction):
   ```
   I don't have any previous context about this topic. Feel free to share more so I can learn!
   ```

3. **Send another message**:
   ```
   @membot What do you remember about me?
   ```

4. **Bot response** (with memory):
   ```
   Based on what I remember about you:

   • You expressed interest in Python programming
   • This is our second conversation

   How can I help you further?
   ```

## Production Deployment

### Option 1: Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Ollama service
  ollama:
    image: ollama/ollama:latest
    container_name: memu-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  # Remove if no GPU

  # PostgreSQL with pgvector
  db:
    image: pgvector/pgvector:pg16
    container_name: memu-postgres
    environment:
      POSTGRES_DB: memu_db
      POSTGRES_USER: memu_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U memu_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MemU Rocket.Chat Bot
  membot:
    build: .
    container_name: memu-rocketchat-bot
    environment:
      ROCKETCHAT_URL: ${ROCKETCHAT_URL}
      ROCKETCHAT_USER: ${ROCKETCHAT_USER}
      ROCKETCHAT_PASSWORD: ${ROCKETCHAT_PASSWORD}
      OLLAMA_API_BASE_URL: http://ollama:11434/api
      MEMU_DB_URL: postgresql+psycopg://memu_user:${POSTGRES_PASSWORD}@db:5432/memu_db
    depends_on:
      db:
        condition: service_healthy
      ollama:
        condition: service_started
    restart: unless-stopped
    command: python examples/rocketchat_bot_ollama.py

volumes:
  postgres_data:
  ollama_data:
```

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir ".[postgres,rocketchat]"

# Copy application
COPY . .

CMD ["python", "examples/rocketchat_bot_ollama.py"]
```

**Start services:**
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f membot

# Stop services
docker-compose down
```

### Option 2: Systemd Service (Linux)

Create `/etc/systemd/system/memu-bot.service`:

```ini
[Unit]
Description=MemU Rocket.Chat Bot
After=network.target postgresql.service

[Service]
Type=simple
User=memu
WorkingDirectory=/opt/memu
Environment="ROCKETCHAT_URL=https://chat.example.com"
Environment="ROCKETCHAT_USER=membot"
Environment="ROCKETCHAT_PASSWORD=your_password"
Environment="OLLAMA_API_BASE_URL=http://localhost:11434/api"
Environment="MEMU_DB_URL=postgresql+psycopg://user:pass@localhost/memu_db"
ExecStart=/usr/bin/python3 examples/rocketchat_bot_ollama.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable memu-bot
sudo systemctl start memu-bot
sudo systemctl status memu-bot
```

## Configuration Guide

### Ollama Model Selection

| Model | Size | Speed | Quality | RAM Required |
|-------|------|-------|---------|--------------|
| `llama2` | 7B | Fast | Good | 8GB |
| `llama2:13b` | 13B | Medium | Better | 16GB |
| `mistral` | 7B | Fast | Excellent | 8GB |
| `codellama` | 7B | Fast | Code-focused | 8GB |
| `phi` | 2.7B | Very Fast | Basic | 4GB |

**Change model in code:**
```python
llm_config = {
    "client_backend": "ollama",
    "base_url": ollama_url,
    "chat_model": "mistral",  # Change here
    "embed_model": "mistral",
}
```

### Memory Categories

Customize memory organization in the code:

```python
service = MemoryService(
    llm_profiles={"default": llm_config},
    memorize_config={
        "memory_categories": [
            {
                "name": "User Preferences",
                "description": "User interests, preferences, and settings",
            },
            {
                "name": "Technical Topics",
                "description": "Programming languages, frameworks, tools discussed",
            },
            {
                "name": "Project Context",
                "description": "Active projects and their requirements",
            },
        ]
    },
)
```

### Polling Interval

Adjust message polling frequency:

```python
# Check for new messages every 3 seconds
await bot.run_polling(interval=3)

# Or every 10 seconds for lower resource usage
await bot.run_polling(interval=10)
```

## Troubleshooting

### Bot doesn't respond to messages

**Check bot is running:**
```bash
# If using systemd
sudo systemctl status memu-bot

# If running directly
ps aux | grep rocketchat_bot
```

**Check bot has channel access:**
- Verify bot user is added to the channel
- Check bot has required permissions (see Step 2)

**Check logs for errors:**
```bash
# Systemd
sudo journalctl -u memu-bot -f

# Docker
docker-compose logs -f membot

# Direct run
tail -f /path/to/logfile
```

### Ollama connection errors

**Verify Ollama is running:**
```bash
# Check service
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

**Check model is installed:**
```bash
ollama list

# If model missing, pull it
ollama pull llama2
```

**Check firewall settings:**
```bash
# Allow port 11434
sudo ufw allow 11434/tcp
```

### Slow response times

**Use a smaller model:**
```bash
# Switch from llama2:13b to llama2:7b
ollama pull llama2
```

**Enable GPU acceleration:**
```bash
# Verify GPU is detected
nvidia-smi

# Pull GPU-optimized model
ollama pull llama2:7b-gpu
```

**Adjust Ollama concurrency:**
```bash
# Allow more concurrent requests
OLLAMA_NUM_PARALLEL=4 ollama serve
```

### Memory/Database issues

**Check database connection:**
```bash
# Test PostgreSQL
psql -h localhost -U memu_user -d memu_db -c "SELECT 1;"
```

**Clear memory database (CAUTION: deletes all memories):**
```bash
psql -h localhost -U memu_user -d memu_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

**Switch to in-memory mode** (testing only):
```python
# Remove MEMU_DB_URL from environment
# MemU will use in-memory storage
```

## Advanced Features

### Multi-User Support

The bot automatically isolates memory by user:

```python
# Each user gets their own memory context
await self.memory_service.memorize(
    resource_url=file_path,
    modality="conversation",
    user={"user_id": user_id, "username": username},
)

# Retrieval is scoped to the user
retrieve_result = await self.memory_service.retrieve(
    queries=[{"role": "user", "content": msg_content}],
    where={"user_id": user_id},  # Filters by user
)
```

### Custom Response Logic

Modify `_process_message()` to customize behavior:

```python
async def _process_message(self, message: dict):
    # ... existing code ...

    # Custom logic: Check for commands
    if msg_content.startswith("/remember"):
        # Extract and store specific information
        info = msg_content.replace("/remember", "").strip()
        await self.memory_service.create_memory_item(
            memory_type="explicit",
            memory_content=info,
            user={"user_id": user_id}
        )
        response_text = f"✅ Remembered: {info}"

    elif msg_content.startswith("/forget"):
        # Clear user's memory
        response_text = "Memory clearing not implemented yet"

    else:
        # Normal memory-based response
        # ... existing retrieval logic ...
```

### Webhooks (Alternative to Polling)

For better performance, use Rocket.Chat webhooks:

1. **Create webhook in Rocket.Chat**:
   - Administration → Integrations → New Integration
   - Type: Outgoing Webhook
   - Event: Message Sent
   - URLs: `http://your-bot-server:8000/webhook`

2. **Modify bot to use FastAPI**:
```python
from fastapi import FastAPI, Request

app = FastAPI()
bot = None  # Initialize globally

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await bot._process_message(data)
    return {"success": True}

@app.on_event("startup")
async def startup():
    global bot
    bot = RocketChatBot(...)
```

## Performance Optimization

### Resource Limits

Set resource constraints in Docker:

```yaml
services:
  membot:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Batch Processing

Process multiple messages together:

```python
# Instead of processing messages one-by-one
for message in messages:
    await self._process_message(message)

# Batch process
tasks = [self._process_message(msg) for msg in messages]
await asyncio.gather(*tasks)
```

### Caching

Implement response caching for common queries:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_response(query: str, user_id: str):
    # Cache retrieval results
    return await self.memory_service.retrieve(...)
```

## Security Best Practices

1. **Use strong passwords** for bot account and database
2. **Restrict bot permissions** to only required channels
3. **Enable SSL/TLS** for Rocket.Chat connections
4. **Keep credentials in `.env`** file (not in code)
5. **Use PostgreSQL password authentication** in production
6. **Regularly backup** the memory database
7. **Monitor bot logs** for suspicious activity
8. **Use rate limiting** to prevent abuse

## Next Steps

- **Customize memory categories** for your use case
- **Implement custom commands** (/remember, /forget, /summary)
- **Add file processing** (documents, images, code)
- **Deploy monitoring** (Prometheus, Grafana)
- **Scale horizontally** with multiple bot instances
- **Integrate with other services** (Slack, Discord, Teams)

## Resources

- [MemU Documentation](https://github.com/btafoya/MemU)
- [Ollama Models](https://ollama.ai/library)
- [Rocket.Chat API](https://developer.rocket.chat)
- [Getting Started Tutorial](../tutorials/getting_started.md)

## Support

- **GitHub Issues**: [Report bugs](https://github.com/btafoya/MemU/issues)
- **Discord**: [Join community](https://discord.com/invite/hQZntfGsbJ)
- **Documentation**: [Read the docs](https://github.com/btafoya/MemU/blob/main/README.md)
