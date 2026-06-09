
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
