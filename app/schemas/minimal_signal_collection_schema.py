from typing import List, Any
from pydantic import BaseModel

class MinimalTopGuestAppearance(BaseModel):
    title: str
    video_id: str
    views: int
    description: str
    publish_date: str
    duration: int
    channel: str

class MinimalTopNicheVideo(BaseModel):
    title: str
    video_id: str
    views: int
    description: str
    publish_date: str
    duration: int
    channel: str

class MinimalTrendingPodcastEpisode(BaseModel):
    title: str
    source: str
    url: str
    description: str

class MinimalApifyScrapeEpisode(BaseModel):
    title: str
    description: str
    view_count: int
    comment_themes: List[str]

class MinimalGuestSignalCollection(BaseModel):
    top_guest_appearances: List[MinimalTopGuestAppearance]
    top_niche_videos: List[MinimalTopNicheVideo]
    trending_podcast_episodes: List[MinimalTrendingPodcastEpisode]
    apify_scrape: List[MinimalApifyScrapeEpisode]
