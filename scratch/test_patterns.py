import os
import sys
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.services.claude_pattern_service import ClaudePatternService
from app.services.signal_collection_service import SignalCollectionService

async def test():
    print("Collecting signals...")
    signal_service = SignalCollectionService()
    signals = await signal_service.collect_signals("Anthony Scaramucci", "politics")
    
    print("Extracting patterns...")
    pattern_service = ClaudePatternService()
    report = await pattern_service.extract_patterns(signals.apify_scrape_episodes)
    
    print("\n=== PATTERN REPORT ===")
    print(f"Title Formulas Count: {len(report.title_formulas)}")
    print(f"Thumbnail Patterns Count: {len(report.thumbnail_patterns)}")
    print(f"Hook Structures Count: {len(report.hook_structures)}")
    print(f"Clip Bait Moments Count: {len(report.clip_bait_moments)}")
    
    for idx, c in enumerate(report.clip_bait_moments):
        print(f"\nClip {idx+1}:")
        print(f"  Title: {c.title}")
        print(f"  Description: {c.description}")
        print(f"  Trigger Statement: {c.trigger_statement}")
        print(f"  Score: {c.virality_score}")
        print(f"  Platforms: {c.platforms}")

if __name__ == '__main__':
    asyncio.run(test())
