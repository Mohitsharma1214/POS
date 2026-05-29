import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pattern_extraction():
    payload = {
        "guest_name": "Sam Altman",
        "guest_company": "OpenAI",
        "guest_niche": "Artificial Intelligence",
        "podcast_context": "AI startup podcast"
    }
    response = client.post("/research/pattern-extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "guest_name" in data
    assert "apify_scrape_episodes" in data
    assert "pattern_report" in data
    
    report = data["pattern_report"]
    assert "title_formulas" in report
    assert "thumbnail_patterns" in report
    assert "hook_structures" in report
    assert "question_styles" in report
    assert "episode_formats" in report
    assert "audience_retention_angles" in report
    assert "clip_bait_moments" in report
    
    # Ensure lists are populated (either by Claude or by our premium fallbacks)
    assert len(report["title_formulas"]) > 0
    assert len(report["clip_bait_moments"]) > 0
    
    # Verify the structure of clip bait moments
    clip = report["clip_bait_moments"][0]
    assert "title" in clip
    assert "trigger_statement" in clip
    assert "virality_score" in clip
    assert "platforms" in clip
