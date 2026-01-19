from fastapi import APIRouter

from app.api.documents import router as documents_router
from app.api.conversations import router as conversations_router
from app.api.config_routes import router as config_router

api_router = APIRouter()

api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
api_router.include_router(config_router, tags=["system"])
