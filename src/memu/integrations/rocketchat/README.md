# MemU Rocket.Chat Bot

This document provides instructions on how to set up and run the MemU Rocket.Chat bot.

## Prerequisites

- A Rocket.Chat server
- A user account on the Rocket.Chat server with the "bot" role
- An OpenAI API key

## Installation

1.  **Install dependencies:**

    ```bash
    pip install ".[rocketchat]"
    ```

2.  **Set environment variables:**

    ```bash
    export ROCKETCHAT_URL="your_rocketchat_server_url"
    export ROCKETCHAT_USER="your_bot_username"
    export ROCKETCHAT_PASSWORD="your_bot_password"
    export OPENAI_API_KEY="your_openai_api_key"
    ```

## Running the bot

```bash
python -m memu.integrations.rocketchat.bot
```
