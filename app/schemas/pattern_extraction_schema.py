from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ClipBaitMoment(BaseModel):
    title: str = Field(..., description="Short name or hook of the clip-bait moment")
    description: str = Field(..., description="Description of the moment or core argument")
    trigger_statement: str = Field(..., description="The highly engaging or polarizing statement or hook segment")
    virality_score: float = Field(..., description="Confidence score of virality from 0.0 to 1.0")
    platforms: List[str] = Field(default_factory=list, description="Recommended platforms, e.g. TikTok, YouTube Shorts, Reels")

class PatternReport(BaseModel):
    title_formulas: List[str] = Field(default_factory=list, description="Extracted title formulas and blueprints")
    thumbnail_patterns: List[str] = Field(default_factory=list, description="Extracted thumbnail visual patterns and hooks")
    hook_structures: List[str] = Field(default_factory=list, description="Common hook structures in the first 60 seconds")
    question_styles: List[str] = Field(default_factory=list, description="Interviewer question styles and pacing methods")
    episode_formats: List[str] = Field(default_factory=list, description="Common macro episode structures and formats")
    audience_retention_angles: List[str] = Field(default_factory=list, description="Storytelling or editing loops used to keep retention")
    clip_bait_moments: List[ClipBaitMoment] = Field(default_factory=list, description="Highly clippable or shareable viral moments")

class PatternExtractionResponse(BaseModel):
    guest_name: str
    apify_scrape_episodes: List[Any] = Field(default_factory=list, description="Scraped episodes analyzed for the report")
    pattern_report: PatternReport

