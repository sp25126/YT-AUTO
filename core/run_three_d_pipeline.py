import os
import sys
import subprocess
import json
import cv2
import numpy as np
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.video_bgm_analyzer import analyze_video_for_bgm, fetch_and_score_best_bgm_candidate
from core.viral_bgm_engine import mix_master_audio_with_sidechain

ARTIFACTS_DIR = r"C:\Users\saumy\.gemini\antigravity-ide\brain\81220eb9-52be-4b9a-b578-1814f56cbf14"

def run_three_d_pipeline():
    print("=" * 70)
    print("STEP 1: WHOLE-VIDEO BGM ANALYSIS & MULTI-CANDIDATE AUDITION")
    print("=" * 70)
    video_source = os.path.join(ROOT_DIR, "temp", "clean_base_30fps.mp4")
    transcript_file = os.path.join(ROOT_DIR, "transcript.json")
    scored_bgm = os.path.join(ROOT_DIR, "assets", "music", "scored_bgm.mp3")

    profile = analyze_video_for_bgm(video_source, transcript_file)
    bgm_path = fetch_and_score_best_bgm_candidate(profile["recommended_bgm_queries"], out_mp3=scored_bgm)

    print("\n" + "=" * 70)
    print("STEP 2: RENDER THREE.JS 3D MOTION DIRECTOR WITH REMOTION")
    print("=" * 70)
    raw_video = os.path.join(ROOT_DIR, "temp", "three_d_raw.mp4")
    os.makedirs(os.path.dirname(raw_video), exist_ok=True)
    remotion_dir = os.path.join(ROOT_DIR, "remotion_studio")

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", "ThreeDMotionDirector",
        raw_video,
        "--concurrency=4"
    ]
    print(f"[*] Running: {' '.join(cmd)} in {remotion_dir}")
    subprocess.run(cmd, cwd=remotion_dir, shell=True, check=True)
    print(f"[OK] Rendered raw 3D video -> {raw_video}")

    print("\n" + "=" * 70)
    print("STEP 3: BROADCAST SIDECHAIN AUDIO MIX & 32.85S CLAMP")
    print("=" * 70)
    out_master = os.path.join(ROOT_DIR, "outputs", "three_d_master_short.mp4")
    os.makedirs(os.path.dirname(out_master), exist_ok=True)

    sfx_cues = [
        # 0:00.0 Left-Aligned Roto Hook Sub Drop
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 30, "vol": 0.52},
        # 0:02.2 Financial Crash Chart Whoosh & Counter Ticks
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 2100, "vol": 0.45},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 2200, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 2500, "vol": 0.30},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 3100, "vol": 0.30},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 3600, "vol": 0.25},
        # 0:06.2 Clean Eye-Anchored Speaker
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 6150, "vol": 0.42},
        # 0:10.6 3D Wireframe Sphere + Card Whoosh (Too Early)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 10550, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 10600, "vol": 0.44},
        # 0:12.8 3D Monolith Descend Whoosh + Card Land (Crushed)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 12750, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 12850, "vol": 0.40},
        # 0:15.4 Clean Eye-Anchored Speaker Setup
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 15350, "vol": 0.42},
        # 0:20.8 3D Network Lattice + Mentor Card Whoosh (Veterans)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 20750, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 20850, "vol": 0.42},
        # 0:26.0 Speaker Bridge
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 25950, "vol": 0.42},
        # 0:27.9 3D All Rosy Card Whoosh
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 27850, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 27950, "vol": 0.40},
        # 0:30.2 3D 180° Flip Whoosh + Card Land (The Details)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 30150, "vol": 0.48},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 30250, "vol": 0.40},
    ]

    mix_master_audio_with_sidechain(
        rendered_remotion_mp4=raw_video,
        bgm_path=bgm_path,
        sfx_cues=sfx_cues,
        clamp_end_sec=32.85,
        output_mp4=out_master,
        voice_source_mp4=video_source
    )
    print(f"[OK] Master Mixed Audio -> {out_master}")

    print("\n" + "=" * 70)
    print("STEP 4: MANDATORY QA FRAME EXTRACTION & CONTACT SHEET")
    print("=" * 70)
    qa_dir = os.path.join(ROOT_DIR, "temp", "qa_frames")
    os.makedirs(qa_dir, exist_ok=True)
    timestamps = [0.8, 3.8, 11.5, 14.0, 20.0, 23.0, 28.8, 30.3, 31.8]
    labels = [
        "0.8s: Roto Hook",
        "3.8s: 3D Crash Pillars 90%",
        "11.5s: 3D Sphere TOO EARLY",
        "14.0s: 3D Monolith CRUSHED",
        "20.0s: Clean Sub Spacing",
        "23.0s: 3D Lattice VETERANS",
        "28.8s: 3D Card ALL ROSY",
        "30.3s: 3D Flip 180deg",
        "31.8s: Single-Line DETAILS"
    ]

    thumbs = []
    for idx, (t, lbl) in enumerate(zip(timestamps, labels)):
        frame_out = os.path.join(qa_dir, f"three_d_qa_{idx+1:02d}_{t:.1f}s.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", out_master,
            "-vframes", "1", "-q:v", "2", frame_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        img = cv2.imread(frame_out)
        if img is not None:
            thumb = cv2.resize(img, (360, 640))
            cv2.rectangle(thumb, (0, 0), (360, 52), (0, 0, 0), -1)
            cv2.putText(thumb, lbl, (10, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 128), 2)
            thumbs.append(thumb)

    if len(thumbs) >= 9:
        row1 = np.hstack(thumbs[0:3])
        row2 = np.hstack(thumbs[3:6])
        row3 = np.hstack(thumbs[6:9])
        grid = np.vstack([row1, row2, row3])
        sheet_path = os.path.join(qa_dir, "QA_CONTACT_SHEET.jpg")
        cv2.imwrite(sheet_path, grid)
        print(f"[OK] Generated Contact Sheet: {sheet_path}")

        if os.path.exists(ARTIFACTS_DIR):
            art_sheet = os.path.join(ARTIFACTS_DIR, "QA_CONTACT_SHEET.jpg")
            shutil.copy(sheet_path, art_sheet)
            print(f"[OK] Mirrored to Artifacts: {art_sheet}")

    print("\n" + "=" * 70)
    print("STEP 5: INTEGRATED LOUDNESS VERIFICATION")
    print("=" * 70)
    res = subprocess.run([
        "ffmpeg", "-i", out_master,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ], stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "I:" in line or "LRA:" in line or "Threshold:" in line:
            print(f"  {line.strip()}")

    print("\n[SUCCESS] Pipeline Complete! Final file: outputs/three_d_master_short.mp4")

if __name__ == "__main__":
    run_three_d_pipeline()
