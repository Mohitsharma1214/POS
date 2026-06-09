import logging
from typing import Dict, Any
from app.services.anthropic_service import AnthropicService

class InterviewIntelligenceService:
    def __init__(self):
        from app.core.config import settings
        self.llm = AnthropicService(model=settings.MODEL_OPUS)

    async def generate_dynamic_follow_ups(self, main_question: str, possible_guest_answer: str) -> Dict[str, Any]:
        """
        Generate dynamic follow-up questions based on the guest's simulated answer.
        """
        prompt = f"""You are an advanced podcast interview intelligence system.

Your task is NOT to only generate standalone interview questions.

You must generate:
1. Primary anchor questions
2. Dynamic follow-up questions
3. Reactive contradiction follow-ups
4. Clarification follow-ups
5. Emotional follow-ups
6. Pressure-testing follow-ups
7. Example-based follow-ups

The key requirement: Follow-up questions MUST depend on the guest’s previous answer.
Do NOT generate generic pre-written follow-ups. Instead, simulate real podcast conversation flow.

---

## CORE BEHAVIOR
When analyzing the guest's response:
* Detect contradictions
* Detect vague claims
* Detect emotional moments
* Detect missing specifics
* Detect bold predictions
* Detect controversial claims
* Detect technical jargon needing clarification

Then generate intelligent follow-up questions based ONLY on the answer.

---

## FOLLOW-UP TYPES
1. Clarification Follow-Up: Ask for explanation when the answer is vague.
2. Contradiction Follow-Up: Compare current answer with past statements or known positions.
3. Pressure Follow-Up: Push the guest to defend claims.
4. Example Follow-Up: Force concrete examples.
5. Emotional Follow-Up: Explore human/emotional moments.
6. Prediction Follow-Up: Expand future-looking statements.
7. Audience Skepticism Follow-Up: Represent viewer objections.

---

## IMPORTANT RULES
* Follow-ups must feel conversational
* They must reference the previous answer
* Avoid robotic phrasing
* Avoid repeating the same structure
* Escalate depth naturally
* Simulate elite podcast interviewers
* Prioritize retention and curiosity gaps
* Generate short follow-ups when appropriate
* Generate aggressive follow-ups if contradictions are detected
* Generate softer follow-ups during emotional moments

---

## INPUT
Main Question: {main_question}
Guest Answer: {possible_guest_answer}

---

## OUTPUT FORMAT
Return ONLY a valid JSON object matching this schema exactly, without any markdown code block formatting or extra text:

{{
  "main_question": "{main_question}",
  "possible_guest_answer": "{possible_guest_answer}",
  "follow_ups": [
    {{
      "type": "clarification",
      "question": "..."
    }},
    {{
      "type": "pressure",
      "question": "..."
    }},
    {{
      "type": "example",
      "question": "..."
    }}
  ]
}}
"""
        try:
            result = await self.llm.complete(prompt, return_json=True, max_tokens=1500)
            if not isinstance(result, dict):
                raise ValueError("Expected dictionary output from LLM parse.")
            return result
        except Exception as e:
            logging.error(f"Interview Intelligence failed to generate follow-ups. Error: {e}")
            raise
