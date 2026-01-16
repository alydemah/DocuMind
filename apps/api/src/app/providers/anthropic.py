from langchain_anthropic import ChatAnthropic

from app.config import settings
from app.providers.base import BaseLLMProvider


class AnthropicLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.client = ChatAnthropic(
            model=settings.llm_model,
            api_key=settings.llm_api_key,
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

        usage = response.response_metadata.get("usage", {})

        return {
            "content": response.content,
            "model": settings.llm_model,
            "usage": {
                "prompt": usage.get("input_tokens", 0),
                "completion": usage.get("output_tokens", 0),
                "total": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            },
        }
