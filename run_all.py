import os
import sys
import json
import subprocess
import argparse
from core.audio_transcribe import extract_and_transcribe
from core.ass_captions import make_ass_subtitles
from core.composer import compose_editor_short

def run_pipeline(video_filename: str):
    video_path = os.path.join("inputs", video_filename) if not os.path.exists(video_filename) else video_filename
    os.makedirs("outputs", exist_ok=True)

    print("\n=== STEP 1: Zero-GPU Local Transcription ===")
    words = extract_and_transcribe(video_path, "transcript.json")

    print("\n=== STEP 2: Running Hook Score & Dead-Air Audits ===")
    hookscore_tool = ".agents/skills/youtube-agent-pack/tools/hookscore.py"
    if os.path.exists(hookscore_tool):
        sample_hook = " ".join([w["word"] for w in words[:25]])
        subprocess.run([sys.executable, hookscore_tool, "--hook", sample_hook])

    print("\n=== STEP 3: Antigravity Agent Directive ===")
    print("Open Antigravity Chat and run:")
    print("> '@elite-video-editor @elite-sound-designer @youtube-agent-pack'")
    print("> 'Analyze transcript.json. Score the best hook, specify punch-in times, SFX cues, and export manifest.json.'")
    print("\nOnce manifest.json is generated, press Enter to render the short...")
    if not os.path.exists("manifest.json"):
        input("[Press Enter after manifest.json is saved]")

    with open("manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    start_t = manifest["start_time"]
    end_t = manifest["end_time"]
    archetype = manifest.get("archetype", "comedy_banter")
    silence_windows = manifest.get("silence_windows", [])
    sfx_markers = manifest.get("sfx_markers", [])

    print(f"\n=== STEP 4: Assembling Dynamic Vector Subtitles [{archetype}] ===")
    make_ass_subtitles(words, start_t, end_t, "captions.ass", archetype=archetype)

    print(f"\n=== STEP 5: Editor Master Composite [{archetype}] (Grade + Drops + SFX) ===")
    output_short = os.path.join("outputs", f"viral_short_{archetype}_{int(start_t)}.mp4")

    compose_editor_short(
        video_path=video_path,
        start_t=start_t,
        end_t=end_t,
        archetype=archetype,
        sfx_markers=sfx_markers,
        silence_windows=silence_windows,
        output_path=output_short
    )

    with open(os.path.join("outputs", "metadata.txt"), "w", encoding="utf-8") as f:
        f.write(f"TITLE:\n{manifest.get('title', '')}\n\nTAGS:\n{' '.join(manifest.get('tags', []))}\n")

    print(f"\n[OK] Render Complete: {output_short}")
    print("Metadata & tags saved in outputs/metadata.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Input video filename in inputs/")
    args = parser.parse_args()
    run_pipeline(args.video)
