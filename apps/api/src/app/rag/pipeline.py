import hashlib
import logging
import uuid
from pathlib import Path

from app.config import settings
from app.db.vector_store import VectorStore
from app.rag.chunker import DocumentChunker
from app.rag.embedder import DocumentEmbedder
from app.rag.extractors import get_extractor
from app.rag.generator import AnswerGenerator
from app.rag.retriever import DocumentRetriever, RetrievedChunk

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.chunker = DocumentChunker()
        self.embedder = DocumentEmbedder()
        self.retriever = DocumentRetriever(vector_store, self.embedder)
        self.generator = AnswerGenerator()

    def ingest_document(
        self,
        file_path: Path,
        file_type: str,
        document_id: str,
        document_name: str,
    ) -> dict:
        logger.info(f"Starting ingestion for {document_name} ({file_type})")

        extractor = get_extractor(file_type)
        result = extractor.extract(file_path)

        logger.info(f"Extracted {result.total_pages} pages from {document_name}")

        pages = [
            {"content": page.content, "page_number": page.page_number}
            for page in result.pages
        ]
        chunks = self.chunker.chunk_pages(
            pages=pages,
            document_id=document_id,
            document_name=document_name,
        )

        logger.info(f"Created {len(chunks)} chunks for {document_name}")

        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_texts(texts)

        logger.info(f"Generated {len(embeddings)} embeddings for {document_name}")

        ids = [str(uuid.uuid4()) for _ in chunks]
        payloads = [
            {
                "document_id": document_id,
                "document_name": document_name,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number,
                "content": chunk.content,
            }
            for chunk in chunks
        ]

        self.vector_store.upsert_vectors(ids=ids, vectors=embeddings, payloads=payloads)

        logger.info(f"Stored {len(chunks)} vectors for {document_name}")

        return {
            "chunk_count": len(chunks),
            "page_count": result.total_pages,
            "chunks": [
                {
                    "content": c.content,
                    "chunk_index": c.chunk_index,
                    "page_number": c.page_number,
                    "token_count": c.token_count,
                    "metadata": c.metadata,
                }
                for c in chunks
            ],
        }

    def query(
        self,
        question: str,
        chat_history: list[dict] | None = None,
        top_k: int | None = None,
        score_threshold: float | None = None,
        document_filter: list[str] | None = None,
    ) -> dict:
        chunks = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            score_threshold=score_threshold,
            document_filter=document_filter,
        )

        if not chunks:
            return {
                "answer": "I don't have enough information in the uploaded documents to answer this.",
                "sources": [],
                "model_used": settings.llm_model,
                "tokens_used": {"prompt": 0, "completion": 0, "total": 0},
            }

        result = self.generator.generate(
            question=question,
            chunks=chunks,
            chat_history=chat_history,
        )

        sources = [
            {
                "document_id": c.document_id,
                "document_name": c.document_name,
                "page_number": c.page_number,
                "chunk_text": c.content[:300],
                "relevance_score": c.relevance_score,
            }
            for c in chunks
        ]

        return {
            "answer": result.answer,
            "sources": sources,
            "model_used": result.model_used,
            "tokens_used": result.tokens_used,
        }

    @staticmethod
    def compute_file_hash(file_path: Path) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(8192), b""):
                sha256.update(block)
        return sha256.hexdigest()
