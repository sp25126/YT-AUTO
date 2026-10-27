import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.surgical_audio_polish import prepare_audible_soundtrack, apply_pro_sfx_and_bgm_mix

def mix_subtle_bgm_track():
    print("=" * 70)
    print("PREPARING SUBTLE BACKGROUND MUSIC BED (PROPERLY AUDIBLE)")
    print("=" * 70)
    
    subtle_carved_bgm = os.path.join(ROOT_DIR, "assets", "music", "subtle_background_music.mp3")
    prepare_audible_soundtrack(subtle_carved_bgm)
    print(f"[OK] Created rich, audible BGM track: {subtle_carved_bgm}")

    raw_video = os.path.join(ROOT_DIR, "temp", "three_d_raw.mp4")
    out_master = os.path.join(ROOT_DIR, "outputs", "three_d_master_short.mp4")
    out_polished = os.path.join(ROOT_DIR, "outputs", "three_d_polished_master.mp4")
    video_source = os.path.join(ROOT_DIR, "temp", "clean_base_30fps.mp4")

    print("\n" + "=" * 70)
    print("STEP: MASTERING AUDIO WITH PROPERLY AUDIBLE BGM & MUSICAL SIDECHAIN")
    print("=" * 70)
    
    # We mix with volume=0.50 and gentle -3.5dB sidechain ducking so BGM is clearly audible behind voice!
    apply_pro_sfx_and_bgm_mix(
        video_in=raw_video,
        output_mp4=out_master,
        voice_source=video_source,
        bgm_file=subtle_carved_bgm,
        bgm_volume=0.50
    )
    import shutil
    shutil.copy(out_master, out_polished)
    print(f"[OK] Master Video with Audible BGM -> {out_master}")
    print(f"[OK] Mirrored to -> {out_polished}")

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
