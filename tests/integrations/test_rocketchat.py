"""Tests for the Rocket.Chat integration."""

# ruff: noqa: S106
import asyncio
import contextlib
import os
import tempfile
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from memu.app import MemoryService
from memu.integrations.rocketchat.bot import RocketChatBot


@pytest.fixture
def mock_memory_service():
    """Fixture for a mock MemoryService."""
    service = AsyncMock(spec=MemoryService)
    # Configure memorize to return a specific structure
    service.memorize.return_value = {"items": [{"summary": "memorized content"}]}
    # Configure retrieve to return a specific structure
    service.retrieve.return_value = {
        "items": [
            {"summary": "retrieved memory 1", "score": 0.9},
            {"summary": "retrieved memory 2", "score": 0.8},
        ]
    }
    return service


@pytest.fixture
def mock_rocketchat_api_class():
    """Fixture for a mock RocketChat API class."""
    with patch("memu.integrations.rocketchat.bot.RocketChat") as MockRocketChat:
        mock_instance = MockRocketChat.return_value
        # Mock channels_list
        mock_instance.channels_list.return_value = MagicMock(
            json=lambda: {"success": True, "channels": [{"_id": "GENERAL", "name": "general"}]}
        )
        # Mock channels_history
        mock_instance.channels_history.return_value = MagicMock(json=lambda: {"success": True, "messages": []})
        # Mock chat_post_message
        mock_instance.chat_post_message.return_value = MagicMock(json=lambda: {"success": True})
        yield MockRocketChat, mock_instance


@pytest.mark.asyncio
async def test_rocketchat_bot_initialization(mock_memory_service, mock_rocketchat_api_class):
    """Test if the RocketChatBot initializes correctly."""
    MockRocketChat, mock_instance = mock_rocketchat_api_class
    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    assert bot.memory_service == mock_memory_service
    assert bot.bot_username == "test_bot"
    MockRocketChat.assert_called_once_with(
        user="test_bot", password="test_password", server_url="http://test.rocketchat.com"
    )
    assert bot.rocket == mock_instance


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_process_message_memorize_and_retrieve(mock_sleep, mock_memory_service, mock_rocketchat_api_class):
    """Test if _process_message calls memorize and retrieve."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    message = {
        "u": {"_id": "user123", "username": "test_user"},
        "rid": "room123",
        "msg": "Hello MemU bot!",
        "ts": datetime.now(UTC).isoformat(),
    }

    await bot._process_message(message)

    mock_memory_service.memorize.assert_awaited_once()
    assert mock_memory_service.memorize.call_args[1]["modality"] == "conversation"
    assert mock_memory_service.memorize.call_args[1]["user"]["user_id"] == "user123"

    mock_memory_service.retrieve.assert_awaited_once()
    assert mock_memory_service.retrieve.call_args[1]["queries"][0]["content"] == "Hello MemU bot!"
    assert mock_memory_service.retrieve.call_args[1]["where"]["user_id"] == "user123"

    mock_instance.chat_post_message.assert_called_once_with(text="retrieved memory 1", channel="room123")


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_process_message_no_retrieved_memories(mock_sleep, mock_memory_service, mock_rocketchat_api_class):
    """Test _process_message when no memories are retrieved."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    mock_memory_service.retrieve.return_value = {"items": []}  # No items found

    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    message = {
        "u": {"_id": "user123", "username": "test_user"},
        "rid": "room123",
        "msg": "Query for something unknown",
        "ts": datetime.now(UTC).isoformat(),
    }

    await bot._process_message(message)

    mock_instance.chat_post_message.assert_called_once_with(
        text="I don't have any relevant memories for that.", channel="room123"
    )


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_process_message_error_during_processing(mock_sleep, mock_memory_service, mock_rocketchat_api_class):
    """Test _process_message behavior when an error occurs during processing."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    mock_memory_service.memorize.side_effect = Exception("Memorize failed")

    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    message = {
        "u": {"_id": "user123", "username": "test_user"},
        "rid": "room123",
        "msg": "Trigger an error",
        "ts": datetime.now(UTC).isoformat(),
    }

    await bot._process_message(message)

    mock_instance.chat_post_message.assert_called_once_with(
        text="An error occurred while processing your request.", channel="room123"
    )


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_temporary_file_cleanup(mock_sleep, mock_memory_service, mock_rocketchat_api_class):
    """Test if temporary files are cleaned up after processing."""
    _MockRocketChat, _mock_instance = mock_rocketchat_api_class
    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    message = {
        "u": {"_id": "user123", "username": "test_user"},
        "rid": "room123",
        "msg": "Content for temp file",
        "ts": datetime.now(UTC).isoformat(),
    }

    # Patch tempfile.gettempdir to create a predictable temporary directory for testing
    with patch("tempfile.gettempdir", return_value=tempfile.mkdtemp()) as mock_gettempdir:
        temp_dir = mock_gettempdir.return_value
        await bot._process_message(message)

        # Assert that a file was created and then removed
        temp_files = os.listdir(temp_dir)
        assert not temp_files, f"Temporary directory not empty: {temp_files}"

        # Clean up the created temporary directory
        os.rmdir(temp_dir)


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_bot_ignores_its_own_messages(mock_sleep, mock_memory_service, mock_rocketchat_api_class):
    """Test that the bot ignores messages from itself."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    message = {
        "u": {"_id": "bot_id", "username": "test_bot"},  # Message from the bot itself
        "rid": "room123",
        "msg": "This is my own message.",
        "ts": datetime.now(UTC).isoformat(),
    }

    await bot._process_message(message)

    mock_memory_service.memorize.assert_not_awaited()
    mock_memory_service.retrieve.assert_not_awaited()
    mock_instance.chat_post_message.assert_not_called()


