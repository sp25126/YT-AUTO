import os
import json
import argparse
from core.audio_transcribe import extract_and_transcribe
from core.ass_captions import make_ass_subtitles
from core.composer import render_short_video

def main():
    parser = argparse.ArgumentParser(description="Zero-GPU Automated Shorts Pipeline")
    parser.add_argument("--video", required=True, help="Input video filename in inputs/")
    parser.add_argument("--manifest", default=None, help="Path to Antigravity-generated manifest.json")
    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)
    video_path = os.path.join("inputs", args.video) if not os.path.isabs(args.video) and not os.path.exists(args.video) else args.video

    if not args.manifest:
        print("[1/2] Generating CPU transcript...")
        extract_and_transcribe(video_path, "transcript.json")
        print("\nTranscription complete -> transcript.json")
        print("Next step: Open Antigravity chat and ask the agent to run the 'shorts-director' skill.")
        return

    print("[2/2] Manifest detected. Rendering short...")
    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    with open("transcript.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    start_t = manifest["start_time"]
    end_t = manifest["end_time"]
    sfx = manifest.get("sfx_markers", [])
    archetype = manifest.get("archetype", "comedy_banter")
    silence_windows = manifest.get("silence_windows", [])

    make_ass_subtitles(words, start_t, end_t, "captions.ass", archetype=archetype)
    output_video = os.path.join("outputs", f"short_{archetype}_{int(start_t)}.mp4")
    render_short_video(
        video_path=video_path,
        start_t=start_t,
        end_t=end_t,
        sfx_markers=sfx,
        output_path=output_video,
        archetype=archetype,
        silence_windows=silence_windows
    )

    with open(os.path.join("outputs", "metadata.txt"), "w", encoding="utf-8") as f:
        f.write(f"TITLE:\n{manifest.get('title')}\n\nTAGS:\n{' '.join(manifest.get('tags', []))}\n")

    print(f"\nPipeline finished.")
    print(f"Output Video: {output_video}")
    print(f"Metadata File: outputs/metadata.txt")

if __name__ == "__main__":
    main()
