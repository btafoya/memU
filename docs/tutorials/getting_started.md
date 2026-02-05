# Quickstart: Adding Long-Term Memory to Python Agents

Welcome to MemU! This guide will help you add robust long-term memory capabilities to your Python agents in just a few minutes. Without MemU, LLMs are limited by their context window. MemU solves this by providing an intelligent, persistent memory layer.

## Prerequisites

Before we begin, ensure you have the following:

-   **Python 3.13+**: MemU takes advantage of modern Python features.
-   **LLM Provider** (choose one):
    -   **OpenAI API Key**: For cloud-based inference with OpenAI's models (`gpt-4o-mini`)
    -   **Ollama**: For local, privacy-focused inference without API costs

## Step-by-Step Guide

### 1. Installation

Install MemU using `pip` or `uv`:

```bash
pip install memu
# OR
uv add memu
```

### 2. LLM Provider Setup

MemU requires an LLM backend to function. You can choose between cloud-based (OpenAI) or local (Ollama) inference.

#### Option A: OpenAI (Cloud-Based)

MemU looks for the `OPENAI_API_KEY` environment variable.

**Linux / macOS / Git Bash:**
```bash
export OPENAI_API_KEY=sk-proj-your-api-key
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-proj-your-api-key"
```

#### Option B: Ollama (Local, Privacy-First)

For local inference without API costs or internet dependency:

1. **Install Ollama**:
```bash
# Linux / macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai
```

2. **Pull a model**:
```bash
# Lightweight model (recommended for getting started)
ollama pull llama2

# Or a more capable model
ollama pull mistral
```

3. **Verify Ollama is running**:
```bash
# Should return a list of installed models
curl http://localhost:11434/api/tags
```

4. **Set environment variable**:
```bash
# Linux / macOS
export OLLAMA_API_BASE_URL=http://localhost:11434/api

# Windows (PowerShell)
$env:OLLAMA_API_BASE_URL="http://localhost:11434/api"
```

### 3. The Robust Starter Script

Below is a complete, production-ready script that demonstrates the full lifecycle of a memory-enabled agent: **Initialization**, **Injection** (adding memory), and **Retrieval** (searching memory). The script automatically detects whether you're using OpenAI or Ollama.

Create a file named `getting_started.py` and paste the following code:

```python
"""
Getting Started with MemU: A Robust Example.

This script demonstrates the core lifecycle of MemU:
1.  **Initialization**: Auto-detecting and configuring LLM provider (OpenAI or Ollama).
2.  **Memory Injection**: Adding a specific memory with metadata.
3.  **Retrieval**: Searching for that memory using natural language.
4.  **Error Handling**: Catching common configuration issues.

Usage:
    # Option 1: With OpenAI
    export OPENAI_API_KEY=your_api_key_here
    python getting_started.py

    # Option 2: With Ollama (local)
    ollama pull llama2
    export OLLAMA_API_BASE_URL=http://localhost:11434/api
    python getting_started.py
"""

import asyncio
import logging
import os
import sys

from memu.app import MemoryService

# Configure logging to show info but suppress noisy libraries
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)


async def main() -> None:
    """Run the MemU lifecycle demonstration."""
    print(">>> MemU Getting Started Example")
    print("-" * 30)

    # 1. LLM Provider Detection
    # MemU supports both OpenAI (cloud) and Ollama (local).
    # We detect which provider is configured and use it.
    openai_key = os.getenv("OPENAI_API_KEY")
    ollama_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434/api")

    # Determine which provider to use
    if openai_key:
        provider = "openai"
        model_name = "gpt-4o-mini"
        llm_config = {
            "api_key": openai_key,
            "chat_model": model_name,
        }
        print(f"[*] Using OpenAI with model: {model_name}...")
    else:
        # Check if Ollama is available
        try:
            import httpx
            response = httpx.get(f"{ollama_url}/tags", timeout=5.0)
            if response.status_code == 200:
                provider = "ollama"
                model_name = "llama2"  # Default model
                llm_config = {
                    "client_backend": "ollama",
                    "base_url": ollama_url,
                    "chat_model": model_name,
                    "embed_model": model_name,
                }
                print(f"[*] Using Ollama (local) with model: {model_name}...")
            else:
                print("[!] Error: No LLM provider configured.")
                print("Please either:")
                print("  1. Set OPENAI_API_KEY: export OPENAI_API_KEY=sk-...")
                print("  2. Or install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
                return
        except Exception:
            print("[!] Error: No LLM provider configured.")
            print("Please either:")
            print("  1. Set OPENAI_API_KEY: export OPENAI_API_KEY=sk-...")
            print("  2. Or install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
            return

    try:
        # 2. Initialization
        # We initialize the MemoryService with:
        # - llm_profiles: Configuration for the LLM (model, api_key or Ollama endpoint).
        # - memorize_config: Pre-defining a memory category ensures we can organize memories efficiently.
        service = MemoryService(
            llm_profiles={"default": llm_config},
            memorize_config={
                "memory_categories": [
                    {
                        "name": "User Facts",
                        "description": "General and specific facts known about the user preference and identity.",
                    }
                ]
            },
        )
        print("[OK] Service initialized successfully.\n")

        # 3. Memory Injection
        # We manually inject a memory into the system.
        # This is useful for bootstrapping a user profile or adding explicit knowledge.
        print("[*] Injecting memory...")
        memory_content = "The user is a senior Python architect who loves clean code and type hints."

        # We use 'create_memory_item' to insert a single memory record.
        # memory_type='profile' indicates this is an attribute of the user.
        result = await service.create_memory_item(
            memory_type="profile",
            memory_content=memory_content,
            memory_categories=["User Facts"],
        )
        print(f"[OK] Memory created! ID: {result.get('memory_item', {}).get('id')}\n")

        # 4. Retrieval
        # Now we query the system naturally to see if it recalls the information.
        query_text = "What kind of code does the user like?"
        print(f"[*] Querying: '{query_text}'")

        search_results = await service.retrieve(
            queries=[{"role": "user", "content": query_text}]
        )

        # 5. Display Results
        items = search_results.get("items", [])
        if items:
            print(f"[OK] Found {len(items)} relevant memory item(s):")
            for idx, item in enumerate(items, 1):
                print(f"   {idx}. {item.get('summary')} (Type: {item.get('memory_type')})")
        else:
            print("[!] No relevant memories found.")

    except Exception as e:
        print(f"\n[!] An error occurred during execution: {e}")
        logging.exception("Detailed traceback:")
    finally:
        print("\n[=] Example execution finished.")


if __name__ == "__main__":
    asyncio.run(main())
```

