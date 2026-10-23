import os
import shutil
import requests
import numpy as np
import scipy.io.wavfile as wav

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "58086702-f40c68777ef64de312fca07dd")

def fetch_pixabay_assets(queries: dict, out_dir: str = "remotion_studio/public/assets"):
    """
    Fetches Pixabay videos (.mp4) and high-res photos (.jpg) directly into Remotion's public folder.
    queries = {"scene2_early": {"type": "image", "q": "desert hourglass sand"}, ...}
    """
    os.makedirs(out_dir, exist_ok=True)
    manifest = {}

    # Check if local assets exist in assets/broll to reuse existing HD files
    local_fallbacks = {
        "scene2_early": "assets/broll/hourglass_timing.jpg",
        "scene2_late": "assets/broll/cyberpunk_megacity.jpg",
        "scene3_boardroom": "assets/broll/boardroom_veterans.jpg",
        "scene3_mentor": "assets/broll/stock_senior_execs.mp4",
        "scene4_rosy": "assets/broll/stock_luxury.mp4",
        "scene4_devil": "assets/broll/stock_stressed_analyst.mp4",
    }

    for key, item in queries.items():
        media_type = item.get("type", "video")
        ext = ".mp4" if media_type == "video" else ".jpg"
        out_file = os.path.join(out_dir, f"{key}{ext}")

        # Check existing local fallback first
        if key in local_fallbacks and os.path.exists(local_fallbacks[key]):
            src = local_fallbacks[key]
            actual_ext = os.path.splitext(src)[1]
            target_file = os.path.join(out_dir, f"{key}{actual_ext}")
            shutil.copy2(src, target_file)
            manifest[key] = f"/assets/{key}{actual_ext}"
            print(f"[OK] Reused local asset for {key}: {target_file}")
            continue

        q = requests.utils.quote(item["q"])

        if media_type == "video" and PIXABAY_API_KEY and PIXABAY_API_KEY != "YOUR_PIXABAY_API_KEY":
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={q}&per_page=3"
            try:
                r = requests.get(url, timeout=10).json()
                hits = r.get("hits", [])
                if hits:
                    vids = hits[0].get("videos", {})
                    candidate = vids.get("large", {}) or vids.get("medium", {}) or vids.get("small", {})
                    vid_url = candidate.get("url")
                    if vid_url:
                        with open(out_file, "wb") as f:
                            f.write(requests.get(vid_url, timeout=20).content)
                        manifest[key] = f"/assets/{key}.mp4"
                        print(f"[OK] Downloaded Pixabay video for {key}: {out_file}")
                        continue
            except Exception as e:
                print(f"[!] Pixabay video fallback for {key}: {e}")

        # Fallback or image request via Pixabay Photo API
        if PIXABAY_API_KEY and PIXABAY_API_KEY != "YOUR_PIXABAY_API_KEY":
            url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={q}&image_type=photo&per_page=3"
            try:
                r = requests.get(url, timeout=10).json()
                hits = r.get("hits", [])
                if hits:
                    img_url = hits[0].get("largeImageURL") or hits[0].get("webformatURL")
                    if img_url:
                        with open(out_file, "wb") as f:
                            f.write(requests.get(img_url, timeout=15).content)
                        manifest[key] = f"/assets/{key}.jpg"
                        print(f"[OK] Downloaded Pixabay photo for {key}: {out_file}")
                        continue
            except Exception as e:
                print(f"[!] Pixabay photo warning for {key}: {e}")

    return manifest

def generate_procedural_sfx(out_dir: str = "assets/sfx"):
    """Generates clean Vox-style UI ticks, pops, sub-hits, and whooshes using Python + NumPy."""
    os.makedirs(out_dir, exist_ok=True)
    sr = 44100

    # 1. Mechanical Counter Tick (40ms crisp click)
    t = np.linspace(0, 0.04, int(sr * 0.04), False)
    tick = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 140)
    wav.write(os.path.join(out_dir, "tick.wav"), sr, (tick * 0.6 * 32767).astype(np.int16))

    # 2. Warm UI Card Pop (90ms pitch-drop sine pop)
    t = np.linspace(0, 0.09, int(sr * 0.09), False)
    freq = np.linspace(520, 140, len(t))
    pop = np.sin(2 * np.pi * freq * t) * np.exp(-t * 45)
    wav.write(os.path.join(out_dir, "pop.wav"), sr, (pop * 0.8 * 32767).astype(np.int16))

    # 3. Deep Documentary Stamp Hit (350ms 808 sub punch)
    t = np.linspace(0, 0.35, int(sr * 0.35), False)
    sub_freq = np.linspace(110, 38, len(t))
    hit = np.tanh(np.sin(2 * np.pi * sub_freq * t) * 2.5) * np.exp(-t * 12)
    wav.write(os.path.join(out_dir, "hit.wav"), sr, (hit * 0.9 * 32767).astype(np.int16))

    # 4. Filtered Noise Whoosh (220ms transition swish)
    t = np.linspace(0, 0.22, int(sr * 0.22), False)
    noise = np.random.normal(0, 1, len(t))
    envelope = np.sin(np.pi * (t / 0.22)) ** 2
    whoosh = noise * envelope * 0.45
    wav.write(os.path.join(out_dir, "whoosh.wav"), sr, (whoosh * 32767).astype(np.int16))

    print(f"[OK] Generated procedural Vox SFX in {out_dir}: tick.wav, pop.wav, hit.wav, whoosh.wav")

if __name__ == "__main__":
    generate_procedural_sfx()
