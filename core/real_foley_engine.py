import os
import subprocess

def build_organic_foley_pack(sfx_dir: str = "assets/sfx"):
    """
    Uses FFmpeg lavfi acoustic synthesis (pink noise + butterworth filters + sub-harmonics)
    instead of raw sine waves so SFX sound like real studio foley (air whoosh, paper thud, sub boom).
    """
    os.makedirs(sfx_dir, exist_ok=True)

    # 1. Real Air Whoosh (Bandpass-filtered pink noise with smooth envelope, ZERO white-noise hiss)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anoisesrc=d=0.28:c=pink:r=44100:a=0.7",
        "-af", "lowpass=f=1400,highpass=f=180,afade=t=in:st=0:d=0.12,afade=t=out:st=0.14:d=0.14",
        os.path.join(sfx_dir, "whoosh.wav")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 2. Deep Cinema Sub-Boom (48Hz sub-bass drop with warm saturation, no high-pitch beep!)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "sine=f=48:d=0.45:r=44100",
        "-af", "lowpass=f=110,afade=t=out:st=0.05:d=0.40,volume=1.8",
        os.path.join(sfx_dir, "hit.wav")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 3. Mechanical Felt Thud / Pop (Low-frequency 140Hz acoustic tap, zero Atari high-frequency beep)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anoisesrc=d=0.06:c=brown:r=44100:a=0.9",
        "-af", "lowpass=f=600,highpass=f=90,afade=t=out:st=0.01:d=0.05,volume=2.0",
        os.path.join(sfx_dir, "pop.wav")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 4. Cinematic Tension Riser
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anoisesrc=d=2.0:c=pink:r=44100:a=0.6",
        "-af", "highpass=f=200,lowpass=f=2200,afade=t=in:st=0:d=1.8,volume=1.2",
        os.path.join(sfx_dir, "riser.wav")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 5. Mechanical Odometer Tick
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anoisesrc=d=0.03:c=brown:r=44100:a=0.8",
        "-af", "lowpass=f=800,highpass=f=200,afade=t=out:st=0.005:d=0.025,volume=1.5",
        os.path.join(sfx_dir, "tick.wav")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[OK] Built Organic Studio Foley Pack in {sfx_dir}")

if __name__ == "__main__":
    build_organic_foley_pack()
