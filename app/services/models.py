# app/services/models.py
"""Pipeline model hierarchy and model‑specific prompt tweaks.

Defines the ordered list of models for each pipeline stage and any
model‑specific prompt snippets that need to be appended (or prepended).
"""

PIPELINE_MODELS = {
    "step2_extraction": [
        "claude-3-5-sonnet-20241022",                 # primary
        "claude-3-5-haiku-20241022"                   # fallback
    ],
    "step3_research": [
        "claude-3-5-sonnet-20241022",                 # primary
        "claude-3-5-haiku-20241022"                   # fallback
    ],
    "step4_brief": [
        "claude-3-5-sonnet-20241022",                 # primary
        "claude-3-5-haiku-20241022"                   # fallback
    ],
    "step4_scoring": [
        "claude-3-5-sonnet-20241022",                 # primary
        "claude-3-5-haiku-20241022"                   # fallback
    ],
    "step5_simulator": [
        "claude-3-5-sonnet-20241022",                 # primary
        "claude-3-5-haiku-20241022"                   # fallback
    ]
}
FREE_TIER_MODELS = ["gpt-3.5-turbo", "claude-instant-1"]  # default free‑tier models

# List of free model slugs for OpenRouter fallback usage
FREE_MODEL_SLUGS = [
    "claude-3-5-haiku-20241022"
]


# Model‑specific prompt tweaks. The value is the snippet that should be added
# to the core prompt (the function `build_prompt` in pipeline.py will handle it).
MODEL_TWEAKS = {
}
