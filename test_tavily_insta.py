import asyncio
from app.services.tavily_signal_service import TavilySignalService

async def main():
    service = TavilySignalService()
    results = await service.search_web('site:instagram.com "Anthony Scaramucci"')
    for r in results:
        print(f"TITLE: {r.title}")
        print(f"SNIPPET: {r.snippet}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
