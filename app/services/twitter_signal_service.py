# app/services/twitter_signal_service.py

import os
import re
import logging
import datetime
import httpx
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from apify_client import ApifyClientAsync

logger = logging.getLogger(__name__)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_API_URL = "https://api.tavily.com/search"

class TwitterSignalService:
    def __init__(self):
        self.api_key = TAVILY_API_KEY
        self.apify_token = settings.APIFY_API_TOKEN
        if self.apify_token:
            self.apify_client = ApifyClientAsync(self.apify_token)
        else:
            self.apify_client = None
            logger.warning(
                "DIAGNOSTIC WARNING: APIFY_API_TOKEN is not configured in .env. "
                "Twitter crawler will operate in high-fidelity mock fallback mode."
            )

    async def search_tweets(
        self,
        query: str,
        query_type: str = "Latest",
        limit: int = 10
    ) -> Tuple[List[Dict[str, Any]], str, bool]:
        """
        Search Twitter/X narratives using Apify's apidojo/tweet-scraper.
        """
        query_clean = query.strip()
        is_simulated = False
        
        # 1. Discover handle first
        username = await self.discover_twitter_handle(query_clean)
        
        raw_results = None
        if self.apify_client:
            search_query = f"from:{username}" if username else query_clean
            logger.info(f"Using Apify tweet-scraper for query: '{search_query}'")
            
            run_input = {
                "searchTerms": [search_query],
                "maxItems": limit,
                "sort": "Latest" if query_type == "Latest" else "Top"
            }
            
            try:
                import asyncio
                # Run the actor and wait for it to finish
                run = await asyncio.wait_for(self.apify_client.actor("apidojo/tweet-scraper").call(run_input=run_input), timeout=5.0)
                
                # Fetch results from the dataset
                dataset = self.apify_client.dataset(run["defaultDatasetId"])
                dataset_items = await dataset.list_items()
                raw_results = dataset_items.items
            except Exception as e:
                logger.error(f"Apify tweet-scraper failed: {e}")

        # Fallback to mock tweets if failed or API key missing
        if not raw_results or len(raw_results) == 0:
            logger.warning(f"Apify search returned empty for {query_clean}. Running simulated social feed modeling...")
            is_simulated = True
            mock_data = self._generate_mock_tweets(query_clean, limit, username)
            return mock_data, username, is_simulated

        normalized = []
        count = 0
        
        for item in raw_results:
            if count >= limit:
                break
                
            text = item.get("text", "")
            if not text:
                continue
                
            url = item.get("url", "")
            author = item.get("author", {})
            author_username = author.get("userName", username or "TwitterUser")
            tweet_id = item.get("id", f"tweet_{count}")
            
            likes = item.get("likeCount", 0)
            retweets = item.get("retweetCount", 0)
            replies = item.get("replyCount", 0)
            views = item.get("viewCount", 0)
            bookmarks = item.get("bookmarkCount", 0)
            
            created_at = item.get("createdAt", (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=2 + count * 4)).strftime("%Y-%m-%dT%H:%M:%SZ"))
            engagement_score = (likes + (retweets * 2) + (replies * 1.5) + (bookmarks * 2)) / max(views, 1)
            
            normalized.append({
                "tweet_id": str(tweet_id),
                "text": text,
                "created_at": str(created_at),
                "likes": likes,
                "retweets": retweets,
                "replies": replies,
                "views": views,
                "bookmarks": bookmarks,
                "author_username": author_username,
                "author_name": f"@{author_username}",
                "is_verified": author.get("isBlueVerified", False),
                "engagement_score": engagement_score,
                "viral_keywords": self.extract_keywords(text)
            })
            count += 1
            
        if not normalized:
            logger.info(f"Apify returned 0 valid tweets for '{query_clean}'. Loading fallback mock data.")
            is_simulated = True
            mock_data = self._generate_mock_tweets(query_clean, limit, username)
            return mock_data, username, is_simulated
            
        logger.info(f"Successfully collected {len(normalized)} real-time Twitter signals via Apify.")
        return normalized, username, is_simulated

    async def discover_twitter_handle(self, guest_name: str) -> str:
        """
        Discovers the guest's official Twitter/X handle by doing a scoped search.
        """
        if not self.api_key:
            return ""
        logging.info(f"Discovering Twitter/X handle for: {guest_name}")
        query = f'site:x.com "{guest_name}"'
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "query": query,
                "max_results": 5
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(TAVILY_API_URL, json=body, headers=headers)
                if resp.status_code != 200:
                    return ""
                results = resp.json().get("results", [])
                
            blacklist = {"status", "search", "hashtag", "i", "settings", "explore", "home", "notifications", "messages", "bookmarks", "lists", "profile", "tos", "privacy"}
            
            for item in results or []:
                url = item.get("url", "")
                title = item.get("title", "")
                
                # Check for profile URL: x.com/username
                match = re.search(r'(?:x|twitter)\.com/([a-zA-Z0-9_]{1,15})/?$', url)
                if not match:
                    match = re.search(r'(?:x|twitter)\.com/([a-zA-Z0-9_]{1,15})/?(\?.*)?$', url)
                
                if match:
                    username = match.group(1).strip()
                    if username.lower() not in blacklist:
                        logging.info(f"Discovered Twitter/X handle '{username}' for guest '{guest_name}' via profile URL.")
                        return username
                
                # Try parsing from title, e.g. "Guest Name (@username) / X"
                title_match = re.search(r'\((@?[a-zA-Z0-9_]{1,15})\)', title)
                if title_match:
                    username = title_match.group(1).replace('@', '').strip()
                    if username.lower() not in blacklist:
                        logging.info(f"Discovered Twitter/X handle '{username}' for guest '{guest_name}' via title pattern.")
                        return username
        except Exception as e:
            logger.error(f"Failed to discover Twitter handle for {guest_name}: {e}")
        return ""

    def _generate_mock_tweets(self, query_clean: str, limit: int, username: str = "") -> List[Dict[str, Any]]:
        fallback = []
        query_lower = query_clean.lower()
        
        if "scaramucci" in query_lower:
            mock_tweets = [
                (
                    f"Wall Street to Washington is a wild ride. Bipartisan coordination, political reform, and financial resilience is more critical than ever. Bypassing noise to focus on real numbers. #macro #finance",
                    "finance_insider",
                    "Alex Rivera",
                    12500,
                    2400,
                    420,
                    150000,
                    120
                ),
                (
                    f"Inflation, crisis communication, and election strategies. Macroeconomic policy must adapt to the digital age. Moderation is a strength, not a compromise. thoughts?",
                    "media_analyst",
                    "Sarah Chen",
                    8500,
                    1100,
                    650,
                    95000,
                    45
                ),
                (
                    f"SkyBridge Capital strategy is adjusting to global pivots. 5 core execution blueprints for scaling macro investments and crypto integration. 🧵👇",
                    "macro_hacker",
                    "David Miller",
                    22000,
                    5500,
                    350,
                    320000,
                    1800
                ),
                (
                    f"Had a great session discussing bipartisan dialogue, macroeconomics, and Bitcoin. Bypassing institutional walls to build sound financial assets.",
                    "podcast_fanatic",
                    "Emma Watson",
                    6400,
                    800,
                    95,
                    75000,
                    30
                )
            ]
        elif "sam altman" in query_lower:
            mock_tweets = [
                (
                    f"AGI timelines are accelerating. Supercomputers, global energy grids, and computing scalability are the primary bottlenecks. The future of compute is here. #AI #compute #AGI",
                    "tech_optimist",
                    "Alex Rivera",
                    12500,
                    2400,
                    420,
                    150000,
                    120
                ),
                (
                    f"Neural scaling laws continue to hold. Safety, developer scaling, and compute allocation must be resolved transparently. The cost of intelligence is dropping fast.",
                    "pixel_pioneer",
                    "Sarah Chen",
                    8500,
                    1100,
                    650,
                    95000,
                    45
                ),
                (
                    f"How to build the future: 5 rules of compound scaling, YC principles, and staying aligned when shipping high-velocity AI products. 🧵👇",
                    "growth_hacker",
                    "David Miller",
                    22000,
                    5500,
                    350,
                    320000,
                    1800
                ),
                (
                    f"Always helpful to sit down and discuss neural networks, safety, and why decentralized compute access is the ultimate freedom for developers.",
                    "podcast_fanatic",
                    "Emma Watson",
                    6400,
                    800,
                    95,
                    75000,
                    30
                )
            ]
        else:
            mock_tweets = [
                (
                    f"The future belongs to those who build. Continuous execution, shipping daily, and ignoring industry skeptics is the only path forward. #startup #execution",
                    "industry_watcher",
                    "Alex Rivera",
                    12500,
                    2400,
                    420,
                    150000,
                    120
                ),
                (
                    f"Strategic leadership means accepting short-term criticisms to secure long-term architectural success. Bypassing bureaucratic filters to ship fast. thoughts?",
                    "analyst_hub",
                    "Sarah Chen",
                    8500,
                    1100,
                    650,
                    95000,
                    45
                ),
                (
                    f"Masterclass thread: 5 step-by-step scaling blueprints and templates for engineering high-velocity product development. 🧵👇",
                    "growth_hacker",
                    "David Miller",
                    22000,
                    5500,
                    350,
                    320000,
                    1800
                ),
                (
                    f"Had a fantastic discussion outlining creative patterns, leadership formulas, and practical workflows for high-growth operations.",
                    "podcast_fanatic",
                    "Emma Watson",
                    6400,
                    800,
                    95,
                    75000,
                    30
                )
            ]
 
        for idx, (text, default_usr, default_name, likes, retweets, replies, views, bookmarks) in enumerate(mock_tweets[:limit]):
            created_at = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=2 + idx * 4)).strftime("%Y-%m-%dT%H:%M:%SZ")
            engagement_score = (likes + (retweets * 2) + (replies * 1.5) + (bookmarks * 2)) / max(views, 1)
            
            fallback.append({
                "tweet_id": f"mock_tweet_{query_clean.lower().replace(' ', '_')}_{idx}",
                "text": text,
                "created_at": created_at,
                "likes": likes,
                "retweets": retweets,
                "replies": replies,
                "views": views,
                "bookmarks": bookmarks,
                "author_username": username or default_usr,
                "author_name": f"@{username}" if username else default_name,
                "is_verified": True,
                "engagement_score": engagement_score,
                "viral_keywords": self.extract_keywords(text),
                "is_simulated": True
            })
            
        return fallback

    def extract_keywords(self, text: str) -> List[str]:
        keywords = []
        trigger_words = [
            "viral", "crazy", "insane", "breakthrough", "controversy",
            "dangerous", "future", "agi", "elon", "openai",
            "startup", "podcast", "ai", "truth", "exposed"
        ]

        text_lower = text.lower()
        for word in trigger_words:
            if word in text_lower:
                keywords.append(word)

        return keywords