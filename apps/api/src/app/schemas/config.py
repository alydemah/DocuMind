from pydantic import BaseModel


class LLMConfigResponse(BaseModel):
    provider: str
    model: str
    temperature: float
    max_tokens: int


class EmbeddingConfigResponse(BaseModel):
    provider: str
    model: str
    dimensions: int


class RAGConfigResponse(BaseModel):
    chunk_size: int
    chunk_overlap: int
    top_k: int
    score_threshold: float


class AppConfigResponse(BaseModel):
    llm: LLMConfigResponse
    embedding: EmbeddingConfigResponse
    rag: RAGConfigResponse


class AppConfigUpdate(BaseModel):
    llm_provider: str | None = None
    llm_model: str | None = None
    llm_temperature: float | None = None
    llm_max_tokens: int | None = None
    embedding_provider: str | None = None
    embedding_model: str | None = None
    rag_chunk_size: int | None = None
    rag_chunk_overlap: int | None = None
    rag_top_k: int | None = None
    rag_score_threshold: float | None = None


class ServiceHealth(BaseModel):
    database: bool = False
    redis: bool = False
    vector_store: bool = False
    llm_provider: bool = False


class HealthResponse(BaseModel):
    status: str
    version: str
    services: ServiceHealth


class StatsResponse(BaseModel):
    document_count: int
    chunk_count: int
    conversation_count: int
    storage_used_bytes: int
    vector_count: int
