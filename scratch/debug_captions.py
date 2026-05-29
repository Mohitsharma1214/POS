"""
Debug script: test what format the caption URL returns.
"""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
resp = requests.get("https://www.youtube.com/watch?v=3hptKYix4X8", headers=headers, timeout=15)
match = re.search(r'"captionTracks":\[.*?"baseUrl":"(https://www\.youtube\.com/api/timedtext[^"]+)"', resp.text)
if match:
    url = match.group(1).replace("\\u0026", "&")
    print("RAW URL:", url[:300])
    print("")
    # Try default XML format
    r2 = requests.get(url, headers=headers, timeout=15)
    print("Status:", r2.status_code)
    print("Content-Type:", r2.headers.get("content-type", ""))
    print("First 800 chars of body:")
    print(r2.text[:800])
    print("")
    # Try with fmt=json3
    url_json = url + "&fmt=json3"
    r3 = requests.get(url_json, headers=headers, timeout=15)
    print("JSON3 Status:", r3.status_code)
    print("JSON3 first 400 chars:")
    print(r3.text[:400])
else:
    print("No captionTracks found in page")
