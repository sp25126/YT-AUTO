import os
import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

def ease_out_quart(t: float) -> float:
    t = float(np.clip(t, 0.0, 1.0))
    return 1.0 - pow(1.0 - t, 4)

def render_live_counter_card(
    badge: str,
    target_num: int,
    suffix: str,
    headline: str,
    subtext: str,
    theme: str = "danger",  # "danger" (red) or "alpha" (emerald)
    duration: float = 4.0,
    fps: int = 30,
    out_mp4: str = "temp/broll_counter.mp4"
) -> str:
    """Renders an After-Effects style card where numbers & bars actively animate every frame."""
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    w, h = 1080, 960
    frames = int(round(duration * fps))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_mp4, fourcc, fps, (w, h))

    accent = (255, 68, 68) if theme == "danger" else (46, 247, 115)
    badge_bg = (90, 20, 25) if theme == "danger" else (18, 80, 42)

    try:
        f_num = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 86)
        f_head = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 52)
        f_badge = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 34)
        f_sub = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 30)
    except Exception:
        f_num = f_head = f_badge = f_sub = ImageFont.load_default()

    # Pre-generate floating background dust particles
    np.random.seed(42)
    particles = np.column_stack([
        np.random.randint(0, w, 35),
        np.random.randint(0, h, 35),
        np.random.uniform(1.0, 3.5, 35)
    ])

    for idx in range(frames):
        t = idx / fps
        # Entry slide-in (first 0.3s) and Exit slide-out (last 0.25s)
        if t < 0.3:
            slide = 1.0 - ease_out_quart(t / 0.3)
        elif t > (duration - 0.25):
            slide = 1.0 - ease_out_quart((duration - t) / 0.25)
        else:
            slide = 0.0

        y_off = int(-slide * 350)

        # Dark studio background with animated drifting particles
        canvas = np.full((h, w, 3), (14, 15, 20), dtype=np.uint8)
        canvas[24::48, 24::48] = (42, 45, 55)
        for p in particles:
            px = int((p[0] + idx * p[2] * 0.5) % w)
            py = int((p[1] - idx * p[2]) % h)
            cv2.circle(canvas, (px, py), int(p[2]), (70, 75, 90), -1)

        pil_img = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img, "RGBA")

        cx1, cy1, cx2, cy2 = 75, 110 + y_off, 1005, 840 + y_off
        draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=36, fill=(24, 26, 34, 245), outline=(*accent, 230), width=4)

        # Badge
        badge_text = f"[{'X' if theme == 'danger' else '✓'}] {badge.upper()}"
        draw.rounded_rectangle([cx1+45, cy1+40, cx1+480, cy1+110], radius=16, fill=(*badge_bg, 255), outline=(*accent, 255), width=2)
        draw.text((cx1+68, cy1+55), badge_text, fill=accent, font=f_badge)

        # Animated Counting Number (counts from 0 to target_num over 1.2s)
        count_prog = ease_out_quart(min(1.0, max(0.0, (t - 0.15) / 1.2)))
        curr_val = int(round(target_num * count_prog))
        draw.text((cx1+45, cy1+140), f"{curr_val}{suffix} {headline.upper()}", fill=(255, 255, 255, 255), font=f_num)

        # Subtext
        draw.text((cx1+45, cy1+265), subtext, fill=(185, 192, 210, 255), font=f_sub)

        # Animated Glowing Progress Bar
        bar_w = int(830 * count_prog * (target_num / 100.0))
        draw.rounded_rectangle([cx1+45, cy1+360, cx1+875, cy1+405], radius=14, fill=(40, 44, 56, 255))
        if bar_w > 15:
            draw.rounded_rectangle([cx1+45, cy1+360, cx1+45+bar_w, cy1+405], radius=14, fill=(*accent, 255))

        # Bottom Divider Accent Line (Separates Top B-Roll from Bottom Speaker)
        draw.rectangle([0, h-8, w, h], fill=(*accent, 255))

        writer.write(cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))

    writer.release()
    print(f"[OK] Rendered Live Counter Card ({duration:.1f}s): {out_mp4}")
    return out_mp4

def render_parallax_ai_broll(
    image_path: str,
    overlay_label: str,
    duration: float = 4.6,
    fps: int = 30,
    out_mp4: str = "temp/broll_parallax.mp4"
) -> str:
    """
    Takes an AI-generated image from Antigravity, crops it to 1080x960, 
    and animates a 2.5D Ken Burns push-in + diagonal light sweep + HUD label.
    """
    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    w, h = 1080, 960
    frames = int(round(duration * fps))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_mp4, fourcc, fps, (w, h))

    img = cv2.imread(image_path)
    if img is None:
        img = np.full((h, w, 3), (25, 30, 45), dtype=np.uint8)
    
    # Scale base image up to provide room for zooming and panning
    img = cv2.resize(img, (int(w * 1.35), int(h * 1.35)), interpolation=cv2.INTER_CUBIC)
    ih, iw = img.shape[:2]

    try:
        f_hud = ImageFont.truetype("assets/fonts/Montserrat-Black.ttf", 36)
    except Exception:
        f_hud = ImageFont.load_default()

    accent_green = (46, 247, 115)

    for idx in range(frames):
        prog = idx / max(1, frames - 1)
        # Smooth Ken Burns zoom-in from 1.0x to 1.22x
        scale = 1.0 + 0.20 * ease_out_quart(prog)
        cw, ch = int(w / scale), int(h / scale)
        cx = (iw - cw) // 2 + int(np.sin(prog * np.pi) * 20)
        cy = (ih - ch) // 2
        cropped = cv2.resize(img[cy:cy+ch, cx:cx+cw], (w, h), interpolation=cv2.INTER_LINEAR)

        # Add moving diagonal light sweep across image
        sweep_x = int(-w + prog * (w * 2.5))
        overlay = cropped.copy()
        cv2.line(overlay, (sweep_x, 0), (sweep_x - 300, h), (255, 255, 255), 120)
        frame = cv2.addWeighted(overlay, 0.12, cropped, 0.88, 0)

        # Dark HUD label for topic clarity
        pil_f = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_f, "RGBA")
        draw.rounded_rectangle([60, 60, 780, 140], radius=18, fill=(10, 12, 18, 225), outline=(*accent_green, 240), width=3)
        draw.text((85, 78), overlay_label.upper(), fill=(*accent_green, 255), font=f_hud)
        # Bottom divider line
        draw.rectangle([0, h-8, w, h], fill=(*accent_green, 255))

        writer.write(cv2.cvtColor(np.array(pil_f), cv2.COLOR_RGB2BGR))

    writer.release()
    print(f"[OK] Rendered Parallax AI B-Roll ({duration:.1f}s): {out_mp4}")
    return out_mp4

def generate_free_ai_video_wan(prompt: str, out_mp4: str = "temp/wan_broll.mp4") -> str:
    """Calls HuggingFace Free Wan2.1 Space via Gradio Client (Zero Local GPU)."""
    try:
        from gradio_client import Client
        client = Client("fffiloni/Wan2.1")
        result = client.predict(prompt=prompt, api_name="/predict")
        if result and os.path.exists(str(result)):
            import shutil
            shutil.copy(str(result), out_mp4)
            return out_mp4
    except Exception as e:
        print(f"[!] Free Wan2.1 Space busy ({e}), falling back to local Parallax B-roll.")
    return ""
