import re

file_path = "e:/Youtube-Transcriptors/podcast-intelligence/Frontend/src/components/dashboard/ResearchDashboard.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Normalize text sizes
content = re.sub(r'text-\[9px\]', 'text-xs', content)
content = re.sub(r'text-\[10px\]', 'text-xs', content)
content = re.sub(r'text-\[11px\]', 'text-xs', content)
content = re.sub(r'text-\[13px\]', 'text-sm', content)

# Normalize non-standard colors
content = re.sub(r'text-neutral-350', 'text-neutral-300', content)
content = re.sub(r'text-neutral-355', 'text-neutral-400', content)
content = re.sub(r'text-neutral-450', 'text-neutral-400', content)
content = re.sub(r'text-neutral-455', 'text-neutral-400', content)
content = re.sub(r'text-orange-505', 'text-orange-500', content)
content = re.sub(r'text-red-550', 'text-red-500', content)
content = re.sub(r'text-red-650', 'text-red-600', content)
content = re.sub(r'bg-neutral-950', 'bg-neutral-900', content)
content = re.sub(r'border-neutral-850', 'border-neutral-800', content)

# Normalize shadow glows
content = re.sub(r'shadow-glow-[a-z]+', 'shadow-lg', content)

# Replace all messy background cards with a standard, clean look
content = re.sub(r'bg-neutral-900/\d+ border border-neutral-900', 'bg-neutral-900/50 border border-neutral-800/60 backdrop-blur-sm', content)
content = re.sub(r'bg-neutral-900 border border-neutral-900', 'bg-neutral-900/50 border border-neutral-800/60 backdrop-blur-sm', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("UI CSS fixes applied successfully")
