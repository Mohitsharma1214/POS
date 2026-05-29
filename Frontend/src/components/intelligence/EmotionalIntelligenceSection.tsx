import type { EmotionalIntelligence } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function EmotionalIntelligenceSection({ emotional }: { emotional: EmotionalIntelligence }) {
  if (!emotional) {
    return <section><h3 className="text-xl font-semibold mb-4 text-white">Emotional Intelligence</h3><div className="text-gray-400 italic">No emotional intelligence found.</div></section>;
  }
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">Emotional Intelligence</h3>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-glass rounded-xl p-6 shadow-glass border border-white/10 flex flex-col gap-4"
      >
        <div className="flex flex-wrap gap-4">
          {Array.isArray(emotional.themes) && emotional.themes.length > 0 ? emotional.themes.map((theme) => (
            <span key={theme} className="bg-accent/20 text-accent px-3 py-1 rounded-full text-sm font-medium">
              {theme}
            </span>
          )) : <span className="text-gray-400 italic">No themes found.</span>}
        </div>
        <div className="flex flex-wrap gap-4">
          {Array.isArray(emotional.audience_reactions) && emotional.audience_reactions.length > 0 ? emotional.audience_reactions.map((reaction) => (
            <span key={reaction} className="bg-pink-500/20 text-pink-400 px-3 py-1 rounded-full text-sm font-medium">
              {reaction}
            </span>
          )) : <span className="text-gray-400 italic">No audience reactions found.</span>}
        </div>
        <div className="flex flex-wrap gap-4">
          {Array.isArray(emotional.tension_patterns) && emotional.tension_patterns.length > 0 ? emotional.tension_patterns.map((tension) => (
            <span key={tension} className="bg-yellow-400/20 text-yellow-400 px-3 py-1 rounded-full text-sm font-medium">
              {tension}
            </span>
          )) : <span className="text-gray-400 italic">No tension patterns found.</span>}
        </div>
        <div className="flex gap-6 mt-4">
          <Stat label="Trust vs Skepticism" value={emotional.trust_vs_skepticism} color="accent" />
          <Stat label="Emotional Intensity" value={emotional.emotional_intensity} color="pink-500" />
          <Stat label="Audience Polarity" value={emotional.audience_polarity} color="blue-500" />
        </div>
        <div className="mt-4">
          {Array.isArray(emotional.heatmap) && emotional.heatmap.length > 0 ? <Heatmap heatmap={emotional.heatmap} /> : <span className="text-gray-400 italic">No heatmap data.</span>}
        </div>
      </motion.div>
    </section>
  );
}

function Stat({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex flex-col items-center">
      <span className={`text-${color} font-bold text-lg`}>{value}</span>
      <span className="text-gray-400 text-xs">{label}</span>
    </div>
  );
}

function Heatmap({ heatmap }: { heatmap: number[][] }) {
  return (
    <div className="flex flex-col gap-1">
      {heatmap.map((row, i) => (
        <div key={i} className="flex gap-1">
          {row.map((cell, j) => (
            <div
              key={j}
              className="w-4 h-4 rounded"
              style={{ background: `rgba(99,102,241,${cell / 100})` }}
            />
          ))}
        </div>
      ))}
    </div>
  );
}
