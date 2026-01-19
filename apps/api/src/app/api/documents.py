import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_db, get_vector_store
from app.db.vector_store import VectorStore
from app.schemas import (
    ChunkResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
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

    # TODO: trigger background ingestion task
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

    vector_store.delete_by_document(str(document_id))
    await service.delete_document(document_id)

    return {"message": "Document deleted successfully"}


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
