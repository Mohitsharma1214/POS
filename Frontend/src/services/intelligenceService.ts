
import type { PodcastIntelligenceOutput } from '../types/intelligence';
import { getApiUrl } from '../lib/api';
import { mapBackendToGuestIntelligence } from './mapBackendToGuestIntelligence';

export async function fetchGuestIntelligence(payload: {
  guest_name: string;
  guest_company?: string;
  guest_niche?: string;
  podcast_context?: string;
}): Promise<PodcastIntelligenceOutput> {
  const res = await fetch(getApiUrl('/research/guest'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to fetch intelligence');
  const raw = await res.json();
  return mapBackendToGuestIntelligence(raw);
}

export async function fetchWorkingPatterns(payload: {
  guest_name: string;
  guest_company?: string;
  guest_niche?: string;
  podcast_context?: string;
  apify_scrape_episodes?: any[];
}): Promise<any> {
  const res = await fetch(getApiUrl('/research/pattern-extract'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to extract patterns');
  return res.json();
}

export async function fetchGuestSpecificIntelligence(payload: {
  guest_name: string;
  guest_company?: string;
  guest_niche?: string;
  podcast_context?: string;
}): Promise<any> {
  const res = await fetch(getApiUrl('/research/guest-intelligence'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to fetch guest specific intelligence');
  return res.json();
}

export async function fetchViralityBrief(payload: {
  guest_name: string;
  guest_niche?: string;
  apify_scrape_episodes?: any[];
  cached_patterns?: any;
  cached_intelligence?: any;
  cached_comments?: any[];
  cached_signals?: any;
}): Promise<any> {
  const res = await fetch(getApiUrl('/research/virality-brief'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to fetch virality brief');
  return res.json();
}

export async function fetchRegenerateViralityItem(payload: {
  item_type: string;
  guest_name: string;
  guest_niche?: string;
  cached_patterns?: any;
  cached_intelligence?: any;
  cached_comments?: any[];
  cached_signals?: any;
  existing_items?: any[];
}): Promise<any> {
  const res = await fetch(getApiUrl('/research/virality-brief/regenerate-item'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to regenerate virality item');
  return res.json();
}

export async function fetchFullPipeline(payload: {
  guest_name: string;
  guest_company?: string;
  guest_niche?: string;
  podcast_context?: string;
}): Promise<PodcastIntelligenceOutput> {
  // We orchestrate the pipeline from the frontend to bypass Vercel's 10-60s timeout limits.
  // By breaking the huge task into 4 separate API calls, no single request times out.

  // Step 1: Collect Signals
  const signalsRes = await fetch(getApiUrl('/research/guest'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!signalsRes.ok) throw new Error('Failed to collect signals (Step 1)');
  const signals = await signalsRes.json();

  // Step 2: Extract Working Patterns
  const patternsPayload = {
    ...payload,
    apify_scrape_episodes: signals.apify_scrape_episodes || []
  };
  const patternsRes = await fetch(getApiUrl('/research/pattern-extract'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patternsPayload),
  });
  if (!patternsRes.ok) throw new Error('Failed to extract patterns (Step 2)');
  const patterns = await patternsRes.json();

  // Step 3: Guest Intelligence
  const intelPayload = {
    ...payload,
    apify_scrape_episodes: signals.apify_scrape_episodes || [],
    cached_comments: signals.comment_intelligence || []
  };
  const intelRes = await fetch(getApiUrl('/research/guest-intelligence'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(intelPayload),
  });
  if (!intelRes.ok) throw new Error('Failed to extract guest intelligence (Step 3)');
  const intelligence = await intelRes.json();

  // Step 4: Virality Brief
  const briefPayload = {
    ...payload,
    guest_niche: signals.inferred_niche || payload.guest_niche,
    apify_scrape_episodes: signals.apify_scrape_episodes || [],
    cached_patterns: patterns.pattern_report,
    cached_intelligence: intelligence,
    cached_comments: signals.comment_intelligence || [],
    cached_signals: signals
  };
  const briefRes = await fetch(getApiUrl('/research/virality-brief'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(briefPayload),
  });
  if (!briefRes.ok) throw new Error('Failed to generate virality brief (Step 4)');
  const brief = await briefRes.json();

  // Combine results
  const raw = {
    result: {
      ...signals,
      patterns: patterns.pattern_report,
      intelligence: intelligence,
      brief: brief
    }
  };

  return mapBackendToGuestIntelligence(raw);
}


