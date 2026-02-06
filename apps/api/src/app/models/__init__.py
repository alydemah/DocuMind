from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.chunk import DocumentChunk 
from app.models.conversation import Conversation 
from app.models.document import Document 
from app.models.message import Message 

__all__ = ["Base", "Document", "DocumentChunk", "Conversation", "Message"]
