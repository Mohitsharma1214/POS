import os
import sys
import asyncio
import json
from dotenv import load_dotenv

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app.services.signal_collection_service import SignalCollectionService

async def main():
    print("Initializing SignalCollectionService...")
    service = SignalCollectionService()
    
    print("Running research pipeline for 'Anthony Scaramucci'...")
    try:
        result = await service.collect_signals("Anthony Scaramucci", "politics")
        print("\n=== PIPELINE SUCCESS ===")
        print(f"Guest Name: {result.guest_name}")
        print(f"Number of Viral Topics Extracted: {len(result.viral_topics)}")
        print(f"Number of Guest Appearances Extracted: {len(result.top_performing_guest_episodes)}")
        print(f"Number of Niche Trends Extracted: {len(result.top_niche_trends)}")
        
        print("\n=== TOP GUEST EPISODES (First 5) ===")
        for idx, ep in enumerate(result.top_performing_guest_episodes[:5]):
            print(f"[{idx+1}] Title: {ep.title}")
            print(f"    Channel: {ep.channel_name}")
            print(f"    Views: {ep.views}")
            print(f"    Publish Date: {ep.publish_date}")
            print("-" * 50)

        print("\n=== TOP NICHE TRENDS (First 5) ===")
        for idx, trend in enumerate(result.top_niche_trends[:5]):
            print(f"[{idx+1}] Title: {trend.title}")
            print(f"    Views: {trend.views}")
            print(f"    Publish Date: {trend.publish_date}")
            print("-" * 50)

        print("\n=== DETAILED VIRAL TOPICS ===")
        for idx, t in enumerate(result.viral_topics):
            # Encode/decode to clean up non-ASCII characters for safe Windows printing
            clean_name = t.topic_name.encode('ascii', 'ignore').decode('ascii')
            clean_desc = t.description.encode('ascii', 'ignore').decode('ascii')
            print(f"[{idx+1}] Topic: {clean_name}")
            print(f"    Freq: {t.frequency}")
            print(f"    Engagement Score: {t.engagement_level}")
            print(f"    Mentions: {t.cross_platform_mentions}")
            print(f"    Description: {clean_desc}")
            print("-" * 50)
            
    except Exception as e:
        clean_err = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"\n[Error] Pipeline failed: {clean_err}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
