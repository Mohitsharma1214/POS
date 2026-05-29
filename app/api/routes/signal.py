from fastapi import APIRouter, HTTPException
from app.schemas.podcast_intelligence_output import PodcastIntelligenceOutput
from app.services.signal_collection_service import SignalCollectionService
from app.schemas.guest import GuestInput
import logging

router = APIRouter()

@router.post("/signals", response_model=PodcastIntelligenceOutput)
async def collect_signals(guest: GuestInput):
    try:
        service = SignalCollectionService()
        result = await service.collect_signals(guest.guest_name, guest.guest_niche)
        return result
    except Exception as e:
        logging.exception("Signal collection failed")
        raise HTTPException(status_code=500, detail="Signal collection failed: " + str(e))
