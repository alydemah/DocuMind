import httpx

from app.config import settings
from app.providers.base import BaseEmbeddingProvider, BaseLLMProvider


class OllamaLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.base_url = settings.ollama_host
        self.model = settings.ollama_llm_model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 2000,
    ) -> dict:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
                "stream": False,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "content": data["message"]["content"],
            "model": self.model,
            "usage": {
                "prompt": data.get("prompt_eval_count", 0),
                "completion": data.get("eval_count", 0),
                "total": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
            },
        }


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self):
        self.base_url = settings.ollama_host
        self.model = settings.ollama_embed_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            response = httpx.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            embeddings.append(data["embedding"])

        return embeddings
