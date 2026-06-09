import httpx
import json

def test_internal_api():
    video_id = "dQw4w9WgXcQ"
    url = "https://www.youtube.com/youtubei/v1/player"
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20230516.00.00"
            }
        },
        "videoId": video_id
    }
    r = httpx.post(url, json=payload)
    data = r.json()
    
    # Try to find heatMarkers in the response
    def find_key(obj, key):
        if isinstance(obj, dict):
            if key in obj:
                yield obj[key]
            for k, v in obj.items():
                yield from find_key(v, key)
        elif isinstance(obj, list):
            for item in obj:
                yield from find_key(item, key)

    heatmaps = list(find_key(data, "heatmap"))
    heatMarkers = list(find_key(data, "heatMarkers"))
    print(f"Heatmaps found: {len(heatmaps)}, heatMarkers: {len(heatMarkers)}")
    if heatMarkers:
        markers = heatMarkers[0]
        most_replayed = max(markers, key=lambda x: x.get('heatMarkerIntensityScoreNormalized', 0))
        print(f"Most replayed: {most_replayed}")

if __name__ == "__main__":
    test_internal_api()
