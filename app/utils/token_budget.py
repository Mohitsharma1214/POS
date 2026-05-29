def estimate_token_count(text: str) -> int:
    # Simple token estimation (1 token ≈ 4 chars for English)
    return max(1, len(text) // 4)

def budget_tokens(texts, max_tokens=2048):
    # Truncate or batch texts to fit within max_tokens
    tokens = 0
    result = []
    for t in texts:
        t_tokens = estimate_token_count(t)
        if tokens + t_tokens > max_tokens:
            break
        result.append(t)
        tokens += t_tokens
    return result
