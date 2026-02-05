"""
Example 6: Using Ollama with MemU

This example demonstrates how to use a local Ollama instance as the LLM backend for MemU.

Usage:
    - Ensure Ollama is running and the desired models are pulled.
    - Run the script: python examples/example_6_ollama_memory.py
"""

import asyncio
import os
import sys

from memu.app import MemoryService

src_path = os.path.abspath("src")
sys.path.insert(0, src_path)


async def main():
    """
    Process a conversation file and retrieve memories using Ollama.

    This example:
    1. Initializes MemoryService with Ollama
    2. Processes a conversation JSON file
    3. Retrieves memories related to the conversation
    """
    print("Example 6: Conversation Memory Processing (Ollama)")
    print("-" * 50)

    # Initialize service with Ollama
    # By default, Ollama runs on http://localhost:11434
    # The API key is not required for Ollama, but the field must be present.
    service = MemoryService(
        llm_profiles={
            "default": {
                "provider": "ollama",
                "client_backend": "httpx",
                "base_url": "http://localhost:11434",
                "api_key": "ollama",
                "chat_model": "llama2",
                "embed_model": "nomic-embed-text",
            },
        },
    )

    conversation_file = "examples/resources/conversations/conv1.json"

    print(f"\nProcessing conversation file: {conversation_file}...")
    if not os.path.exists(conversation_file):
        print(f"Skipped: {conversation_file} not found")
        return

    try:
        memorize_result = await service.memorize(resource_url=conversation_file, modality="conversation")
        print(f"Successfully memorized {len(memorize_result.get('items', []))} items.")
    except Exception as e:
        print(f"Error processing {conversation_file}: {e}")
        return

    print("\nRetrieving memories related to 'What is your name?'...")
    try:
        retrieve_result = await service.retrieve(queries=[{"role": "user", "content": "What is your name?"}])
        print("Retrieved memories:")
        for item in retrieve_result.get("items", []):
            print(f"- {item.get('content')}")
    except Exception as e:
        print(f"Error retrieving memories: {e}")


if __name__ == "__main__":
    asyncio.run(main())
