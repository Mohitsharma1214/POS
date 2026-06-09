# YouTube Comment Intelligence Service
# Handles collection and analysis of YouTube comments

from typing import List
from app.schemas.signal_collection_schema import YouTubeCommentIntelligence, TopGuestAppearance

import os
import httpx
import logging
from app.services.youtube_key_manager import YouTubeKeyManager

logger = logging.getLogger(__name__)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

class YouTubeCommentService:
    def __init__(self):
        self.key_manager = YouTubeKeyManager()
        if not self.key_manager.has_keys():
            logger.warning(
                "DIAGNOSTIC WARNING: YOUTUBE_API_KEY is not configured in environment or .env. "
                "YouTube comment retrieval will be bypassed."
            )

    async def get_comment_threads(self, appearances: List[TopGuestAppearance]) -> List[dict]:
        import asyncio
        
        if not self.key_manager.has_keys():
            logger.warning("Bypassing YouTube comment fetching: YOUTUBE_API_KEY is missing.")
            return []
        
        async def fetch_thread(client, appearance):
            video_id = appearance.video_id
            
            max_attempts = len(self.key_manager.keys)
            attempts = 0
            
            while attempts < max_attempts:
                current_key = self.key_manager.get_current_key()
                # Fetch up to 50 comments per video as requested
                params = {
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": 50,
                    "key": current_key
                }
                try:
                    resp = await client.get(f"{YOUTUBE_API_URL}/commentThreads", params=params)
                    if resp.status_code == 403:
                        error_data = resp.json().get("error", {})
                        reason = ""
                        for error in error_data.get("errors", []):
                            reason = error.get("reason", "")
                            if reason == "commentsDisabled":
                                return None
                        
                        logger.error(
                            f"DIAGNOSTIC ERROR: YouTube Comments call FORBIDDEN (403) for video {video_id}. "
                            f"Reason: {reason}. Rotating key..."
                        )
                        self.key_manager.mark_key_exhausted()
                        attempts += 1
                        continue
                    elif resp.status_code != 200:
                        logger.error(
                            f"DIAGNOSTIC ERROR: YouTube Comments call failed with status {resp.status_code} for video {video_id}. "
                            f"Response: {resp.text}"
                        )
                        return None
                    
                    items = resp.json().get("items", [])
                    comments = []
                    for item in items:
                        top_comment = item["snippet"]["topLevelComment"]["snippet"]
                        comments.append({
                            "text": top_comment.get("textDisplay", ""),
                            "author": top_comment.get("authorDisplayName", ""),
                            "likeCount": top_comment.get("likeCount", 0),
                            "publishedAt": top_comment.get("publishedAt", "")
                        })
                    return {
                        "video_id": video_id,
                        "comments": comments
                    }
                except Exception as e:
                    logger.error(f"Network error while fetching comments for video {video_id}: {str(e)}")
                    return None
                    
            logger.error(f"All {max_attempts} YouTube API keys exhausted for comment threads fetch on video {video_id}.")
            return None

        threads = []
        try:
            # Expand pool to attempt more candidates if comments are disabled
            async with httpx.AsyncClient(timeout=15.0) as client:
                tasks = [fetch_thread(client, app) for app in appearances]
                results = await asyncio.gather(*tasks)
                threads = [r for r in results if r is not None]
        except Exception as e:
            logger.error(f"YouTube client initialization failed for comments: {e}")
        return threads
