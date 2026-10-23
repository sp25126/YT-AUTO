import sys
import json
import subprocess

def search_trending_shorts(niche_query: str, max_results: int = 5):
    """Scrapes top performing Shorts without needing YouTube Data API keys."""
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{niche_query} shorts",
        "--dump-json",
        "--default-search", "ytsearch",
        "--no-playlist"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    results = []
    for line in proc.stdout.strip().split("\n"):
        if line:
            try:
                data = json.loads(line)
                results.append({
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "views": data.get("view_count"),
                    "channel": data.get("channel"),
                    "duration": data.get("duration"),
                    "url": f"https://youtube.com/shorts/{data.get('id')}"
                })
            except Exception:
                pass
    return results

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "viral business podcast"
    print(json.dumps(search_trending_shorts(query), indent=2))
