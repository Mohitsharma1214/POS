from typing import List
from app.schemas.guest import GuestInput, ResearchMetadata, WebResult, YouTubeResult
from app.schemas.intelligence import IntelligenceOutput
from typing import List
from app.schemas.guest import GuestInput, ResearchMetadata, WebResult, YouTubeResult
from app.schemas.intelligence import IntelligenceOutput
def deduplicate_web_results(results: List[WebResult]) -> List[WebResult]:
    seen = set()
    deduped = []
    for r in results:
        key = hashlib.md5((r.title + r.url).encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped
def deduplicate_youtube_results(results: List[YouTubeResult]) -> List[YouTubeResult]:
    seen = set()
    deduped = []
    for r in results:
        key = hashlib.md5((r.title + r.video_url).encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped

from typing import List
from app.schemas.guest import GuestInput, ResearchMetadata, WebResult, YouTubeResult
from app.schemas.intelligence import IntelligenceOutput
from datetime import datetime
import asyncio
import hashlib
from app.intelligence.deduplication import deduplicate_exact_url, deduplicate_normalized_url, deduplicate_fuzzy_title, deduplicate_youtube
from app.classification.source_classifier import classify_source
from app.clustering.topic_clustering import cluster_topics
from app.ranking.relevance import compute_relevance
from app.intelligence.narrative import extract_narrative
from app.intelligence.controversy import detect_controversies
from app.intelligence.research_summary import generate_research_summary

class ResearchAggregator:
    async def aggregate(self, guest: GuestInput, queries: list, web_results: list, youtube_results: list) -> dict:
        from app.agents.intelligence_agent import IntelligenceAgent
        now = datetime.utcnow()
        # Deduplication
        web = deduplicate_exact_url(web_results)
        web = deduplicate_normalized_url(web)
        web = deduplicate_fuzzy_title(web)
        yt = deduplicate_youtube(youtube_results)

        # Source classification and authority scoring
        classified_web = []
        for r in web:
            url, content_type, authority = classify_source(r.url, r.title, r.snippet)
            d = r.dict()
            d['content_type'] = content_type
            d['source_authority_score'] = authority
            classified_web.append(d)
        classified_yt = []
        for r in yt:
            url, content_type, authority = classify_source(r.video_url, r.title, r.description)
            d = r.dict()
            d['content_type'] = content_type
            d['source_authority_score'] = authority
            classified_yt.append(d)

        # Relevance ranking
        for r in classified_web + classified_yt:
            r['relevance_score'] = compute_relevance(r, now)
        classified_web = sorted(classified_web, key=lambda x: x['relevance_score'], reverse=True)
        classified_yt = sorted(classified_yt, key=lambda x: x['relevance_score'], reverse=True)

        # --- Semantic Intelligence Layer ---
        intelligence_agent = IntelligenceAgent()
        intelligence = await intelligence_agent.run(
            guest={
                "name": guest.guest_name,
                "company": guest.guest_company,
                "niche": guest.guest_niche
            },
            web_results=classified_web,
            youtube_results=classified_yt
        )

        metadata = ResearchMetadata(
            generated_at=now.isoformat() + 'Z',
            queries_used=queries,
            sources_count=len(classified_web) + len(classified_yt)
        )

        return {
            "guest": {
                "name": guest.guest_name,
                "company": guest.guest_company,
                "niche": guest.guest_niche
            },
            "research_metadata": metadata.dict(),
            "web_results": classified_web,
            "youtube_results": classified_yt,
            "intelligence": intelligence.get("intelligence", intelligence)
        }
