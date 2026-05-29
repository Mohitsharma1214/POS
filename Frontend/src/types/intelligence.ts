
export interface Episode {
  title: string;
  video_id: string;
  thumbnail_url?: string;
  video_url?: string;
  publish_date?: string;
  views?: number;
  likes?: number;
  comments_count?: number;
  engagement_ratio?: number;
  ctr_proxy?: number;
  growth_velocity?: number;
  score?: number;
  channel_name?: string;
  description?: string;
  real_questions_asked?: string[];
}

export interface NicheTrend {
  title: string;
  video_id: string;
  thumbnail_url?: string;
  video_url?: string;
  publish_date?: string;
  views?: number;
  likes?: number;
  comments_count?: number;
  engagement_ratio?: number;
  ctr_proxy?: number;
  growth_velocity?: number;
  score?: number;
  niche?: string;
  description?: string;
  real_questions_asked?: string[];
}

export interface TwitterSignal {
  tweet_text: string;
  author: string;
  created_at: string;
  likes: number;
  retweets: number;
  replies: number;
  views: number;
  hashtags: string[];
  engagement_score?: number;
  recurring_topic?: string;
  is_simulated?: boolean;
}

export interface WebSignal {
  title: string;
  url: string;
  snippet?: string;
  source?: string;
  trending_score?: number;
}

export interface RawComment {
  text: string;
  author: string;
  like_count: number;
  published_at: string;
}

export interface CommentInsight {
  video_id: string;
  recurring_themes: string[];
  audience_emotions: string[];
  objections: string[];
  requests: string[];
  viral_moments: string[];
  hidden_demand_signals: string[];
  raw_comments?: RawComment[];
  commenter_questions?: string[];
}

export interface NarrativeCluster {
  narrative: string;
  source_platforms: string[];
  frequency?: number;
  sentiment?: string;
  controversy_level?: string;
}

export interface WeightedScore {
  video_id: string;
  score: number;
  reason: string;
  video_url?: string;
  thumbnail_url?: string;
}

export interface RedditDiscussion {
  subreddit?: string;
  post_title: string;
  post_text?: string;
  upvotes?: number;
  comments_count?: number;
  public_sentiment?: string;
  recurring_opinions?: string[];
  controversy_topics?: string[];
  trending_score?: number;
  url?: string;
}

export interface SimilarGuest {
  guest_name: string;
  related_episode_titles: string[];
  audience_overlap_reason?: string;
  overlap_score?: number;
  niche?: string;
  bookability_score?: number;
  primary_platform?: string;
}

export interface ViralTopic {
  topic_name: string;
  frequency: number;
  engagement_level: number;
  cross_platform_mentions: number;
  description?: string;
}

export interface InstagramSignal {
  title: string;
  url: string;
  snippet?: string;
  engagement_score?: number;
  likes?: number;
  comments?: number;
  views?: number;
  is_simulated?: boolean;
}

export interface InstagramIntelligence {
  raw_signals: InstagramSignal[];
  viral_themes: string[];
  audience_sentiment: string;
  persona_delta: string;
  is_simulated?: boolean;
  instagram_handle?: string;
}

export interface TwitterIntelligence {
  raw_signals: TwitterSignal[];
  viral_themes: string[];
  audience_sentiment: string;
  persona_delta: string;
  is_simulated?: boolean;
  twitter_handle?: string;
}

export interface PodcastIntelligenceOutput {
  guest_name?: string;
  inferred_niche?: string;
  inferred_podcast_context?: string;
  top_performing_guest_episodes: Episode[];
  top_niche_trends: NicheTrend[];
  twitter_signals: TwitterSignal[];
  reddit_discussions: RedditDiscussion[];
  instagram_intelligence: InstagramIntelligence;
  twitter_intelligence?: TwitterIntelligence;
  similar_guests: SimilarGuest[];
  viral_topics: ViralTopic[];
  cross_platform_narratives: NarrativeCluster[];
  weighted_scores: WeightedScore[];
  tavily_web_signals: WebSignal[];
  comment_intelligence: CommentInsight[];
  structured_insights?: Record<string, any>;
  trending_podcast_episodes?: TrendingPodcastEpisode[];
  apify_scrape_episodes?: ApifyScrapeEpisode[];
  
