import type { GuestProfile } from '../../types/intelligence';
import { motion } from 'framer-motion';

export default function GuestOverviewCard({ guest }: { guest: GuestProfile }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="bg-glass rounded-2xl shadow-glass p-8 flex flex-col gap-4 backdrop-blur-md border border-white/10"
    >
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white mb-1">{guest.name}</h2>
          <div className="text-accent font-semibold">{guest.company}</div>
          <div className="text-gray-400 text-sm">{guest.niche}</div>
        </div>
        <div className="text-right md:text-left">
          <div className="text-gray-300 text-base font-medium">{guest.public_positioning}</div>
        </div>
      </div>
      <div className="mt-4 text-lg text-gray-200 italic border-l-4 border-accent pl-4">
        {guest.narrative}
      </div>
    </motion.div>
  );
}
