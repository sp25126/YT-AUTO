import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import subprocess
from core.scene_understanding import (
    analyze_speaker_cuts_and_faces,
    extract_speaker_roto_frames,
    fetch_and_inspect_broll_candidates
)
from core.viral_bgm_engine import (
    fetch_viral_bgm_track,
    mix_master_audio_with_sidechain
)

def step1_scene_telemetry_and_roto():
    print("\n" + "="*60)
    print("STEP 1: CAMERA-CUT, FACE TRACKING & SPEAKER ROTO MATTING")
    print("="*60)
    video_path = "temp/clean_base_30fps.mp4"
    if not os.path.exists(video_path):
        video_path = "remotion_studio/public/assets/speaker_base.mp4"

    # Analyze face anchors & cuts
    telemetry = analyze_speaker_cuts_and_faces(video_path, "temp/scene_telemetry.json")

    # Extract transparent roto frames for opening 2.2s hook
    extract_speaker_roto_frames(video_path, start_sec=0.0, duration_sec=2.2, out_dir="remotion_studio/public/assets/roto_hook")

def step2_fetch_candidates():
    print("\n" + "="*60)
    print("STEP 2: B-ROLL VISION GATE & FOREGROUND CUTOUT EXTRACTION")
    print("="*60)
    queries = {
        "early": "person standing alone empty desert horizon",
        "late": "crowded city skyscrapers traffic rush",
        "mentor": "business executives discussing whiteboard office",
        "rosy": "luxury yacht ocean celebration",
        "detail": "stressed entrepreneur working laptop night face"
    }

    grids = {}
    for scene_id, q in queries.items():
        print(f"\n[*] Processing B-roll candidate pool for '{scene_id}' (Query: '{q}')...")
        grid_path = fetch_and_inspect_broll_candidates(scene_id, q)
        grids[scene_id] = grid_path

    print("\n[OK] All candidate grids & foreground cutouts extracted:")
    for k, v in grids.items():
        print(f"  - {k}: {v}")
    return grids

def step4_mix_and_qa(raw_mp4: str = "remotion_studio/temp/pro_depth_raw.mp4", out_mp4: str = "outputs/pro_depth_short.mp4"):
    print("\n" + "="*60)
    print("STEP 4: VIRAL BGM SIDECHAIN DUCKING & QA CONTACT SHEET")
    print("="*60)
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    bgm_path = fetch_viral_bgm_track(vibe="dark_synth_pulse", out_mp3="assets/music/viral_bgm_master.mp3")

    sfx_cues = [
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 30, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 100, "vol": 0.50},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 2150, "vol": 0.45},
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 2200, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 2500, "vol": 0.28},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 3100, "vol": 0.28},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 6150, "vol": 0.45},
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 6800, "vol": 0.42},
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 7600, "vol": 0.42},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 10550, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 10700, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 12750, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 12850, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 15350, "vol": 0.45},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 20750, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 20900, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 25950, "vol": 0.45},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 27850, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 28000, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 30150, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 30250, "vol": 0.40},
    ]

    mix_master_audio_with_sidechain(
        rendered_remotion_mp4=raw_mp4,
        bgm_path=bgm_path,
        sfx_cues=sfx_cues,
        clamp_end_sec=32.85,
        output_mp4=out_mp4
    )

    # QA Contact sheet
    qa_dir = "temp/qa_frames_depth"
    os.makedirs(qa_dir, exist_ok=True)
    timestamps = [1.0, 1.8, 3.5, 5.0, 8.0, 11.5, 14.0, 22.5, 29.0, 31.5]
    frame_paths = []
    for idx, ts in enumerate(timestamps):
        out_f = os.path.join(qa_dir, f"depth_beat_{idx+1:02d}_{ts:.1f}s.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", out_mp4,
            "-vframes", "1", "-q:v", "2", out_f
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frame_paths.append(out_f)

    # Create contact sheet grid
    import cv2
    import numpy as np
    imgs = [cv2.imread(p) for p in frame_paths if os.path.exists(p)]
    if len(imgs) == 10:
        row1 = np.hstack(imgs[:5])
        row2 = np.hstack(imgs[5:])
        sheet = np.vstack([row1, row2])
        sheet_resized = cv2.resize(sheet, (1920, 1080))
        sheet_path = os.path.join(qa_dir, "DEPTH_QA_CONTACT_SHEET.jpg")
        cv2.imwrite(sheet_path, sheet_resized)
        print(f"[OK] Saved depth QA contact sheet -> {sheet_path}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ["telemetry", "all"]:
        step1_scene_telemetry_and_roto()
    if mode in ["candidates", "all"]:
        step2_fetch_candidates()
    if mode == "mix":
        step4_mix_and_qa()
