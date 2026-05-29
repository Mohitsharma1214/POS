from typing import List, Dict

def generate_research_summary(results: List[Dict], clusters: List[Dict], controversies: List[Dict]) -> Dict:
    # Dummy logic for demo
    guest_overview = ' '.join(set([r.get('title', '') for r in results[:3]]))
    dominant_topics = [c['topic'] for c in clusters[:3]]
    recent_narratives = dominant_topics
    controversial_topics = [c['topic'] for c in controversies]
    notable_appearances = [r.get('title', '') for r in results if r.get('content_type') in ['podcast', 'interview']][:3]
    discussion_patterns = dominant_topics
    interesting_angles = dominant_topics
    high_signal_topics = dominant_topics
    return {
        'guest_overview': guest_overview,
        'dominant_topics': dominant_topics,
        'recent_narratives': recent_narratives,
        'controversial_topics': controversial_topics,
        'notable_appearances': notable_appearances,
        'discussion_patterns': discussion_patterns,
        'interesting_angles': interesting_angles,
        'high_signal_topics': high_signal_topics
    }
