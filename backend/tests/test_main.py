import pytest
import requests
from httpx import AsyncClient
from unittest.mock import patch
from main import app  # Adjust import based on your structure
from routes import fetch_all_chapters, fetch_chapter_info, get_chapter_name

# Test Client
@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

# Mock Data
mock_all_chapters_response = {
    "chapters": [
        {"id": 1, "name_complex": "Al-Fatiha"},
        {"id": 2, "name_complex": "Al-Baqarah"}
    ]
}

mock_chapter_info_response = {
    "chapter_info": {
        "text": "Al-Fatiha is the first chapter of the Quran."
    }
}

# Test fetch_all_chapters function
@patch("routes.requests.get")
def test_fetch_all_chapters(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_all_chapters_response

    response = fetch_all_chapters()
    assert "chapters" in response
    assert len(response["chapters"]) > 0
    assert response["chapters"][0]["name_complex"] == "Al-Fatiha"

# Test fetch_chapter_info function
@patch("routes.requests.get")
def test_fetch_chapter_info(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_chapter_info_response

    response = fetch_chapter_info(1)
    assert "Al-Fatiha" in response

# Test get_chapter_name function
def test_get_chapter_name():
    chapter_name = get_chapter_name(mock_all_chapters_response, 1)
    assert chapter_name == "Al-Fatiha"

# Integration Tests for FastAPI Endpoints
@pytest.mark.asyncio
async def test_get_chapters_route(test_client, requests_mock):
    requests_mock.get("https://api.quran.com/api/v4/chapters", json=mock_all_chapters_response)
    response = await test_client.get("/chapters")
    assert response.status_code == 200
    assert "chapters" in response.json()

@pytest.mark.asyncio
async def test_get_chapter_route(test_client, requests_mock):
    chapter_id = 1
    requests_mock.get(f"https://api.quran.com/api/v4/chapters/{chapter_id}/info", json=mock_chapter_info_response)
    response = await test_client.get(f"/chapter/{chapter_id}")
    assert response.status_code == 200
    assert "Al-Fatiha" in response.json().get("text", "")
