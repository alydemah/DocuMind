import logging

import redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_db, get_vector_store
from app.db.vector_store import VectorStore
from app.schemas import (
    AppConfigResponse,
    AppConfigUpdate,
    HealthResponse,
    StatsResponse,
)
from app.schemas.config import (
    EmbeddingConfigResponse,
    LLMConfigResponse,
    RAGConfigResponse,
    ServiceHealth,
)
from app.services.stats_service import StatsService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    services = ServiceHealth()

    try:
        await db.execute("SELECT 1")
        services.database = True
    except Exception:
        services.database = False

    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        services.redis = True
    except Exception:
        services.redis = False

    try:
        vector_store = get_vector_store()
        vector_store.client.get_collections()
        services.vector_store = True
    except Exception:
        services.vector_store = False

    services.llm_provider = bool(settings.llm_api_key or settings.llm_provider == "ollama")

    all_healthy = all([
        services.database,
        services.redis,
        services.vector_store,
        services.llm_provider,
    ])

    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        version="1.0.0",
        services=services,
    )


@router.get("/config", response_model=AppConfigResponse)
async def get_config():
    return AppConfigResponse(
        llm=LLMConfigResponse(
            provider=settings.llm_provider,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        ),
        embedding=EmbeddingConfigResponse(
            provider=settings.embedding_provider,
            model=settings.embedding_model,
            dimensions=settings.embedding_dimensions,
        ),
        rag=RAGConfigResponse(
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap,
            top_k=settings.rag_top_k,
            score_threshold=settings.rag_score_threshold,
        ),
    )


@router.put("/config", response_model=AppConfigResponse)
async def update_config(body: AppConfigUpdate):
    # Note: Runtime config changes are in-memory only
    if body.llm_provider:
        settings.llm_provider = body.llm_provider
    if body.llm_model:
        settings.llm_model = body.llm_model
    if body.llm_temperature is not None:
        settings.llm_temperature = body.llm_temperature
    if body.llm_max_tokens is not None:
        settings.llm_max_tokens = body.llm_max_tokens
    if body.rag_chunk_size is not None:
        settings.rag_chunk_size = body.rag_chunk_size
    if body.rag_chunk_overlap is not None:
        settings.rag_chunk_overlap = body.rag_chunk_overlap
    if body.rag_top_k is not None:
        settings.rag_top_k = body.rag_top_k
    if body.rag_score_threshold is not None:
        settings.rag_score_threshold = body.rag_score_threshold

    return await get_config()


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_vector_store),
):
    service = StatsService(db, vector_store)
    stats = await service.get_stats()
    return StatsResponse(**stats)
