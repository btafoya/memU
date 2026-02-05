"""
MemU Rocket.Chat Bot with Ollama Support.

This example demonstrates how to deploy a Rocket.Chat bot with long-term memory
using Ollama for local, privacy-focused LLM inference.

Features:
- Automatic LLM provider detection (OpenAI or Ollama)
- User-scoped memory (each user has their own memory context)
- Conversation history persistence
- Real-time message processing with polling

Prerequisites:
- Rocket.Chat server instance
- Bot user account on Rocket.Chat with appropriate permissions
- Either OpenAI API key OR Ollama running locally

Environment Variables:
    Required:
        ROCKETCHAT_URL: Your Rocket.Chat server URL (e.g., https://chat.example.com)
        ROCKETCHAT_USER: Bot username
        ROCKETCHAT_PASSWORD: Bot password

    LLM Provider (choose one):
        OPENAI_API_KEY: OpenAI API key (for cloud inference)
        OR
        OLLAMA_API_BASE_URL: Ollama endpoint (default: http://localhost:11434/api)

Usage:
    # With Ollama (local)
    ollama pull llama2
    export ROCKETCHAT_URL=https://chat.example.com
    export ROCKETCHAT_USER=membot
    export ROCKETCHAT_PASSWORD=your_password
    export OLLAMA_API_BASE_URL=http://localhost:11434/api
    python rocketchat_bot_ollama.py

    # With OpenAI (cloud)
    export ROCKETCHAT_URL=https://chat.example.com
    export ROCKETCHAT_USER=membot
    export ROCKETCHAT_PASSWORD=your_password
    export OPENAI_API_KEY=sk-your-api-key
    python rocketchat_bot_ollama.py
"""

import asyncio
import contextlib
import logging
import os
import tempfile
import uuid
from datetime import UTC, datetime

from rocketchat_API.rocketchat import RocketChat

from memu.app import MemoryService

# Setup logger
logger = logging.getLogger("memu.rocketchat_bot")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class RocketChatBot:
    """MemU-powered Rocket.Chat Bot with long-term memory."""

    def __init__(
        self,
        memory_service: MemoryService,
        rocket_user: str,
        rocket_password: str,
        rocket_url: str,
    ):
        """Initialize the bot.

        Args:
            memory_service: Configured MemoryService instance
            rocket_user: Bot username
            rocket_password: Bot password
            rocket_url: Rocket.Chat server URL
        """
        self.memory_service = memory_service
        self.rocket = RocketChat(user=rocket_user, password=rocket_password, server_url=rocket_url)
        self.bot_username = rocket_user
        # Initialize last_message_timestamp to current UTC time to only process new messages
        self.last_message_timestamp = datetime.now(UTC)
        logger.info(
            "RocketChatBot initialized. Bot user: %s, Initial timestamp: %s",
            self.bot_username,
            self.last_message_timestamp,
        )

    async def _process_message(self, message: dict):
        """Process a single incoming message."""
        user_id = message["u"]["_id"]
        rid = message["rid"]  # Room ID
        msg_content = message["msg"]
        username = message["u"]["username"]

        # Ignore messages from self to prevent bot loops
        if username == self.bot_username:
            return

        logger.info(
            "📨 Message from @%s in room %s: %s",
            username,
            rid,
            msg_content[:50] + "..." if len(msg_content) > 50 else msg_content,
        )

        response_text = "I'm processing your message..."
        file_path = None

        try:
            # Save the message temporarily for memorization
            filename = f"rocketchat_msg_{uuid.uuid4()}.txt"
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"User: {username}\nMessage: {msg_content}")

            # Store message in long-term memory
            await self.memory_service.memorize(
                resource_url=file_path,
                modality="conversation",
                user={"user_id": user_id, "username": username},
            )
            logger.info("💾 Message memorized for user @%s", username)

            # Retrieve relevant memories for context-aware response
            retrieve_result = await self.memory_service.retrieve(
                queries=[{"role": "user", "content": msg_content}],
                where={"user_id": user_id},
            )

            items = retrieve_result.get("items", [])
            if items:
                # Build response from the most relevant memories
                memories = [item.get("summary", "") for item in items[:3]]
                response_text = (
                    f"Based on what I remember about you:\n\n"
                    f"{chr(10).join(f'• {mem}' for mem in memories)}\n\n"
                    f"How can I help you further?"
                )
                logger.info("🧠 Retrieved %d memories for @%s", len(items), username)
            else:
                response_text = (
                    "I don't have any previous context about this topic. Feel free to share more so I can learn!"
                )
                logger.info("No relevant memories found for @%s", username)

        except Exception:
            logger.exception("❌ Error processing message for user @%s", username)
            response_text = "I encountered an error processing your message. Please try again or contact support."
        finally:
            # Clean up temporary file
            if file_path and os.path.exists(file_path):
                with contextlib.suppress(OSError):
                    os.remove(file_path)

        # Send response back to Rocket.Chat
        self.rocket.chat_post_message(text=response_text, channel=rid)
        logger.info("✅ Response sent to room %s", rid)

    async def run_polling(self, interval: int = 5):
        """Start polling for new messages.

        Args:
            interval: Polling interval in seconds (default: 5)
        """
        logger.info("🚀 Bot polling started (interval: %d seconds)", interval)

        while True:
            try:
                # Get list of channels
                channels_response = self.rocket.channels_list().json()

                if not channels_response.get("success"):
                    logger.error("Failed to get channels list: %s", channels_response.get("error"))
                    await asyncio.sleep(interval)
                    continue

                # Process each channel
                for channel in channels_response.get("channels", []):
                    rid = channel["_id"]
                    channel_name = channel.get("name", "unknown")

                    # Fetch message history since last poll
                    query_params = {
                        "count": 100,
                        "oldest": self.last_message_timestamp.isoformat().replace("+00:00", "Z"),
                    }

                    history_response = self.rocket.channels_history(room_id=rid, **query_params).json()

                    if not history_response.get("success"):
                        logger.error("Failed to get history for #%s: %s", channel_name, history_response.get("error"))
                        continue

                    messages = history_response.get("messages", [])

                    if messages:
                        logger.debug("📬 %d new messages in #%s", len(messages), channel_name)

                        # Sort by timestamp to process in chronological order
                        messages.sort(key=lambda x: datetime.fromisoformat(x["ts"].replace("Z", "+00:00")))

                        for message in messages:
                            message_dt = datetime.fromisoformat(message["ts"].replace("Z", "+00:00"))

                            # Process only new messages
                            if message_dt > self.last_message_timestamp:
                                await self._process_message(message)
                                self.last_message_timestamp = message_dt

            except Exception:
                logger.exception("❌ Error during polling loop")

            await asyncio.sleep(interval)


