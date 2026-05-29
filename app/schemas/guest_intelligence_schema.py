from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GuestEnrichment(BaseModel):
    bio: str = Field(..., description="Concise high-quality biography of the guest")
    current_roles: List[str] = Field(default_factory=list, description="Active roles, company affiliations, or titles")
    accomplishments: List[str] = Field(default_factory=list, description="Key professional or personal milestones")
    social_profiles: List[str] = Field(default_factory=list, description="Related social media handles or website links")

class TimelineEvent(BaseModel):
    period: str = Field(..., description="The year or time range (e.g., '1964', '1982-1986', '2017')")
    event_type: str = Field(..., description="Category: 'Birth', 'Education', 'Personal Life', 'Career', 'Wealth', 'Controversy'")
    title: str = Field(..., description="A short, catchy summary of the milestone")
    description: str = Field(..., description="In-depth narrative of what happened, who was involved, and its significance")

class PublicStance(BaseModel):
    topic: str = Field(..., description="The subject matter of their public position")
    position: str = Field(..., description="Their stance or perspective on the topic")
    quote_or_source: str = Field(..., description="The quote or contextual sentence representing this position")

class Contradiction(BaseModel):
    stance_a: str = Field(..., description="Position A or historical stance/action")
    stance_b: str = Field(..., description="Position B or current conflicting statement/direction")
    analysis: str = Field(..., description="Brief breakdown of the conversational friction or developmental paradox")

class GuestIntelligenceReport(BaseModel):
    enrichment: GuestEnrichment = Field(..., description="Enriched biographical metadata")
    biography_timeline: List[TimelineEvent] = Field(default_factory=list, description="A detailed chronological record of the guest's life history")
    covered_angles: List[str] = Field(default_factory=list, description="Highly saturated angles/themes they cover on every podcast")
    untapped_angles: List[str] = Field(default_factory=list, description="Fresh, original angles or custom questions to ask")
    public_stances: List[PublicStance] = Field(default_factory=list, description="Known public positions and statements")
    contradictions: List[Contradiction] = Field(default_factory=list, description="Interesting contradictions, career paradoxes, or shifts in stance")
    viewer_curiosity_gaps: List[str] = Field(default_factory=list, description="Gaps in the guest's narrative that spark curiosity")
    emotional_inflection_points: List[str] = Field(default_factory=list, description="Key moments of emotional reflection or vulnerability")
    signature_frameworks: List[str] = Field(default_factory=list, description="The guest's unique mental models or frameworks")
    strongest_predictions: List[str] = Field(default_factory=list, description="The most compelling future predictions made by the guest")
    myths_they_fight: List[str] = Field(default_factory=list, description="Common industry myths the guest actively argues against")
    industry_battles: List[str] = Field(default_factory=list, description="Debates, rivalries, or systemic issues the guest is fighting")
    failure_moments: List[str] = Field(default_factory=list, description="Major failures or near-disasters that shaped their path")
    identity_questions: List[str] = Field(default_factory=list, description="Core questions or struggles regarding the guest's identity or legacy")

class GuestIntelligenceResponse(BaseModel):
    guest_name: str
    intelligence_report: GuestIntelligenceReport
