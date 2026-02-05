from __future__ import annotations

from memu.llm.backends.openai import OpenAILLMBackend


class OllamaLLMBackend(OpenAILLMBackend):
    """
    Backend for Ollama, using the OpenAI-compatible API.
    """

    name: str = "ollama"
    summary_endpoint: str = "/v1/chat/completions"
