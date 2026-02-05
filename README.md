![MemU Banner](assets/banner.png)

<div align="center">

# memU

### 24/7 Always-On Proactive Memory for AI Agents

[![PyPI version](https://badge.fury.io/py/memu-py.svg)](https://badge.fury.io/py/memu-py)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.3.0-brightgreen.svg)](https://github.com/btafoya/MemU/releases)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://github.com/btafoya/MemU/blob/main/docker-compose.yml)
[![Ollama](https://img.shields.io/badge/Ollama-supported-orange.svg)](https://ollama.ai)
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white)](https://discord.gg/memu)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?logo=x&logoColor=white)](https://x.com/memU_ai)

<a href="https://trendshift.io/repositories/17374" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17374" alt="NevaMind-AI%2FmemU | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

**[English](readme/README_en.md) | [中文](readme/README_zh.md) | [日本語](readme/README_ja.md) | [한국어](readme/README_ko.md) | [Español](readme/README_es.md) | [Français](readme/README_fr.md)**

</div>

---

memU is a memory framework built for **24/7 proactive agents**.
It is designed for long-running use and greatly **reduces the LLM token cost** of keeping agents always online, making always-on, evolving agents practical in production systems.
memU **continuously captures and understands user intent**. Even without a command, the agent can tell what you are about to do and act on it by itself.

---

## 📚 Table of Contents

- [Features](#-core-features)
- [How Proactive Memory Works](#-how-proactive-memory-works)
- [Memory Architecture](#️-hierarchical-memory-architecture)
- [Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Production Deployment](#production-deployment-with-dockerpodman)
- [LLM Provider Integration](#llm-provider-integration)
  - [Ollama](#ollama-integration)
  - [OpenRouter](#openrouter-integration)
  - [Custom Providers](#custom-llm-and-embedding-providers)
- [Core APIs](#-core-apis)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🤖 Self-Hosted Bot Integration

<img width="100%" src="https://github.com/btafoya/MemU/blob/main/assets/memUbot.png" />

Deploy your own AI bot with persistent memory:

- **🚀 Self-hosted**: Complete control over your data and infrastructure
- **🧠 Long-term memory**: Understands user intent and acts proactively
- **💰 Cost efficient**: Cuts LLM token cost with smaller context
- **🔌 Platform integrations**: Rocket.Chat, Discord, Slack (via adapters)

**Rocket.Chat Integration**: Built-in bot for enterprise team collaboration
```python
from memu.integrations.rocketchat import RocketChatBot

bot = RocketChatBot(
    memory_service=service,
    rocket_user="bot@example.com",
    rocket_password="password",
    rocket_url="https://chat.example.com"
)
await bot.run()
```

See [Rocket.Chat Integration Guide](src/memu/integrations/rocketchat/README.md) for setup instructions.

---

## 🗃️ Memory as File System, File System as Memory

memU treats **memory like a file system**—structured, hierarchical, and instantly accessible.

| File System | memU Memory |
|-------------|-------------|
| 📁 Folders | 🏷️ Categories (auto-organized topics) |
| 📄 Files | 🧠 Memory Items (extracted facts, preferences, skills) |
| 🔗 Symlinks | 🔄 Cross-references (related memories linked) |
| 📂 Mount points | 📥 Resources (conversations, documents, images) |

**Why this matters:**
- **Navigate memories** like browsing directories—drill down from broad categories to specific facts
- **Mount new knowledge** instantly—conversations and documents become queryable memory
- **Cross-link everything**—memories reference each other, building a connected knowledge graph
- **Persistent & portable**—export, backup, and transfer memory like files

```
memory/
├── preferences/
│   ├── communication_style.md
│   └── topic_interests.md
├── relationships/
│   ├── contacts/
│   └── interaction_history/
├── knowledge/
│   ├── domain_expertise/
│   └── learned_skills/
└── context/
    ├── recent_conversations/
    └── pending_tasks/
```

Just as a file system turns raw bytes into organized data, memU transforms raw interactions into **structured, searchable, proactive intelligence**.

---

## ⭐️ Star the repository

<img width="100%" src="https://github.com/btafoya/MemU/blob/main/assets/star.gif" />
If you find memU useful or interesting, a GitHub Star ⭐️ would be greatly appreciated.

---


## ✨ Core Features

| Capability | Description | Benefits |
|------------|-------------|----------|
| 🤖 **24/7 Proactive Agent** | Always-on memory agent that works continuously in the background—never sleeps, never forgets | Anticipates user needs before they ask |
| 🎯 **User Intention Capture** | Understands and remembers user goals, preferences, and context across sessions automatically | Personalized experiences that improve over time |
| 💰 **Cost Efficient** | Reduces long-running token costs by caching insights and avoiding redundant LLM calls | 10-100x reduction in token usage for long-running agents |
| 🗃️ **Hierarchical Memory** | Three-layer architecture (Resource → Item → Category) for efficient storage and retrieval | Fast queries, organized knowledge, automatic categorization |
| 🔌 **Multi-Provider Support** | Works with OpenAI, Ollama, OpenRouter, and custom LLM providers | Deploy anywhere: cloud, on-premise, or hybrid |
| 🐳 **Production Ready** | Docker/Podman support with health checks, auto-restart, and monitoring | Deploy to production in minutes |
| 🔐 **Privacy First** | Local deployment option with Ollama for complete data privacy | Keep sensitive data on your infrastructure |
| 🚀 **Real-time Processing** | Immediate memory extraction and retrieval with async support | No waiting, instant context availability |

### Why MemU?

| Feature | MemU | Traditional RAG | Vector Databases Only |
|---------|------|-----------------|----------------------|
| **Proactive Intelligence** | ✅ Anticipates needs | ❌ Reactive only | ❌ Query-based only |
| **Automatic Categorization** | ✅ Self-organizing | ⚠️ Manual tags | ❌ Flat structure |
| **Cost Optimization** | ✅ Smart caching | ⚠️ Full context each time | ⚠️ Embedding costs |
| **Long-term Memory** | ✅ Multi-session learning | ⚠️ Session-limited | ✅ Persistent |
| **Cross-reference Linking** | ✅ Knowledge graph | ❌ Independent chunks | ⚠️ Similarity only |
| **Production Deployment** | ✅ Docker-ready | ⚠️ DIY | ⚠️ Infrastructure only |
| **Local LLM Support** | ✅ Ollama integration | ⚠️ Limited | N/A |

---

## 🔄 How Proactive Memory Works

```bash

cd examples/proactive
python proactive.py

```

---

### Proactive Memory Lifecycle
```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         USER QUERY                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                 │                                                           │
                 ▼                                                           ▼
┌────────────────────────────────────────┐         ┌────────────────────────────────────────────────┐
│         🤖 MAIN AGENT                  │         │              🧠 MEMU BOT                       │
│                                        │         │                                                │
│  Handle user queries & execute tasks   │  ◄───►  │  Monitor, memorize & proactive intelligence   │
├────────────────────────────────────────┤         ├────────────────────────────────────────────────┤
│                                        │         │                                                │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  1. RECEIVE USER INPUT           │  │         │  │  1. MONITOR INPUT/OUTPUT                 │  │
│  │     Parse query, understand      │  │   ───►  │  │     Observe agent interactions           │  │
│  │     context and intent           │  │         │  │     Track conversation flow              │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  2. PLAN & EXECUTE               │  │         │  │  2. MEMORIZE & EXTRACT                   │  │
│  │     Break down tasks             │  │   ◄───  │  │     Store insights, facts, preferences   │  │
│  │     Call tools, retrieve data    │  │  inject │  │     Extract skills & knowledge           │  │
│  │     Generate responses           │  │  memory │  │     Update user profile                  │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  3. RESPOND TO USER              │  │         │  │  3. PREDICT USER INTENT                  │  │
│  │     Deliver answer/result        │  │   ───►  │  │     Anticipate next steps                │  │
│  │     Continue conversation        │  │         │  │     Identify upcoming needs              │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  4. LOOP                         │  │         │  │  4. RUN PROACTIVE TASKS                  │  │
│  │     Wait for next user input     │  │   ◄───  │  │     Pre-fetch relevant context           │  │
│  │     or proactive suggestions     │  │  suggest│  │     Prepare recommendations              │  │
│  └──────────────────────────────────┘  │         │  │     Update todolist autonomously         │  │
│                                        │         │  └──────────────────────────────────────────┘  │
└────────────────────────────────────────┘         └────────────────────────────────────────────────┘
                 │                                                           │
                 └───────────────────────────┬───────────────────────────────┘
                                             ▼
                              ┌──────────────────────────────┐
                              │     CONTINUOUS SYNC LOOP     │
                              │  Agent ◄──► MemU Bot ◄──► DB │
                              └──────────────────────────────┘
```

---

## 🎯 Proactive Use Cases

### 1. **Information Recommendation**
*Agent monitors interests and proactively surfaces relevant content*
```python
# User has been researching AI topics
MemU tracks: reading history, saved articles, search queries

# When new content arrives:
Agent: "I found 3 new papers on RAG optimization that align with
        your recent research on retrieval systems. One author
        (Dr. Chen) you've cited before published yesterday."

# Proactive behaviors:
- Learns topic preferences from browsing patterns
- Tracks author/source credibility preferences
- Filters noise based on engagement history
- Times recommendations for optimal attention
```

### 2. **Email Management**
*Agent learns communication patterns and handles routine correspondence*
```python
# MemU observes email patterns over time:
- Response templates for common scenarios
- Priority contacts and urgent keywords
- Scheduling preferences and availability
- Writing style and tone variations

# Proactive email assistance:
Agent: "You have 12 new emails. I've drafted responses for 3 routine
        requests and flagged 2 urgent items from your priority contacts.
        Should I also reschedule tomorrow's meeting based on the
        conflict John mentioned?"

# Autonomous actions:
✓ Draft context-aware replies
✓ Categorize and prioritize inbox
✓ Detect scheduling conflicts
✓ Summarize long threads with key decisions
```

### 3. **Trading & Financial Monitoring**
*Agent tracks market context and user investment behavior*
```python
# MemU learns trading preferences:
- Risk tolerance from historical decisions
- Preferred sectors and asset classes
- Response patterns to market events
- Portfolio rebalancing triggers

# Proactive alerts:
Agent: "NVDA dropped 5% in after-hours trading. Based on your past
        behavior, you typically buy tech dips above 3%. Your current
        allocation allows for $2,000 additional exposure while
        maintaining your 70/30 equity-bond target."

# Continuous monitoring:
- Track price alerts tied to user-defined thresholds
- Correlate news events with portfolio impact
- Learn from executed vs. ignored recommendations
- Anticipate tax-loss harvesting opportunities
```


...

---

## 🗂️ Hierarchical Memory Architecture

MemU's three-layer system enables both **reactive queries** and **proactive context loading**:

<img width="100%" alt="structure" src="assets/structure.png" />

| Layer | Reactive Use | Proactive Use |
|-------|--------------|---------------|
| **Resource** | Direct access to original data | Background monitoring for new patterns |
| **Item** | Targeted fact retrieval | Real-time extraction from ongoing interactions |
| **Category** | Summary-level overview | Automatic context assembly for anticipation |

**Proactive Benefits:**
- **Auto-categorization**: New memories self-organize into topics
- **Pattern Detection**: System identifies recurring themes
- **Context Prediction**: Anticipates what information will be needed next

---

## 🚀 Quick Start

### System Requirements

**Minimum**:
- Python 3.13+
- 4GB RAM (8GB recommended)
- 2GB disk space
- One of: OpenAI API key, Ollama, or compatible LLM provider

**Recommended for Production**:
- Python 3.13+
- 8GB+ RAM (16GB for Ollama with larger models)
- 10GB disk space
- PostgreSQL 16+ with pgvector extension
- Docker/Podman for containerized deployment
- Ollama with GPU for optimal performance

#### Installation

**From PyPI** (stable):
```bash
pip install memu-py

# With PostgreSQL support
pip install memu-py[postgres]

# With all optional dependencies
pip install memu-py[postgres,langgraph,claude,rocketchat]
```

**From Source** (latest):
```bash
# Clone the repository
git clone https://github.com/btafoya/MemU.git
cd MemU

# Install in development mode
pip install -e .

# Or with extras
pip install -e ".[postgres,langgraph]"
```

#### Configuration

Before running memU, configure your environment variables. You have several options:

**Option 1: Environment Variables** (Quick testing):
```bash
# For OpenAI
export OPENAI_API_KEY=sk-your-key-here

# For Ollama (local)
export OLLAMA_API_BASE_URL=http://localhost:11434/api

# For OpenRouter
export OPENROUTER_API_KEY=your-key-here
export OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# For PostgreSQL (if using persistent storage)
export MEMU_DB_URL=postgresql+psycopg://user:password@localhost:5432/memu_db
```

**Option 2: .env File** (Recommended for development):
```bash
# Create .env file
cat > .env << EOF
# Choose your LLM provider (pick one):
OPENAI_API_KEY=sk-your-key-here
# OR
OLLAMA_API_BASE_URL=http://localhost:11434/api
# OR
OPENROUTER_API_KEY=your-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Database (optional, defaults to in-memory)
MEMU_DB_URL=postgresql+psycopg://user:password@localhost:5432/memu_db

# Resource limits (optional)
MEMU_MEMORY_LIMIT=2g
DB_MEMORY_LIMIT=1g
EOF
```

**Available Environment Variables**:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | No* | OpenAI API key | None |
| `OLLAMA_API_BASE_URL` | No* | Ollama endpoint | `http://localhost:11434/api` |
| `OPENROUTER_API_KEY` | No* | OpenRouter API key | None |
| `OPENROUTER_BASE_URL` | No | OpenRouter endpoint | `https://openrouter.ai/api/v1` |
| `MEMU_DB_URL` | No | PostgreSQL connection URL | In-memory storage |
| `POSTGRES_DB` | No | Database name | `memu_db` |
| `POSTGRES_USER` | No | Database user | `postgres` |
| `POSTGRES_PASSWORD` | No | Database password | None |
| `MEMU_MEMORY_LIMIT` | No | Container memory limit | `2g` |
| `DB_MEMORY_LIMIT` | No | Database memory limit | `1g` |

\* At least one LLM provider (OpenAI, Ollama, or OpenRouter) is required.

#### Quick Start Examples

**Example 1: With Ollama (Local, No API Key)**:
```bash
# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# Set environment
export OLLAMA_API_BASE_URL=http://localhost:11434/api

# Run example
cd examples
python example_6_ollama_memory.py
```

**Example 2: With OpenAI**:
```bash
# Set environment
export OPENAI_API_KEY=sk-your-key-here

# Run in-memory test
cd tests
python test_inmemory.py
```

**Example 3: With PostgreSQL (Persistent Storage)**:
```bash
# Start PostgreSQL with pgvector
docker run -d \
  --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Set environment
export OPENAI_API_KEY=sk-your-key-here
export MEMU_DB_URL=postgresql+psycopg://postgres:postgres@localhost:5432/memu

# Run persistent storage test
cd tests
python test_postgres.py
```

All examples demonstrate **proactive memory workflows**:
1. **Continuous Ingestion**: Process multiple files sequentially
2. **Auto-Extraction**: Immediate memory creation
3. **Proactive Retrieval**: Context-aware memory surfacing

See [`examples/`](examples/) directory for more examples.

---

### Production Deployment with Docker/Podman

Deploy memU in production using Docker Compose or Podman Compose with PostgreSQL and Ollama support:

#### Prerequisites
- Docker/Podman and Docker Compose/Podman Compose installed
- Ollama instance running (local or remote)

#### Quick Start

1. **Configure environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your values:
# - OLLAMA_API_BASE_URL: Your Ollama endpoint (e.g., http://192.168.25.165:11434/api)
# - POSTGRES_PASSWORD: Strong password for database
# - API keys if using OpenAI/OpenRouter
```

2. **Build and start services**:
```bash
# Using Docker Compose
docker-compose up -d

# Or using Podman Compose
podman-compose up -d
```

3. **Verify deployment**:
```bash
# Check container status
docker-compose ps  # or podman-compose ps

# Test the API
curl http://localhost:8000/
curl http://localhost:8000/health
```

#### Services

The deployment includes:
- **memU Service** (port 8000): FastAPI server with health endpoints
- **PostgreSQL** (port 5432): Database with pgvector extension
- **Automatic healthchecks** and restart policies for production reliability

#### Configuration

The deployment is configured via environment variables in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `OLLAMA_API_BASE_URL` | Ollama API endpoint | `http://192.168.25.165:11434/api` |
| `POSTGRES_PASSWORD` | Database password | `your-strong-password` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | `sk-...` |
| `OPENROUTER_API_KEY` | OpenRouter API key (optional) | `your-key` |
| `MEMU_MEMORY_LIMIT` | Memory limit for memU container | `2g` |
| `DB_MEMORY_LIMIT` | Memory limit for database | `1g` |

See `.env.example` for all available options.

#### HTTP API Endpoints

The production server exposes the following endpoints:

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Root health check | `{"status": "ok", "service": "MemU Memory Service", "version": "1.3.0", "ollama_endpoint": "..."}` |
| `/health` | GET | Detailed health status | `{"status": "healthy", "database": "...", "ollama": "..."}` |
| `/api/status` | GET | API status information | `{"api_version": "v1", "memory_service": "initialized/not initialized"}` |

**Example requests**:
```bash
# Check service health
curl http://localhost:8000/

# Get detailed health information
curl http://localhost:8000/health

# Check API status
curl http://localhost:8000/api/status
```

#### Monitoring & Observability

**Health Checks**:
- Containers include built-in healthchecks that run automatically
- Database: `pg_isready` check every 10 seconds
- memU Service: HTTP check on `/` endpoint every 30 seconds

**View logs**:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f memu
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 memu
```

**Monitor resource usage**:
```bash
# Container stats
docker stats

# Or with podman
podman stats
```

#### Backup & Recovery

**Database Backup**:
```bash
# Create backup
docker-compose exec db pg_dump -U memu_production_user memu_db > backup.sql

# Or backup the entire volume
docker run --rm -v memu_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_data_backup.tar.gz -C /data .
```

**Restore from Backup**:
```bash
# Restore SQL dump
cat backup.sql | docker-compose exec -T db psql -U memu_production_user memu_db

# Or restore volume
docker run --rm -v memu_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_data_backup.tar.gz -C /data
```

#### Troubleshooting

**Container won't start**:
```bash
# Check logs for errors
docker-compose logs memu
docker-compose logs db

# Verify environment variables
docker-compose config

# Check if ports are already in use
netstat -tulpn | grep -E '8000|5432'
```

**Database connection errors**:
```bash
# Verify database is healthy
docker-compose exec db pg_isready -U memu_production_user

# Check database logs
docker-compose logs db

# Test connection from memu container
docker-compose exec memu env | grep MEMU_DB_URL
```

**Ollama connectivity issues**:
```bash
# Test Ollama endpoint from host
curl http://192.168.25.165:11434/api/tags

# Test from memu container
docker-compose exec memu curl -f $OLLAMA_API_BASE_URL/tags

# Check firewall rules
sudo iptables -L -n | grep 11434
```

**Out of memory errors**:
```bash
# Check current resource limits
docker-compose config | grep mem_limit

# Adjust in .env file
echo "MEMU_MEMORY_LIMIT=4g" >> .env
echo "DB_MEMORY_LIMIT=2g" >> .env

# Restart services
docker-compose down && docker-compose up -d
```

#### Production Considerations

- **Security**:
  - Update default passwords in `.env` before deployment
  - Use strong passwords (32+ characters recommended)
  - Restrict database port exposure if not needed externally
  - Keep `.env` file permissions to 600: `chmod 600 .env`

- **Backups**:
  - The `postgres_data` volume contains your memory data
  - Schedule regular backups using cron or your backup solution
  - Test restore procedures periodically

- **Monitoring**:
  - Check logs regularly: `docker-compose logs -f`
  - Set up log aggregation for production (e.g., ELK, Loki)
  - Monitor container health and resource usage
  - Configure alerts for service failures

- **Updates**:
  - Rebuild after code changes: `docker-compose build`
  - Pull latest changes: `git pull origin main`
  - Review changelog before updating
  - Test updates in staging environment first

- **Scaling**:
  - Current setup is single-instance; for high availability, consider:
  - PostgreSQL replication for database redundancy
  - Load balancer for multiple memU instances
  - Shared storage for consistent state

---

### Ollama Integration

MemU supports [Ollama](https://ollama.ai) for local LLM inference, enabling privacy-focused deployments without external API dependencies.

#### Quick Start with Ollama

1. **Install and start Ollama**:
```bash
# Install Ollama (see https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

2. **Configure MemU**:
```python
from memu import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "client_backend": "ollama",
            "base_url": "http://localhost:11434/api",
            "chat_model": "llama2",
            "embed_model": "llama2"  # Or use a dedicated embedding model
        }
    },
    database_config={
        "metadata_store": {"provider": "inmemory"},
    }
)
```

3. **Run with production deployment**:
```bash
# Edit .env file
echo "OLLAMA_API_BASE_URL=http://localhost:11434/api" >> .env

# Start services
docker-compose up -d
```

#### Recommended Ollama Models

| Model | Size | Use Case | Memory Required |
|-------|------|----------|-----------------|
| `llama2` | 7B | General purpose, fast | 8GB |
| `llama2:13b` | 13B | Better quality | 16GB |
| `mistral` | 7B | Efficient, high quality | 8GB |
| `codellama` | 7B | Code-focused tasks | 8GB |
| `phi` | 2.7B | Lightweight, fast | 4GB |

#### Ollama Configuration Options

```python
service = MemoryService(
    llm_profiles={
        "default": {
            "client_backend": "ollama",
            "base_url": "http://localhost:11434/api",  # Ollama endpoint
            "chat_model": "llama2",                     # Model for chat/memorization
            "embed_model": "llama2",                    # Model for embeddings
            "temperature": 0.7,                         # Creativity (0.0-1.0)
            "top_p": 0.9,                              # Nucleus sampling
            "num_ctx": 4096,                           # Context window size
        }
    }
)
```

#### Remote Ollama Setup

For production deployments with Ollama on a different server:

```bash
# On Ollama server (192.168.25.165)
# Allow external connections
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# On memU server
# Update .env file
echo "OLLAMA_API_BASE_URL=http://192.168.25.165:11434/api" > .env

# Test connectivity
curl http://192.168.25.165:11434/api/tags
```

#### Performance Tuning

**GPU Acceleration**:
```bash
# Verify GPU is detected
ollama list

# Use GPU-enabled models
ollama run llama2:7b-gpu
```

**Concurrent Requests**:
```bash
# Set maximum concurrent requests
OLLAMA_NUM_PARALLEL=4 ollama serve
```

**Memory Optimization**:
```bash
# Limit GPU memory usage (in GiB)
OLLAMA_GPU_MEMORY_FRACTION=0.8 ollama serve
```

#### Example: Complete Ollama Workflow

```python
import asyncio
from memu import MemoryService

async def main():
    # Initialize with Ollama
    service = MemoryService(
        llm_profiles={
            "default": {
                "client_backend": "ollama",
                "base_url": "http://localhost:11434/api",
                "chat_model": "llama2",
            }
        }
    )

    # Memorize a conversation
    result = await service.memorize(
        resource_url="conversation.json",
        modality="conversation",
        user={"user_id": "user123"}
    )

    print(f"Extracted {len(result.memory_items)} memories")

    # Retrieve relevant memories
    memories = await service.retrieve(
        query="What are the user's preferences?",
        user={"user_id": "user123"}
    )

    print(f"Found {len(memories.memory_items)} relevant memories")

asyncio.run(main())
```

See [`examples/example_6_ollama_memory.py`](examples/example_6_ollama_memory.py) for a complete working example.

---

### Custom LLM and Embedding Providers

MemU supports custom LLM and embedding providers beyond OpenAI. Configure them via `llm_profiles`:
```python
from memu import MemUService

service = MemUService(
    llm_profiles={
        # Default profile for LLM operations
        "default": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "your_api_key",
            "chat_model": "qwen3-max",
            "client_backend": "sdk"  # "sdk" or "http"
        },
        # Separate profile for embeddings
        "embedding": {
            "base_url": "https://api.voyageai.com/v1",
            "api_key": "your_voyage_api_key",
            "embed_model": "voyage-3.5-lite"
        }
    },
    # ... other configuration
)
```

---

### OpenRouter Integration

MemU supports [OpenRouter](https://openrouter.ai) as a model provider, giving you access to multiple LLM providers through a single API.

#### Configuration
```python
from memu import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openrouter",
            "client_backend": "httpx",
            "base_url": "https://openrouter.ai",
            "api_key": "your_openrouter_api_key",
            "chat_model": "anthropic/claude-3.5-sonnet",  # Any OpenRouter model
            "embed_model": "openai/text-embedding-3-small",  # Embedding model
        },
    },
    database_config={
        "metadata_store": {"provider": "inmemory"},
    },
)
```

#### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key from [openrouter.ai/keys](https://openrouter.ai/keys) |

#### Supported Features

| Feature | Status | Notes |
|---------|--------|-------|
| Chat Completions | Supported | Works with any OpenRouter chat model |
| Embeddings | Supported | Use OpenAI embedding models via OpenRouter |
| Vision | Supported | Use vision-capable models (e.g., `openai/gpt-4o`) |

#### Running OpenRouter Tests
```bash
export OPENROUTER_API_KEY=your_api_key

# Full workflow test (memorize + retrieve)
python tests/test_openrouter.py

# Embedding-specific tests
python tests/test_openrouter_embedding.py

# Vision-specific tests
python tests/test_openrouter_vision.py
```

See [`examples/example_4_openrouter_memory.py`](examples/example_4_openrouter_memory.py) for a complete working example.

---

## 📖 Core APIs

### `memorize()` - Continuous Learning Pipeline

Processes inputs in real-time and immediately updates memory:

<img width="100%" alt="memorize" src="assets/memorize.png" />

```python
result = await service.memorize(
    resource_url="path/to/file.json",  # File path or URL
    modality="conversation",            # conversation | document | image | video | audio
    user={"user_id": "123"}             # Optional: scope to a user
)

# Returns immediately with extracted memory:
{
    "resource": {...},      # Stored resource metadata
    "items": [...],         # Extracted memory items (available instantly)
    "categories": [...]     # Auto-updated category structure
}
```

**Proactive Features:**
- Zero-delay processing—memories available immediately
- Automatic categorization without manual tagging
- Cross-reference with existing memories for pattern detection

### `retrieve()` - Dual-Mode Intelligence

MemU supports both **proactive context loading** and **reactive querying**:

<img width="100%" alt="retrieve" src="assets/retrieve.png" />

#### RAG-based Retrieval (`method="rag"`)

Fast **proactive context assembly** using embeddings:

- ✅ **Instant context**: Sub-second memory surfacing
- ✅ **Background monitoring**: Can run continuously without LLM costs
- ✅ **Similarity scoring**: Identifies most relevant memories automatically

#### LLM-based Retrieval (`method="llm"`)

Deep **anticipatory reasoning** for complex contexts:

- ✅ **Intent prediction**: LLM infers what user needs before they ask
- ✅ **Query evolution**: Automatically refines search as context develops
- ✅ **Early termination**: Stops when sufficient context is gathered

#### Comparison

| Aspect | RAG (Fast Context) | LLM (Deep Reasoning) |
|--------|-------------------|---------------------|
| **Speed** | ⚡ Milliseconds | 🐢 Seconds |
| **Cost** | 💰 Embedding only | 💰💰 LLM inference |
| **Proactive use** | Continuous monitoring | Triggered context loading |
| **Best for** | Real-time suggestions | Complex anticipation |

#### Usage
```python
# Proactive retrieval with context history
result = await service.retrieve(
    queries=[
        {"role": "user", "content": {"text": "What are their preferences?"}},
        {"role": "user", "content": {"text": "Tell me about work habits"}}
    ],
    where={"user_id": "123"},  # Optional: scope filter
    method="rag"  # or "llm" for deeper reasoning
)

# Returns context-aware results:
{
    "categories": [...],     # Relevant topic areas (auto-prioritized)
    "items": [...],          # Specific memory facts
    "resources": [...],      # Original sources for traceability
    "next_step_query": "..." # Predicted follow-up context
}
```

**Proactive Filtering**: Use `where` to scope continuous monitoring:
- `where={"user_id": "123"}` - User-specific context
- `where={"agent_id__in": ["1", "2"]}` - Multi-agent coordination
- Omit `where` for global context awareness

---

## 💡 Proactive Scenarios

### Example 1: Always-Learning Assistant

Continuously learns from every interaction without explicit memory commands:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_1_conversation_memory.py
```

**Proactive Behavior:**
- Automatically extracts preferences from casual mentions
- Builds relationship models from interaction patterns
- Surfaces relevant context in future conversations
- Adapts communication style based on learned preferences

**Best for:** Personal AI assistants, customer support that remembers, social chatbots

---

### Example 2: Self-Improving Agent

Learns from execution logs and proactively suggests optimizations:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_2_skill_extraction.py
```

**Proactive Behavior:**
- Monitors agent actions and outcomes continuously
- Identifies patterns in successes and failures
- Auto-generates skill guides from experience
- Proactively suggests strategies for similar future tasks

**Best for:** DevOps automation, agent self-improvement, knowledge capture

---

### Example 3: Multimodal Context Builder

Unifies memory across different input types for comprehensive context:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_3_multimodal_memory.py
```

**Proactive Behavior:**
- Cross-references text, images, and documents automatically
- Builds unified understanding across modalities
- Surfaces visual context when discussing related topics
- Anticipates information needs by combining multiple sources

**Best for:** Documentation systems, learning platforms, research assistants

---

## 📊 Performance

MemU achieves **92.09% average accuracy** on the Locomo benchmark across all reasoning tasks, demonstrating reliable proactive memory operations.

<img width="100%" alt="benchmark" src="https://github.com/user-attachments/assets/6fec4884-94e5-4058-ad5c-baac3d7e76d9" />

View detailed experimental data: [memU-experiment](https://github.com/btafoya/MemU-experiment)

---

## 🧩 Ecosystem

| Repository | Description | Proactive Features |
|------------|-------------|-------------------|
| **[memU](https://github.com/btafoya/MemU)** | Core proactive memory engine | 7×24 learning pipeline, auto-categorization |
| **[memU-server](https://github.com/btafoya/MemU-server)** | Backend with continuous sync | Real-time memory updates, webhook triggers |
| **[memU-ui](https://github.com/btafoya/MemU-ui)** | Visual memory dashboard | Live memory evolution monitoring |

**Quick Links:**
- 📚 [Documentation](https://github.com/btafoya/MemU/blob/main/README.md)
- 💬 [Discord Community](https://discord.gg/memu)
- 🐛 [Report Issues](https://github.com/btafoya/MemU/issues)

---

## 🤝 Partners

<div align="center">

<a href="https://github.com/TEN-framework/ten-framework"><img src="https://avatars.githubusercontent.com/u/113095513?s=200&v=4" alt="Ten" height="40" style="margin: 10px;"></a>
<a href="https://openagents.org"><img src="assets/partners/openagents.png" alt="OpenAgents" height="40" style="margin: 10px;"></a>
<a href="https://github.com/milvus-io/milvus"><img src="https://miro.medium.com/v2/resize:fit:2400/1*-VEGyAgcIBD62XtZWavy8w.png" alt="Milvus" height="40" style="margin: 10px;"></a>
<a href="https://xroute.ai/"><img src="assets/partners/xroute.png" alt="xRoute" height="40" style="margin: 10px;"></a>
<a href="https://jaaz.app/"><img src="assets/partners/jazz.png" alt="Jazz" height="40" style="margin: 10px;"></a>
<a href="https://github.com/Buddie-AI/Buddie"><img src="assets/partners/buddie.png" alt="Buddie" height="40" style="margin: 10px;"></a>
<a href="https://github.com/bytebase/bytebase"><img src="assets/partners/bytebase.png" alt="Bytebase" height="40" style="margin: 10px;"></a>
<a href="https://github.com/LazyAGI/LazyLLM"><img src="assets/partners/LazyLLM.png" alt="LazyLLM" height="40" style="margin: 10px;"></a>

</div>

---

## 🤝 How to Contribute

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Getting Started

To start contributing to MemU, you'll need to set up your development environment:

#### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Git

#### Setup Development Environment
```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/memU.git
cd memU

# 2. Install development dependencies
make install
```

The `make install` command will:
- Create a virtual environment using `uv`
- Install all project dependencies
- Set up pre-commit hooks for code quality checks

#### Running Quality Checks

Before submitting your contribution, ensure your code passes all quality checks:
```bash
make check
```

The `make check` command runs:
- **Lock file verification**: Ensures `pyproject.toml` consistency
- **Pre-commit hooks**: Lints code with Ruff, formats with Black
- **Type checking**: Runs `mypy` for static type analysis
- **Dependency analysis**: Uses `deptry` to find obsolete dependencies

### Contributing Guidelines

For detailed contribution guidelines, code standards, and development practices, please see [CONTRIBUTING.md](CONTRIBUTING.md).

**Quick tips:**
- Create a new branch for each feature or bug fix
- Write clear commit messages
- Add tests for new functionality
- Update documentation as needed
- Run `make check` before pushing

---

## ⚡ Performance & Best Practices

### Performance Benchmarks

**Memory Extraction** (memorize operation):
- Small documents (1-5 pages): 2-5 seconds
- Conversations (10-50 messages): 3-8 seconds
- Large documents (50+ pages): 15-30 seconds

**Memory Retrieval** (retrieve operation):
- RAG mode: 100-500ms (embedding-based)
- LLM mode: 2-5 seconds (reasoning-based)
- Hybrid mode: 1-3 seconds (best of both)

**Production Throughput**:
- Concurrent memorize: 10-50 ops/sec (depends on LLM provider)
- Concurrent retrieve: 100-500 ops/sec (RAG mode)
- PostgreSQL capacity: 10K+ memory items per user

### Best Practices

#### 1. Choose the Right Retrieval Method

```python
# For real-time suggestions (fast, low cost)
result = await service.retrieve(query="...", method="rag")

# For complex reasoning (slower, higher quality)
result = await service.retrieve(query="...", method="llm")

# For balanced performance
result = await service.retrieve(query="...", method="hybrid")
```

#### 2. Optimize Database Configuration

```python
# Use PostgreSQL for production
database_config = {
    "provider": "postgres",
    "url": "postgresql://user:pass@localhost/memu",
    "pool_size": 20,        # Adjust based on concurrency
    "max_overflow": 10,      # Extra connections for bursts
}

# Use in-memory for development/testing
database_config = {"provider": "inmemory"}
```

#### 3. Configure Resource Limits

```bash
# In .env file
MEMU_MEMORY_LIMIT=4g          # Increase for high-concurrency
DB_MEMORY_LIMIT=2g            # Scale with data volume
OLLAMA_NUM_PARALLEL=4         # Concurrent Ollama requests
```

#### 4. Batch Operations

```python
# Good: Batch multiple memorize operations
async def batch_memorize(files):
    tasks = [service.memorize(f) for f in files]
    results = await asyncio.gather(*tasks)
    return results

# Avoid: Sequential operations
for file in files:
    await service.memorize(file)  # Slower
```

#### 5. Scope Memory by User/Agent

```python
# Always scope memory to prevent context bleeding
await service.memorize(
    resource_url="data.json",
    user={"user_id": "user123"}  # Essential for multi-tenant
)

await service.retrieve(
    query="preferences",
    where={"user_id": "user123"}  # Filter by user
)
```

#### 6. Monitor and Debug

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Track performance
import time
start = time.time()
result = await service.memorize(...)
print(f"Memorize took {time.time() - start:.2f}s")

# Check memory usage
from memu.app import MemoryService
stats = await service.get_stats()  # Returns memory statistics
```

#### 7. Production Deployment Checklist

- [ ] Use PostgreSQL with pgvector (not in-memory)
- [ ] Configure proper resource limits in docker-compose.yml
- [ ] Set strong passwords in .env file
- [ ] Enable health checks and monitoring
- [ ] Set up automated backups for postgres_data volume
- [ ] Use connection pooling for high concurrency
- [ ] Configure log aggregation (ELK, Loki, etc.)
- [ ] Test failover and recovery procedures
- [ ] Monitor Ollama/LLM provider performance
- [ ] Set up alerting for service failures

### Troubleshooting Performance Issues

**Slow Retrieval**:
```bash
# Check database indexes
docker-compose exec db psql -U memu_production_user -d memu_db \
  -c "SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public';"

# Monitor query performance
docker-compose logs memu | grep "Query took"
```

**High Memory Usage**:
```bash
# Check container memory
docker stats memu_memu_1

# Reduce batch size or concurrency
# Adjust MEMU_MEMORY_LIMIT in .env
```

**Ollama Timeouts**:
```bash
# Increase timeout in Ollama
OLLAMA_TIMEOUT=300 ollama serve

# Use smaller models
ollama pull llama2:7b  # Instead of 13b or 70b

# Enable GPU acceleration
nvidia-smi  # Verify GPU is available
```

---

## ❓ Frequently Asked Questions

### General

**Q: What makes MemU different from other memory frameworks?**
A: MemU is designed for 24/7 proactive agents with automatic categorization, cross-referencing, and cost-optimized token usage. Unlike traditional RAG systems, MemU anticipates what you'll need before you ask.

**Q: Can I use MemU without an internet connection?**
A: Yes! Deploy with Ollama for completely offline operation. All data stays on your infrastructure.

**Q: What's the recommended model for production?**
A: For OpenAI: GPT-4 or GPT-3.5-turbo. For Ollama: llama2:13b or mistral. For cost-efficiency: OpenRouter with smaller models.

### Deployment

**Q: What are the minimum system requirements?**
A: 4GB RAM, Python 3.13+, and an LLM provider (OpenAI API, Ollama, or compatible). 8GB+ RAM recommended for production.

**Q: Can I run multiple MemU instances?**
A: Yes! Use a shared PostgreSQL database and configure each instance with unique identifiers. Consider load balancing for high availability.

**Q: How do I migrate from in-memory to PostgreSQL?**
A: Export data using the backup tools, set up PostgreSQL with pgvector, update database_config, and import data. See the backup section for details.

### Data & Privacy

**Q: Where is my data stored?**
A: With PostgreSQL: in the postgres_data Docker volume. With in-memory: in RAM (lost on restart). For Ollama: models stored locally.

**Q: Is my data encrypted?**
A: Database connections support TLS/SSL. For encryption at rest, use encrypted volumes or managed PostgreSQL services with encryption enabled.

**Q: Can I export my memories?**
A: Yes! Use `service.export_memories()` or backup the PostgreSQL database directly. Memories are stored in standard SQL format.

### Performance

**Q: How many memories can MemU handle?**
A: 10,000+ memories per user with PostgreSQL. For larger scales (100K+ memories), consider partitioning by time or category.

**Q: What's the latency for retrieval?**
A: RAG mode: 100-500ms. LLM mode: 2-5 seconds. Latency depends on your LLM provider and model size.

**Q: Can I use MemU with multiple LLM providers?**
A: Yes! Configure different profiles for different operations (e.g., GPT-4 for memorization, local Ollama for retrieval).

### Troubleshooting

**Q: Why is memorize() slow?**
A: Check your LLM provider response time. Use smaller models for faster processing. Enable concurrent processing for batch operations.

**Q: How do I fix "connection refused" errors?**
A: Verify PostgreSQL is running (`docker-compose ps`), check connection string in .env, ensure firewall allows connections on port 5432.

**Q: Ollama returns empty responses?**
A: Verify the model is pulled (`ollama list`), check Ollama is running (`curl http://localhost:11434/api/tags`), increase timeout settings.

---

## 📝 Version History

### v1.3.0 (Current)
- ✨ Added production Docker/Podman deployment support
- ✨ Integrated Ollama for local LLM inference
- ✨ Added FastAPI HTTP server with health endpoints
- ✨ Improved PostgreSQL setup with pgvector
- ✨ Added Rocket.Chat bot integration
- 🐛 Fixed environment variable handling
- 📚 Comprehensive documentation updates

### v1.2.x
- Feature additions for langgraph and multi-modal support
- Performance improvements for large-scale deployments

### v1.1.x
- Initial stable release with core memory framework
- OpenAI and OpenRouter integration
- Basic PostgreSQL support

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**:
   - Add tests for new functionality
   - Update documentation as needed
   - Follow the existing code style
4. **Run tests**: `pytest tests/`
5. **Run linters**: `ruff check . && ruff format .`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/MemU.git
cd MemU

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Run linters
ruff check .
ruff format .
```

### Code Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for public APIs
- Add tests for new features
- Keep PRs focused on a single feature/fix

---

## 📄 License

[Apache License 2.0](LICENSE.txt)

---

## 🌍 Community

- **GitHub Issues**: [Report bugs & request features](https://github.com/btafoya/MemU/issues)
- **Discussions**: [Join discussions](https://github.com/btafoya/MemU/discussions)
- **Discord**: [Join the community](https://discord.com/invite/hQZntfGsbJ)
- **X (Twitter)**: [Follow @memU_ai](https://x.com/memU_ai)

---

<div align="center">

⭐ **Star us on GitHub** to get notified about new releases!

</div>
