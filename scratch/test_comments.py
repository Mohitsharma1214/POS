import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Load env variables
load_dotenv(r"e:\Youtube-Transcriptors\podcast-intelligence\.env")
sys.path.append(r"e:\Youtube-Transcriptors\podcast-intelligence")

logging.basicConfig(level=logging.INFO)

from app.schemas.signal_collection_schema import TopGuestAppearance
from app.services.youtube_comment_service import YouTubeCommentService
from app.services.openrouter_service import OpenRouterService

async def main():
    comment_service = YouTubeCommentService()
    openrouter_service = OpenRouterService()
    
    # Mock one of the videos to check
    appearance = TopGuestAppearance(
        title="Michael Wolff: Melania Fucking Hates Her Husband | Anthony Scaramucci | Open Book",
        video_id="IRjGoZQShB0",
        views=100000,
        likes=5000,
        thumbnails=[""],
        description="Test video description",
        publish_date="2026-05-22",
        duration=3000,
        channel="Open Book",
        engagement_proxies={},
        virality_score=1.0,
        clip_potential=0.5,
        emotional_intensity=0.5,
        discussion_style="test",
        retention_style="test",
        content_type="podcast",
        duration_seconds=3000,
        relevance_score=100.0
    )
    
    print("\n--- Testing Comments Fetch ---")
    threads = await comment_service.get_comment_threads([appearance])
    if not threads:
        print("ERROR: No threads fetched or fetch returned None.")
        return
        
    thread = threads[0]
    print(f"Successfully fetched {len(thread['comments'])} comments!")
    
    comment_texts = [c["text"] for c in thread["comments"] if c.get("text")]
    
    print("\n--- Testing OpenRouter Synthesis ---")
    prompt = f"""
    Extract YouTube audience intelligence.
    
    Return JSON only:
    {{
        "recurring_themes": [],
        "audience_emotions": [],
        "objections": [],
        "requests": [],
        "viral_moments": [],
        "hidden_demand_signals": []
    }}
    
    Comments:
    {comment_texts}
    """
    
    try:
        print("Sending prompt to OpenRouter...")
        enrichment = await openrouter_service.complete(prompt)
        print("SUCCESS! Enrichment response received.")
        # Print with encoding fallback or just print keys
        print(f"Keys returned in enrichment: {list(enrichment.keys())}")
        for k, v in enrichment.items():
            safe_val = str(v).encode('ascii', errors='replace').decode('ascii')
            print(f"  {k}: {safe_val}")
    except Exception as e:
        print(f"FAILED calling OpenRouter: {e}")

if __name__ == "__main__":
    asyncio.run(main())
