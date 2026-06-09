# YouTube Transcript & Question Extraction Service
# Handles fetching subtitles and extracting interviewer questions

import re
from youtube_transcript_api import YouTubeTranscriptApi
from app.services.anthropic_service import AnthropicService

from app.utils.cache import ttl_cache
from typing import List
import logging

logger = logging.getLogger(__name__)

class YouTubeTranscriptService:
    def __init__(self):
        from app.core.config import settings
        self.llm = AnthropicService(model=settings.MODEL_HAIKU)

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
            # Monkey‑patch the library's internal session for older versions
            if hasattr(YouTubeTranscriptApi, '_session'):
                YouTubeTranscriptApi._session = session
            # Exponential back‑off retry loop
            max_attempts = 4
            backoff = 2
            transcript_list = None
            for attempt in range(1, max_attempts + 1):
                try:
                    if hasattr(YouTubeTranscriptApi, 'get_transcript'):
                        transcript_list = YouTubeTranscriptApi.get_transcript(
                            video_id, languages=["en", "en-US"]
                        )
                    else:
                        api_instance = YouTubeTranscriptApi(http_client=session)
                        transcript_list = api_instance.fetch(video_id, languages=["en", "en-US"])
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
            
            transcript_text = " ".join([
                t.text if hasattr(t, 'text') else t.get("text", "") 
                for t in transcript_list
            ])
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
            # Truncate transcript to first ~100,000 characters (~15,000 words) to scan entire episodes for questions
            truncated_transcript = transcript_text[:200000]
            
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
                response = await self.llm.complete(prompt, return_json=False)
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
                response = await self.llm.complete(prompt, return_json=False)
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

    @ttl_cache(ttl_seconds=300)
    async def get_viral_moment_question(self, video_id: str, video_title: str) -> str:
        """
        Uses yt-dlp to find the most replayed moment, matches it to the transcript,
        and uses the LLM to draft a viral investigative question.
        """
        try:
            import yt_dlp
            logger.info(f"Extracting heatmap for video {video_id} using yt-dlp")
            ydl_opts = {
                'skip_download': True,
                'quiet': True,
                'extract_flat': True,
                'dump_single_json': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                heatmap = info.get('heatmap')
                
            if not heatmap:
                logger.info(f"No heatmap found for {video_id}")
                return ""
                
            # Find the moment with the highest value
            most_replayed = max(heatmap, key=lambda x: x.get('value', 0))
            start_time = most_replayed.get('start_time', 0)
            logger.info(f"Most replayed moment for {video_id} is at {start_time}s")
            
            # Fetch the transcript
            if hasattr(YouTubeTranscriptApi, 'get_transcript'):
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "en-US"])
            else:
                transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US"])
            
            # Find the transcript chunk that surrounds this start_time (-30s to +60s)
            target_start = max(0, start_time - 30)
            target_end = start_time + 60
            
            snippet_texts = []
            for t in transcript_list:
                t_start = getattr(t, 'start', None) if hasattr(t, 'start') else t.get('start', 0)
                if target_start <= t_start <= target_end:
                    t_text = getattr(t, 'text', '') if hasattr(t, 'text') else t.get('text', '')
                    snippet_texts.append(t_text)
                    
            if not snippet_texts:
                return ""
                
            transcript_snippet = " ".join(snippet_texts)
            logger.info(f"Extracted {len(transcript_snippet)} chars around the viral moment for {video_id}")
            
            # Draft the question using Claude
            prompt = f"""You are an elite podcast producer preparing to interview a guest.
            We analyzed their past YouTube interview: "{video_title}".
            Based on YouTube's backend data, the most REPLAYED (most viral) moment of the entire video occurred during this specific transcript snippet:
            
            <viral_moment_transcript>
            {transcript_snippet}
            </viral_moment_transcript>
            
            Your task: Draft exactly ONE highly provocative, investigative question that targets the core insight, controversy, or revelation in this specific viral moment.
            The question must NOT be a simple yes/no. It must challenge or build upon what they said.
            Do not include any introductory or explanatory text. Just output the question itself.
            """
            
            response = await self.llm.complete(prompt, return_json=False)
            question = response.strip().replace('"', '')
            logger.info(f"Drafted viral moment question: {question}")
            return question
            
        except Exception as e:
            logger.warning(f"Failed to extract viral moment question for {video_id}: {e}")
            return ""
