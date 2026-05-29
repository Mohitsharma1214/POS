import type { YoutubeResult } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function YoutubeIntelligenceSection({ youtube }: { youtube: YoutubeResult[] }) {
  if (!Array.isArray(youtube) || youtube.length === 0) {
    return <section><h3 className="text-xl font-semibold mb-4 text-white">YouTube Intelligence</h3><div className="text-gray-400 italic">No YouTube results found.</div></section>;
  }
  return (
    <section>
      <h3 className="text-xl font-semibold mb-4 text-white">YouTube Intelligence</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {youtube.map((video, i) => (
          <motion.div
            key={video.video_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08, duration: 0.5 }}
            className="bg-glass rounded-xl p-4 shadow-glass border border-white/10 flex flex-col gap-3 hover:scale-[1.03] transition-transform cursor-pointer"
          >
            <div className="relative w-full h-40 rounded-lg overflow-hidden">
              <img src={video.thumbnail_url} alt={video.title} className="object-cover w-full h-full" />
            </div>
            <div className="font-bold text-white text-base mt-2 line-clamp-2">{video.title}</div>
            <div className="text-gray-400 text-xs">{video.channel}</div>
            <div className="flex gap-2 mt-1 text-xs">
              <span className="bg-accent/20 text-accent px-2 py-1 rounded">Virality: {video.virality_estimate}</span>
              <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded">{video.format_classification}</span>
              <span className="bg-pink-500/20 text-pink-400 px-2 py-1 rounded">{video.retention_style}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
