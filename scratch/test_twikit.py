import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Set up logging to console
logging.basicConfig(level=logging.INFO)

# Add parent directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables from .env file
load_dotenv()

from app.services.twitter_signal_service import TwitterSignalService

async def main():
    service = TwitterSignalService()
    
    print("\n==================================================")
    print("Testing free X/Twitter crawler via Twikit Async")
    print("==================================================")
    
    # Check if credentials are set
    username = os.getenv("X_USERNAME")
    password = os.getenv("X_PASSWORD")
    
    if not username or username == "your_burner_username":
        print("\nWARNING: X_USERNAME is not set or holds placeholder value in .env.")
        print("We will run the search, which will trigger the high-fidelity mock data fallback gracefully.")
    else:
        print(f"Using X credentials from .env: User='{username}'")
    
    print("\nExecuting search for 'Anthony Scaramucci'...")
    tweets = await service.search_tweets("Anthony Scaramucci", limit=3)
    
    print("\n================== TWITTER RESULTS ==================")
    for idx, t in enumerate(tweets):
        print(f"[{idx+1}] Author: @{t['author_username']} ({t['author_name']})")
        print(f"    Verified: {t['is_verified']}")
        print(f"    Text: {t['text'][:120]}...")
        print(f"    Likes: {t['likes']} | Retweets: {t['retweets']} | Replies: {t['replies']} | Views: {t['views']} | Bookmarks: {t.get('bookmarks', 0)}")
        print(f"    Engagement Score: {t['engagement_score']}")
        print(f"    ID: {t['tweet_id']}")
        print("-" * 52)
    print("=====================================================\n")

if __name__ == '__main__':
    asyncio.run(main())
