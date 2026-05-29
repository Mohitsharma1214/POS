# app/services/pipeline.py
"""Pipeline orchestration with per‑stage model fallback, prompt tweaks, and JSON validation.

The flow follows the specification:
    Step 2 – Pattern Extraction
    Step 3 – Guest Intelligence
    Step 4 – Brief Generation
    Step 4 – Scoring (with optional regeneration)

Each step uses the ordered model list from ``models.PIPELINE_MODELS`` and the
model‑specific prompt snippets from ``models.MODEL_TWEAKS``.
"""

import os
import json
import time
import logging
from typing import Any, Dict, List
from dataclasses import dataclass, field

import httpx

# ---------------------------------------------------------------------------
# Local imports – the model hierarchy and core prompts defined elsewhere
# ---------------------------------------------------------------------------
from .models import PIPELINE_MODELS, MODEL_TWEAKS
from .prompts import (
    STEP2_CORE_PROMPT,
    STEP3_CORE_PROMPT,
    STEP4_BRIEF_CORE_PROMPT,
    STEP4_SCORING_CORE_PROMPT,
    STEP5_SIMULATOR_PROMPT,
)

@dataclass
class PipelineResult:
    guest: str
    patterns: Any = None
    guest_intelligence: Any = None
    brief: Any = None
    scoring: Any = None
    simulation: Any = None
    regenerated: bool = False
    step_history: List[Dict[str, Any]] = field(default_factory=list)

    def record_step(self, stage: str, model: str, output: Any):
        self.step_history.append({
            "stage": stage,
            "model": model,
            "output": output
        })

# ---------------------------------------------------------------------------
# API client helpers
# ---------------------------------------------------------------------------

def _get_client_and_model_id(model: str):
    """Return a (base_url, api_key, model_id) tuple for the given model.

    * Groq models are under ``https://api.groq.com/openai/v1`` and the model id
      is the portion after the ``groq/`` prefix.
    * All other models are routed through OpenRouter (``https://openrouter.ai/api/v1``).
    """
    if model.startswith("groq/"):
        base_url = "https://api.groq.com/openai/v1"
        api_key = os.getenv("GROQ_API_KEY", "")
        model_id = model.replace("groq/", "")
    else:
        base_url = "https://openrouter.ai/api/v1"
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        model_id = model  # OpenRouter expects the full slug (including provider)
    return base_url, api_key, model_id


