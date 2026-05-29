import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.claude_pattern_service import ClaudePatternService

def test():
    print("Testing custom-tailored fallback report for Anthony Scaramucci...")
    service = ClaudePatternService()
    report = service._get_fallback_pattern_report("Anthony Scaramucci")
    
    print("\n=== VERIFIED CUSTOM FALLBACK PATTERNS ===")
    print(f"Title Formulas Count: {len(report.title_formulas)}")
    print(f"Thumbnail Patterns Count: {len(report.thumbnail_patterns)}")
    print(f"Hook Structures Count: {len(report.hook_structures)}")
    print(f"Clip Bait Moments Count: {len(report.clip_bait_moments)}")
    
    # Assertions
    assert len(report.clip_bait_moments) == 4, f"Expected 4 clippable moments, got {len(report.clip_bait_moments)}"
    
    for idx, c in enumerate(report.clip_bait_moments):
        print(f"\nClip {idx+1}:")
        print(f"  Title: {c.title}")
        print(f"  Description: {c.description}")
        print(f"  Trigger Statement: {c.trigger_statement}")
        print(f"  Virality Score: {c.virality_score}")
        print(f"  Platforms: {c.platforms}")
        
        assert c.title != "", "Clip title should not be empty!"
        assert c.trigger_statement != "", "Trigger statement should not be empty!"
        assert len(c.platforms) > 0, "Platforms should not be empty!"

    print("\nAll custom-tailored fallback assertions passed!")

if __name__ == '__main__':
    test()
