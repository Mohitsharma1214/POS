from fastapi import APIRouter, HTTPException
import logging
from app.schemas.interview_intelligence import InterviewIntelligenceInput, InterviewIntelligenceOutput
from app.services.interview_intelligence_service import InterviewIntelligenceService

router = APIRouter()

@router.post("/intelligence", response_model=InterviewIntelligenceOutput)
async def get_interview_intelligence(input_data: InterviewIntelligenceInput) -> InterviewIntelligenceOutput:
    try:
        service = InterviewIntelligenceService()
        result = await service.generate_dynamic_follow_ups(
            main_question=input_data.main_question,
            possible_guest_answer=input_data.possible_guest_answer
        )
        return result
    except Exception as e:
        logging.exception("Interview intelligence extraction failed")
        raise HTTPException(
            status_code=500,
            detail=f"Interview intelligence extraction failed: {e}",
        )
