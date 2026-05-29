# Signal Collection Schemas
from typing import List, Optional
from pydantic import BaseModel

class TopGuestAppearance(BaseModel):
    title: str
    video_id: str
    views: int
    likes: int
    thumbnails: List[str]
    description: str
    publish_date: str
    duration: int
    channel: str
    engagement_proxies: Optional[dict]
    virality_score: Optional[float]
    clip_potential: Optional[float]
    emotional_intensity: Optional[float]
    discussion_style: Optional[str]
    retention_style: Optional[str]
    content_type: Optional[str] = None
    summary: Optional[str] = None
    duration_seconds: Optional[int] = None
    relevance_score: Optional[float] = None
    engagement_rate: Optional[float] = None
    velocity: Optional[float] = None
    score: Optional[float] = None
    real_questions_asked: List[str] = []

class TopNicheVideo(BaseModel):
    title: str
    video_id: str
    views: int
    likes: int
    thumbnails: List[str]
    description: str
    publish_date: str
    duration: int
    channel: str
    engagement_proxies: Optional[dict]
    viral_structures: Optional[List[str]]
    topic_momentum: Optional[str]
    attention_patterns: Optional[List[str]]
    thumbnail_trends: Optional[List[str]]
    title_formulas: Optional[List[str]]
    content_type: Optional[str] = None
    summary: Optional[str] = None
    duration_seconds: Optional[int] = None
    relevance_score: Optional[float] = None
    engagement_rate: Optional[float] = None
    velocity: Optional[float] = None
    score: Optional[float] = None
    real_questions_asked: List[str] = []

class YouTubeCommentIntelligence(BaseModel):
    video_id: str
    top_comments: List[str]
    repeated_reactions: Optional[List[str]]
    emotional_reactions: Optional[List[str]]
    recurring_questions: Optional[List[str]]
    controversial_reactions: Optional[List[str]]
    emotional_themes: Optional[List[str]]
    audience_psychology: Optional[List[str]]
    trust_signals: Optional[List[str]]
    skepticism: Optional[List[str]]
    curiosity: Optional[List[str]]
    outrage: Optional[List[str]]
    inspiration: Optional[List[str]]
    fear: Optional[List[str]]

class TwitterNarrative(BaseModel):
    tweet_id: str
    text: str
    author: str
    created_at: str
    viral_phrasing: Optional[List[str]]
    emotional_framing: Optional[List[str]]
    narrative_acceleration: Optional[str]
    controversy_spikes: Optional[str]
    audience_excitement: Optional[str]
    creator_psychology: Optional[List[str]]

class RedditDiscussion(BaseModel):
    url: str
    title: str
    discussion_themes: Optional[List[str]]
    controversy_momentum: Optional[str]
    public_sentiment: Optional[str]
    recurring_narratives: Optional[List[str]]

class ViralPatterns(BaseModel):
    title_formulas: List[str]
    hook_structures: List[str]
    thumbnail_patterns: List[str]
    retention_patterns: List[str]

class AudienceInterestSignal(BaseModel):
    description: str
    source: str
    score: Optional[float]

class HighSignalMoment(BaseModel):
    description: str
    video_id: Optional[str]
    timestamp: Optional[int]
    score: Optional[float]

class EmotionalPattern(BaseModel):
    type: str
    description: str
    source: str

class GuestSignalCollection(BaseModel):

    top_guest_appearances: List[TopGuestAppearance]
    top_niche_videos: List[TopNicheVideo]
    youtube_comment_intelligence: List[YouTubeCommentIntelligence]
    twitter_narratives: List[TwitterNarrative]
    reddit_discussions: List[RedditDiscussion]
    trending_topics: List[str]
    viral_patterns: ViralPatterns
    audience_interest_signals: List[AudienceInterestSignal]
    high_signal_moments: List[HighSignalMoment]
    emotional_patterns: List[EmotionalPattern]
    guest_overview: Optional[dict] = None
    podcast_intelligence: Optional[dict] = None
    emotional_intelligence: Optional[dict] = None
    narrative_evolution: Optional[dict] = None
    extra: Optional[dict] = None

    class Config:
        extra = 'allow'
