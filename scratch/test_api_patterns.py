import os
import sys
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.api.routes.guest import extract_working_patterns
from app.schemas.guest import GuestInput

async def test():
    print("Calling router function extract_working_patterns directly...")
    guest_input = GuestInput(guest_name="Anthony Scaramucci", guest_niche="politics")
    response = await extract_working_patterns(guest_input)
    
    print("\n=== ROUTER RESPONSE ===")
    print(f"guest_name: {response.guest_name}")
    print(f"apify_scrape_episodes count: {len(response.apify_scrape_episodes)}")
    
    report = response.pattern_report
    print("\n=== PATTERN REPORT ===")
    print(f"title_formulas: {report.title_formulas}")
    print(f"thumbnail_patterns: {report.thumbnail_patterns}")
    print(f"hook_structures: {report.hook_structures}")
    print(f"question_styles: {report.question_styles}")
    print(f"episode_formats: {report.episode_formats}")
    print(f"audience_retention_angles: {report.audience_retention_angles}")
    print(f"clip_bait_moments count: {len(report.clip_bait_moments)}")
    
    for idx, c in enumerate(report.clip_bait_moments):
        print(f"\nClip {idx+1}:")
        print(f"  title: {c.title}")
        print(f"  description: {c.description}")
        print(f"  trigger_statement: {c.trigger_statement}")
        print(f"  virality_score: {c.virality_score}")
        print(f"  platforms: {c.platforms}")

if __name__ == '__main__':
    asyncio.run(test())
