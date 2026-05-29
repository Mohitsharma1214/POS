import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_guest_intelligence_extraction():
    payload = {
        "guest_name": "Anthony Scaramucci",
        "guest_company": "SkyBridge Capital",
        "guest_niche": "Finance",
        "podcast_context": "Political and finance discussion"
    }
    response = client.post("/research/guest-intelligence", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "guest_name" in data
    assert data["guest_name"] == "Anthony Scaramucci"
    assert "intelligence_report" in data
    
    report = data["intelligence_report"]
    assert "enrichment" in report
    assert "covered_angles" in report
    assert "untapped_angles" in report
    assert "public_stances" in report
    assert "contradictions" in report
    
    enrichment = report["enrichment"]
    assert "bio" in enrichment
    assert len(enrichment["bio"]) > 0
    assert "current_roles" in enrichment
    assert len(enrichment["current_roles"]) > 0
    assert "accomplishments" in enrichment
    assert len(enrichment["accomplishments"]) > 0
    assert "social_profiles" in enrichment
    assert len(enrichment["social_profiles"]) > 0
    
    assert len(report["covered_angles"]) > 0
    assert len(report["untapped_angles"]) > 0
    assert len(report["public_stances"]) > 0
    assert len(report["contradictions"]) > 0
    
    # Verify public stance schema
    stance = report["public_stances"][0]
    assert "topic" in stance
    assert "position" in stance
    assert "quote_or_source" in stance
    
    # Verify contradiction schema
    contradiction = report["contradictions"][0]
    assert "stance_a" in contradiction
    assert "stance_b" in contradiction
    assert "analysis" in contradiction
