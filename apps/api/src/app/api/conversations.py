import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.vector_store import VectorStore
from app.dependencies import get_db, get_vector_store
from app.rag.pipeline import RAGPipeline
from app.schemas import (
    AskRequest,
    AskResponse,
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
    SourceResponse,
)
from app.schemas.conversation import TokenUsage
from app.services.conversation_service import ConversationService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=ConversationResponse)
async def create_conversation(
    body: ConversationCreate | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    title = body.title if body else None
    conversation = await service.create_conversation(title=title)
    return ConversationResponse.model_validate(conversation)


@router.get("", response_model=ConversationListResponse)
async def list_conversations(db: AsyncSession = Depends(get_db)):
    service = ConversationService(db)
    conversations, total = await service.list_conversations()
    return ConversationListResponse(
        conversations=[ConversationResponse.model_validate(c) for c in conversations],
        total=total,
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    conversation = await service.get_conversation(conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse.model_validate(conversation)


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    deleted = await service.delete_conversation(conversation_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"message": "Conversation deleted successfully"}


@router.post("/{conversation_id}/ask", response_model=AskResponse)
async def ask_question(
    conversation_id: uuid.UUID,
    body: AskRequest,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_vector_store),
):
    service = ConversationService(db)
    conversation = await service.get_conversation(conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    logger.info(f"[ASK] Question: {body.question[:100]}...")
    logger.info(f"[ASK] Options: {body.options}")

    await service.add_message(
        conversation_id=conversation_id,
        role="user",
        content=body.question,
    )

    chat_history = await service.get_chat_history(conversation_id)
    logger.info(f"[ASK] Chat history: {len(chat_history)} messages")

    try:
        pipeline = RAGPipeline(vector_store)
        logger.info("[ASK] Running RAG query pipeline...")
        result = pipeline.query(
            question=body.question,
            chat_history=chat_history,
            top_k=body.options.get("top_k"),
            score_threshold=body.options.get("score_threshold"),
            document_filter=body.options.get("document_filter"),
        )
        logger.info(
            f"[ASK] Got answer ({len(result['answer'])} chars), "
            f"{len(result['sources'])} sources, model: {result['model_used']}"
        )
    except Exception as e:
        logger.error(f"[ASK] RAG pipeline error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"RAG pipeline error: {e}"
        ) from e

    await service.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=result["answer"],
        sources=result["sources"],
        model_used=result["model_used"],
        tokens_used=result["tokens_used"],
    )

    if conversation.title == "New Conversation":
        title = body.question[:80]
        await service.update_title(conversation_id, title)

    return AskResponse(
        answer=result["answer"],
        sources=[SourceResponse(**s) for s in result["sources"]],
        model_used=result["model_used"],
        tokens_used=TokenUsage(**result["tokens_used"]),
    )
