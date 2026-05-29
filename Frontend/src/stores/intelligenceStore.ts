import { create } from 'zustand';
import type { PodcastIntelligenceOutput } from '../types/intelligence';

interface IntelligenceState {
  data: PodcastIntelligenceOutput | null;
  loading: boolean;
  error: string | null;
  setLoading: (loading: boolean) => void;
  setData: (data: PodcastIntelligenceOutput) => void;
  setError: (error: string | null) => void;
}

export const useIntelligenceStore = create<IntelligenceState>((set) => ({
  data: null,
  loading: false,
  error: null,
  setLoading: (loading) => set({ loading }),
  setData: (data) => set({ data, loading: false, error: null }),
  setError: (error) => set({ error, loading: false }),
}));
