import os
import subprocess
import json
from faster_whisper import WhisperModel

VIDEO_PATH = "inputs/startup_raj_shamani.mp4"
TEMP_DIR = "temp/clips_test"
os.makedirs(TEMP_DIR, exist_ok=True)

clips = [
    {
        "id": "clip_01",
        "title": "Coders Are First To Go",
        "start": 1655.0,
        "end": 1707.0,
        "archetype": "tech_intellectual"
    },
    {
        "id": "clip_02",
        "title": "AI Is Making People Dumber",
        "start": 3868.0,
        "end": 3914.0,
        "archetype": "comedy_banter"
    },
    {
        "id": "clip_03",
        "title": "Brutal Truth About Startup Timing",
        "start": 2043.0,
        "end": 2088.0,
        "archetype": "hustle_alpha"
    },
    {
        "id": "clip_04",
        "title": "HTML Coders Made 1M Dollars",
        "start": 5367.0,
        "end": 5415.0,
        "archetype": "tech_intellectual"
    },
    {
        "id": "clip_05",
        "title": "Your Idea Must Sound Stupid",
        "start": 221.0,
        "end": 264.0,
        "archetype": "hustle_alpha"
    }
]

print("Initializing Faster-Whisper base.en model...")
model = WhisperModel("base.en", device="cpu", compute_type="int8")

for clip in clips:
    cid = clip["id"]
    start = clip["start"]
    dur = clip["end"] - clip["start"]
    wav_path = os.path.join(TEMP_DIR, f"{cid}.wav")
    
    print(f"\n--- Extracting audio for {cid} ({dur:.1f}s) ---")
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", VIDEO_PATH,
        "-t", str(dur),
        "-vn", "-ar", "16000", "-ac", "1",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    print(f"Transcribing {cid}...")
    segments, _ = model.transcribe(wav_path, word_timestamps=True)
    words_list = []
    text_full = []
    
    for seg in segments:
        text_full.append(seg.text.strip())
        if seg.words:
            for w in seg.words:
                words_list.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "prob": round(w.probability, 3)
                })
                
    clip_result = {
        "clip_info": clip,
        "full_text": " ".join(text_full),
        "words": words_list
    }
    
    out_json = os.path.join(TEMP_DIR, f"{cid}_transcript.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(clip_result, f, indent=2)
    print(f"Saved {cid}_transcript.json with {len(words_list)} words.")
    print("Preview text:", " ".join(text_full)[:120] + "...")

print("\nAll 5 clip audio chunks extracted and transcribed successfully!")
