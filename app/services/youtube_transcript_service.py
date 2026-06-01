# YouTube Transcript & Question Extraction Service
# Handles fetching subtitles and extracting interviewer questions

import re
from youtube_transcript_api import YouTubeTranscriptApi
from app.services.openrouter_service import OpenRouterService

from app.utils.cache import ttl_cache
from typing import List
import logging

logger = logging.getLogger(__name__)

class YouTubeTranscriptService:
    def __init__(self):
        self.openrouter = OpenRouterService()

    @ttl_cache(ttl_seconds=300)
    async def get_interviewer_questions(self, video_id: str, video_title: str, video_description: str = "") -> List[str]:
        """
        Fetches the video transcript and extracts the actual questions asked by the host.
        Logs detailed diagnostic errors if the transcript cannot be retrieved or parsed.
        """
        # Coerce video_description to a string if it's a dict or other non-str type
        if isinstance(video_description, dict):
            video_description = video_description.get("text", "") or video_description.get("description", "") or str(video_description)
        elif not isinstance(video_description, str):
            video_description = str(video_description) if video_description is not None else ""

        logger.info(f"Attempting to fetch transcript for video {video_id} ('{video_title}')")
        transcript_text = ""

        try:
            # 1. Fetch transcript using the official youtube-transcript-api with resilience
            # Prepare a custom session with realistic headers
            import os, time, requests
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            # Apply proxy if configured via env var (e.g., YOUTUBE_TRANSCRIPT_PROXY="http://user:pass@proxy:3128")
            proxy = os.getenv("YOUTUBE_TRANSCRIPT_PROXY")
            session = requests.Session()
            session.headers.update(custom_headers)
            if proxy:
                session.proxies.update({"http": proxy, "https": proxy})
            # Monkey‑patch the library's internal session
            YouTubeTranscriptApi._session = session
            # Exponential back‑off retry loop
            max_attempts = 4
            backoff = 2
            transcript_list = None
            for attempt in range(1, max_attempts + 1):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(
                        video_id, languages=["en", "en-US"]
                    )
                    # Success – break out of retry loop
                    break
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "RateLimit" in err_msg or "RequestBlocked" in err_msg:
                        wait = int(os.getenv("YOUTUBE_TRANSCRIPT_RETRY_WAIT", backoff))
                        logger.warning(
                            f"YouTube transcript rate‑limit hit (attempt {attempt}/{max_attempts}). "
                            f"Waiting {wait}s before retry."
                        )
                        time.sleep(wait)
                        backoff *= 2
                    else:
                        # Non‑rate‑limit error – re‑raise to be caught by outer handler
                        raise
            if transcript_list is None:
                raise Exception("Failed to fetch YouTube transcript after retries.")
            transcript_text = " ".join([t.get("text", "") for t in transcript_list])
            logger.info(
                f"Successfully retrieved raw transcript for video {video_id} ({len(transcript_text)} characters)."
            )
        except Exception as e:
            error_msg = str(e)
            if "TranscriptsDisabled" in error_msg or "CouldNotRetrieveTranscript" in error_msg:
                logger.warning(
                    f"DIAGNOSTIC WARNING: Transcripts/Captions are disabled or unavailable for YouTube video {video_id} ('{video_title}'). "
                    f"Details: {error_msg}. Bypassing transcript-based question extraction for this episode."
                )
            elif "NoTranscriptFound" in error_msg:
                logger.warning(
                    f"DIAGNOSTIC WARNING: No English transcript found for YouTube video {video_id} ('{video_title}'). "
                    f"Details: {error_msg}. Bypassing transcript-based question extraction for this episode."
                )
            else:
                logger.error(
                    f"DIAGNOSTIC ERROR: Failed to retrieve YouTube transcript for video {video_id} ('{video_title}') due to a network or scraper issue. "
                    f"Details: {error_msg}. This may indicate that your IP is rate-limited or blocked by YouTube's scrapers."
                )

        # 2. If transcript was retrieved, use LLM to extract the exact interviewer questions
        if transcript_text:
            # Truncate transcript to first ~30,000 characters (~5000-6000 words) to avoid excessive token costs
            truncated_transcript = transcript_text[:30000]
            
            prompt = f"""You are an elite podcast researcher. Analyze this transcript for the video titled "{video_title}" and extract the EXACT questions asked by the host/interviewer to the guest.
            
            Focus on extracting the real, actual, deep questions asked during the conversation. 
            Do not make up questions. Extract them or rephrase them slightly to be clear and self-contained questions.
            Return a JSON list of strings representing the actual questions asked.
            Provide between 5 and 15 distinct, high-quality questions.
            
            IMPORTANT NOTE: If the video is a keynote address, solo presentation, or speech without a formal host/interviewer, analyze the content and extract 5 to 10 core technical, strategic, or operational questions that the speaker addresses, explains, or answers during their presentation.
            
            Transcript segment:
            {truncated_transcript}
            
            Output must be a valid JSON list of strings ONLY:
            [
               "Question 1?",
               "Question 2?"
            ]
            """
            try:
                response = await self.openrouter.complete(prompt, return_json=False)
                import json
                parsed = json.loads(self._clean_json(response))
                if isinstance(parsed, list) and len(parsed) > 0:
                    logger.info(f"Successfully extracted {len(parsed)} real questions from transcript of video {video_id}.")
                    return [str(q) for q in parsed]
            except Exception as ex:
                logger.error(f"LLM question extraction failed for video {video_id} transcript: {ex}")

        # 3. Resilient Fallback: If transcript fails, try to extract questions from the video description
        if video_description.strip():
            logger.info(f"Running fallback question extraction using video description for video {video_id}.")
            prompt = f"""Analyze the YouTube description for the video titled "{video_title}" and extract 3-5 potential questions that were likely asked or discussed in this episode.
            
            IMPORTANT NOTE: If the description represents a keynote, presentation, or solo speech, extract 3-5 core strategic questions that the speaker addresses or answers in the chapters/details.
            
            Description:
            {video_description}
            
            Output must be a valid JSON list of strings ONLY:
            [
               "Question 1?",
               "Question 2?"
            ]
            """
            try:
                response = await self.openrouter.complete(prompt, return_json=False)
                import json
                parsed = json.loads(self._clean_json(response))
                if isinstance(parsed, list) and len(parsed) > 0:
                    logger.info(f"Fallback: Extracted {len(parsed)} questions from description of video {video_id}.")
                    return [str(q) for q in parsed]
            except Exception as ex:
                logger.error(f"Fallback description question extraction failed for video {video_id}: {ex}")

        # 4. Ultimate Local Fallback (guarantees questions are never empty)
        logger.info(f"Ultimate fallback: Generating rule-based questions from title/description chapters for video {video_id}.")
        return self._get_local_fallback_questions(video_title, video_description)

    def _get_local_fallback_questions(self, title: str, description: str = "") -> List[str]:
        # Clean title
        clean_title = title.replace("with NVIDIA CEO Jensen Huang", "").strip()
        
        # 1. Parse chapters from description if present
        chapters = []
        for line in description.splitlines():
            # Match timestamp formats like 0:00, 12:34, 1:23:45
            match = re.search(r'\b(?:\d+:)?\d+:\d+\b\s*(.*)', line)
            if match:
                cap = match.group(1).strip("- ").strip()
                if cap and len(cap) > 3:
                    chapters.append(cap)
                    
        questions = []
        if chapters:
            # Map top 3-4 chapters to questions
            for ch in chapters[:4]:
                questions.append(f"What key insights and strategies were discussed regarding '{ch}'?")
        else:
            # Generate from title
            questions = [
                f"What are the major takeaways and strategic announcements from '{clean_title}'?",
                f"How does the speaker plan to execute the vision outlined in '{clean_title}'?",
                f"What are the long-term implications discussed during '{clean_title}'?"
            ]
        return questions

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
