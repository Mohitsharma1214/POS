import os
import sys
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.services.claude_pattern_service import ClaudePatternService
from app.schemas.podcast_intelligence_output import ApifyScrapeEpisode

async def test():
    print("Testing isolated ClaudePatternService...")
    pattern_service = ClaudePatternService()
    
    # 1. Create a mock list of episodes to bypass SignalCollectionService entirely!
    mock_episodes = [
        ApifyScrapeEpisode(
            title="Anthony Scaramucci on Trump, Bitcoin, & Rebounding | Lex Fridman Podcast #421",
            url="https://youtube.com/watch?v=mock1",
            description="Deep dive on Macro, Trump, and Bitcoin.",
            view_count=1200000,
            comment_themes=["rebounding from failures", "bitcoin macro", "trump strategy"]
        )
    ]
    
    print("Extracting patterns via OpenRouter...")
    report = await pattern_service.extract_patterns(mock_episodes)
    
    print("\n=== ISOLATED PATTERN REPORT ===")
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
