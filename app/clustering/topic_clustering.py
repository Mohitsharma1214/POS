from typing import List, Dict
from collections import Counter
import re

# Simple keyword/phrase extraction and clustering

def extract_keywords(text: str) -> List[str]:
    # Naive: split on non-word, filter stopwords, deduplicate
    stopwords = set(['the', 'and', 'of', 'to', 'in', 'a', 'for', 'on', 'with', 'at', 'by', 'an', 'is', 'as', 'from', 'that', 'this', 'it', 'be', 'are', 'was', 'or', 'has', 'have', 'but', 'not', 'will', 'can', 'about', 'more', 'than', 'into', 'their', 'who', 'what', 'which', 'when', 'where', 'how', 'why'])
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if w not in stopwords and len(w) > 2]
    return list(set(keywords))

def cluster_topics(results: List[Dict]) -> List[Dict]:
    # Aggregate all titles/snippets
    all_text = ' '.join([r.get('title', '') + ' ' + r.get('snippet', '') for r in results])
    keywords = extract_keywords(all_text)
    freq = Counter(keywords)
    clusters = []
    for topic, count in freq.most_common(10):
        related = [r.get('url') or r.get('video_url') for r in results if topic in r.get('title', '').lower() or topic in r.get('snippet', '').lower()]
        clusters.append({
            'topic': topic,
            'frequency': count,
            'related_sources': related
        })
    return clusters
