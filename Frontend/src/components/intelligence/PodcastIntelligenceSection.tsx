import type { PodcastIntelligence } from '../../types/intelligence';
import { motion } from 'framer-motion';
import RetentionChart from '../charts/RetentionChart';

export default function PodcastIntelligenceSection({ podcast }: { podcast: PodcastIntelligence }) {
  if (!podcast) {
    return <section><h3 className="text-xl font-semibold mb-4 text-white">Podcast Intelligence</h3><div className="text-gray-400 italic">No podcast intelligence found.</div></section>;
  }
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">Podcast Intelligence</h3>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-glass rounded-xl p-6 shadow-glass border border-white/10 flex flex-col gap-6"
      >
        <div className="flex flex-wrap gap-6">
          <Stat label="Clip Potential" value={podcast.clip_potential} />
          <Stat label="Storytelling Strength" value={podcast.storytelling_strength} />
          <Stat label="Audience Accessibility" value={podcast.audience_accessibility} />
          <Stat label="Virality Indicators" value={podcast.virality_indicators} />
        </div>
        {podcast.retention_profile && podcast.retention_profile.retention_chart ? (
          <RetentionChart data={podcast.retention_profile.retention_chart} />
        ) : (
          <div className="text-gray-400 italic">No retention data.</div>
        )}
      </motion.div>
    </section>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex flex-col items-center">
      <span className="text-accent font-bold text-lg">{value}</span>
      <span className="text-gray-400 text-xs">{label}</span>
    </div>
  );
}
