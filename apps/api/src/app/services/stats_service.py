import logging
import os
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.vector_store import VectorStore
from app.models.chunk import DocumentChunk
from app.models.conversation import Conversation
from app.models.document import Document

logger = logging.getLogger(__name__)


class StatsService:
    def __init__(self, db: AsyncSession, vector_store: VectorStore):
        self.db = db
        self.vector_store = vector_store

    async def get_stats(self) -> dict:
        doc_count = await self.db.execute(select(func.count(Document.id)))
        chunk_count = await self.db.execute(select(func.count(DocumentChunk.id)))
        conv_count = await self.db.execute(select(func.count(Conversation.id)))

        storage_used = self._get_storage_size(settings.upload_path)
        vector_count = self.vector_store.count()

        return {
            "document_count": doc_count.scalar() or 0,
            "chunk_count": chunk_count.scalar() or 0,
            "conversation_count": conv_count.scalar() or 0,
            "storage_used_bytes": storage_used,
            "vector_count": vector_count,
        }

    def _get_storage_size(self, path: Path) -> int:
        total = 0
        if path.exists():
            for dirpath, _dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
        return total