### Understanding the Code

1.  **Provider Detection**: The script automatically detects which LLM provider is available:
    - First checks for `OPENAI_API_KEY` to use OpenAI's cloud service
    - Falls back to Ollama if available at `OLLAMA_API_BASE_URL`
    - Provides helpful error messages if neither is configured
2.  **Initialization**: We configure `MemoryService` with `llm_profiles` specific to your provider. We also define a `memorize_config` with a "User Facts" category. Categories help the LLM organize and retrieve information more effectively.
3.  **Memory Injection**: `create_memory_item` is used to explicitly add a piece of knowledge. We tag it with `memory_type="profile"` to semantically indicate this is a user attribute.
4.  **Retrieval**: We use `retrieve` with a natural language query. MemU's internal workflow ("RAG" or "LLM" based) will determine the best way to find relevant memories.

## Troubleshooting

### `[!] Error: No LLM provider configured.`

This means the script cannot detect either OpenAI or Ollama configuration.

**Solution:**

**Option 1: Use OpenAI (Cloud)**
Ensure you have exported your API key in your **current terminal session**:
-   **Linux/Mac**: `export OPENAI_API_KEY=sk-...`
-   **Windows PowerShell**: `$env:OPENAI_API_KEY="sk-..."`

Verify you didn't accidentally include spaces around the `=` sign in bash.

**Option 2: Use Ollama (Local)**
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Pull a model: `ollama pull llama2`
3. Verify it's running: `curl http://localhost:11434/api/tags`
4. Set the environment variable:
   - **Linux/Mac**: `export OLLAMA_API_BASE_URL=http://localhost:11434/api`
   - **Windows PowerShell**: `$env:OLLAMA_API_BASE_URL="http://localhost:11434/api"`

### Ollama-Specific Issues

**Ollama returns connection errors:**
- Verify Ollama is running: `ollama list`
- Check the API is accessible: `curl http://localhost:11434/api/tags`
- Ensure firewall allows connections on port 11434

**Ollama is slow or times out:**
- Use a smaller model: `ollama pull llama2` (7B) instead of `llama2:13b`
- Check system resources: Ollama needs 8GB+ RAM for most models
- Enable GPU acceleration if available (automatic on compatible systems)

**Model not found errors:**
- List installed models: `ollama list`
- Pull the required model: `ollama pull llama2`
- Update the `chat_model` in the script to match your installed model

## Next Steps

Now that you have the basics running, consider exploring:
-   **Core Concepts**: Learn about `MemoryService`, `MemoryItem`, and `MemoryCategory`.
-   **Production Deployment**: See the [Rocket.Chat Bot Example](../examples/rocketchat_bot_ollama.md) for deploying a memory-enabled bot with Ollama.
-   **Advanced Configuration**: Switch between LLM providers or use different vector stores.
-   **Other Examples**: Check out the `examples/` directory for conversation memory, skill extraction, and multimodal use cases.

## Community Resources

This tutorial was created as part of the MemU 2026 Challenge. For a summary of the architectural analysis, see the author's [LinkedIn Post](https://www.linkedin.com/posts/david-a-mamani-c_github-nevamind-aimemu-memory-infrastructure-activity-7418493617482207232-_MtG?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFdc0CIB__DJovR2t1BOxxJ6tgEeOqVEgx4).
