import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/Frontend/src/components/dashboard/ResearchDashboard.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix bio
old_bio = """<p className="text-neutral-300 text-sm leading-relaxed whitespace-pre-line bg-neutral-900/40 p-5 rounded-2xl border border-neutral-900/60 shadow-inner">
                        {guestReport.enrichment?.bio || "Biographical notes unavailable."}
                      </p>"""
new_bio = """<div className="text-neutral-300 text-sm leading-relaxed bg-neutral-900/40 p-5 rounded-2xl border border-neutral-900/60 shadow-inner prose prose-invert max-w-none prose-p:mb-4">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {guestReport.enrichment?.bio || "Biographical notes unavailable."}
                        </ReactMarkdown>
                      </div>"""
content = content.replace(old_bio, new_bio)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Bio UI fixes applied successfully")
