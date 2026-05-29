# app/services/models.py
"""Pipeline model hierarchy and model‑specific prompt tweaks.

Defines the ordered list of models for each pipeline stage and any
model‑specific prompt snippets that need to be appended (or prepended).
"""

PIPELINE_MODELS = {
    "step2_extraction": [
        "groq/llama-3.3-70b-versatile",               # primary
        "openrouter/free"                             # fallback for large payloads
    ],
    "step3_research": [
        "groq/llama-3.3-70b-versatile",               # primary
        "openrouter/free"                             # fallback when payload too large or throttled
    ],
    "step4_brief": [
        "groq/llama-3.3-70b-versatile",               # primary
        "openrouter/free",                            # fallback for large payloads
        "openrouter/deepseek-v4-flash:free",           # extra free fallback
        "openrouter/google/gemma-4-31b-it:free"        # another free fallback
    ],
    "step4_scoring": [
        "groq/llama-3.3-70b-versatile",               # primary
        "openrouter/free",                            # fallback for large payloads
        "openrouter/deepseek-v4-flash:free",           # extra fallback model
        "openrouter/google/gemma-4-31b-it:free"        # another fallback
    ],
    "step5_simulator": [
        "groq/llama-3.3-70b-versatile",               # primary
        "openrouter/free",                            # fallback
        "openrouter/deepseek-v4-flash:free",
        "openrouter/google/gemma-4-31b-it:free"
    ]
}
FREE_TIER_MODELS = ["gpt-3.5-turbo", "claude-instant-1"]  # default free‑tier models

# List of free model slugs for OpenRouter fallback usage
FREE_MODEL_SLUGS = [
    "deepseek/deepseek-v4-flash:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter/free",
]


# Model‑specific prompt tweaks. The value is the snippet that should be added
# to the core prompt (the function `build_prompt` in pipeline.py will handle it).
MODEL_TWEAKS = {
    "deepseek/deepseek-r1:free": """
OUTPUT RULE: After your reasoning, output ONLY raw JSON.
No markdown. No code fences. Start with { and end with }.
""",
    "qwen/qwen3-235b-a22b:free": """
/no_think
Output raw JSON only. Begin immediately with {
""",
    "groq/llama-3.3-70b-versatile": """
REMINDER: Return exactly 10 optimized_questions,
10 title_variants, 8 thumbnail_concepts,
5 hook_scripts, 8 clip_angles.
Count before responding.
""",
    "meta-llama/llama-3.3-70b-instruct:free": """
REMINDER: Return exactly 10 optimized_questions,
10 title_variants, 8 thumbnail_concepts,
5 hook_scripts, 8 clip_angles.
Count before responding.
""",
    # Gemini 2.5 Pro does not need a tweak according to the specification.
}
