from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import settings
from app.providers.base import BaseEmbeddingProvider, BaseLLMProvider


class OpenAILLMProvider(BaseLLMProvider):
    def __init__(self):
        self.client = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url or None,
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 2000,
    ) -> dict:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.invoke(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "content": response.content,
            "model": settings.llm_model,
            "usage": {
                "prompt": response.response_metadata.get("token_usage", {}).get(
                    "prompt_tokens", 0
                ),
                "completion": response.response_metadata.get("token_usage", {}).get(
                    "completion_tokens", 0
                ),
                "total": response.response_metadata.get("token_usage", {}).get(
                    "total_tokens", 0
                ),
            },
        }


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self):
        self.client = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.embedding_api_key or settings.llm_api_key,
            dimensions=settings.embedding_dimensions,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)