@pytest.mark.asyncio
async def test_run_polling_fetches_and_processes_messages(mock_memory_service, mock_rocketchat_api_class):
    """Test if run_polling fetches and processes messages."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    # Set bot's last_message_timestamp to a much older time to ensure messages are processed
    bot.last_message_timestamp = datetime.now(UTC) - timedelta(days=1)

    # Mock an incoming message
    # Ensure message1_ts is strictly greater than bot.last_message_timestamp
    message1_ts = (bot.last_message_timestamp + timedelta(seconds=1)).isoformat()
    message1 = {
        "u": {"_id": "user1", "username": "test_user1"},
        "rid": "GENERAL",
        "msg": "Hi bot!",
        "ts": message1_ts,
    }

    # Configure the mock to return messages first time, then always return empty
    # Using a function to avoid StopIteration when side_effect list is exhausted
    call_count = {"count": 0}

    def history_side_effect(*args, **kwargs):
        call_count["count"] += 1
        if call_count["count"] == 1:
            return MagicMock(json=lambda: {"success": True, "messages": [message1]})
        return MagicMock(json=lambda: {"success": True, "messages": []})

    mock_instance.channels_history.side_effect = history_side_effect

    # Use real asyncio.sleep with short interval to allow event loop to execute the polling task
    polling_task = asyncio.create_task(bot.run_polling(interval=0.01))
    await asyncio.sleep(0.05)  # Give polling loop time to execute

    polling_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await polling_task  # Wait for the task to actually be cancelled

    # Check if memorize/retrieve were called for message1
    mock_memory_service.memorize.assert_awaited_once()
    mock_memory_service.retrieve.assert_awaited_once()
    mock_instance.chat_post_message.assert_called_once()

    # Ensure last_message_timestamp is updated (comparing datetime objects directly)
    expected_timestamp = datetime.fromisoformat(message1["ts"].replace("Z", "+00:00"))
    assert bot.last_message_timestamp == expected_timestamp


@pytest.mark.asyncio
async def test_run_polling_handles_no_channels(mock_memory_service, mock_rocketchat_api_class):
    """Test run_polling gracefully handles no channels."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    mock_instance.channels_list.return_value = MagicMock(json=lambda: {"success": True, "channels": []})

    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    polling_task = asyncio.create_task(bot.run_polling(interval=0.01))
    await asyncio.sleep(0.05)  # Give polling loop time to execute

    polling_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await polling_task

    mock_memory_service.memorize.assert_not_awaited()
    mock_instance.channels_history.assert_not_called()
    mock_instance.chat_post_message.assert_not_called()


@pytest.mark.asyncio
async def test_run_polling_handles_history_failure(mock_memory_service, mock_rocketchat_api_class):
    """Test run_polling gracefully handles channel history retrieval failure."""
    _MockRocketChat, mock_instance = mock_rocketchat_api_class
    mock_instance.channels_history.return_value = MagicMock(
        json=lambda: {"success": False, "error": "Failed to get history"}
    )

    bot = RocketChatBot(
        memory_service=mock_memory_service,
        rocket_user="test_bot",
        rocket_password="test_password",
        rocket_url="http://test.rocketchat.com",
    )

    polling_task = asyncio.create_task(bot.run_polling(interval=0.01))
    await asyncio.sleep(0.05)  # Give polling loop time to execute

    polling_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await polling_task

    mock_memory_service.memorize.assert_not_awaited()
    mock_instance.chat_post_message.assert_not_called()
