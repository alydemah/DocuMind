import hashlib
import logging
import uuid
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chunk import DocumentChunk
from app.models.document import Document

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(
        self,
        name: str,
        original_name: str,
        file_type: str,
        file_size: int,
        file_hash: str,
    ) -> Document:
        doc = Document(
            name=name,
            original_name=original_name,
            file_type=file_type,
            file_size=file_size,
            file_hash=file_hash,
            status="pending",
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def get_document(self, document_id: uuid.UUID) -> Document | None:
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def list_documents(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[Document], int]:
        count_result = await self.db.execute(select(func.count(Document.id)))
        total = count_result.scalar() or 0

        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Document)
            .order_by(Document.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        documents = list(result.scalars().all())
        return documents, total

    async def delete_document(self, document_id: uuid.UUID) -> bool:
        doc = await self.get_document(document_id)
        if not doc:
            return False

        file_path = settings.upload_path / str(document_id) / doc.original_name
        if file_path.exists():
            file_path.unlink()
            parent = file_path.parent
            if parent.exists() and not list(parent.iterdir()):
                parent.rmdir()

        await self.db.delete(doc)
        await self.db.commit()
        return True

    async def update_status(
        self,
        document_id: uuid.UUID,
        status: str,
        chunk_count: int = 0,
        page_count: int = 0,
        error_message: str | None = None,
    ) -> Document | None:
        doc = await self.get_document(document_id)
        if not doc:
            return None

        doc.status = status
        doc.chunk_count = chunk_count
        doc.page_count = page_count
        doc.error_message = error_message

        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def store_chunks(
        self,
        document_id: uuid.UUID,
        chunks: list[dict],
    ) -> list[DocumentChunk]:
        db_chunks = []
        for chunk_data in chunks:
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                page_number=chunk_data.get("page_number"),
                token_count=chunk_data.get("token_count"),
                metadata_=chunk_data.get("metadata", {}),
            )
            self.db.add(chunk)
            db_chunks.append(chunk)

        await self.db.commit()
        return db_chunks

    async def get_chunks(self, document_id: uuid.UUID) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
        return list(result.scalars().all())

    async def check_duplicate(self, file_hash: str) -> Document | None:
        result = await self.db.execute(
            select(Document).where(Document.file_hash == file_hash)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def compute_file_hash(file_path: Path) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(8192), b""):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        if ext not in settings.allowed_extensions:
            return False, f"File type .{ext} is not supported. Allowed: {settings.allowed_file_types}"

        if file_size > settings.max_file_size_bytes:
            return False, f"File size exceeds maximum of {settings.max_file_size_mb}MB"

        return True, ""
