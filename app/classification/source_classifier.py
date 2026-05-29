from typing import Tuple
import re

# Simple rules-based classifier for demo; can be replaced with ML/NLP

def classify_source(url: str, title: str, snippet: str) -> Tuple[str, str, float]:
    url = url.lower()
    title = title.lower()
    snippet = snippet.lower()
    # Content type
    if 'podcast' in url or 'podcast' in title:
        content_type = 'podcast'
    elif 'interview' in title or 'interview' in snippet:
        content_type = 'interview'
    elif 'news' in url or 'news' in title:
        content_type = 'news'
    elif 'blog' in url or 'blog' in title:
        content_type = 'blog'
    elif 'clip' in url or 'clip' in title:
        content_type = 'clip'
    elif 'keynote' in title:
        content_type = 'keynote'
    elif 'panel' in title:
        content_type = 'panel'
    elif 'debate' in title or 'controversy' in snippet:
        content_type = 'controversy'
    elif 'discussion' in title or 'discussion' in snippet:
        content_type = 'discussion'
    elif 'advice' in title or 'advice' in snippet:
        content_type = 'founder advice'
    elif 'startup' in title or 'startup' in snippet:
        content_type = 'startup analysis'
    else:
        content_type = 'other'
    # Source authority
    if re.search(r'(cnbc|bloomberg|nytimes|ycombinator|wired|forbes|techcrunch|wsj|bbc|reuters)', url):
        authority = 0.95
    elif re.search(r'(youtube|medium|substack|podcast|anchor|spotify)', url):
        authority = 0.7
    else:
        authority = 0.4
    return (url, content_type, authority)
