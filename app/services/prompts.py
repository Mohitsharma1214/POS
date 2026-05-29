# app/services/prompts.py

# =============================================================
# Core prompts for each pipeline stage
# =============================================================
# Each prompt is a single string that may contain {PLACEHOLDER}
# tokens that the orchestrator replaces before sending to the LLM.
# The schema expected for each stage matches the Pydantic models in
# app/schemas/ so the dashboard can render data directly.
# -------------------------------------------------------------

STEP2_CORE_PROMPT = """
You are an expert podcast research analyst. Analyze the raw data below and extract the exact creative and editorial patterns used in the highest-performing episodes for this guest.

Return a JSON object with EXACTLY these keys and formats:

{
  "title_formulas": [
    "Formula string 1 — e.g. '[Guest] Reveals the [Contrarian Truth] About [Topic]'",
    "Formula string 2",
    ...
  ],
  "thumbnail_patterns": [
    "Visual pattern 1 — e.g. 'Split screen: shocked host face left, bold claim text right on black'",
    "Visual pattern 2",
    ...
  ],
  "hook_structures": [
    "Hook structure 1 — e.g. 'Open with a 3-sentence paradox statement, then cut to the guest's most controversial quote'",
    "Hook structure 2",
    ...
  ],
  "question_styles": [
    "Question style 1 — e.g. 'Biographical pivot: Reference a specific year, then challenge the guest on the contradiction'",
    "Question style 2",
    ...
  ],
  "episode_formats": [
    "Format 1 — e.g. '90-minute deep dive: Cold open → guest backstory → 3 controversy flashpoints → forward-looking thesis'",
    "Format 2",
    ...
  ],
  "audience_retention_angles": [
    "Retention angle 1 — e.g. 'Introduce unresolved tension at minute 12, resolve it only at minute 58'",
    "Retention angle 2",
    ...
  ],
  "clip_bait_moments": [
    {
      "title": "Short title of the clip-bait segment",
      "description": "Why this segment would go viral — the core argument or reveal",
      "trigger_statement": "The exact high-engagement polarizing statement or hook",
      "virality_score": 0.94,
      "platforms": ["TikTok", "YouTube Shorts", "Reels"]
    }
  ]
}

Provide at least 6 items in title_formulas, thumbnail_patterns, hook_structures, question_styles, episode_formats, and audience_retention_angles.
Provide exactly 8 clip_bait_moments.

Raw data (episodes, niche videos, tweets, web results):
{RAW_DATA}
"""

