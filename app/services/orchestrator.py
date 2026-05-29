import asyncio
from app.services.youtube_service import YouTubeService
from app.services.comment_preprocessor import CommentPreprocessor
from app.services.clustering_service import ClusteringService
from app.services.openrouter_service import OpenRouterService
from app.services.intelligence_aggregator import IntelligenceAggregator
from app.core.cache import cache_get, cache_set

class SignalOrchestrator:
    def __init__(self):
        self.youtube = YouTubeService()
        self.preprocessor = CommentPreprocessor()
        self.clustering = ClusteringService()
        self.openrouter = OpenRouterService()
        self.aggregator = IntelligenceAggregator()

    async def collect_guest_signals(self, guest_name, guest_niche):
        cache_key = f"signals:{guest_name}:{guest_niche}"
        cached = await cache_get(cache_key)
        if cached:
            return cached

        # 1. Smart YouTube search (targeted, minimal)
        videos = await self.youtube.search_podcast_appearances(guest_name, guest_niche, max_results=7)
        # 2. Fetch top comments for each video (minimal, high-signal)
        comments = await self.youtube.fetch_top_comments(videos, max_comments=15)
        # 3. Preprocess: dedup, filter, rank
        filtered_comments = self.preprocessor.preprocess(comments)
        # 4. Cluster comments for diversity
        clusters = self.clustering.cluster_comments(filtered_comments, max_clusters=5)
        # 5. Summarize clusters for LLM
        summaries = self.preprocessor.summarize_clusters(clusters)
        # 6. Batch LLM call (compressed prompt)
        intelligence = await self.openrouter.extract_intelligence(summaries)
        # 7. Aggregate and cache
        result = self.aggregator.aggregate(intelligence)
        await cache_set(cache_key, result)
        return result
