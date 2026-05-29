import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/Frontend/src/components/dashboard/ResearchDashboard.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add react-markdown import
if "import ReactMarkdown" not in content:
    content = content.replace("import React, { useState } from 'react';", "import React, { useState } from 'react';\nimport ReactMarkdown from 'react-markdown';\nimport remarkGfm from 'remark-gfm';")

# 2. Fix Executive Briefing paragraph to use ReactMarkdown
old_summary = """<p className="text-neutral-300 text-sm md:text-base leading-relaxed whitespace-pre-line">
                    {data.structured_insights.summary || "No executive summary parsed."}
                  </p>"""
new_summary = """<div className="text-neutral-300 text-sm md:text-base leading-relaxed prose prose-invert max-w-none prose-p:mb-4 prose-ul:my-2 prose-li:my-0.5">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {data.structured_insights.summary || "No executive summary parsed."}
                    </ReactMarkdown>
                  </div>"""
content = content.replace(old_summary, new_summary)

# 3. Fix main note advisory
old_main_note = """<div className="bg-neutral-950/70 border border-neutral-850 rounded-xl p-4 text-xs leading-relaxed text-neutral-300 italic mb-4">
                          "{mainNote}"
                        </div>"""
new_main_note = """<div className="bg-neutral-950/70 border border-neutral-850 rounded-xl p-4 text-xs leading-relaxed text-neutral-300 italic mb-4 prose prose-invert max-w-none">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>{mainNote}</ReactMarkdown>
                        </div>"""
content = content.replace(old_main_note, new_main_note)

# 4. Standardize Card UI across the file
# We will look for bg-neutral-950 or bg-[#xxx] and normalize to bg-neutral-900/40 border border-neutral-800 rounded-2xl p-6
# Actually let's just make sure all cards have a consistent look. 
# But maybe it's safer to just let Tailwind prose handle the markdown lists.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("UI fixes applied successfully")
