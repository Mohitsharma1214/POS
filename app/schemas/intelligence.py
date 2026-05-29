
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Move all class definitions above IntelligenceOutput

class Contradiction(BaseModel):
    topic: str
    claim: str
    counter_argument: str
    sources: List[str]

class TopicHierarchy(BaseModel):
    parent_topic: str
    subtopics: List[str]
    signal_score: float
    confidence_score: float

class Controversy(BaseModel):
    topic: str
    severity: str
    summary: str
    sources: List[str]
    signal_score: float
    confidence_score: float

class EmotionalPattern(BaseModel):
    theme: str
    description: str
    signal_score: float
    confidence_score: float

class PodcastRetentionProfile(BaseModel):
    storytelling_strength: float
    clip_potential: float
    controversy_intensity: float
    education_density: float
    audience_accessibility: float

class HighSignalAngle(BaseModel):
    angle: str
    signal_score: float
    confidence_score: float

class NarrativeEvolution(BaseModel):
    past_narrative: str
    current_narrative: str
    narrative_shift_reason: str
    signal_score: float
    confidence_score: float

class Topic(BaseModel):
    topic: str
    parent_topic: Optional[str] = None
    hierarchy: Optional[List[str]] = None
    signal_score: float
    confidence_score: float

class YouTubeClassification(BaseModel):
    title: str
    channel: str
    estimated_format: str
    estimated_virality: str
    discussion_style: str
    retention_style: str
    classification: str
    url: str
    signal_score: float
    confidence_score: float



class Contradiction(BaseModel):
    topic: str
    claim: str
    counter_argument: str
    sources: List[str]

class TopicHierarchy(BaseModel):
    parent_topic: str
    subtopics: List[str]
    signal_score: float
    confidence_score: float

    topic: str
    severity: str
    summary: str
    sources: List[str]
    signal_score: float
    confidence_score: float

    theme: str
    description: str
    signal_score: float
    confidence_score: float

class PodcastRetentionProfile(BaseModel):
    storytelling_strength: float
    clip_potential: float
    controversy_intensity: float
    education_density: float
    audience_accessibility: float

    angle: str
    signal_score: float
    confidence_score: float

    past_narrative: str
    current_narrative: str
    narrative_shift_reason: str
    signal_score: float
    confidence_score: float

    topic: str
    parent_topic: Optional[str] = None
    hierarchy: Optional[List[str]] = None
    signal_score: float
    confidence_score: float

    title: str
    channel: str
    estimated_format: str
    estimated_virality: str
    discussion_style: str
    retention_style: str
    classification: str
    url: str
    signal_score: float
    confidence_score: float

class IntelligenceOutput(BaseModel):
    dominant_topics: List[Topic] = []
    high_signal_topics: List[Topic] = []
    topic_hierarchy: List[TopicHierarchy] = []
    controversies: List[Controversy] = []
    contradictions: List[Contradiction] = []
    public_positioning: List[str] = []
    emerging_topics: List[Topic] = []
    discussion_patterns: List[str] = []
    podcast_patterns: List[str] = []
    interesting_angles: List[HighSignalAngle] = []
    guest_narrative: str = ""
    narrative_evolution: Optional[NarrativeEvolution] = None
    emotional_patterns: List[EmotionalPattern] = []
    podcast_retention_profile: Optional[PodcastRetentionProfile] = None
    research_summary: str = ""
    youtube_intelligence: Optional[List[YouTubeClassification]] = []
