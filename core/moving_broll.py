import os
import cv2
import numpy as np
import subprocess
from PIL import Image, ImageDraw, ImageFont

def fetch_real_moving_broll_clip(query: str, duration: float = 2.2, out_mp4: str = "temp/stock_clip.mp4") -> str:
    """
    Downloads a real moving HD video clip matching the query using yt-dlp search
    (grabs a 2.5s action slice from Creative Commons / stock B-roll footage).
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    raw_dl = out_mp4.replace(".mp4", "_raw.mp4")
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query} stock footage no copyright",
        "-f", "bestvideo[height<=1080][ext=mp4]/best[ext=mp4]",
        "--download-sections", "*00:00:02-00:00:06",
        "-o", raw_dl,
        "--no-playlist", "--quiet"
    ]
    try:
        subprocess.run(cmd, check=True, timeout=25)
        if os.path.exists(raw_dl):
            # Crop & normalize to 1080x960 @ 30fps CFR
            subprocess.run([
                "ffmpeg", "-y", "-i", raw_dl,
                "-vf", "fps=30,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,eq=contrast=1.15:saturation=1.15",
                "-t", str(duration), "-an",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                out_mp4
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(raw_dl):
                os.remove(raw_dl)
            return out_mp4
    except Exception as e:
        print(f"[!] Stock video fetch fallback triggered for '{query}': {e}")
        if os.path.exists(raw_dl):
            try:
                os.remove(raw_dl)
            except Exception:
                pass
    return ""

def _generate_procedural_backdrop(theme: str, w: int, h: int) -> np.ndarray:
    """Generates high-contrast aesthetic backdrops when images are not pre-rendered."""
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    if "rosy" in theme.lower() or "rose" in theme.lower() or "trophy" in theme.lower():
        # Luxurious golden glow gradient with radial warmth
        for y in range(h):
            gold_ratio = 1.0 - (y / h) * 0.7
            canvas[y, :] = (int(15 * gold_ratio), int(60 * gold_ratio), int(140 * gold_ratio))
        # Draw glowing golden geometric trophy icon / aura
        cv2.circle(canvas, (w // 2, h // 2 - 40), 180, (40, 160, 255), -1)
        cv2.circle(canvas, (w // 2, h // 2 - 40), 140, (70, 200, 255), -1)
    elif "detail" in theme.lower() or "blue" in theme.lower() or "inside" in theme.lower():
        # High-tech blueprint grid with red diagnostic laser accent
        canvas[:] = (22, 18, 12)
        canvas[::40, :] = (65, 45, 25)
        canvas[:, ::40] = (65, 45, 25)
        cv2.circle(canvas, (w // 2, h // 2), 220, (30, 30, 220), 4)
        cv2.line(canvas, (w // 2 - 250, h // 2), (w // 2 + 250, h // 2), (50, 50, 255), 2)
        cv2.line(canvas, (w // 2, h // 2 - 250), (w // 2, h // 2 + 250), (50, 50, 255), 2)
    elif "network" in theme.lower() or "nodes" in theme.lower():
        # Digital node infrastructure with glowing connections
        canvas[:] = (18, 15, 12)
        np.random.seed(99)
        pts = [np.random.randint(80, w-80, 2) for _ in range(25)]
        for pt1 in pts:
            for pt2 in pts:
                if np.linalg.norm(pt1 - pt2) < 220:
                    cv2.line(canvas, tuple(pt1), tuple(pt2), (60, 140, 50), 1)
        for pt in pts:
            cv2.circle(canvas, tuple(pt), 6, (46, 247, 115), -1)
    else:
        # Sleek dark studio grid
        canvas[:] = (18, 20, 26)
        canvas[24::48, 24::48] = (45, 50, 65)
    return canvas

def render_dynamic_motion_subclip(
    img_path: str,
    hud_title: str,
    motion_style: str = "whip_zoom_in",  # "whip_zoom_in", "pan_right_fast", "tilt_up"
    accent_color: tuple = (46, 247, 115),
    duration: float = 2.0,
    fps: int = 30,
    out_mp4: str = "temp/subclip.mp4"
) -> str:
    """
    Converts an image into a high-velocity 30fps CFR motion clip with 
    whip-pan entry, strong Ken Burns movement, animated scanline, and HUD banner.
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    w, h = 1080, 960
    frames = int(round(duration * fps))
    raw_avi = out_mp4.replace(".mp4", "_raw.avi")
    writer = cv2.VideoWriter(raw_avi, cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))

    img = cv2.imread(img_path) if img_path and os.path.exists(img_path) else None
    if img is None:
        img = _generate_procedural_backdrop(hud_title, w, h)
        
    img = cv2.resize(img, (int(w * 1.45), int(h * 1.45)), interpolation=cv2.INTER_CUBIC)
    ih, iw = img.shape[:2]

    try:
        font_hud = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 40)
    except Exception:
        font_hud = ImageFont.load_default()

    for idx in range(frames):
        p = idx / max(1, frames - 1)
        # Fast cubic whip during first 0.2s, then steady dynamic motion
        whip = (1.0 - min(1.0, p / 0.18)) ** 3

        if motion_style == "whip_zoom_in":
            scale = 1.05 + 0.30 * p
            cw, ch = int(w / scale), int(h / scale)
            cx = (iw - cw) // 2 + int(whip * 180)
            cy = (ih - ch) // 2
        elif motion_style == "pan_right_fast":
            cw, ch = int(w / 1.25), int(h / 1.25)
            max_dx = iw - cw
            cx = int(max_dx * p)
            cy = (ih - ch) // 2
        else:
            cw, ch = int(w / 1.25), int(h / 1.25)
            cx = (iw - cw) // 2
            cy = int((ih - ch) * (1.0 - p))

        # Clamp crop bounds
        cx = max(0, min(iw - cw, cx))
        cy = max(0, min(ih - ch, cy))
        crop = cv2.resize(img[cy:cy+ch, cx:cx+cw], (w, h), interpolation=cv2.INTER_LINEAR)

        # Add subtle horizontal motion blur during the initial 0.18s whip-pan
        if whip > 0.05:
            kernel_size = max(3, int(whip * 25)) | 1
            crop = cv2.GaussianBlur(crop, (kernel_size, 1), 0)

        # Draw HUD Pill & Glowing Split Divider
        pil_f = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_f, "RGBA")

        # Sleek HUD Pill
        draw.rounded_rectangle([50, 55, 780, 135], radius=16, fill=(10, 12, 18, 225), outline=(*accent_color, 255), width=3)
        draw.text((75, 72), hud_title.upper(), fill=(*accent_color, 255), font=font_hud)
        # Bottom Glowing Split Divider Line
        draw.rectangle([0, h-8, w, h], fill=(*accent_color, 255))

        writer.write(cv2.cvtColor(np.array(pil_f), cv2.COLOR_RGB2BGR))

    writer.release()

    # Re-encode immediately to rock-solid H.264 30fps CFR so FFmpeg never lags!
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_avi,
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
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
    Concatenates 2-3 rapid B-roll subclips (e.g., 2.0s + 2.2s) into a single
    multi-cut B-roll sequence so the visual changes every ~2 seconds!
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    list_file = out_mp4.replace(".mp4", "_list.txt")
    with open(list_file, "w") as f:
        for clip in subclips:
            f.write(f"file '{os.path.abspath(clip).replace(chr(92), '/')}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", "fps=30,setpts=PTS-STARTPTS,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
        out_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if os.path.exists(list_file):
        try:
            os.remove(list_file)
        except Exception:
            pass

    print(f"[OK] Multi-Cut Sequence Built ({len(subclips)} cuts): {out_mp4}")
    return out_mp4
