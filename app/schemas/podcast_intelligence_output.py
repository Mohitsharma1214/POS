# --- Normalized Schemas ---
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class WebSignal(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    source: Optional[str] = None
    trending_score: Optional[float] = None

class TwitterSignal(BaseModel):
    tweet_text: str
    author: str
    created_at: str
    likes: int
    retweets: int
    replies: int
    views: int
    hashtags: List[str] = []
    engagement_score: Optional[float] = None
    recurring_topic: Optional[str] = None
    is_simulated: Optional[bool] = False

class NicheTrend(BaseModel):
    title: str
    video_id: str
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    publish_date: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    comments_count: Optional[int] = None
    engagement_ratio: Optional[float] = None
    ctr_proxy: Optional[float] = None
    growth_velocity: Optional[float] = None
    score: Optional[float] = None
    niche: Optional[str] = None
    description: Optional[str] = None
    real_questions_asked: List[str] = []

class Episode(BaseModel):
    title: str
    video_id: str
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    publish_date: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    comments_count: Optional[int] = None
    engagement_ratio: Optional[float] = None
    ctr_proxy: Optional[float] = None
    growth_velocity: Optional[float] = None
    score: Optional[float] = None
    channel_name: Optional[str] = None
    description: Optional[str] = None
    real_questions_asked: List[str] = []

class RedditDiscussion(BaseModel):
    subreddit: Optional[str] = None
    post_title: str
    post_text: Optional[str] = None
    upvotes: Optional[int] = None
    comments_count: Optional[int] = None
    public_sentiment: Optional[str] = None
    recurring_opinions: Optional[List[str]] = None
    controversy_topics: Optional[List[str]] = None
    trending_score: Optional[float] = None
    url: Optional[str] = None

class RawComment(BaseModel):
    text: str
    author: str
    like_count: int
    published_at: str

class CommentInsight(BaseModel):
    video_id: str
    recurring_themes: List[str] = []
    audience_emotions: List[str] = []
    objections: List[str] = []
    requests: List[str] = []
    viral_moments: List[str] = []
    hidden_demand_signals: List[str] = []
    raw_comments: List[RawComment] = []
    commenter_questions: List[str] = []

class NarrativeCluster(BaseModel):
    narrative: str
    source_platforms: List[str] = []
    frequency: Optional[int] = None
    sentiment: Optional[str] = None
    controversy_level: Optional[str] = None

class WeightedScore(BaseModel):
    video_id: str
    score: float
    reason: str
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

class SimilarGuest(BaseModel):
    guest_name: str
    related_episode_titles: List[str] = []
    audience_overlap_reason: Optional[str] = None
    overlap_score: Optional[float] = None
    niche: Optional[str] = None
    bookability_score: Optional[float] = None
    primary_platform: Optional[str] = None

class ViralTopic(BaseModel):
    topic_name: str
    frequency: int
    engagement_level: float
    cross_platform_mentions: int
    description: Optional[str] = None

class TrendingPodcastEpisode(BaseModel):
    title: str
    source: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None

class ApifyScrapeEpisode(BaseModel):
    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    view_count: Optional[int] = None
    comment_themes: List[str] = []

class InstagramSignal(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    engagement_score: Optional[float] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    views: Optional[int] = None
    is_simulated: Optional[bool] = False

class InstagramIntelligence(BaseModel):
    raw_signals: List[InstagramSignal] = Field(default_factory=list)
    viral_themes: List[str] = Field(default_factory=list)
    audience_sentiment: str = ""
    persona_delta: str = ""
    is_simulated: Optional[bool] = False
    instagram_handle: Optional[str] = ""

class TwitterIntelligence(BaseModel):
    raw_signals: List[TwitterSignal] = Field(default_factory=list)
    viral_themes: List[str] = Field(default_factory=list)
    audience_sentiment: str = ""
    persona_delta: str = ""
    is_simulated: Optional[bool] = False
    twitter_handle: Optional[str] = ""

class PodcastIntelligenceOutput(BaseModel):
    guest_name: Optional[str] = None
    inferred_niche: Optional[str] = None
    inferred_podcast_context: Optional[str] = None
    
    top_performing_guest_episodes: List[Episode] = Field(default_factory=list, description="Top youtube episodes from guest")
    top_niche_trends: List[NicheTrend] = Field(default_factory=list, description="Top trends within the given niche")
    
    twitter_signals: List[TwitterSignal] = Field(default_factory=list, description="Signals collected from Twitter/X")
    reddit_discussions: List[RedditDiscussion] = Field(default_factory=list, description="Trending and controversial Reddit threads")
    instagram_intelligence: InstagramIntelligence = Field(default_factory=InstagramIntelligence, description="AI-analyzed Instagram signals")
    twitter_intelligence: TwitterIntelligence = Field(default_factory=TwitterIntelligence, description="AI-analyzed Twitter/X signals")
    
    similar_guests: List[SimilarGuest] = Field(default_factory=list, description="Guests with similar audience overlap")
    viral_topics: List[ViralTopic] = Field(default_factory=list, description="Topics currently gaining traction for this guest")
    cross_platform_narratives: List[NarrativeCluster] = Field(default_factory=list, description="Narratives that appear across multiple platforms")
    weighted_scores: List[WeightedScore] = Field(default_factory=list, description="Scoring across various metrics like controversy, engagement, etc")
    
    tavily_web_signals: List[WebSignal] = Field(default_factory=list, description="Web signals collected via Tavily search")
    comment_intelligence: List[CommentInsight] = Field(default_factory=list, description="Insights aggregated from video comments")

    structured_insights: Optional[Dict[str, Any]] = Field(default_factory=dict, description="LLM-generated insights like strategic_recommendations, risks, opportunities, etc.")
    
    trending_podcast_episodes: List[TrendingPodcastEpisode] = []
    apify_scrape_episodes: List[ApifyScrapeEpisode] = []
