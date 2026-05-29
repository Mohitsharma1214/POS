from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from app.schemas.podcast_intelligence_output import PodcastIntelligenceOutput

class GuestInput(BaseModel):
    guest_name: str = Field(..., example="Sam Altman")
    guest_company: Optional[str] = Field(None, example="OpenAI")
    guest_niche: Optional[str] = Field(None, example="Artificial Intelligence")
    podcast_context: Optional[str] = Field(None, example="AI startup podcast")
    apify_scrape_episodes: Optional[List[Any]] = Field(None, example=[])
    cached_patterns: Optional[dict] = Field(None)
    cached_intelligence: Optional[dict] = Field(None)
    cached_comments: Optional[list] = Field(None)




# Expanded for intelligence fields
class WebResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    content_type: str
    published_date: Optional[str] = None
    source_authority_score: Optional[float] = None
    relevance_score: Optional[float] = None


# Expanded for intelligence fields
class YouTubeResult(BaseModel):
    title: str
    channel: str
    published_at: str
    video_url: str
    description: str
    thumbnail_url: str
    content_type: Optional[str] = None
    source_authority_score: Optional[float] = None
    relevance_score: Optional[float] = None

class ResearchMetadata(BaseModel):
    generated_at: str
    queries_used: List[str]
    sources_count: int


# For new API, use PodcastIntelligenceOutput as the response model