STEP3_CORE_PROMPT = """
You are a world-class guest-intelligence engine. Using the information supplied, produce a comprehensive dossier for this guest.

Return a JSON object with EXACTLY these keys and formats:

{
  "enrichment": {
    "bio": "2-4 sentence high-quality biography of the guest",
    "current_roles": ["Role / title / affiliation 1", "Role 2"],
    "accomplishments": ["Major milestone 1", "Major milestone 2"],
    "social_profiles": ["twitter.com/handle", "website.com"]
  },
  "biography_timeline": [
    {
      "period": "1984",
      "event_type": "Birth",
      "title": "Short catchy title of this life event",
      "description": "Detailed narrative of what happened, who was involved, and why it matters"
    },
    {
      "period": "2000-2004",
      "event_type": "Education",
      "title": "Degree or academic milestone title",
      "description": "What they studied, key influences, formative ideas"
    },
    {
      "period": "2015",
      "event_type": "Career",
      "title": "Company founded or major career pivot",
      "description": "What they built, why, and the outcome"
    }
  ],
  "covered_angles": [
    "Oversaturated topic / angle they repeat in nearly every show — e.g. 'Bitcoin as a hedge against inflation'",
    "Angle 2",
    "Angle 3"
  ],
  "untapped_angles": [
    "Under-explored, highly original angle — e.g. 'The psychological toll of managing LP relationships during the FTX crisis'",
    "Angle 2",
    "Angle 3"
  ],
  "public_stances": [
    {
      "topic": "Topic of their public position",
      "position": "Their stance or perspective",
      "quote_or_source": "Verbatim quote or contextual sentence representing this position"
    }
  ],
  "contradictions": [
    {
      "stance_a": "Historical stance or action — what they claimed or did before",
      "stance_b": "Current conflicting statement or direction",
      "analysis": "Brief breakdown of the conversational friction or developmental paradox"
    }
  ],
  "viewer_curiosity_gaps": [
    "e.g. They often mention a 2018 crisis but never explain how they funded the recovery",
    "Gap 2"
  ],
  "emotional_inflection_points": [
    "e.g. The time they were laughed out of a board meeting",
    "Point 2"
  ],
  "signature_frameworks": [
    "e.g. The 'Inversion' mental model they use for hiring",
    "Framework 2"
  ],
  "strongest_predictions": [
    "e.g. Claims AI will replace 80% of middle management by 2027",
    "Prediction 2"
  ],
  "myths_they_fight": [
    "e.g. The idea that you need to be a morning person to be successful",
    "Myth 2"
  ],
  "industry_battles": [
    "e.g. Their ongoing war against proprietary data silos",
    "Battle 2"
  ],
  "failure_moments": [
    "e.g. The 2019 product launch that had zero users",
    "Failure 2"
  ],
  "identity_questions": [
    "e.g. Are they still an engineer at heart, or just a manager now?",
    "Question 2"
  ]
}

Provide at least 8 biography_timeline events spanning their full life.
Provide at least 5 covered_angles, 5 untapped_angles, 5 public_stances, and 3 contradictions.

Input data:
{RAW_DATA}
"""

