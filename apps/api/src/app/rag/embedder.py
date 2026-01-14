import logging

from app.config import settings
from app.providers import get_embedding_provider

logger = logging.getLogger(__name__)


class DocumentEmbedder:
    def __init__(self):
        self.provider = get_embedding_provider()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        batch_size = 100
        all_embeddings: list[list[float]] = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings = self.provider.embed(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings

    def embed_query(self, query: str) -> list[float]:
        embeddings = self.provider.embed([query])
        return embeddings[0]
