import httpx
import re

def test_heatmap():
    video_id = "dQw4w9WgXcQ" # Rick Astley
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = httpx.get(url, headers=headers)
    
    if "heatMarkers" in r.text or "heatMarkerIntensityScoreNormalized" in r.text:
        print("Found heatMarkers in raw HTML!")
        match = re.search(r'"heatMarkers":\[(.+?)\]', r.text)
        if match:
            print("Successfully extracted heatMarkers via regex.")
    else:
        print("heatMarkers NOT found in raw HTML. We might need a full headless browser or it's fetched via XHR.")

if __name__ == "__main__":
    test_heatmap()
