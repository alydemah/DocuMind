from app.config import settings
from app.providers.base import BaseLLMProvider, BaseEmbeddingProvider


def get_llm_provider() -> BaseLLMProvider:
    if settings.llm_provider == "openai":
        from app.providers.openai import OpenAILLMProvider
        return OpenAILLMProvider()
    elif settings.llm_provider == "anthropic":
        from app.providers.anthropic import AnthropicLLMProvider
        return AnthropicLLMProvider()
    elif settings.llm_provider == "ollama":
        from app.providers.ollama import OllamaLLMProvider
        return OllamaLLMProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


def get_embedding_provider() -> BaseEmbeddingProvider:
    if settings.embedding_provider == "openai":
        from app.providers.openai import OpenAIEmbeddingProvider
        return OpenAIEmbeddingProvider()
    elif settings.embedding_provider == "ollama":
        from app.providers.ollama import OllamaEmbeddingProvider
        return OllamaEmbeddingProvider()
    else:
        raise ValueError(f"Unknown embedding provider: {settings.embedding_provider}")


__all__ = ["get_llm_provider", "get_embedding_provider"]
