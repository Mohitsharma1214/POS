from app.services.openrouter_service import OpenRouterService
from app.prompts.intelligence_prompt import build_intelligence_prompt
from typing import Dict, Any
import logging

class IntelligenceAgent:
    def __init__(self, model: str = None):
        self.model = model
        self.llm = OpenRouterService(model=model)

    async def run(self, guest: Dict[str, Any], web_results: list, youtube_results: list) -> dict:
        from app.schemas.intelligence import IntelligenceOutput
        prompt = build_intelligence_prompt(guest, web_results, youtube_results)
        try:
            response = await self.llm.complete(prompt)
            logging.info(f"Raw LLM response: {response}")
            # Defensive: ensure response is a dict and has 'intelligence'
            intelligence = response.get("intelligence") if isinstance(response, dict) else None
            if not intelligence or not isinstance(intelligence, dict):
                logging.warning("LLM response missing 'intelligence' field or not a dict. Returning error intelligence block.")
                return {"intelligence": {"error": "LLM did not return valid intelligence data."}}

            # Validate and fill missing fields using IntelligenceOutput
            try:
                validated = IntelligenceOutput(**intelligence)
                # Return as dict, nested under 'intelligence' key
                return {"intelligence": validated.dict()}
            except Exception as ve:
                logging.error(f"Validation error: {ve}. Attempting to fill missing fields with defaults.")
                # Fill missing fields with defaults
                fields = IntelligenceOutput.__fields__
                filled = {k: intelligence.get(k, fields[k].get_default()) for k in fields}
                try:
                    validated = IntelligenceOutput(**filled)
                    return {"intelligence": validated.dict()}
                except Exception as ve2:
                    logging.error(f"Failed to fill missing fields: {ve2}")
                    return {"intelligence": {"error": f"Validation failed: {ve2}"}}
        except Exception as e:
            logging.error(f"IntelligenceAgent failed: {e}")
            return {"intelligence": {"error": str(e)}}
