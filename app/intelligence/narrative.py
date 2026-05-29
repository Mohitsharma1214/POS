from typing import List, Dict

# Simple narrative extraction (placeholder for LLM or advanced NLP)
def extract_narrative(results: List[Dict]) -> Dict:
    # Find most common themes in titles/snippets
    topics = []
    for r in results:
        t = r.get('title', '').lower()
        if 'ai' in t:
            topics.append('AI')
        if 'startup' in t:
            topics.append('Startup')
        if 'leadership' in t:
            topics.append('Leadership')
        if 'controversy' in t or 'debate' in t:
            topics.append('Controversy')
    # Dummy logic for demo
    return {
        'current_narrative': ' '.join(set(topics)) or 'No dominant narrative detected',
        'public_positioning': list(set(topics)),
        'emerging_topics': list(set(topics)),
        'recurring_discussion_patterns': list(set(topics))
    }
