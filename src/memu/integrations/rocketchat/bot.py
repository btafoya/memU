"""Rocket.Chat bot integration for MemU."""

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
logger = logging.getLogger("memu.integrations.rocketchat.bot")
logging.basicConfig(level=logging.INFO)


class RocketChatBot:
    """MemU Rocket.Chat Bot."""

    def __init__(self, memory_service: MemoryService, rocket_user: str, rocket_password: str, rocket_url: str):
        self.memory_service = memory_service
        self.rocket = RocketChat(user=rocket_user, password=rocket_password, server_url=rocket_url)
        self.bot_username = rocket_user
        # Initialize last_message_timestamp to current UTC time to only process new messages after bot starts
        self.last_message_timestamp = datetime.now(UTC)
        logger.info(
            "RocketChatBot initialized with polling mechanism. Initial timestamp: %s", self.last_message_timestamp
        )

    async def _process_message(self, message: dict):
        """Processes a single incoming message."""
        user_id = message["u"]["_id"]
        rid = message["rid"]  # Room ID
        msg_content = message["msg"]
        username = message["u"]["username"]
        # Convert message timestamp string to datetime object for consistent comparison
        message_dt = datetime.fromisoformat(message["ts"].replace("Z", "+00:00"))

        # Ignore messages from self to prevent bot loops
        if username == self.bot_username:
            return

        logger.info("Received message from user %s in room %s at %s: %s", username, rid, message_dt, msg_content)

        response_text = "I'm sorry, I don't understand."
        file_path = None
        try:
            # Save the message to MemU
            filename = f"rocketchat_input_{uuid.uuid4()}.txt"
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(msg_content)

            await self.memory_service.memorize(
                resource_url=file_path,
                modality="conversation",
                user={"user_id": user_id, "username": username},
            )
            logger.info("Message memorized for user %s.", user_id)

            # Retrieve a response from MemU
            retrieve_result = await self.memory_service.retrieve(
                queries=[{"role": "user", "content": msg_content}],
                where={"user_id": user_id},
            )

            items = retrieve_result.get("items", [])
            if items:
                # For simplicity, use the summary of the most relevant item
                response_text = items[0].get("summary", "I found some information, but I'm not sure how to respond.")
                logger.info("Retrieved memories for user %s. Response: %s", user_id, response_text)
            else:
                response_text = "I don't have any relevant memories for that."

        except Exception:
            logger.exception("Error processing message for user %s", user_id)
            response_text = "An error occurred while processing your request."
        finally:
            if file_path and os.path.exists(file_path):
                with contextlib.suppress(OSError):
                    os.remove(file_path)
                    logger.debug("Cleaned up temporary file: %s", file_path)

        # Send the response back to Rocket.Chat
        self.rocket.chat_post_message(text=response_text, channel=rid)
        logger.info("Sent response to room %s: %s", rid, response_text)

    async def run_polling(self, interval: int = 5):
        """Starts the Rocket.Chat bot polling for new messages."""
        logger.info("Starting Rocket.Chat bot polling for new messages every %d seconds...", interval)
        while True:
            try:
                channels_response = self.rocket.channels_list().json()
                logger.debug(f"Channels response from mock: {channels_response}")
                if not channels_response.get("success"):
                    logger.error("Failed to get channels list: %s", channels_response.get("error"))
                    await asyncio.sleep(interval)
                    continue

                for channel in channels_response.get("channels", []):
                    rid = channel["_id"]
                    query_params = {"count": 100}

                    last_ts_iso = self.last_message_timestamp.isoformat().replace("+00:00", "Z")
                    query_params["oldest"] = last_ts_iso
                    logger.debug(f"Fetching history for room {rid} oldest: {query_params['oldest']}")

                    history_response = self.rocket.channels_history(room_id=rid, **query_params).json()
                    logger.debug(f"History response for room {rid}: {history_response}")

                    if not history_response.get("success"):
                        logger.error(
                            "Failed to get channel history for room %s: %s", rid, history_response.get("error")
                        )
                        continue

                    messages = history_response.get("messages", [])
                    logger.debug(
                        f"Received {len(messages)} messages for room {rid}. Current last_message_timestamp: {self.last_message_timestamp}"
                    )

                    # Sort by timestamp to process in order
                    messages.sort(key=lambda x: datetime.fromisoformat(x["ts"].replace("Z", "+00:00")))

                    for message in messages:
                        message_dt = datetime.fromisoformat(message["ts"].replace("Z", "+00:00"))  # Convert to datetime
                        logger.debug(
                            f"Processing message {message['ts']}. Message_dt: {message_dt}, Last_message_timestamp: {self.last_message_timestamp}. Condition: {message_dt > self.last_message_timestamp}"
                        )
                        # Process message only if it's newer than the last processed timestamp
                        if message_dt > self.last_message_timestamp:
                            await self._process_message(message)
                            self.last_message_timestamp = message_dt  # Update the timestamp after processing

            except Exception:
                logger.exception("Error during polling loop")

            await asyncio.sleep(interval)


async def main():
    """Main function to run the Rocket.Chat bot."""
    rocket_url = os.getenv("ROCKETCHAT_URL")
    rocket_user = os.getenv("ROCKETCHAT_USER")
    rocket_password = os.getenv("ROCKETCHAT_PASSWORD")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([rocket_url, rocket_user, rocket_password, openai_api_key]):
        msg = (
            "Please set ROCKETCHAT_URL, ROCKETCHAT_USER, ROCKETCHAT_PASSWORD, and OPENAI_API_KEY environment variables."
        )
        logger.error(msg)
        raise ValueError(msg)

    # Initialize MemoryService with OpenAI using llm_profiles
    service = MemoryService(
        llm_profiles={
            "default": {
                "api_key": openai_api_key,
                "chat_model": "gpt-4o-mini",  # Using a cost-effective model for the bot
            },
        },
    )

    bot = RocketChatBot(
        memory_service=service,
        rocket_user=rocket_user,
        rocket_password=rocket_password,
        rocket_url=rocket_url,
    )

    await bot.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
