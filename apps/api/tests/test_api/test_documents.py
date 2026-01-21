import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_documents_empty(client: AsyncClient):
    response = await client.get("/api/v1/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["documents"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_document_not_found(client: AsyncClient):
    response = await client.get("/api/v1/documents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_document_not_found(client: AsyncClient):
    response = await client.delete("/api/v1/documents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
