from typing import List, Dict

def detect_controversies(results: List[Dict]) -> List[Dict]:
    controversies = []
    for r in results:
        title = r.get('title', '').lower()
        snippet = r.get('snippet', '').lower()
        if 'controversy' in title or 'controversy' in snippet or 'debate' in title or 'debate' in snippet or 'criticism' in snippet:
            controversies.append({
                'topic': title or snippet,
                'severity': 'high',
                'sources': [r.get('url')]
            })
    return controversies
