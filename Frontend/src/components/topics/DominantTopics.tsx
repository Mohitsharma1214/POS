
import type { Topic } from '../../types/intelligence';
import { motion } from 'framer-motion';

type DominantTopicsProps = {
  topics: Topic[];
};

export default function DominantTopics({ topics }: DominantTopicsProps) {
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">Dominant Topics</h3>
      {(!Array.isArray(topics) || topics.length === 0) ? (
        <div className="text-gray-400 italic">No topics found.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {topics.map((topic, i) => (
            <motion.div
              key={topic.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08, duration: 0.5 }}
              className="bg-glass rounded-xl p-6 shadow-glass flex flex-col gap-2 border border-white/10"
            >
              <div className="font-bold text-accent text-lg mb-1">{topic.title}</div>
              <div className="flex items-center gap-2 text-sm text-gray-300">
                <span>Signal:</span>
                <span className="font-semibold text-white">{topic.signal_score}</span>
                <span className="ml-2">Confidence:</span>
                <span className="font-semibold text-white">{topic.confidence_score}</span>
              </div>
              <div className="flex gap-2 mt-2">
                <ProgressBar label="Importance" value={topic.importance} color="from-accent to-white" />
                <ProgressBar label="Relevance" value={topic.relevance} color="from-blue-500 to-accent" />
                <ProgressBar label="Popularity" value={topic.popularity} color="from-pink-500 to-accent" />
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </section>
  );
}

function ProgressBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex flex-col items-center w-20">
      <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden mb-1">
        <div
          className={`h-2 rounded-full bg-gradient-to-r ${color}`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
      <span className="text-xs text-gray-400">{label}</span>
    </div>
  );
}
