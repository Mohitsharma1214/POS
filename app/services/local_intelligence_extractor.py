# LocalIntelligenceExtractor: Extracts basic intelligence from raw signals without LLMs
import re
from collections import Counter, defaultdict
from typing import List, Dict, Any

class LocalIntelligenceExtractor:
    """
    Extracts dominant topics, controversy, emotional patterns, engagement, etc. from raw podcast signals.
    This is a fallback and base intelligence layer, always available even if AI fails.
    """
    CONTROVERSY_KEYWORDS = ["controversy", "scandal", "debate", "backlash", "boycott", "layoff", "fraud", "lawsuit", "crisis", "sued", "fired"]
    EMOTION_KEYWORDS = ["excited", "angry", "happy", "sad", "concern", "fear", "love", "hate", "joy", "worry", "surprise", "shock"]

    def extract(self, youtube_data: List[Dict[str, Any]], twitter_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Flatten all text
        all_text = " ".join([
            *(video.get("title", "") for video in youtube_data),
            *(video.get("description", "") for video in youtube_data),
            *(tweet.get("text", "") for tweet in twitter_data)
        ])
        words = re.findall(r"\w+", all_text.lower())
        word_counts = Counter(words)

        # Dominant topics: most common non-stopword words
        stopwords = set(["the", "and", "of", "to", "in", "a", "is", "for", "on", "with", "as", "by", "at", "an", "be", "this", "that", "from", "it", "are", "was", "will", "or", "has", "have", "but", "not", "about", "can", "more", "we", "you", "they", "their", "our", "all", "one", "new", "who", "what", "when", "how", "which", "so", "if", "do", "out", "up", "just", "his", "her", "he", "she", "them", "your", "than", "also", "into", "no", "had", "been", "were", "some", "other", "any", "get", "like", "over", "after", "most", "time", "people", "because", "could", "should", "would", "very", "see", "only", "now", "then", "did", "back", "even", "first", "last", "much", "many", "where", "why", "may", "these", "those", "each", "every", "such", "through", "between", "before", "under", "again", "same", "off", "while", "during", "both", "few", "might", "being", "own", "too", "since", "per", "among", "against", "upon", "within", "without", "across", "toward", "towards", "upon", "amongst", "beside", "besides", "via", "upon", "amid", "amidst", "around", "along", "beyond", "despite", "except", "inside", "outside", "past", "regarding", "throughout", "toward", "towards", "upon", "versus", "via", "within", "without"])
        dominant_topics = [w for w, c in word_counts.most_common(20) if w not in stopwords][:5]

        # Controversy indicators
        controversy = [w for w in self.CONTROVERSY_KEYWORDS if w in words]

        # Emotional patterns
        emotions = [w for w in self.EMOTION_KEYWORDS if w in words]

        # Engagement (from YouTube)
        max_likes = max((video.get("likeCount", 0) for video in youtube_data), default=0)
        avg_comments = sum((video.get("commentCount", 0) for video in youtube_data)) // max(1, len(youtube_data))

        # Top channels
        top_channels = [video.get("channelTitle", "") for video in youtube_data]
        top_channels = [c for c in Counter(top_channels).most_common(3) if c[0]]
        top_channels = [c[0] for c in top_channels]

        # Top episodes
        top_episodes = [video.get("title", "") for video in youtube_data[:3] if video.get("title")]

        # Topic momentum (trending topics)
        topic_momentum = dominant_topics[:3]

        return {
            "dominant_topics": dominant_topics,
            "top_channels": top_channels,
            "controversy_indicators": controversy,
            "emotional_patterns": emotions,
            "engagement_insights": {"max_likes": max_likes, "avg_comments": avg_comments},
            "top_episodes": top_episodes,
            "topic_momentum": topic_momentum
        }
