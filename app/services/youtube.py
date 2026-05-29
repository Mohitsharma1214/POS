import aiohttp
import logging
from typing import List
from app.schemas.guest import YouTubeResult
from app.config.settings import settings

class YouTubeSearchService:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY

    async def search(self, query: str, limit: int = 5) -> List[YouTubeResult]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": limit,
            "key": self.api_key
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    results = []
                    for item in data.get("items", []):
                        snippet = item.get("snippet", {})
                        video_id = item.get("id", {}).get("videoId")
                        if not video_id:
                            continue
                        results.append(YouTubeResult(
                            title=snippet.get("title", ""),
                            channel=snippet.get("channelTitle", ""),
                            published_at=snippet.get("publishedAt", ""),
                            video_url=f"https://www.youtube.com/watch?v={video_id}",
                            description=snippet.get("description", ""),
                            thumbnail_url=snippet.get("thumbnails", {}).get("default", {}).get("url", "")
                        ))
                    return results
        except Exception as e:
            logging.error(f"YouTube search failed: {e}")
            return []
