import os
import sys
sys.path.insert(0, os.path.abspath("."))
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove, new_session
from core.pexels_pixabay_fetcher import fetch_pexels_or_pixabay_image

# Fast lightweight CPU ONNX model (u2netp runs fast on CPU)
try:
    REMBG_SESSION = new_session("u2netp")
except Exception as e:
    print(f"[!] Warning initializing u2netp session: {e}, falling back to default")
    try:
        REMBG_SESSION = new_session()
    except Exception:
        REMBG_SESSION = None

def create_bw_collage_cutout(
    query: str,
    out_png: str,
    add_white_stroke: bool = True,
    add_red_eyebar: bool = False,
    add_torn_paper_bottom: bool = False,
    local_fallback: str = ""
) -> str:
    """
    1. Downloads a photo from Pexels/Pixabay (or reuses local image).
    2. Strips the background using rembg on CPU.
    3. Converts subject to high-contrast Black & White (GaryVee / Cosmocuts style).
    4. Adds a crisp white sticker outline or glowing red eye-censor bar.
    5. Saves as transparent .png for Remotion 3-layer depth compositions.
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    raw_jpg = out_png.replace(".png", "_raw.jpg")

    # Use local fallback if provided and exists
    if local_fallback and os.path.exists(local_fallback):
        img_source = local_fallback
    else:
        fetched = fetch_pexels_or_pixabay_image(query, raw_jpg)
        if not fetched or not os.path.exists(raw_jpg):
            print(f"[!] Image search yielded no result for '{query}'")
            if local_fallback and os.path.exists(local_fallback):
                img_source = local_fallback
            else:
                # Generate clean high-contrast silhouette card as safety fallback
                img_source = ""
        else:
            img_source = raw_jpg

    if not img_source or not os.path.exists(img_source):
        # Create a stylized B&W icon fallback
        placeholder = Image.new("RGBA", (800, 900), (0, 0, 0, 0))
        placeholder.save(out_png)
        return out_png

    # 1. Remove background via rembg
    inp_img = Image.open(img_source).convert("RGBA")
    # Resize if extraordinarily large to prevent memory overhead
    if inp_img.width > 1400 or inp_img.height > 1400:
        inp_img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)

    if REMBG_SESSION:
        cutout_rgba = remove(inp_img, session=REMBG_SESSION)
    else:
        cutout_rgba = remove(inp_img)

    # 2. Convert RGB channels to High-Contrast Black & White while preserving Alpha
    r, g, b, alpha = cutout_rgba.split()
    gray = Image.merge("RGB", (r, g, b)).convert("L")
    gray = ImageEnhance.Contrast(gray).enhance(1.45)
    gray = ImageEnhance.Brightness(gray).enhance(1.08)
    bw_rgba = Image.merge("RGBA", (gray, gray, gray, alpha))

    # 3. Optional: Detect face & draw glowing Red Eye-Censor Bar (Winter Media 0:10 / Cosmocuts 0:15 style)
    if add_red_eyebar:
        try:
            cv_img = cv2.cvtColor(np.array(bw_rgba), cv2.COLOR_RGBA2BGRA)
            gray_np = np.array(gray)
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            if os.path.exists(cascade_path):
                face_cascade = cv2.CascadeClassifier(cascade_path)
                faces = face_cascade.detectMultiScale(gray_np, 1.1, 4)
                if len(faces) > 0:
                    for (fx, fy, fw, fh) in faces[:1]:
                        eye_y1 = fy + int(fh * 0.28)
                        eye_y2 = fy + int(fh * 0.44)
                        eye_x1 = max(0, fx - int(fw * 0.08))
                        eye_x2 = min(cv_img.shape[1], fx + int(fw * 1.08))
                        # Red bar with subtle white edge
                        cv2.rectangle(cv_img, (eye_x1, eye_y1), (eye_x2, eye_y2), (35, 25, 235, 255), -1)
                        cv2.rectangle(cv_img, (eye_x1, eye_y1), (eye_x2, eye_y2), (255, 255, 255, 255), 3)
                    bw_rgba = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA))
                else:
                    # Synthetic upper-third eye bar fallback if haarcascade missed
                    alpha_np = np.array(alpha)
                    y_indices, x_indices = np.where(alpha_np > 50)
                    if len(y_indices) > 0 and len(x_indices) > 0:
                        top_y = np.min(y_indices)
                        height = np.max(y_indices) - top_y
                        center_x = int(np.mean(x_indices))
                        bar_w = int(0.35 * (np.max(x_indices) - np.min(x_indices)))
                        eye_y1 = top_y + int(height * 0.18)
                        eye_y2 = eye_y1 + int(height * 0.07)
                        eye_x1 = max(0, center_x - bar_w // 2)
                        eye_x2 = min(cv_img.shape[1], center_x + bar_w // 2)
                        cv2.rectangle(cv_img, (eye_x1, eye_y1), (eye_x2, eye_y2), (35, 25, 235, 255), -1)
                        cv2.rectangle(cv_img, (eye_x1, eye_y1), (eye_x2, eye_y2), (255, 255, 255, 255), 3)
                        bw_rgba = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA))
        except Exception as e:
            print(f"[!] Eye bar drawing notice: {e}")

    # 4. Optional: Crisp White Sticker Stroke around alpha mask
    if add_white_stroke:
        try:
            cur_alpha = bw_rgba.split()[3]
            alpha_dilated = cur_alpha.filter(ImageFilter.MaxFilter(15))
            stroke_layer = Image.new("RGBA", bw_rgba.size, (255, 255, 255, 255))
            stroke_layer.putalpha(alpha_dilated)
            bw_rgba = Image.alpha_composite(stroke_layer, bw_rgba)
        except Exception as e:
            print(f"[!] White stroke notice: {e}")

    # 5. Optional: Jagged Torn-Paper Bottom Edge (Cosmocuts style)
    if add_torn_paper_bottom:
        try:
            arr = np.array(bw_rgba)
            h, w = arr.shape[:2]
            np.random.seed(42)
            jag = np.cumsum(np.random.randint(-3, 4, size=w))
            jag = np.clip(h - 40 + jag, h - 70, h - 10)
            for x in range(w):
                arr[jag[x]:, x, 3] = 0
                if jag[x] - 12 >= 0:
                    arr[jag[x]-12:jag[x], x] = [245, 245, 245, 255]
            bw_rgba = Image.fromarray(arr)
        except Exception as e:
            print(f"[!] Torn paper edge notice: {e}")

    bw_rgba.save(out_png)
    if os.path.exists(raw_jpg) and raw_jpg != img_source:
        try:
            os.remove(raw_jpg)
        except Exception:
            pass

    print(f"[OK] Generated B&W Collage Cutout: {out_png}")
    return out_png

def build_all_collage_cutouts(out_dir: str = "remotion_studio/public/assets"):
    """Generates the complete photographic cutout asset bundle for the 4 collage scenes."""
    os.makedirs(out_dir, exist_ok=True)

    cutouts = [
        {
            "query": "man in suit portrait",
            "file": os.path.join(out_dir, "cutout_founder_eyebar.png"),
            "add_white_stroke": True,
            "add_red_eyebar": True,
            "add_torn_paper_bottom": False,
        },
        {
            "query": "lone man standing desert",
            "file": os.path.join(out_dir, "cutout_empty_desert.png"),
            "add_white_stroke": True,
            "add_red_eyebar": False,
            "add_torn_paper_bottom": False,
        },
        {
            "query": "stressed businessman holding head",
            "file": os.path.join(out_dir, "cutout_crushed_businessman.png"),
            "add_white_stroke": True,
            "add_red_eyebar": True,
            "add_torn_paper_bottom": False,
        },
        {
            "query": "business mentor meeting executives",
            "file": os.path.join(out_dir, "cutout_veteran_mentors.png"),
            "add_white_stroke": True,
            "add_red_eyebar": False,
            "add_torn_paper_bottom": True,
            "local_fallback": "assets/broll/boardroom_veterans.jpg" if os.path.exists("assets/broll/boardroom_veterans.jpg") else ""
        },
        {
            "query": "man celebrating champagne suit",
            "file": os.path.join(out_dir, "cutout_luxury_champagne.png"),
            "add_white_stroke": True,
            "add_red_eyebar": False,
            "add_torn_paper_bottom": False,
        },
        {
            "query": "exhausted man working laptop night",
            "file": os.path.join(out_dir, "cutout_night_coder.png"),
            "add_white_stroke": True,
            "add_red_eyebar": True,
            "add_torn_paper_bottom": False,
        }
    ]

    for item in cutouts:
        create_bw_collage_cutout(
            query=item["query"],
            out_png=item["file"],
            add_white_stroke=item["add_white_stroke"],
            add_red_eyebar=item["add_red_eyebar"],
            add_torn_paper_bottom=item["add_torn_paper_bottom"],
            local_fallback=item.get("local_fallback", "")
        )

if __name__ == "__main__":
    build_all_collage_cutouts()
