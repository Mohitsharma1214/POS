from pydantic import BaseModel
from typing import List

class FollowUp(BaseModel):
    type: str
    question: str

class InterviewIntelligenceInput(BaseModel):
    main_question: str
    possible_guest_answer: str

class InterviewIntelligenceOutput(BaseModel):
    main_question: str
    possible_guest_answer: str
    follow_ups: List[FollowUp]
