import type { PodcastIntelligenceOutput } from '../types/intelligence';

export function mapBackendToGuestIntelligence(raw: any): PodcastIntelligenceOutput {
  // The /research/full-pipeline endpoint wraps its response in { result: {...}, steps: [...] }
  // The /research/guest endpoint returns the fields directly.
  // Unwrap "result" if present so we always work with a flat signal object.
  const d = (raw && raw.result && typeof raw.result === 'object') ? raw.result : raw;

  return {
    guest_name: d.guest_name || undefined,
    top_performing_guest_episodes: d.top_performing_guest_episodes || [],
    top_niche_trends: d.top_niche_trends || [],
    twitter_signals: d.twitter_signals || [],
    reddit_discussions: d.reddit_discussions || [],
    similar_guests: d.similar_guests || [],
    instagram_intelligence: d.instagram_intelligence || {
      raw_signals: [],
      viral_themes: [],
      audience_sentiment: "",
      persona_delta: ""
    },
    twitter_intelligence: d.twitter_intelligence || {
      raw_signals: [],
      viral_themes: [],
      audience_sentiment: "",
      persona_delta: ""
    },
    viral_topics: d.viral_topics || [],
    cross_platform_narratives: d.cross_platform_narratives || [],
    weighted_scores: d.weighted_scores || [],
    tavily_web_signals: d.tavily_web_signals || [],
    comment_intelligence: d.comment_intelligence || [],
    structured_insights: d.structured_insights || {},
    trending_podcast_episodes: d.trending_podcast_episodes || [],
    apify_scrape_episodes: d.apify_scrape_episodes || [],
    
    // Auto-map new precomputed assets
    patterns: d.patterns?.pattern_report || d.patterns || undefined,
    intelligence: d.intelligence?.intelligence_report || d.intelligence || undefined,
    brief: d.brief?.brief_report || d.brief || undefined,
    quality_assessment: d.quality_assessment || d.scoring || undefined,
  };
}
