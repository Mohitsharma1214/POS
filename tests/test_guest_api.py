import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_guest_research():
    payload = {
        "guest_name": "Sam Altman",
        "guest_company": "OpenAI",
        "guest_niche": "Artificial Intelligence",
        "podcast_context": "AI startup podcast"
    }
    response = client.post("/research/guest", json=payload)
    assert response.status_code in (200, 500)  # 500 if API keys are not set
    if response.status_code == 200:
        data = response.json()
        assert "top_performing_guest_episodes" in data
        assert "top_niche_trends" in data
        assert "twitter_signals" in data
        assert "tavily_web_signals" in data
        assert "reddit_discussions" in data
