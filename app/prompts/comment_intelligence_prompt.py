# Prompt for extracting comment intelligence using OpenRouter

from app.schemas.signal_collection_schema import YouTubeCommentIntelligence
import json

async def extract_comment_intelligence(comment_threads, openrouter_service):
    prompt = (
        "Analyze the following YouTube comment threads for each video. "
        "For each video, extract: top comments, repeated audience reactions, emotional reactions, recurring questions, controversial reactions, "
        "and infer emotional themes, audience psychology, trust signals, skepticism, curiosity, outrage, inspiration, and fear. "
        "Return a JSON list of objects, one per video, matching the YouTubeCommentIntelligence schema.\n\n"
    )
    for thread in comment_threads:
        prompt += f"Video ID: {thread['video_id']}\n"
        for c in thread['comments'][:10]:
            prompt += f"- {c['author']}: {c['text']} (Likes: {c['likeCount']})\n"
        prompt += "\n"
    response = await openrouter_service.complete(prompt)
    # Try to parse the response as a list of YouTubeCommentIntelligence
    try:
        parsed = json.loads(response) if isinstance(response, str) else response
        return [YouTubeCommentIntelligence(**item) for item in parsed]
    except Exception:
        return []
