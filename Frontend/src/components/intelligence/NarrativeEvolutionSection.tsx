import type { NarrativeEvolution } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function NarrativeEvolutionSection({ narrative }: { narrative: NarrativeEvolution }) {
  if (!narrative || !Array.isArray(narrative.timeline) || narrative.timeline.length === 0) {
    return <section><h3 className="text-xl font-semibold mb-4 text-white">Narrative Evolution</h3><div className="text-gray-400 italic">No narrative evolution found.</div></section>;
  }
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">Narrative Evolution</h3>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-glass rounded-xl p-6 shadow-glass border border-white/10"
      >
        <Timeline timeline={narrative.timeline} />
      </motion.div>
    </section>
  );
}

function Timeline({ timeline }: { timeline: { date: string; narrative: string; perception_change_reason: string }[] }) {
  return (
    <div className="flex flex-col gap-6">
      {timeline.map((point, i) => (
        <div key={i} className="flex gap-4 items-start">
          <div className="flex flex-col items-center">
            <div className="w-4 h-4 rounded-full bg-accent border-2 border-white" />
            {i < timeline.length - 1 && <div className="w-1 h-12 bg-accent/40 mx-auto" />}
          </div>
          <div>
            <div className="text-gray-400 text-xs mb-1">{point.date}</div>
            <div className="text-white font-semibold mb-1">{point.narrative}</div>
            <div className="text-gray-300 text-sm italic">{point.perception_change_reason}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
