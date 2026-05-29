from app.schemas.guest import GuestInput, ResearchResponse, ResearchMetadata, WebResult, YouTubeResult
from app.services.tavily import TavilySearchService
from app.services.youtube import YouTubeSearchService
from app.aggregators.research_aggregator import ResearchAggregator
from datetime import datetime
import logging

class GuestResearchAgent:
    def __init__(self):
        self.tavily = TavilySearchService()
        self.youtube = YouTubeSearchService()
        self.aggregator = ResearchAggregator()

    async def run(self, guest: GuestInput) -> dict:
        queries = self.generate_queries(guest)
        web_results, youtube_results = [], []
        for query in queries:
            web = await self.tavily.search(query)
            yt = await self.youtube.search(query)
            web_results.extend(web)
            youtube_results.extend(yt)
        agg = await self.aggregator.aggregate(guest, queries, web_results, youtube_results)
        return agg

    def generate_queries(self, guest: GuestInput) -> list:
        name = guest.guest_name.strip()
        queries = [
            f"{name} podcast",
            f"{name} interview",
            f"{name} latest news",
            f"{name} controversy",
            f"{name} startup advice",
            f"{name} AI predictions",
            f"{name} recent discussions"
        ]
        # Optionally add company/niche/context
        if guest.guest_company:
            queries.append(f"{name} {guest.guest_company}")
        if guest.guest_niche:
            queries.append(f"{name} {guest.guest_niche}")
        if guest.podcast_context:
            queries.append(f"{name} {guest.podcast_context}")
        return queries
