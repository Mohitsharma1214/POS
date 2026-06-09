# app/services/linkedin_signal_service.py

import os
import logging
import datetime
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from apify_client import ApifyClientAsync

logger = logging.getLogger(__name__)

class LinkedInSignalService:
    def __init__(self):
        self.apify_token = settings.APIFY_API_TOKEN
        self.linkedin_cookie = os.getenv("LINKEDIN_COOKIE", "")
        if self.apify_token:
            self.apify_client = ApifyClientAsync(self.apify_token)
        else:
            self.apify_client = None
            logger.warning(
                "DIAGNOSTIC WARNING: APIFY_API_TOKEN is not configured in .env. "
                "LinkedIn crawler will operate in high-fidelity mock fallback mode."
            )

    async def get_linkedin_posts(
        self,
        guest_name: str,
        limit: int = 10
    ) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Search LinkedIn posts using Apify's curious_coder/linkedin-profile-scraper.
        """
        is_simulated = False
        raw_results = None
        
        if self.apify_client and self.linkedin_cookie:
            logger.info(f"Using Apify linkedin-profile-scraper for guest: '{guest_name}'")
            
            # Note: actual inputs might vary by actor. We assume it takes a name/url and cookie.
            run_input = {
                "urls": [f"https://www.linkedin.com/search/results/people/?keywords={guest_name.replace(' ', '%20')}"],
                "cookie": self.linkedin_cookie,
                "deepScrape": True,
                "minDelay": 2,
                "maxDelay": 5
            }
            
            try:
                import asyncio
                run = await asyncio.wait_for(self.apify_client.actor("curious_coder/linkedin-profile-scraper").call(run_input=run_input), timeout=10.0)
                
                dataset = self.apify_client.dataset(run["defaultDatasetId"])
                dataset_items = await dataset.list_items()
                raw_results = dataset_items.items
            except Exception as e:
                logger.error(f"Apify linkedin-profile-scraper failed: {e}")

        # Fallback to mock posts if failed or API key/cookie missing
        if not raw_results or len(raw_results) == 0:
            logger.warning(f"Apify search returned empty or missing auth for {guest_name}. Running simulated LinkedIn feed modeling...")
            is_simulated = True
            mock_data = self._generate_mock_posts(guest_name, limit)
            return mock_data, is_simulated

        normalized = []
        count = 0
        
        for item in raw_results:
            # Depending on actor output format
            posts = item.get("posts", [])
            for post in posts:
                if count >= limit:
                    break
                    
                text = post.get("text", "")
                if not text:
                    continue
                    
                likes = post.get("likesCount", 0)
                comments = post.get("commentsCount", 0)
                reposts = post.get("repostsCount", 0)
                
                created_at = post.get("publishedAt", (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=count)).strftime("%Y-%m-%dT%H:%M:%SZ"))
                
                normalized.append({
                    "post_text": text,
                    "author": guest_name,
                    "published_at": str(created_at),
                    "likes": likes,
                    "comments": comments,
                    "reposts": reposts,
                    "url": post.get("url", ""),
                    "is_simulated": False
                })
                count += 1
            if count >= limit:
                break
                
        if not normalized:
            logger.info(f"Apify returned 0 valid posts for '{guest_name}'. Loading fallback mock data.")
            is_simulated = True
            mock_data = self._generate_mock_posts(guest_name, limit)
            return mock_data, is_simulated
            
        logger.info(f"Successfully collected {len(normalized)} real-time LinkedIn signals via Apify.")
        return normalized, is_simulated

    def _generate_mock_posts(self, guest_name: str, limit: int) -> List[Dict[str, Any]]:
        fallback = []
        
        mock_posts = [
            (
                "I am thrilled to announce the next phase of our growth. Building resilient organizations requires focusing on long-term strategy and robust execution.",
                500,
                45,
                12
            ),
            (
                "Reflecting on the recent shifts in the industry. The intersection of technology and scalable frameworks is creating unprecedented opportunities. What are your thoughts on this evolution?",
                320,
                88,
                24
            ),
            (
                "We often talk about disruption, but sustainable innovation is what truly lasts. A huge shoutout to the team for pushing boundaries and shipping incredible features this week.",
                450,
                32,
                18
            ),
            (
                "Had a fantastic conversation on the latest podcast episode covering macroeconomic trends, leadership, and building high-performance cultures. Check it out!",
                610,
                55,
                30
            )
        ]
 
        for idx, (text, likes, comments, reposts) in enumerate(mock_posts[:limit]):
            created_at = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=idx*2)).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            fallback.append({
                "post_text": text,
                "author": guest_name,
                "published_at": created_at,
                "likes": likes,
                "comments": comments,
                "reposts": reposts,
                "url": f"https://www.linkedin.com/posts/mock-post-{idx}",
                "is_simulated": True
            })
            
        return fallback
