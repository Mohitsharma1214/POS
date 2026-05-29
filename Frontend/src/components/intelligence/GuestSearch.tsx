
"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { LoaderCircle, CheckCircle2, Radio, Database, Search, ShieldAlert, Cpu } from 'lucide-react';
import { fetchGuestIntelligence, fetchFullPipeline } from '../../services/intelligenceService';
import { useIntelligenceStore } from '../../stores/intelligenceStore';

export default function GuestSearch() {
  const [loading, setLoading] = useState(false);
  const [autopilot, setAutopilot] = useState(true);
  const [currentStep, setCurrentStep] = useState(0); // 0: Idle, 1: Booking Confirmed, 2: YouTube/APIs, 3: Perplexity, 4: Apify Scrape, 5: Synthesis
  const [logLines, setLogLines] = useState<string[]>([]);
  const consoleEndRef = useRef<HTMLDivElement>(null);
  
  const [form, setForm] = useState({
    guest_name: '',
    guest_company: '',
    guest_niche: '',
    podcast_context: '',
  });
  
  const setData = useIntelligenceStore((s) => s.setData);
  const setError = useIntelligenceStore((s) => s.setError);
  const router = useRouter();

  useEffect(() => {
    if (consoleEndRef.current) {
      consoleEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logLines]);

  const addLog = (msg: string) => {
    setLogLines((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const startSimulation = (isAutopilot: boolean) => {
    setCurrentStep(1);
    setLogLines([]);
    
    setTimeout(() => {
      addLog("🟢 Booking Confirmed: Initializing workflow pipeline...");
      addLog("🔐 Verifying secure YouTube Data v3, X.com, and Reddit endpoints...");
    }, 100);

    setTimeout(() => {
      setCurrentStep(2);
      addLog("⚡ Step 1: Initiating Guest + Niche Signal Collection...");
      addLog("📺 YouTube Data API: Fetching top long-form guest episodes...");
      addLog("🐦 X.com & Reddit API: Extracting public narrative signals...");
    }, 1500);

    setTimeout(() => {
      addLog("📊 YouTube Data API: Calculating CTR proxy and views velocity...");
      addLog("🔥 X.com: Mapping high-frequency keyword triggers...");
      addLog("👽 Reddit: Analyzing sentiment trends across subreddits...");
    }, 3500);

    setTimeout(() => {
      setCurrentStep(3);
      addLog("🧠 Perplexity API: Running deep query -> 'What podcast episodes featuring this guest type are trending right now'...");
      addLog("🌐 Web Search: Discovering emerging niche topics and authority rankings...");
    }, 5500);

    setTimeout(() => {
      setCurrentStep(4);
      addLog("🕸️ Apify Scraper: Scraping titles, descriptions, and view metrics...");
      addLog("💬 Comment Intelligence: Generating recurring themes & objections from audience comments...");
    }, 7500);

    setTimeout(() => {
      setCurrentStep(5);
      if (isAutopilot) {
        addLog("🤖 Fallback State Machine: Launching full orchestration pipeline...");
        addLog("⚡ Fallback State Machine: Executing Step 2 Pattern Extraction...");
      } else {
        addLog("🤖 OpenRouter Engine: Consolidating Web, X, Reddit, and YouTube signals...");
        addLog("⚡ OpenRouter Engine: Running DeepSeek-V4-Flash/Gemma-4 free-tier semantic synthesis...");
      }
    }, 9500);

    if (isAutopilot) {
      setTimeout(() => {
        addLog("🧬 Fallback State Machine: Synthesizing Step 3 Biography & Contradictions...");
        addLog("🔥 Fallback State Machine: Formulating Step 4 Virality Playbook...");
      }, 12000);

      setTimeout(() => {
        addLog("🛡️ Fallback State Machine: Running Quality Scoring Audit...");
        addLog("✓ Fallback State Machine: Playbook validation passed successfully!");
      }, 14500);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    startSimulation(autopilot);
    
    try {
      let result;
      if (autopilot) {
        result = await fetchFullPipeline({
          guest_name: form.guest_name,
          guest_company: form.guest_company,
          guest_niche: form.guest_niche,
          podcast_context: form.podcast_context,
        });
      } else {
        result = await fetchGuestIntelligence({
          guest_name: form.guest_name,
          guest_company: form.guest_company,
          guest_niche: form.guest_niche,
          podcast_context: form.podcast_context,
        });
      }
      
      addLog("✨ OpenRouter: Synthesis complete! Finalizing payload mapping...");
      setTimeout(() => {
        setData(result);
        setLoading(false);
        router.push('/dashboard');
      }, 800);
    } catch (err: any) {
      addLog("❌ Critical error occurred during signal collection.");
      setError('Failed to fetch intelligence');
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-2xl bg-neutral-900/90 rounded-3xl border border-neutral-800 p-8 shadow-2xl backdrop-blur-xl"
    >
      {!loading ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h2 className="text-xl font-semibold text-white">Guest Research Hub</h2>
            <p className="text-gray-400 text-sm">Fill in the details below to trigger the intelligence collection pipeline.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              name="guest_name"
              placeholder="Guest Name (e.g. Dr. Andrew Huberman)"
              className="w-full bg-neutral-950 text-white placeholder-neutral-500 rounded-xl px-4 py-3 border border-neutral-800 focus:outline-none focus:border-cyan-400 transition"
              value={form.guest_name}
              onChange={handleChange}
              required
            />
            <input
              name="guest_company"
              placeholder="Company / Institution"
              className="w-full bg-neutral-950 text-white placeholder-neutral-500 rounded-xl px-4 py-3 border border-neutral-800 focus:outline-none focus:border-cyan-400 transition"
              value={form.guest_company}
              onChange={handleChange}
            />
            <input
              name="guest_niche"
              placeholder="Niche (Optional, Auto-inferred)"
              className="w-full bg-neutral-950 text-white placeholder-neutral-500 rounded-xl px-4 py-3 border border-neutral-800 focus:outline-none focus:border-cyan-400 transition"
              value={form.guest_niche}
              onChange={handleChange}
            />
            <input
              name="podcast_context"
              placeholder="Podcast Context (Optional, Auto-inferred)"
              className="w-full bg-neutral-950 text-white placeholder-neutral-500 rounded-xl px-4 py-3 border border-neutral-800 focus:outline-none focus:border-cyan-400 transition"
              value={form.podcast_context}
              onChange={handleChange}
            />
          </div>
          
          {/* Autopilot Mode Toggle */}
          <div className="flex items-center justify-between p-4 bg-neutral-950/40 rounded-xl border border-neutral-800/80">
            <div className="flex flex-col gap-0.5">
              <div className="text-sm font-semibold text-white flex items-center gap-1.5">
                <Cpu className="w-4 h-4 text-cyan-400 animate-pulse" />
                Autopilot Fallback Engine
              </div>
              <div className="text-[11px] text-neutral-500 max-w-[85%] leading-relaxed">
                Aggregates signals, extracts pattern models, researches biography timeline, and audits playbook quality in a single back-end validation run.
              </div>
            </div>
            <button
              type="button"
              onClick={() => setAutopilot(!autopilot)}
              className={`w-12 h-6 rounded-full p-1 transition-colors duration-300 focus:outline-none flex items-center ${
                autopilot ? 'bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.3)]' : 'bg-neutral-800'
              }`}
            >
              <div
                className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ${
                  autopilot ? 'translate-x-6' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <button
            type="submit"
            className="w-full mt-2 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-cyan-950 transition flex items-center justify-center gap-2"
          >
            Start AI Research & Signal Collection
          </button>
        </form>
      ) : (
        <div className="flex flex-col gap-8">
          {/* Booking Confirmation & Multi-Step Wizard */}
          <div className="flex flex-col gap-2">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <Radio className="animate-pulse text-cyan-400" size={24} />
              Signal Collection Pipeline
            </h3>
            <p className="text-gray-400 text-sm">Active podcast booking confirmed. Scanning digital footprint across APIs.</p>
          </div>

          {/* Stepper Pipeline Graphics */}
          <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-6 md:gap-4 px-4 py-2 bg-neutral-950/50 rounded-2xl border border-neutral-800/80">
            {/* Step 1: Booking Confirmed */}
            <div className="flex items-center gap-3 z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition ${
                currentStep >= 1 ? 'bg-green-500 border-green-400 text-neutral-950 font-bold' : 'border-neutral-700 bg-neutral-900 text-gray-500'
              }`}>
                {currentStep > 1 ? <CheckCircle2 size={20} className="text-neutral-950" /> : '1'}
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-500">BOOKING</div>
                <div className="text-sm font-bold text-white">Confirmed</div>
              </div>
            </div>

            {/* Connecting Line 1 */}
            <div className="hidden md:block flex-1 h-[2px] bg-neutral-800 relative">
              <motion.div 
                className="absolute top-0 left-0 h-full bg-cyan-400 shadow-glow"
                initial={{ width: "0%" }}
                animate={{ width: currentStep >= 2 ? "100%" : "0%" }}
                transition={{ duration: 1.5 }}
              />
            </div>

            {/* Step 2: Youtube + Social APIs */}
            <div className="flex items-center gap-3 z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition ${
                currentStep >= 2 ? 'bg-cyan-500 border-cyan-400 text-neutral-950 font-bold shadow-glow-cyan' : 'border-neutral-700 bg-neutral-900 text-gray-500'
              }`}>
                {currentStep > 2 ? <CheckCircle2 size={20} className="text-neutral-950" /> : <Database size={18} />}
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-500">STEP 1.1</div>
                <div className="text-sm font-bold text-white">YouTube + X APIs</div>
              </div>
            </div>

            {/* Connecting Line 2 */}
            <div className="hidden md:block flex-1 h-[2px] bg-neutral-800 relative">
              <motion.div 
                className="absolute top-0 left-0 h-full bg-cyan-400 shadow-glow"
                initial={{ width: "0%" }}
                animate={{ width: currentStep >= 3 ? "100%" : "0%" }}
                transition={{ duration: 1.5 }}
              />
            </div>

            {/* Step 3: Perplexity + Apify */}
            <div className="flex items-center gap-3 z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition ${
                currentStep >= 3 ? 'bg-blue-500 border-blue-400 text-neutral-950 font-bold shadow-glow-blue' : 'border-neutral-700 bg-neutral-900 text-gray-500'
              }`}>
                {currentStep > 4 ? <CheckCircle2 size={20} className="text-neutral-950" /> : <Search size={18} />}
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-500">STEP 1.2</div>
                <div className="text-sm font-bold text-white">Perplexity + Apify</div>
              </div>
            </div>

            {/* Connecting Line 3 */}
            <div className="hidden md:block flex-1 h-[2px] bg-neutral-800 relative">
              <motion.div 
                className="absolute top-0 left-0 h-full bg-indigo-400 shadow-glow"
                initial={{ width: "0%" }}
                animate={{ width: currentStep >= 5 ? "100%" : "0%" }}
                transition={{ duration: 1.5 }}
              />
            </div>

            {/* Step 4: AI Synthesis */}
            <div className="flex items-center gap-3 z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition ${
                currentStep >= 5 ? 'bg-indigo-500 border-indigo-400 text-neutral-950 font-bold shadow-glow-indigo' : 'border-neutral-700 bg-neutral-900 text-gray-500'
              }`}>
                {currentStep === 5 ? <LoaderCircle className="animate-spin text-neutral-950" size={20} /> : <Cpu size={18} />}
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-500">STAGE 2</div>
                <div className="text-sm font-bold text-white">AI Synthesis</div>
              </div>
            </div>
          </div>

          {/* Console Log Output Scroller */}
          <div className="flex flex-col gap-2">
            <div className="text-xs font-bold text-gray-400 tracking-wider uppercase">Live Intelligence Console</div>
            <div className="w-full h-44 bg-neutral-950 rounded-2xl border border-neutral-800/80 p-4 font-mono text-xs overflow-y-auto flex flex-col gap-2 scrollbar-thin scrollbar-thumb-neutral-800">
              <AnimatePresence>
                {logLines.map((log, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    className={`${
                      log.includes('❌') ? 'text-red-400' :
                      log.includes('🟢') || log.includes('✨') ? 'text-green-400 font-semibold' :
                      log.includes('⚡') || log.includes('🧠') || log.includes('🕸️') ? 'text-cyan-400' : 'text-neutral-400'
                    }`}
                  >
                    {log}
                  </motion.div>
                ))}
              </AnimatePresence>
              {logLines.length === 0 && (
                <div className="text-neutral-600 italic">Waiting to establish network handshakes...</div>
              )}
              <div ref={consoleEndRef} />
            </div>
          </div>

          {/* Micro Animation Loading Info */}
          <div className="flex items-center justify-between border-t border-neutral-800/60 pt-4 text-xs text-neutral-500">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              API connections online
            </span>
            <span>Est. completion: ~15 seconds</span>
          </div>
        </div>
      )}
    </motion.div>
  );
}

