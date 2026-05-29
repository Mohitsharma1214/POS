import os
import sys
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.services.youtube_signal_service import YouTubeSignalService

async def test():
    print("Initializing YouTubeSignalService...")
    service = YouTubeSignalService()
    
    print("\n1. Testing get_top_guest_appearances for Anthony Scaramucci...")
    podcasts = await service.get_top_guest_appearances("Anthony Scaramucci")
    print(f"Total podcasts returned: {len(podcasts)}")
    
    print("\n--- SAMPLE PODCASTS ---")
    for idx, p in enumerate(podcasts[:3]):
        print(f"[{idx+1}] Title: {p.title}")
        print(f"    Channel: {p.channel}")
        print(f"    Publish Date: {p.publish_date}")
        print(f"    Duration: {p.duration}s ({p.duration/60:.1f}m)")
        print(f"    Views: {p.views}")
        print(f"    Likes: {p.likes}")
        print(f"    Engagement Score: {p.engagement_proxies.get('engagement_score')}")
    
    # Assertions
    assert len(podcasts) == 20, f"Expected 20 podcasts, got {len(podcasts)}"
    for p in podcasts:
        # Verify date is within 1 year
        from datetime import datetime, timezone
        pub_dt = datetime.fromisoformat(p.publish_date.replace("Z", "+00:00"))
        days_diff = (datetime.now(timezone.utc) - pub_dt).days
        assert days_diff <= 365, f"Publish date {p.publish_date} is older than 1 year! ({days_diff} days ago)"
    print("All podcast validation checks passed!")

    print("\n2. Testing get_top_niche_videos for politics...")
    niche_videos = await service.get_top_niche_videos("politics")
    print(f"Total niche videos returned: {len(niche_videos)}")
    
    print("\n--- SAMPLE NICHE VIDEOS ---")
    for idx, n in enumerate(niche_videos[:3]):
        print(f"[{idx+1}] Title: {n.title}")
        print(f"    Channel: {n.channel}")
        print(f"    Publish Date: {n.publish_date}")
        print(f"    Duration: {n.duration}s ({n.duration/60:.1f}m)")
        print(f"    Views: {n.views}")
    
    # Assertions
    assert len(niche_videos) == 20, f"Expected 20 niche videos, got {len(niche_videos)}"
    for n in niche_videos:
        from datetime import datetime, timezone
        pub_dt = datetime.fromisoformat(n.publish_date.replace("Z", "+00:00"))
        days_diff = (datetime.now(timezone.utc) - pub_dt).days
        assert days_diff <= 365, f"Niche publish date {n.publish_date} is older than 1 year! ({days_diff} days ago)"
    print("All niche video validation checks passed!")

if __name__ == '__main__':
    asyncio.run(test())
