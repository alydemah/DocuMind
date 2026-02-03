import logging
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.message import Message

logger = logging.getLogger(__name__)


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, title: str | None = None) -> Conversation:
        conversation = Conversation(title=title or "New Conversation")
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return await self.get_conversation(conversation.id)

    async def get_conversation(self, conversation_id: uuid.UUID) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def list_conversations(self) -> tuple[list[Conversation], int]:
        count_result = await self.db.execute(select(func.count(Conversation.id)))
        total = count_result.scalar() or 0

        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.updated_at.desc())
        )
        conversations = list(result.scalars().all())
        return conversations, total

    async def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        conv = await self.get_conversation(conversation_id)
        if not conv:
            return False

        await self.db.delete(conv)
        await self.db.commit()
        return True

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        sources: list | None = None,
        model_used: str | None = None,
        tokens_used: dict | None = None,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            sources=sources or [],
            model_used=model_used,
            tokens_used=tokens_used or {},
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_chat_history(
        self, conversation_id: uuid.UUID, limit: int = 20
    ) -> list[dict]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = list(result.scalars().all())
        messages.reverse()

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    async def update_title(
        self, conversation_id: uuid.UUID, title: str
    ) -> Conversation | None:
        conv = await self.get_conversation(conversation_id)
        if not conv:
            return None

        conv.title = title
        await self.db.commit()
        await self.db.refresh(conv)
        return conv
