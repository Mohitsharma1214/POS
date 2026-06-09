import asyncio
import json
from dotenv import load_dotenv
load_dotenv('.env')

from app.services.tavily_signal_service import TavilySignalService

async def test():
    tavily = TavilySignalService()
    results = await tavily.search_web('Instagram Charles Hoskinson "Cardano" OR site:instagram.com "Charles Hoskinson" "Cardano"', max_results=5)
    print(json.dumps([r if isinstance(r, dict) else vars(r) for r in results], indent=2))

asyncio.run(test())