async def main():
    """Main entry point for the Rocket.Chat bot."""
    print("=" * 60)
    print("MemU Rocket.Chat Bot with Ollama Support")
    print("=" * 60)

    # Get Rocket.Chat configuration
    rocket_url = os.getenv("ROCKETCHAT_URL")
    rocket_user = os.getenv("ROCKETCHAT_USER")
    rocket_password = os.getenv("ROCKETCHAT_PASSWORD")

    if not all([rocket_url, rocket_user, rocket_password]):
        logger.error(
            "❌ Missing Rocket.Chat configuration. Please set:\n   ROCKETCHAT_URL, ROCKETCHAT_USER, ROCKETCHAT_PASSWORD"
        )
        return

    # Detect LLM provider
    openai_key = os.getenv("OPENAI_API_KEY")
    ollama_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434/api")

    if openai_key:
        logger.info("🌐 Using OpenAI for LLM inference")
        llm_config = {
            "api_key": openai_key,
            "chat_model": "gpt-4o-mini",
        }
    else:
        # Check if Ollama is available
        try:
            import httpx

            response = httpx.get(f"{ollama_url}/tags", timeout=5.0)
            if response.status_code == 200:
                logger.info("🏠 Using Ollama (local) for LLM inference")
                logger.info("   Endpoint: %s", ollama_url)
                llm_config = {
                    "client_backend": "ollama",
                    "base_url": ollama_url,
                    "chat_model": "llama2",
                    "embed_model": "llama2",
                }
            else:
                logger.error(
                    "❌ No LLM provider configured. Please either:\n"
                    "   1. Set OPENAI_API_KEY for cloud inference\n"
                    "   2. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh\n"
                    "      Then run: ollama pull llama2"
                )
                return
        except Exception:
            logger.exception(
                "❌ Failed to connect to Ollama at %s\n"
                "   Please either:\n"
                "   1. Set OPENAI_API_KEY for cloud inference\n"
                "   2. Start Ollama: ollama serve",
                ollama_url,
            )
            return

    # Initialize MemoryService
    logger.info("🧠 Initializing MemoryService...")
    service = MemoryService(
        llm_profiles={"default": llm_config},
        memorize_config={
            "memory_categories": [
                {
                    "name": "User Preferences",
                    "description": "User preferences, interests, and personal information",
                },
                {
                    "name": "Conversations",
                    "description": "Previous conversation topics and context",
                },
            ]
        },
    )
    logger.info("✅ MemoryService initialized")

    # Initialize and run bot
    bot = RocketChatBot(
        memory_service=service,
        rocket_user=rocket_user,
        rocket_password=rocket_password,
        rocket_url=rocket_url,
    )

    logger.info("🤖 Bot connected to %s as @%s", rocket_url, rocket_user)
    logger.info("💬 Ready to receive messages!")

    await bot.run_polling(interval=5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
    except Exception:
        logger.exception("❌ Fatal error")
