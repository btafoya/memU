"""MemU Server CLI entry point."""

import logging

import uvicorn


def main():
    """Start the MemU server."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("memu.server")

    logger.info("Starting MemU server on port 8000...")
    logger.info("Ollama endpoint: http://192.168.25.165:11434/api")

    # Run the FastAPI app

    uvicorn.run("memu.server.app:app", host="0.0.0.0", port=8000, log_level="info")  # noqa: S104


if __name__ == "__main__":
    main()
