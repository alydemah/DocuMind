from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    original_name: str
    file_type: str
    file_size: int
    file_hash: str
    status: str
    chunk_count: int
    page_count: int
    error_message: str | None = None
    metadata: dict = {}
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    id: UUID
    name: str
    status: str
    message: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int


class ChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    page_number: int | None = None
    token_count: int | None = None
    metadata: dict = {}
    created_at: datetime

    model_config = {"from_attributes": True}
