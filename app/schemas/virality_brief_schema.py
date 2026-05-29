from pydantic import BaseModel, Field
from typing import List, Optional

class OptimizedQuestion(BaseModel):
    question_type: Optional[str] = Field(default=None, description="The category of the question (e.g. Story, Framework, Contrarian, etc.)")
    primary_question: str = Field(..., description="Short, punchy, conversational primary interview question. Do not over-explain.")
    follow_ups: List[str] = Field(default_factory=list, description="2-3 natural, reactive follow-up questions to drill down based on their answer.")
    objective: str = Field(..., description="What this question aims to extract or reveal")
    supporting_evidence: str = Field(..., description="The real data signal this question is built from (e.g. objection X, viewer comment Y)")
    retention_potential: float = Field(..., description="Predicted retention potential score from 0.0 to 1.0")

class TitleVariant(BaseModel):
    title: str = Field(..., description="High-performing video title variant")
    trigger_type: str = Field(..., description="Psychological trigger, e.g. Curiosity Gap, FOMO, Contrarian")
    predicted_ctr: float = Field(..., description="Predicted Click-Through Rate percentage, e.g. 14.5")

class ThumbnailConcept(BaseModel):
    concept_name: str = Field(..., description="Title of the thumbnail concept")
    visual_description: str = Field(..., description="Detailed visual layout and imagery description")
    text_overlay: str = Field(..., description="Bold copy to overlay on the thumbnail")
    accent_color: str = Field(..., description="Primary high-contrast color recommendation")

class HookScript(BaseModel):
    hook_type: str = Field(..., description="Hook strategy, e.g. Story loop, Metric shock")
    script_text: str = Field(..., description="Exact word-by-word 0-60s script to read")
    pacing_notes: str = Field(..., description="Spoken pacing, pauses, and tone notes")
    visual_cue: str = Field(..., description="B-roll or zoom-in visual directions")

class ClipAngle(BaseModel):
    title: str = Field(..., description="Catchy title of the clip segment")
    description: str = Field(..., description="Core topic or argument discussed")
    trigger_statement: str = Field(..., description="The highly shareable or controversial statement/hook")
    virality_score: float = Field(..., description="Predicted virality score from 0.0 to 1.0")
    platforms: List[str] = Field(default_factory=list, description="Target platforms, e.g. TikTok, YouTube Shorts, Reels")

class CalendarItem(BaseModel):
    day: str = Field(..., description="Suggested publishing day, e.g. Day 1, Monday")
    content_type: str = Field(..., description="Video type, e.g. Short, Full Episode, Reel")
    angle_topic: str = Field(..., description="Core angle or clip bait topic to publish")
    optimal_time: str = Field(..., description="Best time slot for maximum reach")

class ViralityBriefReport(BaseModel):
    optimized_questions: List[OptimizedQuestion] = Field(default_factory=list, description="10-12 tailored interview questions")
    title_variants: List[TitleVariant] = Field(default_factory=list, description="10 high-CTR title options")
    thumbnail_concepts: List[ThumbnailConcept] = Field(default_factory=list, description="8 concrete visual ideas")
    hook_scripts: List[HookScript] = Field(default_factory=list, description="5 detailed opening scripts")
    clip_angles: List[ClipAngle] = Field(default_factory=list, description="8 high-potency clippable blueprints")
    content_calendar: List[CalendarItem] = Field(default_factory=list, description="Weekly publishing schedule")

class ViralityBriefResponse(BaseModel):
    guest_name: str
    brief_report: ViralityBriefReport
