from fastapi import APIRouter, HTTPException
import logging
from app.schemas.guest import GuestInput
from app.schemas.podcast_intelligence_output import PodcastIntelligenceOutput, ApifyScrapeEpisode
from app.schemas.pattern_extraction_schema import PatternExtractionResponse
from app.schemas.guest_intelligence_schema import GuestIntelligenceResponse
from app.schemas.virality_brief_schema import ViralityBriefResponse
from app.services.signal_collection_service import SignalCollectionService
from app.services.claude_pattern_service import ClaudePatternService
from app.services.guest_intelligence_service import GuestIntelligenceService
from app.services.virality_brief_service import ViralityBriefService
from app.services.pipeline import run_full_pipeline
from app.services.anthropic_service import AnthropicService

router = APIRouter()

@router.post("/guest", response_model=PodcastIntelligenceOutput)
async def research_guest(guest: GuestInput) -> PodcastIntelligenceOutput:
    try:
        inferred_niche = guest.guest_niche
        inferred_context = guest.podcast_context

        if not inferred_niche or not inferred_context:
            from app.core.config import settings
            llm = AnthropicService(model=settings.MODEL_HAIKU)
            inferred_data = await llm.infer_guest_context(
                guest.guest_name, guest.guest_company or ""
            )
            inferred_niche = inferred_niche or inferred_data.get("guest_niche", "")
            inferred_context = inferred_context or inferred_data.get(
                "podcast_context", ""
            )

        active_niche = inferred_niche or guest.guest_niche
        signal_service = SignalCollectionService()
        signals = await signal_service.collect_signals(
            guest.guest_name, active_niche, guest.guest_company or ""
        )
        signals.inferred_niche = inferred_niche
        signals.inferred_podcast_context = inferred_context
        return signals
    except Exception as e:
        logging.exception("Guest research failed")
        raise HTTPException(status_code=500, detail=f"Research failed: {e}")

@router.post("/pattern-extract", response_model=PatternExtractionResponse)
async def extract_working_patterns(guest: GuestInput) -> PatternExtractionResponse:
    try:
        pattern_service = ClaudePatternService()
        if guest.apify_scrape_episodes:
            logging.info(
                f"Using {len(guest.apify_scrape_episodes)} cached episodes for pattern extraction of {guest.guest_name}"
            )
            episodes = []
            for item in guest.apify_scrape_episodes:
                if isinstance(item, dict):
                    episodes.append(
                        ApifyScrapeEpisode(
                            title=item.get("title", ""),
                            url=item.get("url", ""),
                            description=item.get("description", ""),
                            view_count=item.get("view_count")
                            or item.get("viewCount", 0),
                            comment_themes=item.get("comment_themes")
                            or item.get("commentThemes")
                            or [],
                        )
                    )
                elif hasattr(item, "title"):
                    episodes.append(item)
            pattern_report = await pattern_service.extract_patterns(
                episodes, guest_name=guest.guest_name
            )
            return PatternExtractionResponse(
                guest_name=guest.guest_name,
                apify_scrape_episodes=episodes,
                pattern_report=pattern_report,
            )
        else:
            logging.info(
                f"No cached episodes provided. Running full Step 1 collect_signals for {guest.guest_name}"
            )
            signal_service = SignalCollectionService()
            signals = await signal_service.collect_signals(
                guest.guest_name, guest.guest_niche, guest.guest_company or ""
            )
            pattern_report = await pattern_service.extract_patterns(
                signals.apify_scrape_episodes, guest_name=guest.guest_name
            )
            return PatternExtractionResponse(
                guest_name=guest.guest_name,
                apify_scrape_episodes=signals.apify_scrape_episodes,
                pattern_report=pattern_report,
            )
    except Exception as e:
        logging.exception("Working pattern extraction failed")
        raise HTTPException(
            status_code=500, detail=f"Pattern extraction failed: {e}"
        )

@router.post("/guest-intelligence", response_model=GuestIntelligenceResponse)
async def get_guest_intelligence(guest: GuestInput) -> GuestIntelligenceResponse:
    try:
        service = GuestIntelligenceService()
        return await service.extract_guest_intelligence(
            guest_name=guest.guest_name,
            guest_company=guest.guest_company or "",
            guest_niche=guest.guest_niche or "",
            apify_episodes=guest.apify_scrape_episodes or [],
            comment_intelligence=guest.cached_comments or [],
        )
    except Exception as e:
        logging.exception("Guest specific intelligence extraction failed")
        raise HTTPException(
            status_code=500,
            detail=f"Guest intelligence extraction failed: {e}",
        )

