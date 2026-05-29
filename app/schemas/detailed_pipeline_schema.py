from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Step1Signals(BaseModel):
    """Raw data collected in Step 1 (Signal Collection)."""
    apify_scrape_episodes: List[Any] = Field(default_factory=list)
    top_performing_guest_episodes: List[Any] = Field(default_factory=list)
    tavily_web_signals: List[Any] = Field(default_factory=list)
    comment_intelligence: List[Any] = Field(default_factory=list)
    twitter_signals: List[Any] = Field(default_factory=list)
    reddit_discussions: List[Any] = Field(default_factory=list)
    instagram_intelligence: Dict[str, Any] = Field(default_factory=dict)
    twitter_intelligence: Dict[str, Any] = Field(default_factory=dict)
    similar_guests: List[Any] = Field(default_factory=list)
    viral_topics: List[Any] = Field(default_factory=list)
    cross_platform_narratives: List[Any] = Field(default_factory=list)
    weighted_scores: List[Any] = Field(default_factory=list)
    structured_insights: Dict[str, Any] = Field(default_factory=dict)
    trending_podcast_episodes: List[Any] = Field(default_factory=list)

class DetailedPipelineOutput(BaseModel):
    step1: Step1Signals
    step2_patterns: Dict[str, Any] = Field(default_factory=dict)
    step3_intelligence: Dict[str, Any] = Field(default_factory=dict)
    step4_brief: Dict[str, Any] = Field(default_factory=dict)
    step4_scoring: Dict[str, Any] = Field(default_factory=dict)
