"use client";

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GuestSearch from '../intelligence/GuestSearch';
import {
  Sparkles, Play, MessageCircle, Globe, Zap,
  User, Flame, Heart, Twitter, ArrowRight,
  Brain, Radio, Database, BarChart2, Layers,
  ChevronDown, Star, Shield, Activity
} from 'lucide-react';

const MODULES = [
  {
    id: 'strategic',
    icon: Sparkles,
    color: 'cyan',
    gradient: 'from-cyan-500/20 to-cyan-500/5',
    border: 'border-cyan-500/30',
    iconColor: 'text-cyan-400',
    glowColor: 'shadow-cyan-500/20',
    badge: 'Step 1',
    title: 'Strategic Intelligence',
    description: 'Executive briefing, viral anchor topics, host advisory notes, and audience demand metrics computed from YouTube & web signals.',
    features: ['Executive Bio & Core Thesis', 'Viral Anchor Topics', 'Host Advisory Notes', 'Strategic Content Angles'],
  },
  {
    id: 'videos',
    icon: Play,
    color: 'blue',
    gradient: 'from-blue-500/20 to-blue-500/5',
    border: 'border-blue-500/30',
    iconColor: 'text-blue-400',
    glowColor: 'shadow-blue-500/20',
    badge: 'Step 1',
    title: 'Niche Video Library',
    description: 'Top-performing guest episodes and niche videos ranked by views, engagement score, CTR proxy, and growth velocity.',
    features: ['Top Guest Appearances', 'Niche Video Rankings', 'Engagement Score Matrix', 'CTR & Velocity Proxies'],
  },
  {
    id: 'comments',
    icon: MessageCircle,
    color: 'emerald',
    gradient: 'from-emerald-500/20 to-emerald-500/5',
    border: 'border-emerald-500/30',
    iconColor: 'text-emerald-400',
    glowColor: 'shadow-emerald-500/20',
    badge: 'Step 1',
    title: 'Audience & Theme Mining',
    description: 'Deep comment intelligence: recurring objections, hidden demand signals, commenter questions, and viral moment detection.',
    features: ['Recurring Objections', 'Hidden Demand Signals', 'Commenter Questions', 'Viral Moment Detection'],
  },
  {
    id: 'social',
    icon: Globe,
    color: 'purple',
    gradient: 'from-purple-500/20 to-purple-500/5',
    border: 'border-purple-500/30',
    iconColor: 'text-purple-400',
    glowColor: 'shadow-purple-500/20',
    badge: 'Step 1',
    title: 'Social & Web Narratives',
    description: 'Reddit community sentiment, cross-platform web signals, controversy scores, and brand risk vectors from Tavily search.',
    features: ['Reddit Discussions', 'Web Signal Explorer', 'Controversy Scoring', 'Brand Risk Vectors'],
  },
  {
    id: 'patterns',
    icon: Zap,
    color: 'cyan',
    gradient: 'from-indigo-500/20 to-cyan-500/5',
    border: 'border-indigo-500/30',
    iconColor: 'text-indigo-400',
    glowColor: 'shadow-indigo-500/20',
    badge: 'Step 2',
    title: 'Creative Patterns',
    description: 'AI-extracted title formulas, thumbnail patterns, hook structures, question styles, and audience-retention clip bait moments.',
    features: ['Title Formula Extraction', 'Hook Structure Analysis', 'Thumbnail Patterns', 'Clip Bait Moments'],
  },
  {
    id: 'guest',
    icon: User,
    color: 'emerald',
    gradient: 'from-emerald-500/20 to-teal-500/5',
    border: 'border-emerald-500/30',
    iconColor: 'text-emerald-400',
    glowColor: 'shadow-emerald-500/20',
    badge: 'Step 3',
    title: 'Guest Deep-Dive',
    description: 'Live-researched biography timeline, covered vs untapped angles, public stances, and contradictions extracted from real transcripts.',
    features: ['Biography Timeline', 'Covered vs Untapped Angles', 'Public Stances & Quotes', 'Career Contradictions'],
    highlight: true,
  },
  {
    id: 'virality',
    icon: Flame,
    color: 'orange',
    gradient: 'from-orange-500/20 to-red-500/5',
    border: 'border-orange-500/30',
    iconColor: 'text-orange-400',
    glowColor: 'shadow-orange-500/20',
    badge: 'Step 4',
    title: 'Virality Playbook',
    description: 'Full virality brief: 10 optimised questions, 10 title variants, 8 thumbnail concepts, 5 hook scripts, and a content calendar.',
    features: ['Optimised Interview Questions', 'High-CTR Title Variants', 'Thumbnail Concepts', 'Content Calendar'],
    highlight: true,
  },
  {
    id: 'instagram',
    icon: Heart,
    color: 'pink',
    gradient: 'from-pink-500/20 to-rose-500/5',
    border: 'border-pink-500/30',
    iconColor: 'text-pink-400',
    glowColor: 'shadow-pink-500/20',
    badge: 'Social',
    title: 'Instagram Intel',
    description: 'Instagram signal analysis: viral themes, audience sentiment, and persona delta comparing Instagram persona vs podcast persona.',
    features: ['Viral Theme Extraction', 'Audience Sentiment', 'Persona Delta Analysis', 'Platform Crossover Signals'],
  },
  {
    id: 'twitter',
    icon: Twitter,
    color: 'sky',
    gradient: 'from-sky-500/20 to-blue-500/5',
    border: 'border-sky-500/30',
    iconColor: 'text-sky-400',
    glowColor: 'shadow-sky-500/20',
    badge: 'Social',
    title: 'X (Twitter) Intel',
    description: 'Real-time tweet analysis, engagement scoring, hashtag trends, and narrative tracking across the X (formerly Twitter) platform.',
    features: ['Tweet Engagement Scoring', 'Hashtag Trend Tracking', 'Narrative Analysis', 'Real-time Signal Feed'],
  },
];

