# Podcast Guest Research Infrastructure

## Overview
A modular, async-first backend system to research podcast guests using web and YouTube search. Built with FastAPI, Tavily API, and YouTube Data API v3.

---

## Features
- Accepts guest info via API
- Generates intelligent search queries
- Aggregates Tavily and YouTube results
- Returns structured research intelligence
- Async, modular, production-grade code

---

## Project Structure
```
podcast-intelligence/
│
├── app/
│   ├── api/
│   │   └── routes/
│   ├── agents/
│   ├── services/
│   ├── aggregators/
│   ├── schemas/
│   ├── config/
│   ├── utils/
│   └── main.py
├── tests/
├── .env.example
├── requirements.txt
├── README.md
```

---

## Setup Instructions

1. **Clone the repo**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Add your Tavily and YouTube API keys
   - Add your OpenRouter API key for semantic intelligence (see https://openrouter.ai/)
     - `OPENROUTER_API_KEY=your_openrouter_api_key_here`
4. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## API Usage

### Endpoint
`POST /research/guest`

#### Request Example
```
{
  "guest_name": "Sam Altman",
  "guest_company": "OpenAI",
  "guest_niche": "Artificial Intelligence",
  "podcast_context": "AI startup podcast"
}
```

#### Response Example
```
{
  "guest": {
    "name": "Sam Altman",
    "company": "OpenAI",
    "niche": "Artificial Intelligence"
  },
  "research_metadata": {
    "generated_at": "2024-05-20T12:00:00Z",
    "queries_used": [
      "Sam Altman podcast",
      "Sam Altman interview",
      "Sam Altman latest news"
    ],
    "sources_count": 7
  },
  "web_results": [
    {
      "title": "Sam Altman on AI",
      "url": "https://example.com/sam-altman-ai",
      "snippet": "Sam Altman discusses AI...",
      "source": "example.com",
      "content_type": "article"
    }
  ],
  "youtube_results": [
    {
      "title": "Sam Altman Interview",
      "channel": "Lex Fridman Podcast",
      "published_at": "2023-11-01T00:00:00Z",
      "video_url": "https://youtube.com/watch?v=abc123",
      "description": "Lex interviews Sam Altman...",
      "thumbnail_url": "https://img.youtube.com/vi/abc123/default.jpg"
    }
  ]
}
```

---

## Intelligence Output Example
```
"intelligence": {
  "dominant_topics": [
    "AI and Human Cognition",
    "Startup Leadership",
    "Health Optimization Protocols"
  ],
  "high_signal_topics": [
    "dopamine optimization",
    "sleep protocols",
    "motivation neuroscience"
  ],
  "controversies": [
    {
      "topic": "AI safety debates",
      "severity": "high",
      "summary": "Ongoing debates about the risks and regulation of advanced AI systems.",
      "sources": ["https://example.com/ai-safety"]
    }
  ],
  "public_positioning": [
    "AI thought leader",
    "Startup mentor"
  ],
  "emerging_topics": [
    "AI for health",
    "Founder mental health"
  ],
  "discussion_patterns": [
    "performance optimization",
    "founder mindset"
  ],
  "podcast_patterns": [
    "long-form interviews",
    "technical deep dives"
  ],
  "interesting_angles": [
    "How neuroscience became mainstream self-improvement"
  ],
  "guest_narrative": "Sam Altman is positioned as a leading voice in AI, startup leadership, and health optimization.",
  "research_summary": "Sam Altman is a frequent guest on top podcasts, discussing AI, startups, and health. Recent narratives focus on AI safety, founder resilience, and the future of technology."
}
```

---

## Architecture
- **Guest Input Layer**: Validates and normalizes guest info, triggers research
- **Guest Research Agent**: Generates queries, coordinates web/YouTube search
- **Web Search Infrastructure**: Tavily and YouTube async services, aggregation, deduplication

---

## Extensibility
- Add transcript analysis, virality scoring, vector DBs, RAG, etc. by extending agents/services/aggregators

---

## License
MIT
