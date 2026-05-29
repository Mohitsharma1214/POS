from typing import Dict, List, Any
import json

def build_intelligence_prompt(guest: Dict[str, Any], web_results: List[dict], youtube_results: List[dict]) -> str:
    # Only keep top 10 results for each to keep prompt size reasonable
    web = web_results[:10]
    yt = youtube_results[:10]
    return f"""
You are an elite podcast research intelligence agent. Your job is to analyze the following guest and their recent web and YouTube appearances, and produce a structured, high-signal, podcast-ready research intelligence report for a top podcast producer.

Instructions:
- DO NOT extract keywords or unigrams. Only extract real topics, themes, and narratives.
- Focus on podcast relevance, narrative, controversy, and high-signal topics.
- Ignore generic or low-value terms (e.g., 'lab', '2026', 'profile').
- Use only the provided data. Do not hallucinate.
- Output must be valid JSON matching the schema below.
- Every major object (topic, controversy, narrative, angle, etc.) must include signal_score and confidence_score (0.0-1.0).
- Rank all topics, controversies, and angles by signal_score.
- Build topic hierarchy (parent_topic/subtopics) and cluster related topics.
- Track narrative evolution and contradiction (shifts, conflicting claims, criticism).
- Extract emotional patterns and podcast retention intelligence.
- Classify YouTube videos by format, virality, style, and retention.
- Generate high-signal, tension-driven, contradiction-driven, and emotionally loaded podcast question angles.
- The research_summary must feel like an elite producer briefing, not a generic summary.

Schema:
{{
  "intelligence": {{
    "dominant_topics": [{{"topic": "", "signal_score": 0.0, "confidence_score": 0.0}}],
    "high_signal_topics": [{{"topic": "", "signal_score": 0.0, "confidence_score": 0.0}}],
    "topic_hierarchy": [{{"parent_topic": "", "subtopics": [""], "signal_score": 0.0, "confidence_score": 0.0}}],
    "controversies": [{{"topic": "", "severity": "low|medium|high", "summary": "", "sources": [], "signal_score": 0.0, "confidence_score": 0.0}}],
    "contradictions": [{{"topic": "", "claim": "", "counter_argument": "", "sources": []}}],
    "public_positioning": ["..."],
    "emerging_topics": [{{"topic": "", "signal_score": 0.0, "confidence_score": 0.0}}],
    "discussion_patterns": ["..."],
    "podcast_patterns": ["..."],
    "interesting_angles": [{{"angle": "", "signal_score": 0.0, "confidence_score": 0.0}}],
    "guest_narrative": "",
    "narrative_evolution": {{"past_narrative": "", "current_narrative": "", "narrative_shift_reason": "", "signal_score": 0.0, "confidence_score": 0.0}},
    "emotional_patterns": [{{"theme": "", "description": "", "signal_score": 0.0, "confidence_score": 0.0}}],
    "podcast_retention_profile": {{
      "storytelling_strength": 0.0,
      "clip_potential": 0.0,
      "controversy_intensity": 0.0,
      "education_density": 0.0,
      "audience_accessibility": 0.0
    }},
    "research_summary": "",
    "youtube_intelligence": [{{
      "title": "",
      "channel": "",
      "estimated_format": "",
      "estimated_virality": "",
      "discussion_style": "",
      "retention_style": "",
      "classification": "",
      "url": "",
      "signal_score": 0.0,
      "confidence_score": 0.0
    }}]
  }}
}}

Guest:
{json.dumps(guest, ensure_ascii=False, indent=2)}

Web Results:
{json.dumps(web, ensure_ascii=False, indent=2)}

YouTube Results:
{json.dumps(yt, ensure_ascii=False, indent=2)}

Return ONLY valid JSON.
"""