STEP4_BRIEF_CORE_PROMPT = """
You are a senior creative director for podcast production. Combine the patterns from Step 2 and the guest dossier from Step 3 to produce a complete virality brief playbook.

Return a JSON object with EXACTLY these keys and formats:

{
  "optimized_questions": [
    {
      "question_type": "Story",
      "primary_question": "Short, punchy, and highly conversational opening question. Written exactly as a human host would speak it naturally. Do not over-explain or cram too much context.",
      "follow_ups": [
        "If they give a generic answer, ask: 'Wait, but didn't you previously claim [contradiction]?'",
        "If they focus on X, pivot to: 'What is the actual operational bottleneck there?'"
      ],
      "objective": "Deep strategic interview objective for the host",
      "supporting_evidence": "e.g. Timeline [2015 investment] + Quote + YouTube Objection",
      "retention_potential": 0.95
    }
  ],
  "title_variants": [
    {
      "title": "High-impact click-worthy video title (no placeholders)",
      "trigger_type": "Curiosity Gap",
      "predicted_ctr": 13.5
    }
  ],
  "thumbnail_concepts": [
    {
      "concept_name": "Short concept name",
      "visual_description": "Concrete layout: face crop, color palette, background graphic, text position",
      "text_overlay": "BOLD OVERLAY TEXT",
      "accent_color": "#FF0055"
    }
  ],
  "hook_scripts": [
    {
      "hook_type": "Story Loop",
      "script_text": "Full 0-60 second hook script written in first person for the host to read aloud. Must be dramatic, natural, and compelling.",
      "pacing_notes": "Tone directions, pauses, speed notes - e.g. 'Spoken fast, pause after the key reveal, whisper the final line'",
      "visual_cue": "Specific camera angles, zooms, B-roll notes - e.g. 'Tight close-up on host, zoom in on the word BILLION'"
    }
  ],
  "clip_angles": [
    {
      "title": "Viral clip title",
      "description": "What makes this segment viral - the thesis or reveal",
      "trigger_statement": "The exact polarizing or highly engaging statement that hooks the viewer",
      "virality_score": 0.96,
      "platforms": ["TikTok", "YouTube Shorts", "Reels"]
    }
  ],
  "content_calendar": [
    {
      "day": "Day 1",
      "content_type": "Full Episode",
      "angle_topic": "Specific topic and viral hook to publish",
      "optimal_time": "12:00 PM EST"
    }
  ]
}

Requirements:
- Provide exactly 10 optimized_questions, 10 title_variants, 8 thumbnail_concepts, 5 hook_scripts, 8 clip_angles, and 7 content_calendar entries.
- retention_potential and virality_score must be floats between 0.0 and 1.0.
- predicted_ctr must be a float (e.g. 13.5 for 13.5%).
- No placeholders, no generic text. Every item must be specific to this guest.

QUESTION GENERATION SYSTEM

You are a world-class podcast producer.

Your job is not to create interview questions.

Your job is to design a conversation that maximizes:

* Retention
* Virality
* Emotional engagement
* Curiosity
* Storytelling
* Learning
* Future predictions
* Memorable clips

Research supports questions.

Research does not create questions.

====================================================
MANDATORY INTERVIEW STRUCTURE
=============================

Generate exactly 10 questions.

Question 1:
Story

Question 2:
Story

Question 3:
Framework

Question 4:
Framework

Question 5:
Contrarian

Question 6:
Contrarian

Question 7:
Prediction

Question 8:
Prediction

Question 9:
Emotional

Question 10:
Legacy

This structure is mandatory.

====================================================
QUESTION SOURCE MAPPING
=======================

Story Questions:

* biography_timeline
* failure_moments
* emotional_inflection_points

Framework Questions:

* signature_frameworks
* public_stances

Contrarian Questions:

* contradictions
* myths_they_fight
* industry_battles

Prediction Questions:

* strongest_predictions

Emotional Questions:

* emotional_inflection_points
* failure_moments
* identity_questions

Legacy Questions:

* identity_questions
* biography_timeline

Do NOT default to contradictions.

====================================================
PRIMARY QUESTION RULES
======================

Primary questions must:

* Sound conversational
* Feel natural when spoken aloud
* Contain a single idea
* Create immediate curiosity
* Be easy to understand

Target Length:
8-18 words

Maximum Length:
25 words

Research should rarely appear directly in the primary question.

Avoid placing:

* Competitor benchmarks
* Statistics
* Metrics
* Timelines
* Community objections
* Multiple quotes

inside primary questions.

Use those in supporting evidence and follow-ups instead.

====================================================
STORY QUESTIONS
===============

Purpose:
Reveal turning points.

Explore:

* Origin stories
* Career pivots
* Failures
* Near disasters
* Unexpected lessons
* Hard decisions

Examples:

"What was the moment you knew you had to leave Ethereum?"

"What's the closest Cardano ever came to failing?"

====================================================
FRAMEWORK QUESTIONS
===================

Purpose:
Teach the audience.

Explore:

* Mental models
* Decision systems
* Evaluation frameworks
* Repeatable processes

Examples:

"How do you tell the difference between innovation and hype?"

"What's your framework for evaluating a blockchain project?"

====================================================
CONTRARIAN QUESTIONS
====================

Purpose:
Create debate.

Explore:

* Industry myths
* Unpopular beliefs
* Strong disagreements

Examples:

"What's something the crypto industry gets completely wrong?"

"What's the strongest criticism of Cardano that you agree with?"

====================================================
PREDICTION QUESTIONS
====================

Purpose:
Create future-focused clips.

Explore:

* Future trends
* Winners
* Losers
* Industry shifts
* 5-year forecasts
* 10-year forecasts

Examples:

"What's a crypto prediction that sounds crazy today?"

"Which blockchain won't matter in ten years?"

====================================================
EMOTIONAL QUESTIONS
===================

Purpose:
Reveal the human being.

Explore:

* Fear
* Regret
* Doubt
* Criticism
* Failure
* Sacrifice

Examples:

"What criticism bothered you because it was true?"

"When did you realize you were wrong?"

====================================================
LEGACY QUESTIONS
================

Purpose:
Create memorable endings.

Explore:

* Meaning
* Purpose
* Impact
* Legacy
* Long-term vision

Examples:

"What future are you trying to create?"

"What do you hope people remember about your work?"

====================================================
FOLLOW-UP RULES
===============

Follow-ups should prioritize:

1. Story expansion
2. Emotional depth
3. Framework extraction
4. Specific examples
5. Predictions
6. Evidence
7. Contradictions

Good:

"What happened next?"

"What did that feel like?"

"When did you first realize that?"

"What framework do you use for that?"

"What would someone who disagrees with you say?"

Bad:

"Can you elaborate?"

====================================================
BANNED PATTERNS
===============

Maximum usage across all questions:

"You said X but Y happened" = 2

"Critics argue..." = 2

"How do you reconcile..." = 2

"Some people say..." = 2

If exceeded:

REGENERATE.

====================================================
HOST STYLE
==========

Write like:

* Lex Fridman
* Steven Bartlett
* Chris Williamson
* Shaan Puri

Avoid sounding like:

* Researchers
* Journalists
* Governance analysts
* Policy consultants

Questions should feel conversational.

====================================================
FINAL VALIDATION
================

Before returning output verify:

Story Questions = 2
Framework Questions = 2
Contrarian Questions = 2
Prediction Questions = 2
Emotional Questions = 1
Legacy Questions = 1

Verify:

* Questions under 25 words
* Conversational tone
* No repetitive structures
* No research-summary questions
* Maximum 2 contradiction-based questions
* Every answer could become a title
* Every answer could become a viral clip

If validation fails:

REGENERATE ENTIRE QUESTION SET.

====================================================
QUESTION SCORING
================

Internally score every question:

Guest Incentive: /10
Viewer Curiosity: /10
Clip Potential: /10
Depth: /10
Headline Potential: /10

Only output questions scoring 40+/50.

Patterns JSON (Step 2 output):
{PATTERNS_JSON}

Guest intelligence JSON (Step 3 output):
{INTEL_JSON}
"""

