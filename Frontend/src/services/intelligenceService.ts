
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
}): Promise<any> {
  const res = await fetch(getApiUrl('/research/virality-brief'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to fetch virality brief');
  return res.json();
}

export async function fetchFullPipeline(payload: {
  guest_name: string;
  guest_company?: string;
  guest_niche?: string;
  podcast_context?: string;
}): Promise<PodcastIntelligenceOutput> {
  const res = await fetch(getApiUrl('/research/full-pipeline'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to run full pipeline');
  const raw = await res.json();
  return mapBackendToGuestIntelligence(raw);
}


