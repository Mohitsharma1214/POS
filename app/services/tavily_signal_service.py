
import re
import os
import httpx
from typing import List
from app.schemas.podcast_intelligence_output import WebSignal, RedditDiscussion

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_API_URL = "https://api.tavily.com/search"


class TavilySignalService:
    def __init__(self):
        self.api_key = TAVILY_API_KEY

    async def search_web(self, guest_name: str, max_results: int = 15) -> List[WebSignal]:
        """
        Searches the web for signals related to the guest using Tavily API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Append active year filters to strictly restrict results to the last 1 year
        body = {
            "query": f"{guest_name} (2025 OR 2026)", 
            "max_results": max_results,
            "time_range": "year"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(TAVILY_API_URL, json=body, headers=headers)
                if resp.status_code != 200:
                    return []
                items = resp.json().get("results", [])
        except Exception as e:
            import logging
            logging.error(f"Tavily search_web failed for {guest_name}: {e}")
            return []

        web_signals = []
        for item in items:
            web_signals.append(WebSignal(
                title=item.get("title", ""),
                url=item.get("url", ""),
                source=item.get("source", ""),
                snippet=item.get("content", "") or item.get("snippet", ""),
                trending_score=item.get("score", 0.0)
            ))
        return web_signals

    async def get_reddit_discussions(self, guest_name: str) -> List[RedditDiscussion]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Append strict year parameters to ensure no legacy/9-year-old threads leak in
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
                        import logging
                        logging.error(f"Tavily get_reddit_discussions failed for {q}: {e}")
                        continue
        except Exception as e:
            import logging
            logging.error(f"Tavily client initialization failed for discussions: {e}")
        return discussions

    async def get_trending_topics(self, guest_name: str) -> List[str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "query": f"{guest_name} trending (2025 OR 2026)", 
            "max_results": 10,
            "time_range": "year"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(TAVILY_API_URL, json=body, headers=headers)
                if resp.status_code != 200:
                    return []
                items = resp.json().get("results", [])
                return [item.get("title", "") for item in items]
        except Exception as e:
            import logging
            logging.error(f"Tavily get_trending_topics failed for {guest_name}: {e}")
            return []
