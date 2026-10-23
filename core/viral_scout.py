import os
import json
import subprocess
from yt_dlp import YoutubeDL

def scout_youtube_video(video_url: str):
    """
    Extracts video metadata, the native viewer replay heatmap,
    and searches for existing viral shorts on the same topic.
    """
    ydl_opts = {
        'skip_download': True,
        'extract_flat': False
    }

    print("[*] Fetching metadata and replay heatmap...")
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    title = info.get("title", "")
    duration = info.get("duration", 0)
    channel = info.get("channel", "")
    video_id = info.get("id", "")
    heatmap = info.get("heatmap", [])

    # Filter heatmap for peaks (replay intensity >= 0.65)
    heat_peaks = []
    if heatmap:
        for point in heatmap:
            if point.get("value", 0) >= 0.65:
                heat_peaks.append({
                    "start": round(point.get("start_time", 0), 1),
                    "end": round(point.get("end_time", 0), 1),
                    "intensity": round(point.get("value", 0), 2)
                })

    # Search for existing viral shorts featuring this subject/guest
    search_query = f"{title.split('|')[0].split('-')[0].strip()} shorts"
    print(f"[*] Cross-referencing viral signals for: '{search_query}'...")
    
    cmd = [
        "yt-dlp",
        f"ytsearch5:{search_query}",
        "--dump-json",
        "--no-playlist"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    existing_viral_shorts = []
    for line in proc.stdout.strip().split("\n"):
        if line:
            try:
                data = json.loads(line)
                existing_viral_shorts.append({
                    "title": data.get("title"),
                    "views": data.get("view_count"),
                    "url": f"https://youtube.com/shorts/{data.get('id')}"
                })
            except Exception:
                continue

    scout_report = {
        "video_id": video_id,
        "title": title,
        "duration": duration,
        "channel": channel,
        "heat_peaks": heat_peaks,
        "existing_viral_shorts": existing_viral_shorts
    }

    with open("scout_report.json", "w", encoding="utf-8") as f:
        json.dump(scout_report, f, indent=2)

    print(f"[OK] Scout report saved. Found {len(heat_peaks)} heatmap spikes.")
    return scout_report

def download_video_temporary(video_url: str, output_path: str = "temp/source.mp4"):
    """Downloads source video directly to temp/ at 1080p."""
    print(f"[*] Downloading source video temporarily to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", output_path,
        video_url
    ]
    subprocess.run(cmd, check=True)
    print("[OK] Temporary download ready.")
