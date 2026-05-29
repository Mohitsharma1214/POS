import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY", "")
print("Key:", api_key)

async def test_search():
    params = {
        "part": "snippet",
        "q": "Jensen Huang podcast",
        "type": "video",
        "maxResults": 5,
        "key": api_key
    }
    url = "https://www.googleapis.com/youtube/v3/search"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        print("Status code:", resp.status_code)
        print("Body:", resp.text[:1000])

asyncio.run(test_search())