  // New Autopilot pre-cached fields
  patterns?: any;
  intelligence?: any;
  brief?: any;
  quality_assessment?: any;
}

export interface SimilarGuest {
  guest_name: string;
  relevance_reason?: string;
  niche?: string;
  audience_overlap?: string;
  bookability_score?: number;
  primary_platform?: string;
}

export interface MinimalTopGuestAppearance {
  title: string;
  video_id: string;
  views: number;
  description: string;
  publish_date: string;
  duration: number;
  channel: string;
}

export interface MinimalTopNicheVideo {
  title: string;
  video_id: string;
  views: number;
  description: string;
  publish_date: string;
  duration: number;
  channel: string;
}

export interface GuestOverview {
  who_they_are: string;
  why_they_are_trending: string;
  audience_overlap: string;
  controversy_level: 'low' | 'medium' | 'high' | string;
}

export interface PodcastIntelligence {
  top_title_patterns: string[];
  high_retention_hooks: string[];
  viral_topics: string[];
  best_clip_moments: string[];
}

export interface EmotionalIntelligence {
  dominant_emotions: string[];
  audience_pain_points: string[];
  identity_signals: string[];
}

export interface NarrativeEvolution {
  old_positioning: string;
  current_positioning: string;
  emerging_angles: string[];
}

export interface TrendingPodcastEpisode {
  title: string;
  source?: string;
  url?: string;
  description?: string;
}

export interface ApifyScrapeEpisode {
  title: string;
  url?: string;
  description?: string;
  view_count?: number;
  comment_themes?: string[];
}

export interface GuestProfile {
  name: string;
  company: string;
  niche: string;
  public_positioning: string;
  narrative: string;
}

export interface ResearchMetadata {
  started_at: string;
  completed_at: string;
  duration_seconds: number;
}

export interface WebResult {
  title: string;
  url: string;
  snippet: string;
  authority_score: number;
  controversy_score: number;
  virality_score: number;
}

export interface YoutubeResult {
  video_id: string;
  title: string;
  channel: string;
  thumbnail_url: string;
  virality_estimate: number;
  format_classification: string;
  retention_style: string;
}

export interface Intelligence {
  topics: Topic[];
  controversies: Controversy[];
  podcast: PodcastIntelligence;
  emotional: EmotionalIntelligence;
  narrative_evolution: NarrativeEvolution;
  summary: ResearchSummary;
}

export interface Topic {
  title: string;
  signal_score: number;
  confidence_score: number;
  importance: number;
  relevance: number;
  popularity: number;
}

export interface Controversy {
  title: string;
  severity: number;
  summary: string;
  sources: string[];
}

export interface PodcastIntelligence {
  patterns: string[];
  clip_potential: number;
  storytelling_strength: number;
  audience_accessibility: number;
  virality_indicators: number;
  retention_profile: RetentionProfile;
}

export interface RetentionProfile {
  retention_chart: number[];
  engagement_meter: number;
  virality_gauge: number;
}

export interface EmotionalIntelligence {
  themes: string[];
  audience_reactions: string[];
  tension_patterns: string[];
  trust_vs_skepticism: number;
  emotional_intensity: number;
  audience_polarity: number;
  heatmap: number[][];
}

export interface NarrativeEvolution {
  timeline: NarrativePoint[];
}

export interface NarrativePoint {
  date: string;
  narrative: string;
  perception_change_reason: string;
}

export interface ResearchSummary {
  who: string;
  why: string;
  conversations: string;
  risks: string;
  emotional_tensions: string;
}

export interface TimelineEvent {
  period: string;
  event_type: 'Birth' | 'Education' | 'Personal Life' | 'Career' | 'Wealth' | 'Controversy' | string;
  title: string;
  description: string;
}

export interface GuestEnrichment {
  bio: string;
  current_roles: string[];
  accomplishments: string[];
  social_profiles: string[];
}

export interface PublicStance {
  topic: string;
  position: string;
  quote_or_source: string;
}

export interface Contradiction {
  stance_a: string;
  stance_b: string;
  analysis: string;
}

export interface GuestIntelligenceReport {
  enrichment: GuestEnrichment;
  biography_timeline: TimelineEvent[];
  covered_angles: string[];
  untapped_angles: string[];
  public_stances: PublicStance[];
  contradictions: Contradiction[];
}
