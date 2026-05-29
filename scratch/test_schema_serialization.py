import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas.pattern_extraction_schema import PatternExtractionResponse, PatternReport, ClipBaitMoment
from app.services.claude_pattern_service import ClaudePatternService

def test():
    print("Testing serialization of ClaudePatternService fallback report...")
    service = ClaudePatternService()
    fallback = service._get_fallback_pattern_report()
    
    response = PatternExtractionResponse(
        guest_name="Anthony Scaramucci",
        apify_scrape_episodes=[],
        pattern_report=fallback
    )
    
    # Model dump / json serialization in Pydantic
    try:
        # Pydantic v2
        json_str = response.model_dump_json(indent=2)
    except AttributeError:
        # Pydantic v1
        json_str = response.json(indent=2)
        
    print("\n=== SERIALIZED JSON ===")
    print(json_str[:1200] + "\n...")

if __name__ == '__main__':
    test()
