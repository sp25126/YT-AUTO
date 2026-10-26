import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import subprocess
import cv2
import numpy as np

from core.clause_subtitles import generate_clause_phrases_file
from core.viral_bgm_engine import fetch_viral_bgm_track, mix_master_audio_with_sidechain

def run_masterpiece_mix_and_qa(
    raw_video: str = "remotion_studio/temp/masterpiece_raw.mp4",
    out_final: str = "outputs/masterpiece_short.mp4"
):
    print("\n" + "="*60)
    print("STEP: MASTERPIECE AUDIO MIX & QA FRAME VERIFICATION")
    print("="*60)
    os.makedirs(os.path.dirname(out_final) or ".", exist_ok=True)

    bgm_path = fetch_viral_bgm_track(vibe="dark_synth_pulse", out_mp3="assets/music/viral_bgm_master.mp3")

    sfx_cues = [
        # 0:00.0 Left-Aligned Roto Hook Sub Drop
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 30, "vol": 0.52},
        # 0:02.1 Financial Crash Chart Whoosh & Counter Ticks
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 2100, "vol": 0.45},
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 2200, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 2500, "vol": 0.30},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 3100, "vol": 0.30},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 3600, "vol": 0.25},
        # 0:06.2 Clean Eye-Anchored Speaker
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 6150, "vol": 0.42},
        # 0:10.6 Parallax Scene 2A (Too Early)
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 10550, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 10600, "vol": 0.44},
        # 0:12.8 Parallax Scene 2B (Crushed)
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 12750, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 12850, "vol": 0.40},
        # 0:15.4 Clean Eye-Anchored Speaker Setup
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 15350, "vol": 0.42},
        # 0:20.8 Parallax Scene 3 (Veterans)
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 20750, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 20850, "vol": 0.42},
        # 0:26.0 Speaker Bridge
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 25950, "vol": 0.42},
        # 0:27.9 Parallax Scene 4A (All Rosy)
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 27850, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 27950, "vol": 0.40},
        # 0:30.2 Parallax Scene 4B (The Details)
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 30150, "vol": 0.48},
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 30250, "vol": 0.40},
    ]

    print("[*] Running broadcast sidechain compression audio mix & 32.85s hard clamp...")
    mix_master_audio_with_sidechain(
        rendered_remotion_mp4=raw_video,
        bgm_path=bgm_path,
        sfx_cues=sfx_cues,
        clamp_end_sec=32.85,
        output_mp4=out_final
    )

    print("[*] Extracting Mandatory QA Frames [0.8, 3.8, 8.0, 11.5, 14.0, 20.0, 23.0, 28.8, 31.5]...")
    qa_dir = "temp/qa_frames"
    os.makedirs(qa_dir, exist_ok=True)
    timestamps = [0.8, 3.8, 8.0, 11.5, 14.0, 20.0, 23.0, 28.8, 31.5]
    frame_paths = []
    for idx, ts in enumerate(timestamps):
        out_f = os.path.join(qa_dir, f"masterpiece_beat_{idx+1:02d}_{ts:.1f}s.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", out_final,
            "-vframes", "1", "-q:v", "2", out_f
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frame_paths.append(out_f)

    # Build QA Contact Sheet (3x3 grid)
    imgs = [cv2.imread(p) for p in frame_paths if os.path.exists(p)]
    if len(imgs) >= 9:
        # Resize to uniform thumbnail
        thumb_w, thumb_h = 360, 640
        resized_thumbs = []
        labels = [
            "0.8s: Left-Aligned Hook",
            "3.8s: Area Chart 90%",
            "8.0s: Clean Eye Zoom",
            "11.5s: TOO EARLY Parallax",
            "14.0s: CRUSHED Parallax",
            "20.0s: Clean 'network' Sub",
            "23.0s: VETERANS Parallax",
            "28.8s: ALL ROSY Parallax",
            "31.5s: THE DETAILS Parallax"
        ]
        for img, lbl in zip(imgs[:9], labels):
            t_img = cv2.resize(img, (thumb_w, thumb_h))
            cv2.rectangle(t_img, (0, 0), (thumb_w, 48), (0, 0, 0), -1)
            cv2.putText(t_img, lbl, (8, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 128), 2)
            resized_thumbs.append(t_img)

        r1 = np.hstack(resized_thumbs[0:3])
        r2 = np.hstack(resized_thumbs[3:6])
        r3 = np.hstack(resized_thumbs[6:9])
        grid = np.vstack([r1, r2, r3])
        sheet_path = os.path.join(qa_dir, "QA_CONTACT_SHEET.jpg")
        cv2.imwrite(sheet_path, grid)
        print(f"[OK] Masterpiece QA Contact sheet saved -> {sheet_path}")

if __name__ == "__main__":
    generate_clause_phrases_file()
    run_masterpiece_mix_and_qa()