@router.post("/virality-brief", response_model=ViralityBriefResponse)
async def generate_virality_brief(guest: GuestInput) -> ViralityBriefResponse:
    try:
        service = ViralityBriefService()
        return await service.generate_virality_brief(
            guest_name=guest.guest_name,
            guest_niche=guest.guest_niche,
            cached_patterns=guest.cached_patterns,
            cached_intelligence=guest.cached_intelligence,
            cached_comments=guest.cached_comments,
            cached_signals=guest.cached_signals,
        )
    except Exception as e:
        logging.exception("Step 4 Virality Brief generation failed")
        raise HTTPException(
            status_code=500,
            detail=f"Virality brief generation failed: {e}",
        )

from app.schemas.virality_brief_schema import RegenerateItemRequest, RegenerateItemResponse

@router.post("/virality-brief/regenerate-item", response_model=RegenerateItemResponse)
async def regenerate_virality_item(req: RegenerateItemRequest) -> RegenerateItemResponse:
    try:
        service = ViralityBriefService()
        new_item = await service.regenerate_single_item(
            item_type=req.item_type,
            guest_name=req.guest_name,
            guest_niche=req.guest_niche,
            cached_patterns=req.cached_patterns,
            cached_intelligence=req.cached_intelligence,
            cached_comments=req.cached_comments,
            cached_signals=req.cached_signals,
            existing_items=req.existing_items,
        )
        return RegenerateItemResponse(item_type=req.item_type, item=new_item)
    except Exception as e:
        logging.exception(f"Virality brief item regeneration failed for {req.item_type}")
        raise HTTPException(
            status_code=500,
            detail=f"Item regeneration failed: {e}",
        )

@router.post("/full-pipeline")
async def execute_fallback_pipeline(guest: GuestInput):
    try:
        signal_service = SignalCollectionService()
        signals = await signal_service.collect_signals(
            guest.guest_name, guest.guest_niche or "General", guest.guest_company or ""
        )
        signals_dict = {
            "apify_scrape_episodes": [
                {
                    "title": ep.title,
                    "description": ep.description,
                    "view_count": ep.view_count,
                    "comment_themes": ep.comment_themes,
                }
                for ep in signals.apify_scrape_episodes
            ],
            "top_performing_guest_episodes": [
                {
                    "title": ep.title,
                    "video_id": ep.video_id,
                    "real_questions_asked": ep.real_questions_asked,
                }
                for ep in signals.top_performing_guest_episodes
            ],
            "tavily_web_signals": [
                {
                    "title": s.get("title", ""),
                    "source": s.get("source", ""),
                    "url": s.get("url", ""),
                    "snippet": s.get("snippet", ""),
                }
                if isinstance(s, dict)
                else {
                    "title": getattr(s, "title", ""),
                    "source": getattr(s, "source", ""),
                    "url": getattr(s, "url", ""),
                    "snippet": getattr(s, "snippet", ""),
                }
                for s in signals.tavily_web_signals
            ],
            "comment_intelligence": [
                {
                    "objections": insight.objections,
                    "commenter_questions": insight.commenter_questions,
                }
                for insight in signals.comment_intelligence
            ],
        }

        try:
            pipeline_output = run_full_pipeline(
                guest_name=guest.guest_name,
                guest_niche=guest.guest_niche or "General",
                guest_company=guest.guest_company or "",
                collected_signals=signals_dict,
                max_retries_per_model=3,
            )
        except Exception as e:
            logging.error(f"run_full_pipeline failed (likely Anthropic API limits): {e}")
            pipeline_output = {}
            
        if not pipeline_output:
            logging.warning(
                "run_full_pipeline returned None or failed; initializing empty result."
            )
            pipeline_output = {}

        # pipeline returns {"result": {...}, "steps": [...]}
        # unwrap the inner "result" dict so we get the actual stage outputs
        pipeline_result = pipeline_output.get("result") or pipeline_output

        result = (
            signals.dict()
            if hasattr(signals, "dict")
            else signals.model_dump()
        )
        result.update(
            {
                # "guest_intelligence" is the key used inside pipeline.py
                "intelligence": pipeline_result.get("guest_intelligence"),
                "patterns": pipeline_result.get("patterns"),
                "brief": pipeline_result.get("brief"),
                "scoring": pipeline_result.get("scoring"),
            }
        )
        return {"result": result, "steps": pipeline_output.get("steps")}
    except Exception as e:
        logging.exception("Fallback pipeline failed")
        raise HTTPException(
            status_code=500, detail=f"Pipeline failed: {e}"
        )
