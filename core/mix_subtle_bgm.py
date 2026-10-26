import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.viral_bgm_engine import mix_master_audio_with_sidechain

def mix_subtle_bgm_track():
    print("=" * 70)
    print("PREPARING SUBTLE BACKGROUND MUSIC BED")
    print("=" * 70)
    
    # We choose the warm ambient documentary bed: BPM 76, centroid 562Hz, lowest vocal clash
    raw_bgm = os.path.join(ROOT_DIR, "temp", "subtle_audits", "ambient_doc.mp3")
    if not os.path.exists(raw_bgm):
        raw_bgm = os.path.join(ROOT_DIR, "assets", "music", "ambient_doc.mp3")
    
    subtle_carved_bgm = os.path.join(ROOT_DIR, "assets", "music", "subtle_background_music.mp3")
    
    # Process BGM with vocal pocket EQ & smooth leveling
    print(f"[*] Processing subtle BGM from {raw_bgm} -> {subtle_carved_bgm}...")
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_bgm,
        "-af", (
            "silenceremove=start_periods=1:start_threshold=-40dB,"
            "highpass=f=70,"
            "equalizer=f=120:width_type=o:width=1.5:g=2,"        # Warmth
            "equalizer=f=2200:width_type=o:width=2.2:g=-6.5,"   # Clear vocal pocket
            "lowpass=f=9500,"                                   # Remove harsh highs
            "dynaudnorm=f=200:g=9:p=0.92"
        ),
        "-b:a", "192k", subtle_carved_bgm
    ], check=True)
    print(f"[OK] Created subtle BGM track: {subtle_carved_bgm}")

    raw_video = os.path.join(ROOT_DIR, "temp", "three_d_raw.mp4")
    out_master = os.path.join(ROOT_DIR, "outputs", "three_d_master_short.mp4")
    video_source = os.path.join(ROOT_DIR, "temp", "clean_base_30fps.mp4")

    sfx_cues = [
        # 0:00.0 Left-Aligned Roto Hook Sub Drop
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 30, "vol": 0.45},
        # 0:02.2 Financial Crash Chart Whoosh & Counter Ticks
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 2100, "vol": 0.40},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 2200, "vol": 0.42},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 2500, "vol": 0.25},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 3100, "vol": 0.25},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/counter_tick.wav"), "time_ms": 3600, "vol": 0.20},
        # 0:06.2 Clean Eye-Anchored Speaker
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 6150, "vol": 0.38},
        # 0:10.6 3D Wireframe Sphere + Card Whoosh (Too Early)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 10550, "vol": 0.42},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/sub_hit.wav"), "time_ms": 10600, "vol": 0.38},
        # 0:12.8 3D Monolith Descend Whoosh + Card Land (Crushed)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 12750, "vol": 0.42},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 12850, "vol": 0.35},
        # 0:15.4 Clean Eye-Anchored Speaker Setup
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 15350, "vol": 0.38},
        # 0:20.8 3D Network Lattice + Mentor Card Whoosh (Veterans)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 20750, "vol": 0.42},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 20850, "vol": 0.35},
        # 0:26.0 Speaker Bridge
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 25950, "vol": 0.38},
        # 0:27.9 3D All Rosy Card Whoosh
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 27850, "vol": 0.42},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 27950, "vol": 0.35},
        # 0:30.2 3D 180° Flip Whoosh + Card Land (The Details)
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/whoosh_fast.wav"), "time_ms": 30150, "vol": 0.45},
        {"file": os.path.join(ROOT_DIR, "assets/sfx/earshot_kit/card_land.wav"), "time_ms": 30250, "vol": 0.35},
    ]

    print("\n" + "=" * 70)
    print("STEP: MASTERING AUDIO WITH SUBTLE BGM & BROADCAST SIDECHAIN")
    print("=" * 70)
    
    # We mix with subtle BGM volume (volume=0.24 raw before sidechain, so it breathes under the voice)
    mix_master_audio_with_sidechain(
        rendered_remotion_mp4=raw_video,
        bgm_path=subtle_carved_bgm,
        sfx_cues=sfx_cues,
        clamp_end_sec=32.85,
        output_mp4=out_master,
        voice_source_mp4=video_source
    )
    print(f"[OK] Master Video with Subtle BGM -> {out_master}")

    print("\n" + "=" * 70)
    print("MEASURING INTEGRATED LOUDNESS")
    print("=" * 70)
    res = subprocess.run([
        "ffmpeg", "-i", out_master,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ], stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "I:" in line or "LRA:" in line or "Threshold:" in line:
            print(f"  {line.strip()}")

if __name__ == "__main__":
    mix_subtle_bgm_track()
