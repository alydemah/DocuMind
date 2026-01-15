import logging
from dataclasses import dataclass

from app.config import settings
from app.providers import get_llm_provider
from app.rag.prompts import SYSTEM_PROMPT, build_qa_prompt
from app.rag.retriever import RetrievedChunk

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    answer: str
    model_used: str
    tokens_used: dict


class AnswerGenerator:
    def __init__(self):
        self.provider = get_llm_provider()

    def generate(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        chat_history: list[dict] | None = None,
    ) -> GenerationResult:
        chunk_dicts = [
            {
                "document_id": c.document_id,
                "document_name": c.document_name,
                "page_number": c.page_number,
                "content": c.content,
            }
            for c in chunks
        ]

        prompt = build_qa_prompt(
            question=question,
            chunks=chunk_dicts,
            chat_history=chat_history or [],
        )

        response = self.provider.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

        return GenerationResult(
            answer=response["content"],
            model_used=response.get("model", settings.llm_model),
            tokens_used=response.get("usage", {}),
        )
