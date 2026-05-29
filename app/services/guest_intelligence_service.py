import re
import json
import logging
import asyncio
from typing import List, Optional, Any

from app.schemas.guest_intelligence_schema import (
    GuestEnrichment,
    TimelineEvent,
    PublicStance,
    Contradiction,
    GuestIntelligenceReport,
    GuestIntelligenceResponse,
)
from app.services.openrouter_service import OpenRouterService
from app.services.tavily_signal_service import TavilySignalService
from app.services.youtube_transcript_service import YouTubeTranscriptService


class GuestIntelligenceService:
    def __init__(self):
        self.tavily = TavilySignalService()
        self.openrouter = OpenRouterService()
        self.transcript_service = YouTubeTranscriptService()

    @staticmethod
    def _extract_video_id(url: str) -> Optional[str]:
        """Extracts an 11-character YouTube video ID from a full URL or bare ID."""
        if not url:
            return None
        if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url):
            return url
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
        return match.group(1) if match else None

    async def extract_guest_intelligence(
        self,
        guest_name: str,
        guest_company: str = "",
        guest_niche: str = "",
        apify_episodes: Optional[list] = None,
        comment_intelligence: Optional[list] = None,
    ) -> GuestIntelligenceResponse:
        """
        Step 3: Guest-Specific Intelligence Layer.
        Pulls live Tavily web data + YouTube transcripts from prior appearances,
        then synthesises the full intelligence report via two sequential LLM calls.
        """
        logging.info(f"[Step 3] Starting guest intelligence extraction for '{guest_name}'")

        apify_episodes = apify_episodes or []
        comment_intelligence = comment_intelligence or []
        current_year = "2026"

        # ── 1. Build search queries ─────────────────────────────────────────────
        base = f'"{guest_name}"'
        if guest_company:
            base += f' "{guest_company}"'
        if guest_niche:
            base += f" {guest_niche}"

        career_query = (
            f"{base} biography accomplishments career controversial statements public stance interviews"
        )
        bio_query = (
            f'"{guest_name}" timeline birth childhood education net worth career breaks controversies'
        )

        # ── 2. Identify top-3 video IDs from apify_episodes for transcript pull ─
        episode_meta: List[tuple] = []
        seen_vids: set = set()
        for ep in apify_episodes:
            url = ep.get("url", "") if isinstance(ep, dict) else getattr(ep, "url", "")
            title = ep.get("title", "") if isinstance(ep, dict) else getattr(ep, "title", "")
            description = (
                ep.get("description", "") if isinstance(ep, dict) else getattr(ep, "description", "")
            )
            vid = self._extract_video_id(url)
            if vid and vid not in seen_vids:
                seen_vids.add(vid)
                episode_meta.append((vid, title, description))
            if len(episode_meta) >= 3:
                break

        # ── 3. Run Tavily + transcript extraction in parallel ───────────────────
        async def safe_tavily(query: str, n: int = 20) -> list:
            try:
                return await self.tavily.search_web(query, max_results=n)
            except Exception as e:
                logging.warning(f"[Step 3] Tavily search failed for '{query[:60]}': {e}")
                return []

        async def safe_transcript(vid: str, title: str, desc: str) -> list:
            try:
                return await self.transcript_service.get_interviewer_questions(vid, title, desc)
            except Exception as e:
                logging.warning(f"[Step 3] Transcript extraction failed for video {vid}: {e}")
                return []

        parallel_tasks: list = [
            safe_tavily(career_query, 20),
            safe_tavily(bio_query, 20),
        ] + [safe_transcript(vid, title, desc) for vid, title, desc in episode_meta]

        raw_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)

        tavily_career = raw_results[0] if not isinstance(raw_results[0], Exception) else []
        tavily_bio = raw_results[1] if not isinstance(raw_results[1], Exception) else []
        transcript_questions: list = []
        for i in range(2, len(raw_results)):
            r = raw_results[i]
            if not isinstance(r, Exception) and isinstance(r, list):
                transcript_questions.extend(r)

        # Deduplicate Tavily results by URL
        seen_urls: set = set()
        tavily_results: list = []
        for item in list(tavily_career) + list(tavily_bio):
            url = (
                getattr(item, "url", "") if not isinstance(item, dict) else item.get("url", "")
            )
            if url not in seen_urls:
                seen_urls.add(url)
                tavily_results.append(
                    {
                        "title": (
                            getattr(item, "title", "")
                            if not isinstance(item, dict)
                            else item.get("title", "")
                        ),
                        "url": url,
                        "snippet": (
                            getattr(item, "snippet", "")
                            if not isinstance(item, dict)
                            else item.get("snippet", "")
                        ),
                    }
                )

        logging.info(
            f"[Step 3] Data ready for '{guest_name}': "
            f"{len(tavily_results)} web signals, "
            f"{len(transcript_questions)} transcript questions from "
            f"{len(episode_meta)} episodes."
        )

        # ── 4. Build context strings for LLM prompts ───────────────────────────
        episode_titles = [
            ep.get("title", "") if isinstance(ep, dict) else getattr(ep, "title", "")
            for ep in apify_episodes[:10]
        ]
        episode_titles_text = (
            "\n".join(f"- {t}" for t in episode_titles if t)
            if episode_titles
            else "No prior episode data available."
        )
        prior_questions_text = (
            "\n".join(f"- {q}" for q in transcript_questions[:25] if q)
            if transcript_questions
            else "No transcript data available for this guest."
        )

        # ── 5. LLM Call 1 — Enrichment + Biography Timeline ────────────────────
        prompt_bio = f"""You are a world-class investigative journalist and podcast researcher.
Analyse the following live web research footprint for the guest: {guest_name}
Company: {guest_company or "N/A"} | Niche: {guest_niche or "General"} | Current Year: {current_year}

Web Research Signals:
{json.dumps(tavily_results[:25], indent=2)}

Return a PURE JSON object with EXACTLY these two top-level keys:

1. "enrichment": An object containing:
   - "bio": A detailed, comprehensive, high-quality 4-6 sentence professional biography in English. Make it fact-dense: name key companies, massive breakthroughs, market valuations or funding raised, unique career origins, and their precise present-day status as of {current_year}.
   - "current_roles": A list of their current active titles, board memberships, or company roles as of {current_year}.
   - "accomplishments": A list of 5-7 key career or life accomplishments. Each accomplishment must be extremely detailed: cite specific figures, names of acquisitions/companies, product architectures, dates, and direct organizational impact.
   - "social_profiles": A list of known social media handles or official website URLs found in the research data.

2. "biography_timeline": A list of chronological life milestones from birth to {current_year}. Include at least 10 events. Each item must have:
   - "period": The year or time range (e.g. "1978", "1995-1999", "{current_year}").
   - "event_type": One of: Birth, Education, Personal Life, Career, Wealth, Controversy.
   - "title": A short, descriptive title (5-10 words).
   - "description": A highly detailed, 3-4 sentence narrative containing exact names of co-founders, schools, companies, specific capital amounts, strategic friction points, and operational developments.

Rules:
- All text must be in English ONLY — no Chinese, Arabic, or any non-English characters.
- Do NOT use placeholder text such as "[Name]" or "[Year]".
- Return ONLY the raw JSON object — no markdown code blocks, no introduction, no explanation.
"""

        # ── 6. LLM Call 2 — Intelligence Layer ─────────────────────────────────
        prompt_intel = f"""You are an elite podcast content strategist and viral episode architect.
Guest: {guest_name} | Niche: {guest_niche or "General"} | Company: {guest_company or "N/A"}

RESEARCH CONTEXT:

[Prior Podcast Episode Titles — Topics Already Covered]:
{episode_titles_text}

[Real Questions Already Asked in Prior Podcast Appearances]:
{prior_questions_text}

[Live Web Intelligence Snippets]:
{json.dumps(tavily_results[:15], indent=2)}

Using this live research data, return a PURE JSON object with EXACTLY these four top-level keys:

1. "covered_angles": A list of 4-5 topics or angles this guest discusses on nearly EVERY podcast appearance. Make each item a highly descriptive sentence detailing the standard narrative or talking points they repeat (avoid short generic titles like "AI growth").
2. "untapped_angles": A list of 4-5 genuinely original, specific narrative paths that NO OTHER HOST has explored with this guest. Each must be: Fact-dense, highly specific, and detail-laden. Frame each as a substantial 2-3 sentence investigative angle or controversial prompt clearly specifying the underlying operational tension, omitted web signal, or strategic counterweight.
3. "public_stances": A list of 4-5 major public positions this guest has taken. Each item must be a JSON object with:
   - "topic": The subject matter (e.g. "AI Safety", "Monetary Policy").
   - "position": Their highly specific, concrete public stance, complete with strategic rationale or key trade-off.
   - "quote_or_source": A real, exact, or highly faithful illustrative quote, including the specific context/event (e.g. GTC keynote, White House forum) where it was stated.
4. "contradictions": A list of 3-4 core contradictions, career paradoxes, or stark shifts in stance. Each item must be a JSON object with:
   - "stance_a": Their traditional, former, or publicly declared position or action, citing specific periods or products.
   - "stance_b": A conflicting statement, recent pivot, or contradictory reality, detailed with metrics or current initiatives.
   - "analysis": A detailed 2-3 sentence strategic analysis of the underlying commercial, technical, or philosophical tension/friction between A and B, explaining how it creates an elite interview pivot zone.

Rules:
- All text must be in English ONLY.
- Untapped angles must genuinely NOT appear in the prior questions list.
- Do NOT use placeholder text.
- Return ONLY the raw JSON object — no markdown code blocks.
"""

        # ── 7. Execute both LLM calls ───────────────────────────────────────────
        bio_data: Optional[dict] = None
        intel_data: Optional[dict] = None

        try:
            raw_bio = await self.openrouter.complete_long(prompt_bio, return_json=True)
            if isinstance(raw_bio, dict) and "enrichment" in raw_bio:
                bio_data = raw_bio
                logging.info(f"[Step 3] Call 1 (Bio+Timeline) succeeded for '{guest_name}'.")
            else:
                logging.warning(
                    f"[Step 3] Call 1 returned unexpected structure for '{guest_name}': "
                    f"{str(raw_bio)[:200]}"
                )
        except Exception as e:
            logging.error(f"[Step 3] LLM Call 1 (Bio+Timeline) failed for '{guest_name}': {e}")

        try:
            raw_intel = await self.openrouter.complete_long(prompt_intel, return_json=True)
            if isinstance(raw_intel, dict) and (
                "covered_angles" in raw_intel or "untapped_angles" in raw_intel
            ):
                intel_data = raw_intel
                logging.info(f"[Step 3] Call 2 (Intelligence) succeeded for '{guest_name}'.")
            else:
                logging.warning(
                    f"[Step 3] Call 2 returned unexpected structure for '{guest_name}': "
                    f"{str(raw_intel)[:200]}"
                )
        except Exception as e:
            logging.error(f"[Step 3] LLM Call 2 (Intelligence) failed for '{guest_name}': {e}")

        # ── 8. Merge or fall back ──────────────────────────────────────────────
        if bio_data or intel_data:
            report = self._merge_reports(bio_data or {}, intel_data or {})
            return GuestIntelligenceResponse(guest_name=guest_name, intelligence_report=report)

        # Both LLM calls failed — build a minimal live report from Tavily data only
        logging.warning(
            f"[Step 3] Both LLM calls failed for '{guest_name}'. "
            f"Building minimal Tavily-driven fallback report."
        )
        return GuestIntelligenceResponse(
            guest_name=guest_name,
            intelligence_report=self._build_tavily_fallback(
                guest_name, guest_niche, tavily_results, episode_titles
            ),
        )

    # ── Helpers ──────────────────────────────────────────────────────────────────

    def _merge_reports(self, bio_data: dict, intel_data: dict) -> GuestIntelligenceReport:
        """Merges outputs from the two LLM calls into a single GuestIntelligenceReport."""

        enrichment_raw = bio_data.get("enrichment") or {}
        raw_profiles = (
            enrichment_raw.get("social_profiles")
            or enrichment_raw.get("socialProfiles")
            or []
        )
        social_profiles_normalized = []
        for p in raw_profiles:
            if isinstance(p, dict):
                plat = p.get("platform", "")
                hnd = p.get("handle") or p.get("url") or p.get("username") or ""
                if plat and hnd:
                    social_profiles_normalized.append(f"{plat}: {hnd}")
                elif hnd:
                    social_profiles_normalized.append(str(hnd))
            else:
                social_profiles_normalized.append(str(p))

        enrichment = GuestEnrichment(
            bio=enrichment_raw.get("bio") or "Accomplished professional and thought leader.",
            current_roles=(
                enrichment_raw.get("current_roles")
                or enrichment_raw.get("currentRoles")
                or []
            ),
            accomplishments=enrichment_raw.get("accomplishments") or [],
            social_profiles=social_profiles_normalized,
        )

        timeline: list = []
        raw_timeline = (
            bio_data.get("biography_timeline")
            or bio_data.get("biographyTimeline")
            or []
        )
        for t in raw_timeline:
            if isinstance(t, dict):
                timeline.append(
                    TimelineEvent(
                        period=str(t.get("period") or "N/A"),
                        event_type=t.get("event_type") or t.get("eventType") or "Career",
                        title=t.get("title") or "Life Milestone",
                        description=t.get("description") or "Biographical event.",
                    )
                )

        stances: list = []
        raw_stances = (
            intel_data.get("public_stances")
            or intel_data.get("publicStances")
            or []
        )
        for s in raw_stances:
            if isinstance(s, dict):
                stances.append(
                    PublicStance(
                        topic=s.get("topic") or "General",
                        position=s.get("position") or "Undeclared stance.",
                        quote_or_source=(
                            s.get("quote_or_source")
                            or s.get("quoteOrSource")
                            or "Public record."
                        ),
                    )
                )

        contradictions: list = []
        raw_contradictions = intel_data.get("contradictions") or []
        for c in raw_contradictions:
            if isinstance(c, dict):
                contradictions.append(
                    Contradiction(
                        stance_a=c.get("stance_a") or c.get("stanceA") or "Position A.",
                        stance_b=c.get("stance_b") or c.get("stanceB") or "Position B.",
                        analysis=c.get("analysis") or "Tension analysis.",
                    )
                )

        return GuestIntelligenceReport(
            enrichment=enrichment,
            biography_timeline=timeline,
            covered_angles=(
                intel_data.get("covered_angles")
                or intel_data.get("coveredAngles")
                or []
            ),
            untapped_angles=(
                intel_data.get("untapped_angles")
                or intel_data.get("untappedAngles")
                or []
            ),
            public_stances=stances,
            contradictions=contradictions,
        )

    def _build_tavily_fallback(
        self,
        guest_name: str,
        guest_niche: str,
        tavily_results: list,
        episode_titles: list,
    ) -> GuestIntelligenceReport:
        """
        Constructs a minimal but real GuestIntelligenceReport entirely from
        live Tavily web snippets. No hardcoded names or profiles. Works for any guest.
        """
        # Bio from the most informative snippet
        bio_text = (
            f"{guest_name} is a professional and thought leader "
            f"in the {guest_niche or 'business'} space."
        )
        for item in tavily_results[:5]:
            snippet = item.get("snippet", "")
            if snippet and len(snippet) > 80:
                bio_text = snippet[:500]
                break

        # Covered angles — inferred from prior episode titles
        covered: list = []
        for t in episode_titles[:4]:
            if t and len(t) > 5:
                covered.append(f"Topics discussed in prior appearance: '{t[:100]}'")
        if not covered:
            covered = [
                f"Standard career journey and biographical overview of {guest_name}",
                "General industry predictions and trend forecasts",
                "High-level framework overviews without tactical depth",
            ]

        # Untapped angles — inferred from later Tavily snippets
        untapped: list = []
        for item in tavily_results[3:8]:
            snippet = item.get("snippet", "")
            title = item.get("title", "")
            if snippet and len(snippet) > 40:
                untapped.append(
                    f"Explore the angle in '{title[:80]}': {snippet[:140]}"
                )
        if not untapped:
            untapped = [
                f"The specific financial pivots and career decisions that defined {guest_name}'s trajectory",
                f"Contrarian views {guest_name} holds that differ from mainstream {guest_niche or 'industry'} consensus",
                "Personal failures and hard lessons — rarely explored in standard interviews",
                "The backstory behind their most controversial public statement or decision",
            ]

        # Accomplishments from Tavily titles
        accomplishments = [
            item.get("title", "")
            for item in tavily_results[:4]
            if item.get("title")
        ]

        return GuestIntelligenceReport(
            enrichment=GuestEnrichment(
                bio=bio_text,
                current_roles=[],
                accomplishments=accomplishments,
                social_profiles=[
                    item.get("url", "")
                    for item in tavily_results[:3]
                    if item.get("url")
                ],
            ),
            biography_timeline=[
                TimelineEvent(
                    period="Career",
                    event_type="Career",
                    title=f"{guest_name} — Professional Journey",
                    description=bio_text,
                )
            ],
            covered_angles=covered,
            untapped_angles=untapped,
            public_stances=[],
            contradictions=[],
        )
