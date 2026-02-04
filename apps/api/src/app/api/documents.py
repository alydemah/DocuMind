import logging
import traceback
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import async_session_maker
from app.dependencies import get_db, get_vector_store
from app.db.vector_store import VectorStore
from app.rag.pipeline import RAGPipeline
from app.schemas import (
    ChunkResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService

router = APIRouter()
logger = logging.getLogger(__name__)


async def process_document_task(document_id: uuid.UUID, file_path: Path, file_type: str, document_name: str):
    """Background task to process an uploaded document through the RAG pipeline."""
    logger.info(f"[PROCESS] Starting processing for document {document_id} ({document_name})")

    async with async_session_maker() as db:
        service = DocumentService(db)
        try:
            await service.update_status(document_id, "processing")
            logger.info(f"[PROCESS] Status set to 'processing' for {document_name}")

            vector_store = get_vector_store()
            pipeline = RAGPipeline(vector_store)

            logger.info(f"[PROCESS] Running ingestion pipeline for {document_name}...")
            result = pipeline.ingest_document(
                file_path=file_path,
                file_type=file_type,
                document_id=str(document_id),
                document_name=document_name,
            )

            logger.info(f"[PROCESS] Ingestion complete: {result['chunk_count']} chunks, {result['page_count']} pages")

            await service.store_chunks(document_id, result["chunks"])
            logger.info(f"[PROCESS] Stored {result['chunk_count']} chunks in database")

            await service.update_status(
                document_id,
                status="ready",
                chunk_count=result["chunk_count"],
                page_count=result["page_count"],
            )
            logger.info(f"[PROCESS] Document {document_name} is ready!")

        except Exception as e:
            logger.error(f"[PROCESS] Failed to process {document_name}: {e}")
            logger.error(f"[PROCESS] Traceback: {traceback.format_exc()}")
            await service.update_status(
                document_id,
                status="failed",
                error_message=str(e),
            )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_size = 0
    content = await file.read()
    file_size = len(content)

    service = DocumentService(db)
    valid, error_msg = service.validate_file(file.filename, file_size)
    if not valid:
        raise HTTPException(status_code=400, detail=error_msg)

    ext = file.filename.rsplit(".", 1)[-1].lower()
    doc_id = uuid.uuid4()
    upload_dir = settings.upload_path / str(doc_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(content)

    file_hash = service.compute_file_hash(file_path)

    existing = await service.check_duplicate(file_hash)
    if existing:
        file_path.unlink()
        upload_dir.rmdir()
        raise HTTPException(
            status_code=409,
            detail=f"Document already uploaded as '{existing.name}'",
        )

    doc = await service.create_document(
        name=file.filename,
        original_name=file.filename,
        file_type=ext,
        file_size=file_size,
        file_hash=file_hash,
    )

    logger.info(f"[UPLOAD] Document saved: {doc.id} ({file.filename}), scheduling processing...")
    background_tasks.add_task(process_document_task, doc.id, file_path, ext, file.filename)

    return DocumentUploadResponse(
        id=doc.id,
        name=doc.name,
        status=doc.status,
        message="Document uploaded successfully. Processing will begin shortly.",
    )


@router.post("/bulk-upload", response_model=list[DocumentUploadResponse])
async def bulk_upload_documents(
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    results = []
    service = DocumentService(db)

    for file in files:
        if not file.filename:
            continue

        content = await file.read()
        file_size = len(content)

        valid, error_msg = service.validate_file(file.filename, file_size)
        if not valid:
            results.append(
                DocumentUploadResponse(
                    id=uuid.uuid4(),
                    name=file.filename,
                    status="failed",
                    message=error_msg,
                )
            )
            continue

        ext = file.filename.rsplit(".", 1)[-1].lower()
        doc_id = uuid.uuid4()
        upload_dir = settings.upload_path / str(doc_id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename

        with open(file_path, "wb") as f:
            f.write(content)

        file_hash = service.compute_file_hash(file_path)

        existing = await service.check_duplicate(file_hash)
        if existing:
            file_path.unlink()
            upload_dir.rmdir()
            results.append(
                DocumentUploadResponse(
                    id=existing.id,
                    name=file.filename,
                    status="duplicate",
                    message=f"Already uploaded as '{existing.name}'",
                )
            )
            continue

        doc = await service.create_document(
            name=file.filename,
            original_name=file.filename,
            file_type=ext,
            file_size=file_size,
            file_hash=file_hash,
        )

        results.append(
            DocumentUploadResponse(
                id=doc.id,
                name=doc.name,
                status=doc.status,
                message="Uploaded successfully. Processing will begin shortly.",
            )
        )

    return results


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    documents, total = await service.list_documents(page=page, page_size=page_size)

    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(d) for d in documents],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    doc = await service.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse.model_validate(doc)


@router.delete("/{document_id}")
async def delete_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_vector_store),
):
    service = DocumentService(db)
    doc = await service.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        vector_store.delete_by_document(str(document_id))
    except Exception as e:
        logger.warning(f"Failed to delete vectors for document {document_id}: {e}")

    await service.delete_document(document_id)

    return {"message": "Document deleted successfully"}


@router.post("/{document_id}/process")
async def process_document(
    document_id: uuid.UUID,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    doc = await service.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.status == "ready":
        return {"message": "Document is already processed", "status": doc.status}

    file_path = settings.upload_path / str(document_id) / doc.original_name
    if not file_path.exists():
        raise HTTPException(status_code=400, detail=f"File not found on disk: {file_path}")

    logger.info(f"[PROCESS] Manual trigger for document {document_id} ({doc.name})")
    background_tasks.add_task(process_document_task, document_id, file_path, doc.file_type, doc.name)

    return {"message": "Processing started", "status": "processing"}


@router.get("/{document_id}/chunks", response_model=list[ChunkResponse])
async def get_document_chunks(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DocumentService(db)
    doc = await service.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = await service.get_chunks(document_id)
    return [ChunkResponse.model_validate(c) for c in chunks]