def call_model(model: str, prompt: str) -> str:
    """Synchronously call the LLM endpoint and return the raw text response.

    The function uses ``httpx`` for a simple POST request compatible with both
    OpenRouter and Groq (they share the OpenAI‑compatible chat endpoint).
    """
    base_url, api_key, model_id = _get_client_and_model_id(model)
    if not api_key:
        raise ValueError(f"API key missing for model {model}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that returns pure JSON as instructed."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 1500,  # reduced to lower payload size and speed
    }

    try:
        response = httpx.post(f"{base_url}/chat/completions", json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        # OpenAI‑compatible response shape
        content = data["choices"][0]["message"]["content"]
        return content
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error from {model} ({e.response.status_code}): {e.response.text}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error calling model {model}: {e}")
        raise

# ---------------------------------------------------------------------------
# Prompt handling utilities
# ---------------------------------------------------------------------------

def build_prompt(core_prompt: str, model: str) -> str:
    """Inject model‑specific tweak strings into the core prompt.

    For DeepSeek and Qwen the tweak is a *prepend*; for Groq/Meta‑Llama it is an
    *append*. The ``MODEL_TWEAKS`` dict contains the exact snippet; for models
    without a tweak we simply return the original prompt.
    """
    tweak = MODEL_TWEAKS.get(model, "")
    # For simplicity we always append the tweak (the wording works for both prepend/append cases).
    return core_prompt + ("\n" + tweak if tweak else "")


def extract_and_parse_json(response: str) -> Any:
    """Sanitize the LLM output and return a Python object or ``None``.

    Mirrors the helper supplied in the specification.
    """
    # Strip Qwen thinking tags
    if "<thinking>" in response:
        response = response.split("</thinking>")[-1]

    # Remove markdown fences
    response = response.strip()
    if response.startswith("```"):
        parts = response.split("```")
        if len(parts) >= 3:
            response = parts[1]
        else:
            response = parts[-1]
        if response.lstrip().startswith("json"):
            response = response.lstrip()[4:]

    try:
        return json.loads(response.strip())
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Core fallback runner used by each pipeline stage
# ---------------------------------------------------------------------------

def call_with_fallback(stage: str, prompt: str, max_retries: int = 1) -> Any:
    """Iterate over the model list for *stage* until a valid JSON response appears.
    Raises ``RuntimeError`` if every model fails.
    """
    models = PIPELINE_MODELS.get(stage, [])
    if not models:
        raise ValueError(f"No models configured for stage {stage}")

    for model in models:
        for attempt in range(max_retries + 1):
            try:
                full_prompt = build_prompt(prompt, model)
                response = call_model(model, full_prompt)
                parsed = extract_and_parse_json(response)
                if parsed is not None:
                    logging.info(f"✓ {stage} succeeded with {model}")
                    return (model, parsed)
                else:
                    logging.warning(f"✗ {model} returned invalid JSON, trying next")
                    break  # move to next model
            except httpx.HTTPStatusError as e:
                # Treat both 429 (rate‑limit) and 413 (payload too large) as retryable
                if e.response.status_code in (429, 413) and attempt < max_retries:
                    # Respect Retry‑After header if the service provides it
                    retry_after = e.response.headers.get('Retry-After')
                    try:
                        wait_seconds = int(float(retry_after)) if retry_after else 5
                    except Exception:
                        wait_seconds = 5
                        
                    if wait_seconds > 10:
                        logging.warning(f"{e.response.status_code} on {model}, retry-after is {wait_seconds}s (too long). Skipping this model.")
                        break

                    logging.warning(
                        f"{e.response.status_code} on {model}, retrying after {wait_seconds}s back‑off"
                    )
                    time.sleep(wait_seconds)
                    continue
                logging.error(
                    f"✗ {model} HTTP error {e.response.status_code}: {e.response.text}"
                )
                break
            except Exception as e:
                logging.error(f"✗ {model} failed: {e}, advancing")
                break
    raise RuntimeError(f"All models failed for stage: {stage}")

# ---------------------------------------------------------------------------
# Output normalization helpers
# ---------------------------------------------------------------------------

def _safe_float(val: Any, default: float = 0.85) -> float:
    """Coerce a value to float, returning default if invalid."""
    try:
        f = float(val)
        return f if 0.0 <= f <= 100.0 else default
    except (TypeError, ValueError):
        return default


def normalize_patterns(raw: Any) -> Dict[str, Any]:
    """Ensure the step-2 patterns dict matches the PatternReport schema."""
    if not isinstance(raw, dict):
        raw = {}
    result = {
        "title_formulas": raw.get("title_formulas") or [],
        "thumbnail_patterns": raw.get("thumbnail_patterns") or [],
        "hook_structures": raw.get("hook_structures") or [],
        "question_styles": raw.get("question_styles") or [],
        "episode_formats": raw.get("episode_formats") or [],
        "audience_retention_angles": raw.get("audience_retention_angles") or [],
        "clip_bait_moments": [],
    }
    for cm in (raw.get("clip_bait_moments") or []):
        if isinstance(cm, dict):
            result["clip_bait_moments"].append({
                "title": cm.get("title") or "",
                "description": cm.get("description") or "",
                "trigger_statement": cm.get("trigger_statement") or cm.get("triggerStatement") or "",
                "virality_score": _safe_float(cm.get("virality_score") or cm.get("viralityScore"), 0.80),
                "platforms": cm.get("platforms") or ["TikTok", "YouTube Shorts"],
            })
    return result


def normalize_intel(raw: Any) -> Dict[str, Any]:
    """Ensure the step-3 intel dict matches the GuestIntelligenceReport schema."""
    if not isinstance(raw, dict):
        raw = {}
    enrichment = raw.get("enrichment") or {}
    result = {
        "enrichment": {
            "bio": enrichment.get("bio") or "",
            "current_roles": enrichment.get("current_roles") or [],
            "accomplishments": enrichment.get("accomplishments") or [],
            "social_profiles": enrichment.get("social_profiles") or [],
        },
        "biography_timeline": [],
        "covered_angles": raw.get("covered_angles") or [],
        "untapped_angles": raw.get("untapped_angles") or [],
        "public_stances": [],
        "contradictions": [],
        "viewer_curiosity_gaps": raw.get("viewer_curiosity_gaps") or [],
        "emotional_inflection_points": raw.get("emotional_inflection_points") or [],
        "signature_frameworks": raw.get("signature_frameworks") or [],
        "strongest_predictions": raw.get("strongest_predictions") or [],
        "myths_they_fight": raw.get("myths_they_fight") or [],
        "industry_battles": raw.get("industry_battles") or [],
        "failure_moments": raw.get("failure_moments") or [],
        "identity_questions": raw.get("identity_questions") or [],
    }
    for ev in (raw.get("biography_timeline") or []):
        if isinstance(ev, dict):
            result["biography_timeline"].append({
                "period": ev.get("period") or "",
                "event_type": ev.get("event_type") or "Career",
                "title": ev.get("title") or "",
                "description": ev.get("description") or "",
            })
    for ps in (raw.get("public_stances") or []):
        if isinstance(ps, dict):
            result["public_stances"].append({
                "topic": ps.get("topic") or "",
                "position": ps.get("position") or "",
                "quote_or_source": ps.get("quote_or_source") or ps.get("quoteOrSource") or "",
            })
    for c in (raw.get("contradictions") or []):
        if isinstance(c, dict):
            result["contradictions"].append({
                "stance_a": c.get("stance_a") or c.get("stanceA") or "",
                "stance_b": c.get("stance_b") or c.get("stanceB") or "",
                "analysis": c.get("analysis") or "",
            })
    return result


def normalize_brief(raw: Any) -> Dict[str, Any]:
    """Ensure the step-4 brief dict matches the ViralityBriefReport schema with valid floats."""
    if not isinstance(raw, dict):
        raw = {}
    result: Dict[str, Any] = {
        "optimized_questions": [],
        "title_variants": [],
        "thumbnail_concepts": [],
        "hook_scripts": [],
        "clip_angles": [],
        "content_calendar": [],
    }
    for q in (raw.get("optimized_questions") or raw.get("optimizedQuestions") or []):
        if isinstance(q, dict):
            result["optimized_questions"].append({
                "question_type": q.get("question_type") or q.get("questionType") or None,
                "primary_question": q.get("primary_question") or q.get("primaryQuestion") or q.get("question") or "",
                "follow_ups": q.get("follow_ups") or q.get("followUps") or [],
                "objective": q.get("objective") or "",
                "supporting_evidence": q.get("supporting_evidence") or q.get("supportingEvidence") or q.get("origin_signal") or q.get("originSignal") or "",
                "retention_potential": _safe_float(q.get("retention_potential") or q.get("retentionPotential"), 0.85),
            })
    for t in (raw.get("title_variants") or raw.get("titleVariants") or []):
        if isinstance(t, dict):
            ctr = _safe_float(t.get("predicted_ctr") or t.get("predictedCtr"), 10.0)
            # Groq sometimes returns 0-1 scale; normalise to percentage
            if ctr < 1.0:
                ctr = round(ctr * 100, 1)
            result["title_variants"].append({
                "title": t.get("title") or "",
                "trigger_type": t.get("trigger_type") or t.get("triggerType") or "Curiosity Gap",
                "predicted_ctr": ctr,
            })
    for th in (raw.get("thumbnail_concepts") or raw.get("thumbnailConcepts") or []):
        if isinstance(th, dict):
            result["thumbnail_concepts"].append({
                "concept_name": th.get("concept_name") or th.get("conceptName") or "",
                "visual_description": th.get("visual_description") or th.get("visualDescription") or "",
                "text_overlay": th.get("text_overlay") or th.get("textOverlay") or "",
                "accent_color": th.get("accent_color") or th.get("accentColor") or "#FF0055",
            })
    for hk in (raw.get("hook_scripts") or raw.get("hookScripts") or []):
        if isinstance(hk, dict):
            result["hook_scripts"].append({
                "hook_type": hk.get("hook_type") or hk.get("hookType") or "Story Loop",
                "script_text": hk.get("script_text") or hk.get("scriptText") or "",
                "pacing_notes": hk.get("pacing_notes") or hk.get("pacingNotes") or "",
                "visual_cue": hk.get("visual_cue") or hk.get("visualCue") or "",
            })
    for cl in (raw.get("clip_angles") or raw.get("clipAngles") or []):
        if isinstance(cl, dict):
            result["clip_angles"].append({
                "title": cl.get("title") or "",
                "description": cl.get("description") or "",
                "trigger_statement": cl.get("trigger_statement") or cl.get("triggerStatement") or "",
                "virality_score": _safe_float(cl.get("virality_score") or cl.get("viralityScore"), 0.85),
                "platforms": cl.get("platforms") or ["TikTok", "YouTube Shorts"],
            })
    for item in (raw.get("content_calendar") or raw.get("contentCalendar") or []):
        if isinstance(item, dict):
            result["content_calendar"].append({
                "day": item.get("day") or "",
                "content_type": item.get("content_type") or item.get("contentType") or "Short Form",
                "angle_topic": item.get("angle_topic") or item.get("angleTopic") or "",
                "optimal_time": item.get("optimal_time") or item.get("optimalTime") or "12:00 PM EST",
            })
    return result


def normalize_simulation(raw: Any) -> List[Dict[str, Any]]:
    """Ensure the step-5 simulator output is a list matching the InterviewSimulation schema."""
    if not isinstance(raw, list):
        if isinstance(raw, dict) and "simulation" in raw:
            raw = raw["simulation"]
        elif isinstance(raw, dict) and "simulations" in raw:
            raw = raw["simulations"]
        else:
            raw = []
    
    result = []
    for item in raw:
        if isinstance(item, dict):
            follow_ups_raw = item.get("follow_ups") or item.get("followUps") or []
            follow_ups = []
            for fu in follow_ups_raw:
                if isinstance(fu, dict):
                    follow_ups.append({
                        "type": fu.get("type") or "clarification",
                        "question": fu.get("question") or ""
                    })
            result.append({
                "main_question": item.get("main_question") or item.get("mainQuestion") or "",
                "possible_guest_answer": item.get("possible_guest_answer") or item.get("possibleGuestAnswer") or "",
                "follow_ups": follow_ups
            })
    return result

# ---------------------------------------------------------------------------
# High‑level pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(
    guest_name: str,
    guest_niche: str = "",
    guest_company: str = "",
    collected_signals: Dict[str, Any] | None = None,
    max_retries_per_model: int = 3,
) -> Dict[str, Any]:
    """Execute the full 4‑step pipeline for *guest_name*.

    Returns a dict containing stage outputs, the final score, and a ``regenerated``
    flag indicating whether Step 4 was re‑run with a fallback model.
    """
    result_obj = PipelineResult(guest=guest_name)
    # STEP 1 – raw data collection (unchanged from existing services)
    from .signal_collection_service import SignalCollectionService

    if collected_signals is not None:
        # Use the signals dict supplied by the calling route (already in the correct shape)
        raw_data = collected_signals
    else:
        collector = SignalCollectionService()
        raw_data = collector.collect_raw_data_for_guest(guest_name, guest_niche)

    # STEP 2 – Pattern Extraction
    # Groq llama-3.3-70b handles up to 128k tokens; we still truncate raw data
    # to 8k chars to keep latency reasonable while giving the model rich context.
    MAX_RAW_CHARS = 8000
    raw_data_str = json.dumps(raw_data, ensure_ascii=False)
    if len(raw_data_str) > MAX_RAW_CHARS:
        raw_data_str = raw_data_str[:MAX_RAW_CHARS] + "... (truncated)"
    step2_prompt = STEP2_CORE_PROMPT.replace("{RAW_DATA}", raw_data_str)
    model, patterns_raw = call_with_fallback(
        "step2_extraction",
        step2_prompt,
        max_retries=max_retries_per_model,
    )
    patterns_json = normalize_patterns(patterns_raw)
    result_obj.patterns = patterns_json
    result_obj.record_step("step2_extraction", model, patterns_json)

    # STEP 3 – Guest Intelligence
    MAX_RAW_CHARS_STEP3 = 8000
    raw_data_str_step3 = json.dumps(raw_data, ensure_ascii=False)
    if len(raw_data_str_step3) > MAX_RAW_CHARS_STEP3:
        raw_data_str_step3 = raw_data_str_step3[:MAX_RAW_CHARS_STEP3] + "... (truncated)"
    step3_prompt = STEP3_CORE_PROMPT.replace("{RAW_DATA}", raw_data_str_step3)
    model, intel_raw = call_with_fallback(
        "step3_research",
        step3_prompt,
        max_retries=max_retries_per_model,
    )
    intel_json = normalize_intel(intel_raw)
    result_obj.guest_intelligence = intel_json
    result_obj.record_step("step3_research", model, intel_json)

    # STEP 4A – Brief Generation (may be regenerated if scoring is low)
    MAX_RAW_CHARS_STEP4 = 6000
    patterns_str = json.dumps(patterns_json, ensure_ascii=False)
    if len(patterns_str) > MAX_RAW_CHARS_STEP4:
        patterns_str = patterns_str[:MAX_RAW_CHARS_STEP4] + "... (truncated)"
    intel_str = json.dumps(intel_json, ensure_ascii=False)
    if len(intel_str) > MAX_RAW_CHARS_STEP4:
        intel_str = intel_str[:MAX_RAW_CHARS_STEP4] + "... (truncated)"
    def generate_brief() -> Dict[str, Any]:
        prompt = (
            STEP4_BRIEF_CORE_PROMPT.replace("{PATTERNS_JSON}", patterns_str)
            .replace("{INTEL_JSON}", intel_str)
        )
        return call_with_fallback("step4_brief", prompt, max_retries=max_retries_per_model)

    model, brief_raw = generate_brief()
    brief_json = normalize_brief(brief_raw)
    result_obj.brief = brief_json
    result_obj.record_step("step4_brief", model, brief_json)

    # STEP 4B – Scoring
    # Truncate the brief JSON before sending to the model.
    brief_str = json.dumps(brief_json, ensure_ascii=False)
    if len(brief_str) > MAX_RAW_CHARS_STEP4:
        brief_str = brief_str[:MAX_RAW_CHARS_STEP4] + "... (truncated)"
    def score_brief(brief: Dict[str, Any]) -> Dict[str, Any]:
        prompt = STEP4_SCORING_CORE_PROMPT.replace("{BRIEF_JSON}", brief_str)
        return call_with_fallback("step4_scoring", prompt, max_retries=max_retries_per_model)

    model, score_result = score_brief(brief_json)
    result_obj.scoring = score_result
    result_obj.record_step("step4_scoring", model, score_result)

    # Regenerate if score < 7 using the next model in the step4 list
    if isinstance(score_result, dict) and score_result.get("score", 0) < 7:
        logging.info("Score below threshold – attempting regeneration with fallback models")
        remaining_models = PIPELINE_MODELS["step4_brief"][1:]
        for fallback_model in remaining_models:
            # Build the prompt once; the fallback logic inside call_with_fallback will try the specific model.
            prompt = (
                STEP4_BRIEF_CORE_PROMPT.replace("{PATTERNS_JSON}", json.dumps(patterns_json, ensure_ascii=False))
                .replace("{INTEL_JSON}", json.dumps(intel_json, ensure_ascii=False))
            )
            try:
                # Directly call the fallback model by temporarily overriding the stage list.
                # We'll call call_with_fallback but it will iterate over the whole list again;
                # to force a single model we temporarily replace the stage entry.
                original_list = PIPELINE_MODELS["step4_brief"]
                PIPELINE_MODELS["step4_brief"] = [fallback_model]
                model, brief_candidate_raw = call_with_fallback("step4_brief", prompt, max_retries=max_retries_per_model)
                brief_candidate = normalize_brief(brief_candidate_raw)
                model_s, new_score = score_brief(brief_candidate)
                if isinstance(new_score, dict) and new_score.get("score", 0) >= 7:
                    brief_json = brief_candidate
                    score_result = new_score
                    result_obj.brief = brief_json
                    result_obj.scoring = score_result
                    result_obj.regenerated = True
                    result_obj.record_step("step4_brief", model, brief_candidate)
                    result_obj.record_step("step4_scoring", model_s, new_score)
                    PIPELINE_MODELS["step4_brief"] = original_list
                    break
                PIPELINE_MODELS["step4_brief"] = original_list
            except Exception as e:
                logging.warning(f"Fallback model {fallback_model} failed during regeneration: {e}")
                PIPELINE_MODELS["step4_brief"] = original_list

    # STEP 5 - Interview Simulation (Dynamic Follow-Ups)
    def generate_simulation() -> Dict[str, Any]:
        prompt = (
            STEP5_SIMULATOR_PROMPT.replace("{INTEL_JSON}", json.dumps(intel_json, ensure_ascii=False))
            .replace("{BRIEF_JSON}", json.dumps(brief_json, ensure_ascii=False))
        )
        return call_with_fallback("step5_simulator", prompt, max_retries=max_retries_per_model)
    
    model, sim_raw = generate_simulation()
    sim_json = normalize_simulation(sim_raw)
    result_obj.simulation = sim_json
    result_obj.record_step("step5_simulator", model, sim_json)

    return {
        "guest_name": result_obj.guest,
        "patterns": result_obj.patterns,
        "intelligence": result_obj.guest_intelligence,
        "brief": result_obj.brief,
        "scoring": result_obj.scoring,
        "simulation": result_obj.simulation,
        "regenerated_brief": result_obj.regenerated,
        "step_history": result_obj.step_history
    }

# Alias for backward compatibility (routes import run_full_pipeline)
run_full_pipeline = run_pipeline


# ---------------------------------------------------------------------------
# Monkey‑patch SignalCollectionService to expose raw data for the pipeline
# ---------------------------------------------------------------------------
def _patch_signal_collection_service():
    from .signal_collection_service import SignalCollectionService

    def collect_raw_data_for_guest(self, guest_name: str, guest_niche: str = "") -> Dict[str, Any]:
        """Return a plain‑dict of the raw signals used by the prompts.
        It re‑uses the existing ``collect_signals`` implementation and converts the
        resulting Pydantic model to a dictionary.
        """
        output = self.collect_signals(guest_name, guest_niche)
        return output.dict()

    setattr(SignalCollectionService, "collect_raw_data_for_guest", collect_raw_data_for_guest)

_patch_signal_collection_service()

# End of pipeline.py
