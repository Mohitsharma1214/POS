from datetime import datetime
from typing import Dict

def compute_relevance(result: Dict, now: datetime) -> float:
    # Recency: newer = higher
    published = result.get('published_date') or result.get('published_at')
    recency_score = 0.5
    if published:
        try:
            dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
            days = (now - dt).days
            recency_score = max(0.1, 1.0 - min(days, 365) / 365)
        except Exception:
            recency_score = 0.5
    # Authority
    authority = result.get('source_authority_score', 0.5)
    # Keyword match (simple)
    keyword_score = 1.0 if 'podcast' in result.get('title', '').lower() else 0.5
    # Engagement (placeholder)
    engagement = 0.5
    # Podcast relevance (placeholder)
    podcast_relevance = 1.0 if result.get('content_type') in ['podcast', 'interview'] else 0.5
    # Weighted sum
    score = 0.3 * recency_score + 0.3 * authority + 0.2 * keyword_score + 0.1 * engagement + 0.1 * podcast_relevance
    return round(score, 3)
