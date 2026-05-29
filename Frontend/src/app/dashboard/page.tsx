"use client";

import { useEffect, useState } from 'react';
import { useIntelligenceStore } from '../../stores/intelligenceStore';
import ResearchDashboard from '../../components/dashboard/ResearchDashboard';

export default function DashboardPage() {
  const { data, setData } = useIntelligenceStore();
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    // 1. Try to load from localStorage on client-side mount
    const saved = localStorage.getItem('podcast_intelligence_data');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed) {
          setData(parsed);
        }
      } catch (e) {
        console.error("Failed to parse saved research data:", e);
      }
    }
    setHydrated(true);
  }, [setData]);

  useEffect(() => {
    // 2. Persist data to localStorage whenever it changes
    if (data) {
      localStorage.setItem('podcast_intelligence_data', JSON.stringify(data));
    }
  }, [data]);

  if (!hydrated) {
    return (
      <div className="min-h-screen bg-[#06070B] flex items-center justify-center font-sans">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-neutral-500 font-bold uppercase tracking-widest">Syncing workspace...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-[#06070B] text-center text-gray-400 py-20 flex flex-col items-center justify-center font-sans p-6">
        <div className="bg-neutral-950 border border-neutral-900 rounded-3xl p-8 max-w-sm w-full shadow-2xl relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-full h-[3px] bg-orange-500" />
          <h2 className="text-lg font-black text-white mb-2 tracking-tight">No Research Dossier Loaded</h2>
          <p className="text-xs text-neutral-400 leading-relaxed mb-6">
            You haven't run any research yet or the current session has expired. Start a new research task on the homepage.
          </p>
          <a
            href="/"
            className="w-full block bg-orange-500 hover:bg-orange-600 active:scale-95 text-white font-bold text-xs py-3 rounded-xl transition shadow-md uppercase tracking-wider"
          >
            Go Back Home
          </a>
        </div>
      </div>
    );
  }

  return <ResearchDashboard data={data} />;
}