STEP4_SCORING_CORE_PROMPT = """
You are an objective quality-scoring model. Score the virality brief JSON below on a scale of 0-10 (higher is better). Check for: specificity, completeness of all required arrays, valid float scores, and actionable content.

Return a JSON object with exactly two fields:
{
  "score": 8,
  "analysis": "Detailed explanation of strengths and any weaknesses found"
}

Virality brief JSON:
{BRIEF_JSON}
"""

STEP5_SIMULATOR_PROMPT = """
You are an advanced podcast interview intelligence system acting as a world-class interviewer. 
Your task is to generate a dynamic interview flow tree based on the provided guest intelligence and anchor questions.

You must generate:
1. Primary anchor questions (using the provided optimized questions as a base)
2. A deeply simulated, highly realistic guest answer to each main question.
3. 3-4 dynamic follow-up questions categorized by type (clarification, contradiction, pressure, example, emotional, prediction, audience_skepticism).

The key requirement:
Follow-up questions MUST depend strictly on the guest's simulated previous answer. Do NOT generate generic pre-written follow-ups.
Instead, simulate real podcast conversation flow by detecting contradictions, vague claims, emotional moments, missing specifics, or bold predictions in their simulated answer.

Return a JSON array with EXACTLY this format:
[
  {
    "main_question": "...",
    "possible_guest_answer": "...",
    "follow_ups": [
      {
        "type": "clarification",
        "question": "..."
      },
      {
        "type": "pressure",
        "question": "..."
      }
    ]
  }
]

Follow-up Types you can use:
- clarification: Ask for explanation when the answer is vague.
- contradiction: Compare current answer with past statements/stances from the intel.
- pressure: Push the guest to defend claims.
- example: Force concrete examples.
- emotional: Explore human/emotional moments.
- prediction: Expand future-looking statements.
- audience_skepticism: Represent viewer objections.

Important Rules:
- Follow-ups must feel conversational.
- They must reference the simulated previous answer.
- Simulate elite podcast interviewers (e.g., tough, inquisitive, empathetic where needed).
- Prioritize retention and curiosity gaps.
- Provide exactly 5 interview tree structures (5 main questions).
- Generate 3 to 4 follow-ups for each.

Guest Intelligence:
{INTEL_JSON}

Anchor Questions / Virality Brief:
{BRIEF_JSON}
"""

# End of prompts.py
