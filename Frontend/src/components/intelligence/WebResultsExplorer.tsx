
"use client";
import type { WebResult } from '../../types/intelligence';
import { useState } from 'react';

const sortOptions = [
  { label: 'Relevance', value: 'authority_score' },
  { label: 'Controversy', value: 'controversy_score' },
  { label: 'Authority', value: 'authority_score' },
  { label: 'Virality', value: 'virality_score' },
];

export default function WebResultsExplorer({ webResults }: { webResults: WebResult[] }) {
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('authority_score');

  if (!Array.isArray(webResults) || webResults.length === 0) {
    return <div className="bg-glass rounded-xl shadow-glass p-6 border border-white/10 text-gray-400 italic">No web results found.</div>;
  }

  const filtered = webResults
    .filter((r) => r.title.toLowerCase().includes(query.toLowerCase()) || r.snippet.toLowerCase().includes(query.toLowerCase()))
    .sort((a, b) => b[sort as keyof WebResult] as number - (a[sort as keyof WebResult] as number));

  return (
    <div className="bg-glass rounded-xl shadow-glass p-6 border border-white/10 flex flex-col gap-4">
      <div className="flex gap-2 mb-2">
        <input
          className="bg-[#23272f] text-white placeholder-gray-400 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-accent flex-1"
          placeholder="Search research..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          className="bg-[#23272f] text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-accent"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
        >
          {sortOptions.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>
      <div className="flex flex-col gap-3 max-h-80 overflow-y-auto">
        {filtered.map((r) => (
          <div key={r.url} className="bg-[#23272f] rounded-lg p-3 border border-white/5 hover:border-accent transition">
            <a href={r.url} target="_blank" rel="noopener noreferrer" className="text-accent font-semibold hover:underline">
              {r.title}
            </a>
            <div className="text-gray-300 text-sm mt-1 line-clamp-2">{r.snippet}</div>
            <div className="flex gap-2 mt-2 text-xs text-gray-400">
              <span>Authority: {r.authority_score}</span>
              <span>Controversy: {r.controversy_score}</span>
              <span>Virality: {r.virality_score}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
