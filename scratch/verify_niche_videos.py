import asyncio
import logging
import sys
import os

# Load .env variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual fallback loading of .env
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

# Adjust PYTHONPATH to project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.signal_collection_service import SignalCollectionService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def test_verify():
    guest_name = "Andrei Grachev"
    logging.info(f"Starting verification for primary guest: '{guest_name}'")
    
    service = SignalCollectionService()
    signals = await service.collect_signals(guest_name=guest_name)
    
    print("\n" + "="*80)
    print(f"VERIFICATION REPORT FOR '{guest_name}'")
    print("="*80)
    
    print(f"\n1. Verified Guest Appearances (Verified Long-Form): {len(signals.top_performing_guest_episodes)} items")
    for idx, ep in enumerate(signals.top_performing_guest_episodes[:5]):
        print(f"   [{idx+1}] {ep.title} ({ep.channel_name or ep.channel_name}) - Video ID: {ep.video_id}")
        
    print(f"\n2. Similar Guests Discovered: {len(signals.similar_guests)} items")
    similar_names = [g.guest_name for g in signals.similar_guests]
    for idx, sg in enumerate(signals.similar_guests):
        print(f"   [{idx+1}] {sg.guest_name} - Niche: {sg.niche} (Overlap Score: {sg.overlap_score:.2f})")
        
    print(f"\n3. Niche Content Benchmarking (Competitor/Niche Trends): {len(signals.top_niche_trends)} items")
    has_primary_guest_leak = False
    for idx, nt in enumerate(signals.top_niche_trends[:10]):
        title_lower = nt.title.lower()
        contains_guest = "grachev" in title_lower or "andrei" in title_lower or "грачев" in title_lower or "андрей" in title_lower
        mark = "LEAK!" if contains_guest else "OK"
        if contains_guest:
            has_primary_guest_leak = True
        print(f"   [{idx+1}] [{mark}] {nt.title} (Channel/Source: {nt.video_url})")
        
    print("\n" + "="*80)
    if has_primary_guest_leak:
        print("RESULT: FAILED - Primary guest leaked into niche benchmarking videos!")
    else:
        print("RESULT: SUCCESS - Niche/competitor videos are clean and feature similar guests/competitors!")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_verify())
