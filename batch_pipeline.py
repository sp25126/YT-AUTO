import os
import json
import shutil
import argparse
from core.viral_scout import scout_youtube_video, download_video_temporary
from core.audio_transcribe import extract_and_transcribe
from core.ass_captions import generate_styled_ass
from core.composer import compose_editor_short

def run_batch_forge(video_url: str):
    os.makedirs("temp", exist_ok=True)
    temp_video = "temp/source.mp4"

    # Step 1: Scout YouTube heatmap & download source video
    if video_url.startswith("http://") or video_url.startswith("https://"):
        scout_data = scout_youtube_video(video_url)
        video_id = scout_data["video_id"]
        download_video_temporary(video_url, temp_video)
    else:
        # Support local files directly for offline runs
        video_id = os.path.splitext(os.path.basename(video_url))[0]
        shutil.copyfile(video_url, temp_video)
        scout_data = {
            "video_id": video_id,
            "title": video_id,
            "duration": 0,
            "channel": "Local",
            "heat_peaks": [],
            "existing_viral_shorts": []
        }
        with open("scout_report.json", "w", encoding="utf-8") as f:
            json.dump(scout_data, f, indent=2)

    output_dir = os.path.join("outputs", video_id)
    os.makedirs(output_dir, exist_ok=True)

    # Step 2: Transcribe full episode once on CPU
    print("\n[*] Transcribing full audio on CPU...")
    transcription_data = extract_and_transcribe(temp_video, "transcript.json")
    words = transcription_data if isinstance(transcription_data, list) else transcription_data.get("words", [])

    # Step 3: Interactive Agent Step in Antigravity Chat
    print("\n" + "="*70)
    print("STEP 3: ANTIGRAVITY AGENT CLIPPING DIRECTIVE")
    print("="*70)
    print("Open your Antigravity chat window and run:")
    print("> '@viral-batch-director'")
    print("> 'Read channel_profile.json, scout_report.json, and transcript.json.'")
    print("> 'Select the most viral 5 to 10 clips matching our brand DNA and output batch_manifest.json.'")
    print("="*70)
    
    if not os.path.exists("batch_manifest.json"):
        input("\nPress [Enter] once batch_manifest.json has been generated in the project root...")

    if not os.path.exists("batch_manifest.json"):
        print("[!] Error: batch_manifest.json not found.")
        return

    with open("batch_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    clips = manifest.get("clips", [])
    print(f"\n[*] Starting batch render for {len(clips)} vertical shorts...")

    # Step 4: Render all clips sequentially
    for idx, clip in enumerate(clips, start=1):
        clip_id = clip.get("clip_id", f"clip_{idx:02d}")
        archetype = clip.get("archetype", "comedy_banter")
        start_t = clip["start_time"]
        end_t = clip["end_time"]
        silence_windows = clip.get("silence_windows", [])
        sfx_markers = clip.get("sfx_markers", [])

        print(f"\n---> Rendering [{idx}/{len(clips)}]: {clip_id} ({archetype}) [{start_t}s -> {end_t}s]")
        
        # Subtitle file generation
        ass_path = f"temp/{clip_id}.ass"
        generate_styled_ass(words, start_t, end_t, archetype=archetype, output_file=ass_path)

        # Video composition
        final_mp4 = os.path.join(output_dir, f"{clip_id}.mp4")
        compose_editor_short(
            video_path=temp_video,
            start_t=start_t,
            end_t=end_t,
            archetype=archetype,
            sfx_markers=sfx_markers,
            silence_windows=silence_windows,
            output_path=final_mp4,
            ass_path=ass_path
        )

        # Metadata file generation
        meta_path = os.path.join(output_dir, f"{clip_id}_metadata.txt")
        with open(meta_path, "w", encoding="utf-8") as mf:
            mf.write(f"TITLE: {clip.get('title')}\n")
            mf.write(f"TAGS: {' '.join(clip.get('tags', []))}\n")
            mf.write(f"HOOK: {clip.get('hook_text')}\n")
            mf.write(f"THUMBNAIL PROMPT:\n{clip.get('thumbnail_prompt')}\n")

    # Step 5: Clean up temporary files to preserve local storage
    print("\n[*] Cleaning up temporary source video to save disk space...")
    if os.path.exists(temp_video):
        os.remove(temp_video)
    if os.path.exists("temp_mono.wav"):
        os.remove("temp_mono.wav")

    print("\n" + "="*70)
    print(f"[OK] Batch production complete! All {len(clips)} shorts saved in: {output_dir}")
    print("="*70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Clip Viral Podcast Short Pipeline")
    parser.add_argument("--url", required=True, help="YouTube video URL or local video path to analyze and clip")
    args = parser.parse_args()
    run_batch_forge(args.url)
