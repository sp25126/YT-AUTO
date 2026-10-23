import os
from PIL import Image, ImageDraw, ImageFont

def cubic_out(t: float) -> float:
    """After Effects 'Ease Out' cubic bezier curve for snappy slide-ins."""
    t = max(0.0, min(1.0, float(t)))
    return 1.0 - pow(1.0 - t, 3)

def render_ae_ui_card_image(
    headline: str,
    metric_badge: str,
    subtext: str,
    card_type: str = "winner",  # "winner" (green glow) or "loser" (red warning)
    out_png: str = "temp/ae_card.png"
):
    """
    Renders a 1080x960 (top-half split screen) After-Effects style 
    glassmorphic UI card on dark studio grid canvas with zero watermarks.
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    w, h = 1080, 960

    # Deep charcoal studio canvas (RGB)
    bg = Image.new("RGBA", (w, h), (18, 18, 22, 255))
    draw = ImageDraw.Draw(bg)

    # Studio dot matrix grid every 40px
    for x in range(20, w, 40):
        for y in range(20, h, 40):
            draw.rectangle([x, y, x+2, y+2], fill=(55, 58, 65, 255))

    accent_rgb = (46, 247, 110) if card_type == "winner" else (255, 65, 65)
    badge_bg = (20, 85, 45) if card_type == "winner" else (95, 25, 25)

    font_path = "assets/fonts/Montserrat-Black.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/arialbd.ttf"

    font_big = ImageFont.truetype(font_path, 58)
    font_med = ImageFont.truetype(font_path, 36)
    font_sub = ImageFont.truetype(font_path, 30)

    cx1, cy1 = 80, 150
    cx2, cy2 = 1000, 780

    # 1. Drop shadow + Glassmorphic Card Body + Neon Border
    draw.rounded_rectangle([cx1+12, cy1+18, cx2+12, cy2+18], radius=32, fill=(0, 0, 0, 180))
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=32, fill=(30, 32, 40, 245), outline=(*accent_rgb, 220), width=4)

    # 2. Top Metric Pill Badge
    # Replace unicode emoji if not supported by font
    clean_badge = metric_badge.replace("❌", "[X]").replace("✅", "[✓]").replace("⚠️", "[!]")
    draw.rounded_rectangle([cx1+45, cy1+40, cx1+520, cy1+115], radius=18, fill=(*badge_bg, 255), outline=(*accent_rgb, 255), width=2)
    draw.text((cx1+65, cy1+56), clean_badge.upper(), fill=accent_rgb, font=font_med)

    # 3. Main Headline
    draw.text((cx1+45, cy1+165), headline.upper(), fill=(255, 255, 255, 255), font=font_big)

    # 4. Subtext / Proof line
    draw.text((cx1+45, cy1+275), subtext, fill=(195, 205, 220, 255), font=font_sub)

    # 5. Animated Progress Bar baseline
    draw.rounded_rectangle([cx1+45, cy1+440, cx1+875, cy1+475], radius=12, fill=(45, 48, 58, 255))
    draw.rounded_rectangle([cx1+45, cy1+440, cx1+720, cy1+475], radius=12, fill=(*accent_rgb, 255))

    bg.save(out_png)
    return out_png

def render_ae_ui_card_clip(
    headline: str,
    metric_badge: str,
    subtext: str,
    card_type: str = "winner",
    duration: float = 3.0,
    fps: int = 30,
    out_mp4: str = "temp/ae_card.mp4"
):
    """
    Renders an animated card by creating the base PNG and wrapping it with FFmpeg.
    """
    png_path = out_mp4.replace(".mp4", ".png")
    render_ae_ui_card_image(headline, metric_badge, subtext, card_type, png_path)
    import subprocess
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", png_path,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_mp4
