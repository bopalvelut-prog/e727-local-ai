import pytest
from httpx import AsyncClient
from src.coordinator import app

@pytest.mark.asyncio
async def test_coordinator_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert "swarm" in response.json()
