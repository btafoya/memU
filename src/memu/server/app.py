"""MemU FastAPI application."""

import os

from fastapi import FastAPI

from memu.app import MemoryService

app = FastAPI(title="MemU Memory Service", version="1.3.0")

# Initialize MemoryService (will be lazy-loaded when needed)
_memory_service = None


def get_memory_service() -> MemoryService:
    """Get or create the MemoryService instance."""
    global _memory_service
    if _memory_service is None:
        ollama_url = os.getenv("OLLAMA_API_BASE_URL", "http://192.168.25.165:11434/api")
        _memory_service = MemoryService(
            llm_profiles={"default": {"client_backend": "ollama", "base_url": ollama_url, "model": "llama2"}}
        )
    return _memory_service


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "MemU Memory Service",
        "version": "1.3.0",
        "ollama_endpoint": os.getenv("OLLAMA_API_BASE_URL", "http://192.168.25.165:11434/api"),
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": os.getenv("MEMU_DB_URL", "not configured"),
        "ollama": os.getenv("OLLAMA_API_BASE_URL", "not configured"),
    }


@app.get("/api/status")
async def api_status():
    """API status endpoint."""
    return {"api_version": "v1", "memory_service": "initialized" if _memory_service else "not initialized"}
