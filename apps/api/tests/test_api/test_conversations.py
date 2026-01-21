import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient):
    response = await client.post("/api/v1/conversations", json={"title": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_conversations_empty(client: AsyncClient):
    response = await client.get("/api/v1/conversations")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_get_conversation_not_found(client: AsyncClient):
    response = await client.get("/api/v1/conversations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_conversation_not_found(client: AsyncClient):
    response = await client.delete("/api/v1/conversations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
