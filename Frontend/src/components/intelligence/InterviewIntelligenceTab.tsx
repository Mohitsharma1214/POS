import React, { useState } from 'react';
import { Bot, RefreshCw, Send, Sparkles, MessageCircle, AlertTriangle, Activity, HelpCircle, Eye, ShieldAlert } from 'lucide-react';

interface FollowUp {
  type: string;
  question: string;
}

interface IntelligenceResponse {
  main_question: string;
  possible_guest_answer: string;
  follow_ups: FollowUp[];
}

const getTypeIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'clarification':
      return <HelpCircle className="w-5 h-5 text-blue-400" />;
    case 'contradiction':
      return <AlertTriangle className="w-5 h-5 text-red-400" />;
    case 'pressure':
      return <ShieldAlert className="w-5 h-5 text-orange-400" />;
    case 'example':
      return <Eye className="w-5 h-5 text-green-400" />;
    case 'emotional':
      return <Activity className="w-5 h-5 text-pink-400" />;
    case 'prediction':
      return <Sparkles className="w-5 h-5 text-purple-400" />;
    case 'skepticism':
      return <MessageCircle className="w-5 h-5 text-yellow-400" />;
    default:
      return <MessageCircle className="w-5 h-5 text-indigo-400" />;
  }
};

const getTypeColor = (type: string) => {
  switch (type.toLowerCase()) {
    case 'clarification': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    case 'contradiction': return 'bg-red-500/10 text-red-400 border-red-500/20';
    case 'pressure': return 'bg-orange-500/10 text-orange-400 border-orange-500/20';
    case 'example': return 'bg-green-500/10 text-green-400 border-green-500/20';
    case 'emotional': return 'bg-pink-500/10 text-pink-400 border-pink-500/20';
    case 'prediction': return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
    case 'skepticism': return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
    default: return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
  }
};

export const InterviewIntelligenceTab: React.FC = () => {
  const [mainQuestion, setMainQuestion] = useState('');
  const [guestAnswer, setGuestAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IntelligenceResponse | null>(null);
  const [error, setError] = useState('');

  const generateIntelligence = async () => {
    if (!mainQuestion.trim() || !guestAnswer.trim()) {
      setError('Please provide both a main question and a guest answer.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // In a real app we might read this from a config or env
      const baseUrl = typeof window !== 'undefined' && window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : '';
        
      const response = await fetch(`${baseUrl}/interview/intelligence`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          main_question: mainQuestion,
          possible_guest_answer: guestAnswer,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate intelligence');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while generating intelligence.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3 mb-8">
        <div className="p-3 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
          <Bot className="w-6 h-6 text-indigo-400" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Dynamic Interview Intelligence</h2>
          <p className="text-zinc-400 mt-1">Generate real-time, context-aware follow-up questions based on guest responses.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          <div className="bg-[#111111] border border-zinc-800 rounded-xl p-6 shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 blur-3xl rounded-full pointer-events-none" />
            
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <MessageCircle className="w-5 h-5 mr-2 text-zinc-400" />
              Conversation Context
            </h3>
            
            <div className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">Main Anchor Question</label>
                <textarea
                  value={mainQuestion}
                  onChange={(e) => setMainQuestion(e.target.value)}
                  placeholder="e.g. What is your stance on the future of AI regulation?"
                  className="w-full h-24 bg-zinc-900/50 border border-zinc-800 rounded-lg p-3 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-all resize-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">Guest's Response</label>
                <textarea
                  value={guestAnswer}
                  onChange={(e) => setGuestAnswer(e.target.value)}
                  placeholder="e.g. We believe regulation is necessary, but we must protect open-source innovation at all costs."
                  className="w-full h-32 bg-zinc-900/50 border border-zinc-800 rounded-lg p-3 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-all resize-none"
                />
              </div>

              {error && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400">
                  {error}
                </div>
              )}

              <button
                onClick={generateIntelligence}
                disabled={loading}
                className="w-full flex items-center justify-center space-x-2 py-3 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:hover:bg-indigo-600 text-white rounded-lg font-medium transition-all group shadow-lg shadow-indigo-500/20"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    <span>Analyzing Response...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 group-hover:scale-110 transition-transform" />
                    <span>Generate Dynamic Follow-ups</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Output Section */}
        <div className="space-y-6">
          {!result && !loading && (
            <div className="h-full min-h-[400px] flex flex-col items-center justify-center p-8 bg-zinc-900/30 border border-zinc-800/50 border-dashed rounded-xl text-center">
              <Bot className="w-12 h-12 text-zinc-700 mb-4" />
              <h3 className="text-lg font-medium text-zinc-300 mb-2">Awaiting Context</h3>
              <p className="text-zinc-500 max-w-sm">
                Enter the main question and the guest's response to generate intelligent, context-aware follow-ups tailored to their exact phrasing and claims.
              </p>
            </div>
          )}

          {loading && (
            <div className="h-full min-h-[400px] flex flex-col items-center justify-center p-8 bg-[#111111] border border-zinc-800 rounded-xl">
              <div className="relative">
                <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full animate-pulse" />
                <Bot className="w-12 h-12 text-indigo-400 animate-bounce relative z-10" />
              </div>
              <p className="text-zinc-400 mt-6 animate-pulse">Running advanced conversational analysis...</p>
            </div>
          )}

          {result && !loading && (
            <div className="bg-[#111111] border border-zinc-800 rounded-xl p-6 shadow-xl space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-lg font-semibold text-white flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-indigo-400" />
                Recommended Follow-ups
              </h3>
              
              <div className="space-y-4">
                {result.follow_ups.map((followUp, idx) => (
                  <div 
                    key={idx} 
                    className="group relative p-5 bg-zinc-900/50 border border-zinc-800 hover:border-zinc-700 rounded-xl transition-all duration-300"
                  >
                    <div className="flex items-start space-x-4">
                      <div className="mt-1">
                        {getTypeIcon(followUp.type)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full uppercase tracking-wider border ${getTypeColor(followUp.type)}`}>
                            {followUp.type}
                          </span>
                        </div>
                        <p className="text-zinc-200 text-base leading-relaxed group-hover:text-white transition-colors">
                          "{followUp.question}"
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
