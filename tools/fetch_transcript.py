"""YouTube 자막을 받아 transcripts/<video_id>.transcript.txt 로 저장한다.

usage: python tools/fetch_transcript.py <video_id or url> [lang ...]
requires: pip install youtube-transcript-api
"""
import re
import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


def video_id(arg):
    m = re.search(r"(?:v=|youtu\.be/|/live/|/shorts/)([\w-]{11})", arg)
    return m.group(1) if m else arg


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    vid = video_id(sys.argv[1])
    langs = sys.argv[2:] or ["ko", "en"]
    segments = YouTubeTranscriptApi().fetch(vid, languages=langs).to_raw_data()

    out = Path(__file__).resolve().parent.parent / "transcripts" / f"{vid}.transcript.txt"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for s in segments:
            t = int(s["start"])
            f.write(f"[{t // 3600:d}:{t % 3600 // 60:02d}:{t % 60:02d}] {s['text']}\n")
    print(f"{len(segments)} segments -> {out}")


if __name__ == "__main__":
    main()
