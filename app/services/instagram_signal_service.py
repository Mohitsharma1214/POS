import logging
import re
from typing import List, Tuple
from app.schemas.podcast_intelligence_output import InstagramSignal
from app.services.tavily_signal_service import TavilySignalService
from app.core.config import settings
from apify_client import ApifyClientAsync

class InstagramSignalService:
    def __init__(self):
        self.tavily = TavilySignalService()
        self.apify_token = settings.APIFY_API_TOKEN
        if self.apify_token:
            self.apify_client = ApifyClientAsync(self.apify_token)
        else:
            self.apify_client = None
            logging.warning("APIFY_API_TOKEN not set. Instagram service will fallback to simulated signals.")

    async def collect_instagram_signals(self, guest_name: str) -> Tuple[List[InstagramSignal], str]:
        """
        Fetches Instagram signals by executing Apify's apify/instagram-scraper.
        """
        logging.info(f"Collecting Instagram signals via Apify for: {guest_name}")
        
        # 1. Discover handle first
        username = await self.discover_instagram_handle(guest_name)
        
        raw_results = None
        if self.apify_client:
            search_query = username if username else guest_name
            logging.info(f"Using Apify instagram-scraper for query: '{search_query}'")
            
            run_input = {
                "search": search_query,
                "searchType": "user" if username else "hashtag",
                "resultsLimit": 10,
            }
            
            try:
                import asyncio
                run = await asyncio.wait_for(self.apify_client.actor("apify/instagram-scraper").call(run_input=run_input), timeout=5.0)
                dataset = self.apify_client.dataset(run["defaultDatasetId"])
                dataset_items = await dataset.list_items()
                raw_results = dataset_items.items
            except Exception as e:
                logging.error(f"Apify instagram-scraper failed: {e}")

        # Fallback to AI simulation
        if not raw_results or len(raw_results) == 0:
            logging.warning(f"Apify search returned empty for {guest_name}. Running AI-simulated engagement modeling...")
            simulated = await self._generate_simulated_signals(guest_name)
            return simulated, username

        signals = []
        try:
            for item in raw_results or []:
                url = item.get("url", "")
                title = item.get("caption", "") or "Instagram Post"
                snippet = item.get("caption", "")
                
                likes = item.get("likesCount", 0)
                comments = item.get("commentsCount", 0)
                views = item.get("videoViewCount", 0) if item.get("type") == "Video" else 0

                engagement_score = likes + (comments * 2) + (len(url) * 10)
                
                signals.append(InstagramSignal(
                    title=title,
                    url=url,
                    snippet=snippet,
                    engagement_score=float(engagement_score),
                    likes=likes,
                    comments=comments,
                    views=views,
                    is_simulated=False
                ))
        except Exception as e:
            logging.error(f"Failed to parse Instagram signals for {guest_name}: {e}")

        max_likes = max([s.likes or 0 for s in signals]) if signals else 0
        if not signals or max_likes < 500:
            logging.info(f"Top real-time Instagram signal has low traction ({max_likes} likes). Supplementing with high-traction simulated signals.")
            simulated_signals = await self._generate_simulated_signals(guest_name)
            signals = [s for s in signals if (s.likes or 0) >= 100]
            signals.extend(simulated_signals)

        signals.sort(key=lambda x: x.engagement_score or 0.0, reverse=True)
        return signals, username

    async def discover_instagram_handle(self, guest_name: str) -> str:
        """
        Discovers the guest's official Instagram handle by doing a scoped search.
        Returns the username if found, otherwise empty string.
        """
        logging.info(f"Discovering Instagram handle for: {guest_name}")
        query = f'site:instagram.com "{guest_name}"'
        try:
            results = await self.tavily.search_web(query, max_results=5)
            blacklist = {"p", "reel", "reels", "stories", "explore", "developer", "login", "about", "legal", "direct", "terms", "privacy", "blog"}
            
            for item in results or []:
                url = getattr(item, "url", "") if not isinstance(item, dict) else item.get("url", "")
                title = getattr(item, "title", "") if not isinstance(item, dict) else item.get("title", "")
                
                # Check for standard profile URL: https://www.instagram.com/username/
                match = re.search(r'instagram\.com/([a-zA-Z0-9_\.]+)/?$', url)
                if not match:
                    match = re.search(r'instagram\.com/([a-zA-Z0-9_\.]+)/?(\?.*)?$', url)
                
                if match:
                    username = match.group(1).strip()
                    if username.lower() not in blacklist:
                        logging.info(f"Discovered Instagram handle '{username}' for guest '{guest_name}' via profile URL.")
                        return username
                
                # Try parsing from title, e.g. "Guest Name (@username) on Instagram"
                title_match = re.search(r'\((@?[a-zA-Z0-9_\.]+)\)', title)
                if title_match:
                    username = title_match.group(1).replace('@', '').strip()
                    if username.lower() not in blacklist:
                        logging.info(f"Discovered Instagram handle '{username}' for guest '{guest_name}' via title pattern.")
                        return username
                        
        except Exception as e:
            logging.error(f"Failed to discover Instagram handle for {guest_name}: {e}")
        
        return ""

    async def _generate_simulated_signals(self, guest_name: str) -> List[InstagramSignal]:
        """
        Queries OpenRouter to generate realistic simulated Instagram signals specific to the guest.
        """
        logging.info(f"Generating high-fidelity simulated Instagram signals for: {guest_name}")
        prompt = f"""
You are an expert social media analyst and digital branding researcher.
Real-time Instagram search returned no results for the guest "{guest_name}" due to platform search rate-limiting or anti-scraping walls.
Generate exactly 3 highly realistic, simulated high-traction Instagram signals (posts or reels) that this guest would typically have, based on their known profile, background, or typical professional/personal branding.

Provide a structured JSON response containing a list under the key "signals". Each signal must have exactly these keys:
1. "title": A compelling, highly specific title for the post/reel (e.g., "Reel: 3 Habits That Doubled My Startup's Revenue", "Post: Behind-the-scenes family life"). Make it specific to "{guest_name}".
2. "url": A realistic-looking Instagram URL (e.g., "https://www.instagram.com/reel/C8xYz12A3bB/"). Use varied random slug strings.
3. "snippet": A realistic caption snippet describing the post/reel, written in the guest's style, including some hashtags and engagement indicators.
4. "likes": A realistic high engagement likes count (integer between 1200 and 45000).
5. "comments": A realistic comments count (integer between 24 and 1800).
6. "views": A realistic view count if it's a Reel (integer between 25000 and 350000), or 0 if it's a static image post.

Respond ONLY with valid JSON.
"""
        try:
            from app.services.openrouter_service import OpenRouterService
            openrouter = OpenRouterService()
            parsed = await openrouter.complete(prompt, return_json=True)
            
            if isinstance(parsed, str):
                import json
                cleaned = parsed.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(cleaned)
                
            if not isinstance(parsed, dict) or "signals" not in parsed:
                logging.warning("No signals found in parsed LLM response for simulated signals fallback.")
                return []
            
            signals = []
            for item in parsed["signals"]:
                likes = item.get("likes", 0)
                comments = item.get("comments", 0)
                url = item.get("url", f"https://www.instagram.com/p/C{re.sub(r'[^a-zA-Z0-9]', '', guest_name)[:5]}/")
                # Calculate score
                engagement_score = likes + (comments * 2) + (len(url) * 10)
                
                signals.append(InstagramSignal(
                    title=item.get("title", "Instagram Post"),
                    url=url,
                    snippet=item.get("snippet", "Instagram post details"),
                    engagement_score=float(engagement_score),
                    likes=likes,
                    comments=comments,
                    views=item.get("views", 0),
                    is_simulated=True
                ))
            return signals
        except Exception as e:
            logging.error(f"Failed to generate simulated Instagram signals: {e}")
            return []
