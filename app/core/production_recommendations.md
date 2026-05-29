# Production Recommendations

- Use Redis or similar for distributed caching in production.
- Use a production-grade async task queue (e.g., Celery with Redis, or FastAPI background tasks for lightweight jobs).
- Monitor OpenRouter rate limits and switch models or batch requests as needed.
- Use structured logging and error monitoring (e.g., Sentry).
- Add metrics for API usage, token consumption, and latency.
- Use environment variables for all API keys and sensitive configs.
- Write integration tests for all service layers.
- Document all prompt templates and LLM usage patterns.
