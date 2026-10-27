import os
import sys
import subprocess
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.surgical_audio_polish import apply_pro_sfx_and_bgm_mix

ARTIFACTS_DIR = r"C:\Users\saumy\.gemini\antigravity-ide\brain\81220eb9-52be-4b9a-b578-1814f56cbf14"

def run_pipeline():
    print("=" * 70)
    print("STEP 1: RENDER REMOTION THREE.JS WITH EFFECTCRAFT POLISH")
    print("=" * 70)
    raw_video = os.path.join(ROOT_DIR, "temp", "three_d_raw.mp4")
    os.makedirs(os.path.dirname(raw_video), exist_ok=True)
    remotion_dir = os.path.join(ROOT_DIR, "remotion_studio")

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", "ThreeDMotionDirector",
        raw_video,
        "--concurrency=2"
    ]
    print(f"[*] Executing Remotion render in {remotion_dir}...")
    subprocess.run(cmd, cwd=remotion_dir, shell=True, check=True)
    print(f"[OK] Raw 3D Video Rendered -> {raw_video}")

    print("\n" + "=" * 70)
    print("STEP 2: SURGICAL AUDIO POLISH (116 BPM DARK PULSE + LOUD SFX)")
    print("=" * 70)
    output_mp4 = os.path.join(ROOT_DIR, "outputs", "three_d_polished_master.mp4")
    voice_source = os.path.join(ROOT_DIR, "temp", "clean_base_30fps.mp4")
    
    apply_pro_sfx_and_bgm_mix(
        video_in=raw_video,
        output_mp4=output_mp4,
        voice_source=voice_source
    )
    print(f"[OK] Polished Master Short Ready -> {output_mp4}")

    # Also keep three_d_master_short.mp4 synced with the latest polish
    master_backup = os.path.join(ROOT_DIR, "outputs", "three_d_master_short.mp4")
    shutil.copy(output_mp4, master_backup)

    print("\n" + "=" * 70)
    print("STEP 3: QA SPOT-CHECK FRAME EXTRACTION [3.5, 11.2, 22.0, 30.5]")
    print("=" * 70)
    qa_dir = os.path.join(ROOT_DIR, "temp", "qa_frames")
    os.makedirs(qa_dir, exist_ok=True)
    timestamps = [3.5, 11.2, 22.0, 30.5]
    labels = [
        "01_CrashChart_3.5s",
        "02_TooEarly_Burst_11.2s",
        "03_Veterans_Pills_22.0s",
        "04_CardFlip_Detail_30.5s"
    ]

    for t, lbl in zip(timestamps, labels):
        out_f = os.path.join(qa_dir, f"spotcheck_{lbl}.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", output_mp4,
            "-vframes", "1", "-q:v", "2", out_f
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(ARTIFACTS_DIR):
            shutil.copy(out_f, os.path.join(ARTIFACTS_DIR, f"spotcheck_{lbl}.jpg"))
        print(f"  -> Extracted {lbl} @ {t}s -> {out_f}")

    print("\n" + "=" * 70)
    print("STEP 4: INTEGRATED LOUDNESS & AUDIO TELEMETRY VERIFICATION")
    print("=" * 70)
    res = subprocess.run([
        "ffmpeg", "-i", output_mp4,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ], stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "I:" in line or "LRA:" in line or "Threshold:" in line:
            print(f"  {line.strip()}")

    print("\n[SUCCESS] Surgical polish pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()
