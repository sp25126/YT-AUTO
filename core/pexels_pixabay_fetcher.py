import os
import requests
import subprocess
import numpy as np

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "58086702-f40c68777ef64de312fca07dd")

def fetch_pexels_or_pixabay_video(query: str, out_raw: str = "temp/raw_stock.mp4") -> str:
    """
    1. Queries Pexels Video API for real moving HD B-roll.
    2. Falls back to Pixabay Video API if Pexels has no match.
    """
    os.makedirs(os.path.dirname(out_raw) or ".", exist_ok=True)

    # --- Try Pexels Videos First ---
    if PEXELS_API_KEY and PEXELS_API_KEY != "YOUR_PEXELS_API_KEY":
        try:
            url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&per_page=3&orientation=landscape"
            resp = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=10).json()
            for vid in resp.get("videos", []):
                for vf in vid.get("video_files", []):
                    if vf.get("width", 0) >= 1280 and vf.get("file_type") == "video/mp4":
                        print(f"[*] Downloading Pexels video for '{query}'...")
                        r = requests.get(vf["link"], timeout=20)
                        with open(out_raw, "wb") as f:
                            f.write(r.content)
                        return out_raw
        except Exception as e:
            print(f"[!] Pexels video search warning: {e}")

    # --- Try Pixabay Videos Second ---
    if PIXABAY_API_KEY and PIXABAY_API_KEY != "YOUR_PIXABAY_API_KEY":
        try:
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={requests.utils.quote(query)}&per_page=5"
            resp = requests.get(url, timeout=10).json()
            hits = resp.get("hits", [])
            for hit in hits:
                vids = hit.get("videos", {})
                target_url = None
                for size_key in ["large", "medium", "small"]:
                    candidate = vids.get(size_key, {})
                    if candidate.get("url"):
                        target_url = candidate["url"]
                        break
                
                if target_url:
                    print(f"[*] Downloading Pixabay video for '{query}' from {target_url[:60]}...")
                    r = requests.get(target_url, timeout=25)
                    with open(out_raw, "wb") as f:
                        f.write(r.content)
                    print(f"[OK] Saved stock video: {out_raw} ({os.path.getsize(out_raw)} bytes)")
                    return out_raw
        except Exception as e:
            print(f"[!] Pixabay video search warning: {e}")

    return ""

def fetch_pexels_or_pixabay_image(query: str, out_img: str = "temp/raw_stock.jpg") -> str:
    """Fetches a high-res photo from Pexels or Pixabay when specific still imagery is needed."""
    os.makedirs(os.path.dirname(out_img) or ".", exist_ok=True)

    if PEXELS_API_KEY and PEXELS_API_KEY != "YOUR_PEXELS_API_KEY":
        try:
            url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&per_page=3&orientation=landscape"
            resp = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=10).json()
            photos = resp.get("photos", [])
            if photos:
                img_url = photos[0]["src"]["large2x"]
                with open(out_img, "wb") as f:
                    f.write(requests.get(img_url, timeout=15).content)
                return out_img
        except Exception:
            pass

    if PIXABAY_API_KEY and PIXABAY_API_KEY != "YOUR_PIXABAY_API_KEY":
        try:
            url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={requests.utils.quote(query)}&image_type=photo&per_page=3"
            resp = requests.get(url, timeout=10).json()
            hits = resp.get("hits", [])
            if hits:
                img_url = hits[0].get("largeImageURL") or hits[0].get("webformatURL")
                if img_url:
                    with open(out_img, "wb") as f:
                        f.write(requests.get(img_url, timeout=15).content)
                    return out_img
        except Exception:
            pass

    return ""
