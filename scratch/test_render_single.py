import os
import sys
import subprocess
import json

sys.path.insert(0, os.path.abspath("."))
from core.dynamic_ass_styler import build_contextual_ass
from core.composer import compose_editor_short

# Load transcript for clip_01
with open("temp/clips_test/clip_01_transcript.json", "r", encoding="utf-8") as f:
    data = json.load(f)

clip_info = data["clip_info"]
words = data["words"]
duration = clip_info["end"] - clip_info["start"]

# Define beats for clip_01
# Hook (0-6s): "jobs that we do, coders are first to go" -> shock
# Revelation (6-18s): "knowledge worker paradigm shift" -> neutral
# Horror (30-40s): "industrial revolution 4 decades of pain" -> shock
beats = [
    {"start": 0.0, "end": 7.0, "tone": "shock"},
    {"start": 7.0, "end": 28.0, "tone": "neutral"},
    {"start": 28.0, "end": 50.0, "tone": "shock"}
]

ass_path = "temp/clips_test/clip_01.ass"
build_contextual_ass(
    words=words,
    beats=beats,
    bg_profile={"visual_tone": "dark_background"},
    start_t=0.0,
    end_t=duration,
    output_file=ass_path
)

os.makedirs("outputs/FO572", exist_ok=True)
out_mp4 = "outputs/FO572/clip_01.mp4"

st = clip_info["start"]
sfx_markers = [
    {"time": st + 0.5, "effect": "whoosh"},
    {"time": st + 4.5, "effect": "braam_hit"},
    {"time": st + 33.0, "effect": "braam_hit"}
]

silence_windows = [
    {"start": st + 4.0, "end": st + 5.5}
]

print("Rendering test clip_01...")
compose_editor_short(
    video_path="inputs/startup_raj_shamani.mp4",
    start_t=clip_info["start"],
    end_t=clip_info["end"],
    archetype=clip_info["archetype"],
    sfx_markers=sfx_markers,
    silence_windows=silence_windows,
    output_path=out_mp4,
    ass_path=ass_path
)

if os.path.exists(out_mp4):
    sz = os.path.getsize(out_mp4)
    print(f"SUCCESS: Rendered {out_mp4} ({sz / (1024*1024):.2f} MB)")
else:
    print("FAILED: Output file not created.")
