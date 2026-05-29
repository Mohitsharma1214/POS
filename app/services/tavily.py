import aiohttp
import logging
from typing import List
from app.schemas.guest import WebResult
from app.config.settings import settings

class TavilySearchService:
    BASE_URL = "https://api.tavily.com/search"

    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY

    async def search(self, query: str, limit: int = 5) -> List[WebResult]:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"query": query, "max_results": limit}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.BASE_URL, headers=headers, json=payload, timeout=10) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    results = []
                    for item in data.get("results", []):
                        results.append(WebResult(
                            title=item.get("title", ""),
                            url=item.get("url", ""),
                            snippet=item.get("snippet", ""),
                            source=item.get("source", ""),
                            content_type=item.get("content_type", ""),
                            published_date=item.get("published_date")
                        ))
                    return results
        except Exception as e:
            logging.error(f"Tavily search failed: {e}")
            return []
