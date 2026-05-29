import hashlib
from typing import List
from app.schemas.guest import WebResult, YouTubeResult
import difflib

# Exact URL deduplication

def deduplicate_exact_url(results: List[WebResult]) -> List[WebResult]:
    seen = set()
    deduped = []
    for r in results:
        if r.url not in seen:
            seen.add(r.url)
            deduped.append(r)
    return deduped

# Normalized URL deduplication

def normalize_url(url: str) -> str:
    return url.lower().replace('www.', '').split('?')[0].rstrip('/')

def deduplicate_normalized_url(results: List[WebResult]) -> List[WebResult]:
    seen = set()
    deduped = []
    for r in results:
        norm = normalize_url(r.url)
        if norm not in seen:
            seen.add(norm)
            deduped.append(r)
    return deduped

# Fuzzy title matching (preparing for embedding similarity)

def deduplicate_fuzzy_title(results: List[WebResult], threshold: float = 0.85) -> List[WebResult]:
    deduped = []
    for r in results:
        if not any(difflib.SequenceMatcher(None, r.title, d.title).ratio() > threshold for d in deduped):
            deduped.append(r)
    return deduped

# For YouTube, deduplicate by video_url and fuzzy title

def deduplicate_youtube(results: List[YouTubeResult], threshold: float = 0.85) -> List[YouTubeResult]:
    seen = set()
    deduped = []
    for r in results:
        if r.video_url not in seen and not any(difflib.SequenceMatcher(None, r.title, d.title).ratio() > threshold for d in deduped):
            seen.add(r.video_url)
            deduped.append(r)
    return deduped