const PIPELINE_STEPS = [
  { icon: Database, label: 'Signal Collection', sub: 'YouTube · Reddit · X · Tavily', color: 'text-cyan-400', step: '01' },
  { icon: Brain, label: 'Pattern Extraction', sub: 'Claude AI / OpenRouter', color: 'text-indigo-400', step: '02' },
  { icon: User, label: 'Guest Intelligence', sub: 'Transcripts · Web Research', color: 'text-emerald-400', step: '03' },
  { icon: Flame, label: 'Virality Brief', sub: 'Questions · Titles · Hooks', color: 'text-orange-400', step: '04' },
  { icon: Shield, label: 'Human Review', sub: 'Final Approval & Export', color: 'text-purple-400', step: '05' },
];

const colorMap: Record<string, string> = {
  cyan: 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400',
  blue: 'bg-blue-500/10 border-blue-500/20 text-blue-400',
  emerald: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400',
  purple: 'bg-purple-500/10 border-purple-500/20 text-purple-400',
  indigo: 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400',
  orange: 'bg-orange-500/10 border-orange-500/20 text-orange-400',
  pink: 'bg-pink-500/10 border-pink-500/20 text-pink-400',
  sky: 'bg-sky-500/10 border-sky-500/20 text-sky-400',
};

export default function LandingPage() {
  const [showSearch, setShowSearch] = useState(false);
  const [hoveredModule, setHoveredModule] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-[#090a0f] text-white font-sans overflow-x-hidden">

      {/* ── Ambient background glows ────────────────────────────────────── */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-cyan-500/5 rounded-full blur-[120px]" />
        <div className="absolute top-[30%] right-[-15%] w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] left-[30%] w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-[80px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-12">

        {/* ── HERO ──────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="text-center mb-16"
        >
          {/* Live badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-4 py-2 rounded-full text-xs font-bold tracking-widest uppercase mb-6"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            AI Pipeline · 5-Step Automated Intelligence Engine
          </motion.div>

          <h1 className="text-5xl md:text-7xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-neutral-200 to-neutral-500 leading-[1.05] mb-6">
            Podcast Intelligence<br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-indigo-400">
              Command Center
            </span>
          </h1>

          <p className="text-lg md:text-xl text-neutral-400 max-w-3xl mx-auto leading-relaxed mb-10">
            A fully automated guest research pipeline — from booking confirmation to a complete
            virality brief. 9 intelligence modules, real transcript analysis, and AI-synthesised
            questions built from live data.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => setShowSearch(true)}
              className="bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-white font-bold px-8 py-4 rounded-2xl shadow-lg shadow-cyan-950/50 flex items-center gap-3 text-base transition-all"
            >
              <Radio className="w-5 h-5 animate-pulse" />
              Start Guest Research
              <ArrowRight className="w-4 h-4" />
            </motion.button>
            <button
              onClick={() => document.getElementById('modules')?.scrollIntoView({ behavior: 'smooth' })}
              className="text-neutral-400 hover:text-white border border-neutral-800 hover:border-neutral-600 px-8 py-4 rounded-2xl font-semibold text-base flex items-center gap-2 transition-all"
            >
              Explore Modules
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>
        </motion.div>

        {/* ── PIPELINE STEPS BAR ────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="relative bg-neutral-900/60 border border-neutral-800/80 rounded-3xl p-6 mb-16 backdrop-blur-xl overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/3 via-transparent to-purple-500/3 pointer-events-none" />
          <div className="text-[10px] font-bold text-neutral-500 tracking-widest uppercase text-center mb-6 flex items-center justify-center gap-2">
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
            Automated 5-Step Research Pipeline
          </div>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {PIPELINE_STEPS.map((step, i) => {
              const Icon = step.icon;
              return (
                <div key={i} className="relative flex flex-col items-center text-center gap-2 group">
                  {i < PIPELINE_STEPS.length - 1 && (
                    <div className="hidden md:block absolute top-5 left-[calc(50%+22px)] right-[-50%] h-[1px] bg-gradient-to-r from-neutral-700 to-transparent z-0" />
                  )}
                  <div className={`relative z-10 w-11 h-11 rounded-xl bg-neutral-950 border border-neutral-800 group-hover:border-neutral-600 flex items-center justify-center transition-all shadow-sm`}>
                    <Icon className={`w-5 h-5 ${step.color}`} />
                  </div>
                  <div className="text-[9px] font-black text-neutral-600 tracking-widest">STEP {step.step}</div>
                  <div className="text-xs font-bold text-white leading-tight">{step.label}</div>
                  <div className="text-[10px] text-neutral-500 leading-tight">{step.sub}</div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* ── SEARCH PANEL (slide in) ───────────────────────────────────── */}
        <AnimatePresence>
          {showSearch && (
            <motion.div
              id="search"
              key="search"
              initial={{ opacity: 0, height: 0, marginBottom: 0 }}
              animate={{ opacity: 1, height: 'auto', marginBottom: 64 }}
              exit={{ opacity: 0, height: 0, marginBottom: 0 }}
              transition={{ duration: 0.5, ease: 'easeInOut' }}
              className="overflow-hidden"
            >
              <div className="flex justify-center">
                <div className="w-full max-w-2xl">
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-sm font-semibold text-neutral-400 flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-cyan-400" />
                      Guest Research Hub
                    </div>
                    <button
                      onClick={() => setShowSearch(false)}
                      className="text-neutral-600 hover:text-neutral-400 text-xs transition"
                    >
                      Collapse ↑
                    </button>
                  </div>
                  <GuestSearch />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── MODULE GRID ───────────────────────────────────────────────── */}
        <div id="modules">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="flex items-center justify-between mb-8"
          >
            <div>
              <h2 className="text-2xl md:text-3xl font-black text-white">Intelligence Modules</h2>
              <p className="text-neutral-500 text-sm mt-1">
                9 modules across 5 pipeline stages — all accessible from the dashboard after research runs.
              </p>
            </div>
            <span className="hidden md:flex items-center gap-2 text-xs text-neutral-500 border border-neutral-800 px-3 py-1.5 rounded-full">
              <Layers className="w-3.5 h-3.5 text-indigo-400" />
              {MODULES.length} Modules
            </span>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {MODULES.map((mod, i) => {
              const Icon = mod.icon;
              const badgeStyle = colorMap[mod.color] || colorMap.cyan;
              const isHovered = hoveredModule === mod.id;
              return (
                <motion.div
                  key={mod.id}
                  initial={{ opacity: 0, y: 24 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * i, duration: 0.5 }}
                  onMouseEnter={() => setHoveredModule(mod.id)}
                  onMouseLeave={() => setHoveredModule(null)}
                  onClick={() => setShowSearch(true)}
                  className={`relative group cursor-pointer rounded-2xl border bg-gradient-to-br ${mod.gradient} ${mod.border} p-6 transition-all duration-300 overflow-hidden
                    ${isHovered ? `shadow-xl ${mod.glowColor} shadow-lg` : 'shadow-sm'}
                    ${mod.highlight ? 'ring-1 ring-white/5' : ''}
                  `}
                >
                  {/* Highlight glow for Step 3 & 4 */}
                  {mod.highlight && (
                    <div className={`absolute -top-px left-0 right-0 h-[2px] bg-gradient-to-r ${
                      mod.color === 'orange' ? 'from-orange-500 to-red-500' : 'from-emerald-500 to-teal-500'
                    }`} />
                  )}

                  {/* Hover shimmer */}
                  <div className={`absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none rounded-2xl`} />

                  <div className="relative z-10">
                    {/* Header row */}
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-11 h-11 rounded-xl flex items-center justify-center border ${mod.border} bg-neutral-950/60`}>
                        <Icon className={`w-5 h-5 ${mod.iconColor}`} />
                      </div>
                      <div className="flex items-center gap-2">
                        {mod.highlight && (
                          <span className="flex items-center gap-1 text-[9px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full uppercase tracking-wider">
                            <Star className="w-2.5 h-2.5" /> New
                          </span>
                        )}
                        <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full border ${badgeStyle}`}>
                          {mod.badge}
                        </span>
                      </div>
                    </div>

                    {/* Title & description */}
                    <h3 className="text-base font-bold text-white mb-2 group-hover:text-white transition-colors">
                      {mod.title}
                    </h3>
                    <p className="text-xs text-neutral-400 leading-relaxed mb-4">
                      {mod.description}
                    </p>

                    {/* Feature list */}
                    <ul className="space-y-1.5 mb-4">
                      {mod.features.map((f, fi) => (
                        <li key={fi} className="flex items-center gap-2 text-[11px] text-neutral-400">
                          <span className={`w-1 h-1 rounded-full flex-shrink-0 ${mod.iconColor.replace('text-', 'bg-')}`} />
                          {f}
                        </li>
                      ))}
                    </ul>

                    {/* CTA hint */}
                    <div className={`flex items-center gap-1.5 text-[11px] font-semibold ${mod.iconColor} opacity-0 group-hover:opacity-100 transition-all duration-200`}>
                      Run research to access
                      <ArrowRight className="w-3 h-3" />
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* ── STATS BAR ─────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.6 }}
          className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {[
            { label: 'Intelligence Modules', value: '9', icon: Layers, color: 'text-cyan-400' },
            { label: 'Pipeline Steps', value: '5', icon: Activity, color: 'text-indigo-400' },
            { label: 'Data Sources', value: '7+', icon: Database, color: 'text-emerald-400' },
            { label: 'AI Engine', value: 'OpenRouter', icon: Brain, color: 'text-purple-400' },
          ].map((stat, i) => {
            const Icon = stat.icon;
            return (
              <div key={i} className="bg-neutral-900/50 border border-neutral-800/60 rounded-2xl p-5 flex items-center gap-4">
                <div className="w-10 h-10 rounded-xl bg-neutral-950 border border-neutral-800 flex items-center justify-center flex-shrink-0">
                  <Icon className={`w-4.5 h-4.5 ${stat.color}`} />
                </div>
                <div>
                  <div className="text-xl font-black text-white">{stat.value}</div>
                  <div className="text-[10px] text-neutral-500 font-medium uppercase tracking-wider">{stat.label}</div>
                </div>
              </div>
            );
          })}
        </motion.div>

        {/* ── FOOTER CTA ────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4 }}
          className="mt-16 text-center py-12 border-t border-neutral-900"
        >
          <p className="text-neutral-600 text-sm mb-4">
            Ready to analyse your next guest?
          </p>
          <motion.button
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => { setShowSearch(true); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            className="bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-white font-bold px-10 py-4 rounded-2xl shadow-lg shadow-cyan-950/40 flex items-center gap-3 mx-auto text-base transition-all"
          >
            <Radio className="w-5 h-5" />
            Launch Intelligence Pipeline
            <ArrowRight className="w-4 h-4" />
          </motion.button>
          <p className="text-neutral-700 text-xs mt-6">
            Podcast Intelligence Command Center · Powered by YouTube API · Tavily · OpenRouter
          </p>
        </motion.div>

      </div>
    </main>
  );
}
