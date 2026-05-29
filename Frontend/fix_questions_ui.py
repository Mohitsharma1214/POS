import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/Frontend/src/components/dashboard/ResearchDashboard.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_code = """                                <p className="text-xs font-bold text-neutral-100 italic leading-relaxed font-sans">
                                  "{q.question}"
                                </p>"""

new_code = """                                <p className="text-xs font-bold text-neutral-100 italic leading-relaxed font-sans">
                                  "{q.primary_question || q.question}"
                                </p>
                                {q.follow_ups && q.follow_ups.length > 0 && (
                                  <div className="mt-3 space-y-1.5 bg-neutral-900/60 p-2.5 rounded-lg border border-neutral-800/80">
                                    <span className="text-[10px] text-cyan-400/90 font-bold uppercase tracking-wider block mb-1 flex items-center gap-1.5">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 10 4 15 9 20"></polyline><path d="M20 4v7a4 4 0 0 1-4 4H4"></path></svg>
                                      Dynamic Follow-ups
                                    </span>
                                    {q.follow_ups.map((fUp: string, fIdx: number) => (
                                      <div key={fIdx} className="flex items-start gap-2 text-xs text-neutral-300">
                                        <span className="text-cyan-500/50 mt-0.5 text-[10px]">●</span>
                                        <span className="leading-relaxed">{fUp}</span>
                                      </div>
                                    ))}
                                  </div>
                                )}"""

content = content.replace(old_code, new_code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("UI update applied successfully")
