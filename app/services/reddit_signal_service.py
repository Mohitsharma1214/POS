import os
import re
import httpx
import logging
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from apify_client import ApifyClientAsync
from app.schemas.podcast_intelligence_output import RedditDiscussion

logger = logging.getLogger(__name__)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_API_URL = "https://api.tavily.com/search"

class RedditSignalService:
    def __init__(self):
        self.apify_token = settings.APIFY_API_TOKEN
        self.tavily_api_key = TAVILY_API_KEY
        if self.apify_token:
            self.apify_client = ApifyClientAsync(self.apify_token)
        else:
            self.apify_client = None
            logger.warning("DIAGNOSTIC WARNING: APIFY_API_TOKEN not configured. Reddit crawler will use Tavily fallback.")

    async def get_reddit_discussions(self, guest_name: str) -> List[RedditDiscussion]:
        """
        Search Reddit discussions using Apify. Falls back to Tavily if API key is missing or Apify fails.
        """
        discussions = []
        if self.apify_client:
            logger.info(f"Using Apify Reddit scraper for query: '{guest_name}'")
            run_input = {
                "searches": [f"{guest_name}"],
                "maxItems": 15,
                "sort": "relevance",
                "time": "year"
            }
            try:
                import asyncio
                run = await asyncio.wait_for(
                    self.apify_client.actor("trudax/reddit-scraper").call(run_input=run_input), 
                    timeout=15.0
                )
                
                dataset = self.apify_client.dataset(run["defaultDatasetId"])
                dataset_items = await dataset.list_items()
                raw_results = dataset_items.items

                for item in raw_results:
                    url = item.get("url", "")
                    subreddit = item.get("subreddit", "r/podcast")
                    if not subreddit.startswith("r/"):
                        subreddit = f"r/{subreddit}"
                        
                    discussions.append(RedditDiscussion(
                        subreddit=subreddit,
                        post_title=item.get("title", ""),
                        post_text=item.get("text", "") or item.get("selftext", ""),
                        upvotes=item.get("upvotes", 0) or item.get("score", 0),
                        comments_count=item.get("numComments", 0),
                        public_sentiment=None,
                        recurring_opinions=[],
                        controversy_topics=[],
                        trending_score=float(item.get("upvotes", 0)),
                        url=url
                    ))
            except Exception as e:
                logger.error(f"Apify Reddit scraper failed: {e}. Falling back to Tavily.")

        if not discussions:
            logger.info(f"Falling back to Tavily for Reddit discussions for '{guest_name}'")
            discussions = await self._get_tavily_reddit_fallback(guest_name)
            
        return discussions

    async def _get_tavily_reddit_fallback(self, guest_name: str) -> List[RedditDiscussion]:
        if not self.tavily_api_key:
            return []
            
        headers = {
            "Authorization": f"Bearer {self.tavily_api_key}",
            "Content-Type": "application/json"
        }
        queries = [
            f"site:reddit.com {guest_name} controversy (2025 OR 2026)",
            f"site:reddit.com best {guest_name} podcast (2025 OR 2026)",
            f"{guest_name} criticism (2025 OR 2026)",
            f"site:reddit.com {guest_name} trending discussion (2025 OR 2026)"
        ]
        discussions = []
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                for q in queries:
                    body = {
                        "query": q, 
                        "max_results": 5,
                        "time_range": "year"
                    }
                    try:
                        resp = await client.post(TAVILY_API_URL, json=body, headers=headers)
                        if resp.status_code != 200:
                            continue
                        items = resp.json().get("results", [])
                        for item in items:
                            url = item.get("url", "")
                            # Try to extract a subreddit from the URL
                            subreddit_match = re.search(r"reddit\.com/r/([^/]+)", url)
                            subreddit = f"r/{subreddit_match.group(1)}" if subreddit_match else "r/podcast"
                            
                            discussions.append(RedditDiscussion(
                                subreddit=subreddit,
                                post_title=item.get("title", ""),
                                post_text=item.get("snippet", ""),
                                upvotes=int(item.get("score", 0) * 100),
                                comments_count=12,
                                public_sentiment=None,
                                recurring_opinions=[],
                                controversy_topics=[],
                                trending_score=item.get("score", 0.0),
                                url=url
                            ))
                    except Exception as e:
                        logger.error(f"Tavily get_reddit_discussions failed for {q}: {e}")
                        continue
        except Exception as e:
            logger.error(f"Tavily client initialization failed for discussions: {e}")
        return discussions
