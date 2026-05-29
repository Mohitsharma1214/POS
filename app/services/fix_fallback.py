import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/app/services/virality_brief_service.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all OptimizedQuestion(question= with OptimizedQuestion(primary_question=
# And add follow_ups property.
def replace_optimized_question(match):
    prefix = match.group(1)
    q_val = match.group(2)
    rest = match.group(3)
    # Add a generic follow-up array to satisfy the schema
    return f"{prefix}primary_question={q_val}, follow_ups=[\"Can you give a specific operational example?\", \"What did you do differently to avoid the common pitfall?\"], {rest}"

content = re.sub(r'(OptimizedQuestion\s*\(\s*)question=(.*?),\s*(objective=.*?\))', replace_optimized_question, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Virality Brief Fallback updated successfully")
