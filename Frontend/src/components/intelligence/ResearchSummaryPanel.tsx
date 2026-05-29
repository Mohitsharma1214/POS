import type { ResearchSummary } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function ResearchSummaryPanel({ summary }: { summary: ResearchSummary }) {
  if (!summary) {
    return <div className="bg-glass rounded-2xl shadow-glass p-6 text-gray-400 italic">No executive briefing found.</div>;
  }
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="bg-glass rounded-2xl shadow-glass p-6 flex flex-col gap-4 backdrop-blur-md border border-white/10"
    >
      <h3 className="text-lg font-bold text-accent mb-2">AI Executive Briefing</h3>
      <div className="text-white text-base"><span className="font-semibold">Who:</span> {summary.who}</div>
      <div className="text-white text-base"><span className="font-semibold">Why they matter:</span> {summary.why}</div>
      <div className="text-white text-base"><span className="font-semibold">Conversations that work:</span> {summary.conversations}</div>
      <div className="text-white text-base"><span className="font-semibold">Risks:</span> {summary.risks}</div>
      <div className="text-white text-base"><span className="font-semibold">Emotional Tensions:</span> {summary.emotional_tensions}</div>
    </motion.div>
  );
}
