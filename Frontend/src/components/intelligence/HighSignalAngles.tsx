import type { Intelligence } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function HighSignalAngles({ angles }: { angles: Intelligence }) {
  // For demo, use topics and controversies to generate angles
  const angleTypes = [
    { label: 'Tension-Driven', color: 'from-yellow-400 to-accent' },
    { label: 'Contradiction-Driven', color: 'from-pink-500 to-accent' },
    { label: 'Emotionally Loaded', color: 'from-blue-500 to-accent' },
    { label: 'Viral Discussion', color: 'from-accent to-pink-500' },
  ];
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">High-Signal Podcast Angles</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-6">
        {angleTypes.map((type, i) => (
          <motion.div
            key={type.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className={`bg-gradient-to-br ${type.color} rounded-xl p-6 shadow-glass border border-white/10 flex flex-col gap-2`}
          >
            <div className="font-bold text-lg text-white mb-2">{type.label} Angle</div>
            <div className="text-gray-100 text-base">Premium insight for producers. (Auto-generated)</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
