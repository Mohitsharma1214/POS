import os
import logging
from app.utils.logging import setup_logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def on_startup():
    setup_logging()
    
    # Run API diagnostics
    youtube_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip() or settings.ANTHROPIC_API_KEY
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()
    apify_token = os.getenv("APIFY_API_TOKEN", "").strip() or settings.APIFY_API_TOKEN
    
    print("\n" + "=" * 80)
    print("              PODCAST INTELLIGENCE API READINESS DIAGNOSTIC REPORT")
    print("=" * 80)
    
    # 1. YouTube API Key Check
    if youtube_key:
        print(f"  [ OK ] YOUTUBE_API_KEY:    ACTIVE (Found: '{youtube_key[:8]}...{youtube_key[-4:] if len(youtube_key) > 4 else ''}')")
        print("         STATUS: Real YouTube video metadata, search, and comment retrieval is active.")
    else:
        print("  [ MISSING ] YOUTUBE_API_KEY:    Bypassed")
        print("              WARNING: Real YouTube features are offline.")
        print("              All YouTube search data and comments will run via high-fidelity fallback mock pipelines.")
    print("-" * 80)
    
    # 2. Anthropic API Key Check
    if anthropic_key:
        print(f"  [ OK ] ANTHROPIC_API_KEY:  ACTIVE (Found: '{anthropic_key[:8]}...{anthropic_key[-4:] if len(anthropic_key) > 4 else ''}')")
        print("         STATUS: LLM deep synthesis, transcript question extraction, and Step 4 playbooks active.")
    else:
        print("  [ MISSING ] ANTHROPIC_API_KEY:  MISSING")
        print("              CRITICAL ERROR: LLM question extraction, Step 2 Pattern Report, and")
        print("              Step 4 Virality Brief generation will fail! Please configure your Anthropic key.")
    print("-" * 80)
    
    # 3. Tavily API Key Check
    if tavily_key:
        print(f"  [ OK ] TAVILY_API_KEY:     ACTIVE (Found: '{tavily_key[:8]}...{tavily_key[-4:] if len(tavily_key) > 4 else ''}')")
        print("         STATUS: Real-time Google/Reddit search discovery is active.")
    else:
        print("  [ MISSING ] TAVILY_API_KEY:     Bypassed")
        print("              WARNING: Web discovery is offline. Web signal/Reddit lists will run on fallbacks.")
    print("-" * 80)
    

    
    # 5. Apify Token Check
    if apify_token:
        print(f"  [ OK ] APIFY_API_TOKEN:    ACTIVE (Found: '{apify_token[:8]}...{apify_token[-4:] if len(apify_token) > 4 else ''}')")
        print("         STATUS: Live Twitter, LinkedIn, Instagram, and Reddit scraping via Apify is active.")
    else:
        print("  [ MISSING ] APIFY_API_TOKEN:    Bypassed")
        print("              WARNING: Real-time scraping is offline for major social platforms.")
        print("              Will run on high-fidelity mock data fallback.")
    print("-" * 80)
    

    print("=" * 80)
    print("  * For absolute real-time mock-free execution, ensure all keys above are [ OK ].")
    print("=" * 80 + "\n")


