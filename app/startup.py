import os
import logging
from app.utils.logging import setup_logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def on_startup():
    setup_logging()
    
    # Run API diagnostics
    youtube_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()
    x_username = os.getenv("X_USERNAME", "").strip() or settings.X_USERNAME
    x_password = os.getenv("X_PASSWORD", "").strip() or settings.X_PASSWORD
    
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
    
    # 2. OpenRouter API Key Check
    if openrouter_key:
        print(f"  [ OK ] OPENROUTER_API_KEY: ACTIVE (Found: '{openrouter_key[:8]}...{openrouter_key[-4:] if len(openrouter_key) > 4 else ''}')")
        print("         STATUS: LLM deep synthesis, transcript question extraction, and Step 4 playbooks active.")
    else:
        print("  [ MISSING ] OPENROUTER_API_KEY: MISSING")
        print("              CRITICAL ERROR: LLM question extraction, Step 2 Pattern Report, and")
        print("              Step 4 Virality Brief generation will fail! Please configure your OpenRouter key.")
    print("-" * 80)
    
    # 3. Tavily API Key Check
    if tavily_key:
        print(f"  [ OK ] TAVILY_API_KEY:     ACTIVE (Found: '{tavily_key[:8]}...{tavily_key[-4:] if len(tavily_key) > 4 else ''}')")
        print("         STATUS: Real-time Google/Reddit search discovery is active.")
    else:
        print("  [ MISSING ] TAVILY_API_KEY:     Bypassed")
        print("              WARNING: Web discovery is offline. Web signal/Reddit lists will run on fallbacks.")
    print("-" * 80)
    
    # 4. Twitter / X Credentials Check
    if x_username and x_password:
        print(f"  [ OK ] X_CREDENTIALS:      ACTIVE (Username: '{x_username}')")
        print("         STATUS: Live X/Twitter signal scraping via Twikit is active.")
    else:
        print("  [ MISSING ] X_CREDENTIALS:      Bypassed")
        print("              WARNING: Live Twitter scraping is offline.")
        print("              Ensure both X_USERNAME and X_PASSWORD are set in your .env file to enable live scraping.")
        
    print("=" * 80)
    print("  * For absolute real-time mock-free execution, ensure all keys above are [ OK ].")
    print("=" * 80 + "\n")


