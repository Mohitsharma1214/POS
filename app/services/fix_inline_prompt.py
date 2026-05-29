import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/app/services/virality_brief_service.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the inline prompt
old_prompt_q = '"question": "Fully synthesized, challenging, self-contained question integrating quotes, paradoxes, and comments?"'
new_prompt_q = '"primary_question": "Short, punchy, conversational opening question. Written exactly as a human host would speak it naturally.",\n                    "follow_ups": ["If they say X, ask Y", "If they say A, ask B"]'
content = content.replace(old_prompt_q, new_prompt_q)

# Add explicit rules to the prompt
old_req = '- No placeholders, no generic text. Every item must be specific to this guest.'
new_req = '- No placeholders, no generic text. Every item must be specific to this guest.\n        - For optimized_questions, keep the primary_question extremely short and punchy like spoken dialogue. Do NOT hide multiple questions inside it. Provide 2-3 reactive follow-ups.'
content = content.replace(old_req, new_req)

# Fix _normalize_report_keys
old_normalize = 'primary_question=q.get("question") or "High-retention question?", follow_ups=["Can you give a specific operational example?", "What did you do differently to avoid the common pitfall?"]'
new_normalize = 'primary_question=q.get("primary_question") or q.get("question") or "High-retention question?", follow_ups=q.get("follow_ups") or ["Can you give a specific operational example?", "What did you do differently to avoid the common pitfall?"]'
content = content.replace(old_normalize, new_normalize)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Virality Brief Service inline prompt and normalization fixed successfully")
