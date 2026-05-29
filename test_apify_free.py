import os
import asyncio
from dotenv import load_dotenv
from apify_client import ApifyClientAsync

async def main():
    load_dotenv()
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        print("NO TOKEN")
        return
    client = ApifyClientAsync(token)
    
    run_input = {
        "searchTerms": ["Charles Hoskinson"],
        "maxItems": 2,
        "sort": "Latest"
    }
    
    print(f"Starting run with quacker/twitter-scraper...")
    try:
        run = await client.actor("quacker/twitter-scraper").call(run_input=run_input)
        print("Run finished. Status:", run.get('status'))
        dataset = client.dataset(run["defaultDatasetId"])
        dataset_items = await dataset.list_items()
        items = dataset_items.items
        print(f"Got {len(items)} items")
        for item in items:
            print("-", item.get("text", "")[:50])
    except Exception as e:
        print(f"Error quacker: {e}")

    print(f"\nStarting run with microworlds/twitter-scraper...")
    try:
        run2 = await client.actor("microworlds/twitter-scraper").call(run_input=run_input)
        print("Run finished. Status:", run2.get('status'))
        dataset2 = client.dataset(run2["defaultDatasetId"])
        dataset_items2 = await dataset2.list_items()
        items2 = dataset_items2.items
        print(f"Got {len(items2)} items")
        for item in items2:
            print("-", item.get("text", "")[:50])
    except Exception as e:
        print(f"Error microworlds: {e}")


if __name__ == "__main__":
    asyncio.run(main())
