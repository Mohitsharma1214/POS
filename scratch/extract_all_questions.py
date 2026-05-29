"""
Batch Transcript Question Extractor - Jensen Huang Videos
Direct YouTube timedtext HTTP (no library, no LLM).
Run: python scratch/extract_all_questions.py
"""

import json
import sys
import os
import re
import time
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv
load_dotenv()

VIDEOS = [
    {"id": "_waPvOwL9Z8",  "title": "GTC March 2025 Keynote with NVIDIA CEO Jensen Huang",                         "channel": "NVIDIA"},
    {"id": "jw_o0xr8MWU",  "title": "NVIDIA GTC Keynote 2026",                                                     "channel": "NVIDIA"},
    {"id": "Y2F8yisiS6E",  "title": "GTC March 2024 Keynote with NVIDIA CEO Jensen Huang",                         "channel": "NVIDIA"},
    {"id": "0NBILspM4c4",  "title": "NVIDIA Live at CES with CEO Jensen Huang",                                     "channel": "NVIDIA"},
    {"id": "DiGB5uAYKAg",  "title": "GTC 2023 Keynote with NVIDIA CEO Jensen Huang",                               "channel": "NVIDIA"},
    {"id": "PWcNlRI00jo",  "title": "GTC Sept 2022 Keynote with NVIDIA CEO Jensen Huang",                          "channel": "NVIDIA"},
    {"id": "TLzna9__DnI",  "title": "NVIDIA CEO Jensen Huang Keynote at COMPUTEX 2025",                           "channel": "NVIDIA"},
    {"id": "39ubNuxnrK8",  "title": "GTC 2022 Spring Keynote with NVIDIA CEO Jensen Huang",                        "channel": "NVIDIA"},
    {"id": "lQHK61IDFH4",  "title": "NVIDIA GTC Washington D.C. Keynote with CEO Jensen Huang",                    "channel": "NVIDIA"},
    {"id": "RTmSrIFZanc",  "title": "NVIDIA GTC Live 2026 Keynote Pregame",                                        "channel": "NVIDIA"},
    {"id": "k82RwXqZHY8",  "title": "NVIDIA CEO Jensen Huang Keynote at CES 2025",                                "channel": "NVIDIA"},
    {"id": "6fbyiPRhMSs",  "title": "Cisco AI Summit | Special live event with Jensen Huang",                      "channel": "Cisco"},
    {"id": "X9cHONwKkn4",  "title": "NVIDIA CEO Jensen Huang Live GTC Paris Keynote at VivaTech 2025",            "channel": "NVIDIA"},
    {"id": "pKXDVsWZmUU",  "title": "NVIDIA CEO Jensen Huang Keynote at COMPUTEX 2024",                           "channel": "NVIDIA"},
    {"id": "7ARBJQn6QkM",  "title": "NVIDIA CEO Jensen Huang's Vision for the Future",                            "channel": "Cleo Abram"},
    {"id": "w-cmMcMZoZ4",  "title": "AI and The Next Computing Platforms - Jensen Huang and Mark Zuckerberg",     "channel": "NVIDIA"},
    {"id": "3hptKYix4X8",  "title": "Joe Rogan Experience #2422 - Jensen Huang",                                   "channel": "PowerfulJRE"},
    {"id": "DpQQi2scsHo",  "title": "Nvidia CEO Jensen Huang | 60 Minutes",                                       "channel": "60 Minutes"},
    {"id": "vEd-LqBCONg",  "title": "Don't Learn to Code - says NVIDIA CEO Jensen Huang",                         "channel": "Goda Go"},
    {"id": "1zURUZtPAE0",  "title": "The AI Factory: Infrastructure for Intelligence | Jensen Huang",             "channel": "Cisco"},
    {"id": "Pkj-BLHs6dE",  "title": "Jensen Huang of Nvidia on the Future of A.I. | DealBook Summit 2023",        "channel": "New York Times Events"},
    {"id": "_ltuZlGdMsg",  "title": "Elon Musk and Jensen Huang discuss the future of technology AI and space",   "channel": "Sky News"},
    {"id": "Hrbq66XqtCo",  "title": "Jensen Huang - Will Nvidia's moat persist? (Dwarkesh Patel)",               "channel": "Dwarkesh Patel"},
    {"id": "I9TxUsibexQ",  "title": "Alswaha x Elon Musk x Jensen Huang: Huge AI Reveals",                        "channel": "MCIT Saudi"},
    {"id": "eqpkLUUDvNg",  "title": "Nvidia CEO Huang on Future of AI and Global Economy - BlackRock Fink",      "channel": "DRM News"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

QUESTION_RE = re.compile(
    r"^(what|how|why|can you|could you|do you|did you|are you|were you|is it|will you|"
    r"would you|tell me|talk me through|describe|explain|walk me through|let'?s talk|"
    r"so what|so how|so why|i want to ask|i'?m curious|you'?ve said|you mentioned|"
    r"you talked about|looking back|going forward|in your view|from your perspective|"
    r"when did|when you|where do|who is|which|has nvidia|has the|have you|"
    r"and you|and how|and why|and what|jensen|mr\.? huang)",
    re.IGNORECASE,
)


def get_caption_url(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        html = resp.text
        match = re.search(
            r'"captionTracks":\[.*?"baseUrl":"(https://www\.youtube\.com/api/timedtext[^"]+)"',
            html
        )
        if not match:
            return None
        raw_url = match.group(1).replace("\\u0026", "&")
        if "lang=en" not in raw_url:
            raw_url += "&lang=en"
        if "fmt=json3" not in raw_url:
            raw_url += "&fmt=json3"
        return raw_url
    except Exception as e:
        return None


def fetch_transcript_text(caption_url):
    try:
        resp = requests.get(caption_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return ""
        data = resp.json()
        words = []
        for event in data.get("events", []):
            for seg in event.get("segs", []):
                t = seg.get("utf8", "").strip()
                if t and t != "\n":
                    words.append(t)
        return " ".join(words)
    except Exception:
        return ""


def extract_questions(text):
    if not text:
        return []
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    questions = []
    seen = set()
    for s in sentences:
        s = s.strip()
        if not s.endswith("?"):
            continue
        if len(s) < 25 or len(s) > 350:
            continue
        if not QUESTION_RE.match(s):
            continue
        norm = re.sub(r"\s+", " ", s.lower())
        if norm in seen:
            continue
        seen.add(norm)
        questions.append(s)
    return questions


def main():
    results = []
    total_q = 0
    total_ok = 0

    print("")
    print("=" * 72)
    print("  Jensen Huang - Transcript Question Extractor (%d videos)" % len(VIDEOS))
    print("  Method: Direct YouTube timedtext HTTP")
    print("=" * 72)
    print("")

    for i, v in enumerate(VIDEOS, 1):
        vid_id  = v["id"]
        title   = v["title"]
        channel = v["channel"]

        print("[%02d/%02d] %s" % (i, len(VIDEOS), title[:65]))
        print("   Channel : %s" % channel)
        print("   URL     : https://www.youtube.com/watch?v=%s" % vid_id)

        caption_url = get_caption_url(vid_id)
        if not caption_url:
            print("   STATUS  : No captions/page blocked")
            questions = []
            status = "no_captions"
        else:
            transcript_text = fetch_transcript_text(caption_url)
            if not transcript_text:
                print("   STATUS  : Caption URL found but text empty")
                questions = []
                status = "caption_empty"
            else:
                print("   STATUS  : Transcript OK (%d chars)" % len(transcript_text))
                questions = extract_questions(transcript_text)
                status = "ok" if questions else "no_questions_detected"

        results.append({
            "video_id": vid_id,
            "title": title,
            "channel": channel,
            "url": "https://www.youtube.com/watch?v=%s" % vid_id,
            "questions": questions,
            "question_count": len(questions),
            "status": status,
        })

        if questions:
            total_ok += 1
            total_q += len(questions)
            print("   QUESTIONS (%d found):" % len(questions))
            for qi, q in enumerate(questions, 1):
                print("     %2d. %s" % (qi, q))
        else:
            print("   QUESTIONS : None detected (%s)" % status)

        print("")
        time.sleep(2)

    # Save JSON
    out_path = os.path.join(os.path.dirname(__file__), "questions_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=" * 72)
    print("  DONE: %d/%d videos with questions | %d total questions" % (total_ok, len(VIDEOS), total_q))
    print("  Saved: %s" % out_path)
    print("=" * 72)
    print("")

    # Final clean report
    print("")
    print("=" * 72)
    print("  FULL QUESTION REPORT - ALL JENSEN HUANG VIDEOS")
    print("=" * 72)
    print("")
    for r in results:
        print("[%s] %s" % (r["channel"], r["title"]))
        print("  %s" % r["url"])
        if r["questions"]:
            for qi, q in enumerate(r["questions"], 1):
                print("  %2d. %s" % (qi, q))
        else:
            print("  [No questions - %s]" % r["status"])
        print("")


if __name__ == "__main__":
    main()
