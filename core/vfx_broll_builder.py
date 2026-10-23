import os
import cv2
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_vfx_broll_subclip(
    source_path: str,          # Can be a moving .mp4 from Pexels/Pixabay OR an image .jpg/.png
    hud_text: str,
    accent_rgb: tuple = (46, 247, 115),
    duration: float = 2.2,
    fps: int = 30,
    out_mp4: str = "temp/vfx_subclip.mp4"
) -> str:
    """
    Renders a sub-clip with sub-pixel warpAffine motion, 4-frame whip-pan blur,
    RGB chromatic aberration impact, dark vignette, and glowing HUD pill.
    Supports both moving MP4 stock videos and static images.
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    w, h = 1080, 960
    total_frames = int(round(duration * fps))
    raw_avi = out_mp4.replace(".mp4", "_temp.avi")
    writer = cv2.VideoWriter(raw_avi, cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))

    is_video = source_path.lower().endswith((".mp4", ".mov", ".webm", ".mkv")) and os.path.exists(source_path)
    cap = cv2.VideoCapture(source_path) if is_video else None
    static_img = None if is_video else (cv2.imread(source_path) if os.path.exists(source_path) else None)
    if static_img is None and not is_video:
        static_img = np.full((h, w, 3), (20, 24, 32), dtype=np.uint8)

    try:
        font_hud = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 38)
    except Exception:
        font_hud = ImageFont.load_default()

    # Pre-compute radial dark vignette mask for cinematic depth
    Y, X = np.ogrid[:h, :w]
    vignette = np.clip(1.15 - np.sqrt(((X - w/2)/(w*0.65))**2 + ((Y - h/2)/(h*0.65))**2) * 0.45, 0.55, 1.0)
    vignette_3c = np.dstack([vignette]*3).astype(np.float32)

    for idx in range(total_frames):
        prog = idx / max(1, total_frames - 1)

        if is_video:
            ret, base = cap.read()
            if not ret or base is None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, base = cap.read()
            if base is None:
                base = np.full((h, w, 3), (20, 24, 32), dtype=np.uint8)
            base = cv2.resize(base, (int(w * 1.25), int(h * 1.25)), interpolation=cv2.INTER_LINEAR)
        else:
            base = cv2.resize(static_img, (int(w * 1.35), int(h * 1.35)), interpolation=cv2.INTER_CUBIC)

        bh, bw = base.shape[:2]

        # Sub-pixel smooth floating-point zoom (1.0x -> 1.22x) + slight cinematic pan
        zoom = 1.0 + 0.22 * prog
        angle = -1.5 * (1.0 - prog)  # Subtle 1.5-degree Dutch-tilt leveling
        center = (bw / 2.0 + prog * 35.0, bh / 2.0)
        M = cv2.getRotationMatrix2D(center, angle, zoom)
        M[0, 2] += (w / 2.0) - center[0]
        M[1, 2] += (h / 2.0) - center[1]

        frame = cv2.warpAffine(base, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

        # VFX 1: First 4 frames (0.13s) Whip-Pan Directional Blur + RGB Chromatic Split!
        if idx < 4:
            blur_k = (4 - idx) * 12 + 1
            frame = cv2.GaussianBlur(frame, (blur_k, 1), 0)
            # Shift Red channel left and Blue channel right for an After-Effects RGB Glitch impact
            shift = (4 - idx) * 6
            b_ch, g_ch, r_ch = cv2.split(frame)
            r_ch = np.roll(r_ch, -shift, axis=1)
            b_ch = np.roll(b_ch, shift, axis=1)
            frame = cv2.merge([b_ch, g_ch, r_ch])

        # VFX 2: Apply Cinematic Vignette & Contrast Pop
        frame = np.clip(frame.astype(np.float32) * vignette_3c * 1.08, 0, 255).astype(np.uint8)

        # VFX 3: Animated Glass HUD Pill & Glowing Seam Bar
        pil_f = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_f, "RGBA")
        draw.rounded_rectangle([48, 52, 740, 132], radius=16, fill=(10, 12, 18, 230), outline=(*accent_rgb, 255), width=3)
        draw.text((76, 70), hud_text.upper(), fill=(*accent_rgb, 255), font=font_hud)
        draw.rectangle([0, h-8, w, h], fill=(*accent_rgb, 255))

        writer.write(cv2.cvtColor(np.array(pil_f), cv2.COLOR_RGB2BGR))

    if cap:
        cap.release()
    writer.release()

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_avi,
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
        out_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(raw_avi):
        try:
            os.remove(raw_avi)
        except Exception:
            pass

    return out_mp4

def build_multicut_broll_sequence(subclips: list, out_mp4: str) -> str:
    """
    Concatenates 2-3 rapid B-roll subclips into a single multi-cut sequence at 30fps CFR.
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    list_file = out_mp4.replace(".mp4", "_list.txt")
    with open(list_file, "w") as f:
        for clip in subclips:
            f.write(f"file '{os.path.abspath(clip).replace(chr(92), '/')}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", "fps=30,setpts=PTS-STARTPTS,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
        out_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if os.path.exists(list_file):
        try:
            os.remove(list_file)
        except Exception:
            pass

    print(f"[OK] Multi-Cut Sequence Built ({len(subclips)} cuts): {out_mp4}")
    return out_mp4
