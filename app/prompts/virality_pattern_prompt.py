# Prompt for extracting virality patterns using OpenRouter

from app.schemas.signal_collection_schema import ViralPatterns
import json

async def extract_virality_patterns(appearances, niche_videos, comments, twitter_narratives, reddit_discussions, openrouter_service):
    prompt = (
        "Given the following podcast video data, comments, Twitter narratives, and Reddit discussions, "
        "extract the most common and effective: title formulas, hook structures, thumbnail patterns, and retention patterns. "
        "Return a JSON object matching the ViralPatterns schema.\n\n"
    )
    prompt += "Sample Titles:\n" + "\n".join([a.title for a in appearances[:5] if hasattr(a, 'title')]) + "\n"
    prompt += "Sample Niche Titles:\n" + "\n".join([n.title for n in niche_videos[:5] if hasattr(n, 'title')]) + "\n"
    prompt += "Sample Comments:\n" + "\n".join([c['comments'][0]['text'] for c in comments if c['comments']]) + "\n"
    # Handle twitter_narratives as dict with 'tweets' key (list of dicts)
    tweets = twitter_narratives.get("tweets", []) if isinstance(twitter_narratives, dict) else twitter_narratives
    prompt += "Sample Tweets:\n" + "\n".join([t["text"] for t in tweets[:5] if "text" in t]) + "\n"
    prompt += "Sample Reddit Titles:\n" + "\n".join([r.title for r in reddit_discussions[:5] if hasattr(r, 'title')]) + "\n"
    response = await openrouter_service.complete(prompt)
    try:
        parsed = json.loads(response) if isinstance(response, str) else response
        return ViralPatterns(**parsed)
    except Exception:
        return ViralPatterns(title_formulas=[], hook_structures=[], thumbnail_patterns=[], retention_patterns=[])
