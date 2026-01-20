import asyncio
import logging
from pathlib import Path

from app.config import settings
from app.db.session import async_session_maker
from app.db.vector_store import VectorStore
from app.rag.pipeline import RAGPipeline
from app.services.document_service import DocumentService
from app.workers import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="ingest_document")
def ingest_document(self, document_id: str, file_path: str, file_type: str, document_name: str):
    logger.info(f"Starting ingestion task for document {document_id}")

    try:
        self.update_state(state="PROCESSING", meta={"progress": 10, "step": "extracting"})

        vector_store = VectorStore(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            collection_name=settings.qdrant_collection,
        )
        pipeline = RAGPipeline(vector_store)

        self.update_state(state="PROCESSING", meta={"progress": 30, "step": "chunking"})

        result = pipeline.ingest_document(
            file_path=Path(file_path),
            file_type=file_type,
            document_id=document_id,
            document_name=document_name,
        )

        self.update_state(state="PROCESSING", meta={"progress": 90, "step": "storing"})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                _update_document_status(
                    document_id=document_id,
                    status="completed",
                    chunk_count=result["chunk_count"],
                    page_count=result["page_count"],
                    chunks=result["chunks"],
                )
            )
        finally:
            loop.close()

        logger.info(f"Ingestion complete for {document_id}: {result['chunk_count']} chunks")
        return {"status": "completed", "chunk_count": result["chunk_count"]}

    except Exception as e:
        logger.error(f"Ingestion failed for {document_id}: {e}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                _update_document_status(
                    document_id=document_id,
                    status="failed",
                    error_message=str(e),
                )
            )
        finally:
            loop.close()

        raise


async def _update_document_status(
    document_id: str,
    status: str,
    chunk_count: int = 0,
    page_count: int = 0,
    error_message: str | None = None,
    chunks: list[dict] | None = None,
):
    import uuid

    async with async_session_maker() as db:
        service = DocumentService(db)
        await service.update_status(
            document_id=uuid.UUID(document_id),
            status=status,
            chunk_count=chunk_count,
            page_count=page_count,
            error_message=error_message,
        )

        if chunks:
            await service.store_chunks(
                document_id=uuid.UUID(document_id),
                chunks=chunks,
            )
