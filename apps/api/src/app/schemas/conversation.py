from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SourceResponse(BaseModel):
    document_id: str
    document_name: str
    page_number: int | None = None
    chunk_text: str
    relevance_score: float


class TokenUsage(BaseModel):
    prompt: int = 0
    completion: int = 0
    total: int = 0


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    sources: list[SourceResponse] = []
    model_used: str | None = None
    tokens_used: TokenUsage | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreate(BaseModel):
    title: str | None = None


class ConversationResponse(BaseModel):
    id: UUID
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse] = []

    model_config = {"from_attributes": True}


class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
    total: int


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
    options: dict = Field(default_factory=dict)


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    model_used: str
    tokens_used: TokenUsage
