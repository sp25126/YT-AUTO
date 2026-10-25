import os
import sys
import time
import subprocess

sys.path.insert(0, os.path.abspath("."))
from core.viral_bgm_engine import mix_master_audio_with_sidechain, fetch_viral_bgm_track
from core.frame_inspector import generate_qa_inspection_sheet

def run_pro_pipeline():
    raw_video = "remotion_studio/temp/pro_motion_raw.mp4"
    if not os.path.exists(raw_video):
        print(f"[!] Waiting for {raw_video} to finish encoding...")
        while not os.path.exists(raw_video) or os.path.getsize(raw_video) < 5000000:
            time.sleep(3)

    bgm_path = fetch_viral_bgm_track("dark_synth_pulse")

    sfx_cues = [
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 30, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 550, "vol": 0.25},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 850, "vol": 0.25},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 1150, "vol": 0.25},
        {"file": "assets/sfx/earshot_kit/cursor_click.wav", "time_ms": 1334, "vol": 0.45}, # -2 frames before 1.4s
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 1400, "vol": 0.25},
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 1550, "vol": 0.48}, # -1.5 frames before 1.6s
        {"file": "assets/sfx/earshot_kit/sub_hit.wav", "time_ms": 1600, "vol": 0.38},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 1700, "vol": 0.25},
        {"file": "assets/sfx/earshot_kit/counter_tick.wav", "time_ms": 1950, "vol": 0.25},
        # Mode Transitions with Whoosh + Pops
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 6100, "vol": 0.42}, # Transition to Fullscreen
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 10500, "vol": 0.45}, # Transition to Dual Showcase
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 10550, "vol": 0.42},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 12000, "vol": 0.42}, # Card 2 enters
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 12100, "vol": 0.40},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 15300, "vol": 0.42}, # Transition to Fullscreen
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 20700, "vol": 0.42}, # Transition to Floating Studio
        {"file": "assets/sfx/earshot_kit/cursor_click.wav", "time_ms": 22134, "vol": 0.45}, # Filter click
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 22150, "vol": 0.38},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 25900, "vol": 0.42}, # Transition to Fullscreen
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 27800, "vol": 0.45}, # Transition to Dual Showcase
        {"file": "assets/sfx/earshot_kit/ui_pop.wav", "time_ms": 27850, "vol": 0.42},
        {"file": "assets/sfx/earshot_kit/whoosh_fast.wav", "time_ms": 29700, "vol": 0.42}, # Card 2 enters
        {"file": "assets/sfx/earshot_kit/card_land.wav", "time_ms": 29800, "vol": 0.40},
    ]

    out_final = "outputs/pro_motion_short.mp4"
    print("[*] Running sidechain compression audio mix and 32.85s hard clamp...")
    mix_master_audio_with_sidechain(
        rendered_remotion_mp4=raw_video,
        bgm_path=bgm_path,
        sfx_cues=sfx_cues,
        clamp_end_sec=32.85,
        output_mp4=out_final
    )

    print("[*] Generating Frame-by-Frame QA Contact Sheet...")
    timestamps = [1.8, 6.2, 8.5, 11.2, 13.5, 19.0, 23.5, 28.5, 31.0, 32.8]
    sheet, frames = generate_qa_inspection_sheet(out_final, timestamps)
    print(f"[OK] QA Contact sheet generated at {sheet}")

if __name__ == "__main__":
    run_pro_pipeline()
