import logging
from dataclasses import dataclass

from app.config import settings
from app.db.vector_store import VectorStore
from app.rag.embedder import DocumentEmbedder

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    document_id: str
    document_name: str
    chunk_index: int
    page_number: int | None
    content: str
    relevance_score: float


class DocumentRetriever:
    def __init__(self, vector_store: VectorStore, embedder: DocumentEmbedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        score_threshold: float | None = None,
        document_filter: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        top_k = top_k or settings.rag_top_k
        score_threshold = score_threshold or settings.rag_score_threshold

        query_vector = self.embedder.embed_query(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            score_threshold=score_threshold,
            document_filter=document_filter,
        )

        chunks = [
            RetrievedChunk(
                document_id=r["document_id"],
                document_name=r["document_name"],
                chunk_index=r["chunk_index"],
                page_number=r.get("page_number"),
                content=r["content"],
                relevance_score=r["score"],
            )
            for r in results
        ]

        chunks.sort(key=lambda c: c.relevance_score, reverse=True)

        logger.info(f"Retrieved {len(chunks)} chunks for query: {query[:50]}...")
        return chunks
