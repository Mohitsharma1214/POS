import type { Controversy } from '../../types/intelligence';
import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';

export default function ControversySection({ controversies }: { controversies: Controversy[] }) {
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">Controversy Intelligence</h3>
      <div className="flex flex-col gap-4">
        {!Array.isArray(controversies) || controversies.length === 0 ? (
          <div className="text-gray-400 italic">No controversies found.</div>
        ) : (
          controversies.map((c, i) => (
            <motion.div
              key={c.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className={`bg-glass rounded-xl p-6 shadow-glass border-l-4 ${getSeverityColor(c.severity)} border-white/10`}
            >
              <div className="flex items-center gap-3 mb-2">
                <AlertTriangle className="text-yellow-400" />
                <span className="font-bold text-lg text-white">{c.title}</span>
                <span className={`ml-2 px-2 py-1 rounded text-xs font-semibold ${getSeverityBadge(c.severity)}`}>{severityLabel(c.severity)}</span>
              </div>
              <div className="text-gray-300 mb-2">{c.summary}</div>
              <details className="mt-2 cursor-pointer">
                <summary className="text-accent underline">Supporting Sources</summary>
                <ul className="list-disc ml-6 mt-2 text-gray-400">
                  {Array.isArray(c.sources) && c.sources.length > 0 ? (
                    c.sources.map((s) => (
                      <li key={s}><a href={s} target="_blank" rel="noopener noreferrer" className="hover:text-accent underline">{s}</a></li>
                    ))
                  ) : (
                    <li>No sources available.</li>
                  )}
                </ul>
              </details>
            </motion.div>
          ))
        )}
      </div>
    </section>
  );
}

function getSeverityColor(severity: number) {
  if (severity >= 8) return 'border-red-500';
  if (severity >= 5) return 'border-yellow-400';
  return 'border-yellow-200';
}

function getSeverityBadge(severity: number) {
  if (severity >= 8) return 'bg-red-500 text-white';
  if (severity >= 5) return 'bg-yellow-400 text-black';
  return 'bg-yellow-200 text-black';
}

function severityLabel(severity: number) {
  if (severity >= 8) return 'Severe';
  if (severity >= 5) return 'Moderate';
  return 'Low';
}
