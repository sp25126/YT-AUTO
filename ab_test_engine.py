import os
import json
import subprocess
from core.face_tracker import CPUFaceFramingEngine
from core.ass_captions import generate_styled_ass

def render_variant(
    video_path: str,
    start_t: float,
    end_t: float,
    variant_config: dict,
    output_path: str
):
    duration = end_t - start_t
    framing_engine = CPUFaceFramingEngine()
    
    # 1. Detect faces and generate framing filter
    w, h, traj = framing_engine.analyze_faces_trajectory(video_path, start_t, duration)
    framing_filter = framing_engine.compute_crop_filter(
        mode=variant_config["framing_mode"],
        width=w, height=h,
        trajectories=traj,
        punch_in_times=variant_config.get("punch_in_times", [])
    )

    # 2. Build subtitle file
    with open("transcript.json", "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
    words = transcript_data if isinstance(transcript_data, list) else transcript_data.get("words", [])

    os.makedirs("temp", exist_ok=True)
    ass_file = f"temp/{variant_config['id']}.ass"
    generate_styled_ass(
        words=words,
        start_t=start_t,
        end_t=end_t,
        archetype=variant_config["archetype"],
        output_file=ass_file
    )
    clean_ass = ass_file.replace("\\", "/")

    # 3. Audio & VFX filtergraph assembly
    bgm_path = os.path.join("assets/music", variant_config["bgm"])
    if not os.path.exists(bgm_path):
        bgm_path = "assets/music/chill_lofi.mp3"
        
    sfx_path = os.path.join("assets/sfx", variant_config["primary_sfx"])
    if not os.path.exists(sfx_path):
        sfx_path = "assets/sfx/whoosh.wav"
    
    filter_graph = [
        framing_filter + ";",
        f"[framed_v]{variant_config['vfx_filter']}[v_graded];",
        f"[v_graded]subtitles='{clean_ass}'[v_out];",
        f"[1:a]volume={variant_config['bgm_volume']}[bgm_ducked];",
        f"[2:a]adelay=150|150,volume=0.45[sfx_cued];",
        f"[0:a][bgm_ducked]amix=inputs=2:duration=first[speech_bgm];",
        f"[speech_bgm][sfx_cued]amix=inputs=2:duration=first[a_out]"
    ]

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_t), "-t", str(duration), "-i", video_path,
        "-stream_loop", "-1", "-i", bgm_path,
        "-i", sfx_path,
        "-filter_complex", "".join(filter_graph),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered: {output_path}")

def run_ab_generator(video_path: str, start_t: float, end_t: float, base_name="clip_01"):
    os.makedirs("outputs/ab_experiments", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    # Variant A: Fast-Paced Kinetic Track + Neon Green + Driving Beat
    variant_a = {
        "id": f"{base_name}_varA_hype",
        "framing_mode": "smooth_follow",
        "archetype": "hustle_alpha",
        "bgm": "dark_synth_drive.mp3",
        "bgm_volume": 0.12,
        "primary_sfx": "braam.wav",
        "vfx_filter": "eq=contrast=1.18:saturation=1.15,unsharp=5:5:1.2",
        "punch_in_times": [{"start": start_t + 1.2, "end": start_t + 3.0}]
    }

    # Variant B: Dual Split-Screen + Comedic Tilt + Lo-Fi Groove + Punchline Drop
    variant_b = {
        "id": f"{base_name}_varB_split",
        "framing_mode": "dual_split",
        "archetype": "comedy_banter",
        "bgm": "pizzicato_comedy.mp3",
        "bgm_volume": 0.10,
        "primary_sfx": "pop.wav",
        "vfx_filter": "eq=contrast=1.08:saturation=1.20",
        "punch_in_times": []
    }

    print("\n--- Generating Variant A (Kinetic Face-Track + High-Stakes) ---")
    render_variant(video_path, start_t, end_t, variant_a, f"outputs/ab_experiments/{base_name}_Variant_A.mp4")

    print("\n--- Generating Variant B (Dual Split-Screen + Comedic Punch) ---")
    render_variant(video_path, start_t, end_t, variant_b, f"outputs/ab_experiments/{base_name}_Variant_B.mp4")

    # Save tracking manifest to log audience results
    test_manifest = {
        "clip_name": base_name,
        "timestamps": {"start": start_t, "end": end_t},
        "variants": {
            "Variant_A": {
                "file": f"{base_name}_Variant_A.mp4",
                "framing": "smooth_follow",
                "color_palette": "neon_green",
                "bgm_vibe": "dark_synth"
            },
            "Variant_B": {
                "file": f"{base_name}_Variant_B.mp4",
                "framing": "dual_split",
                "color_palette": "warm_yellow_tilt",
                "bgm_vibe": "comedy_pizzicato"
            }
        }
    }
    with open(f"outputs/ab_experiments/{base_name}_experiment.json", "w", encoding="utf-8") as f:
        json.dump(test_manifest, f, indent=2)
    print(f"\n[OK] A/B Test Pack ready in outputs/ab_experiments/")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A/B Variant Generator for Shorts")
    parser.add_argument("--video", default="stage-website-feedback-on-the-live-page-no-install-review.mp4", help="Video path")
    parser.add_argument("--start", type=float, default=67.7, help="Start time in seconds")
    parser.add_argument("--end", type=float, default=110.3, help="End time in seconds")
    parser.add_argument("--name", default="clip_01", help="Base clip name")
    args = parser.parse_args()

    v_path = args.video if os.path.exists(args.video) else os.path.join("inputs", args.video)
    run_ab_generator(v_path, args.start, args.end, args.name)
