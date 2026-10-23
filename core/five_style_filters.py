import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

def create_top_luma_mask_png(out_png: str = "temp/top_luma_mask.png") -> str:
    """
    Replicates Style 1 (DetnsvBN1fs): A 1080x1920 alpha mask where the top 45% (y=0..820)
    is opaque white, smoothly feathering down to y=1020 (0% opacity).
    Allows blending moving HD video into the black studio space above the speaker's head!
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    w, h = 1080, 1920
    rgba = np.zeros((h, w, 4), dtype=np.uint8)

    # Top solid region (y=0..720)
    rgba[:720, :, :3] = 255
    rgba[:720, :, 3] = 220  # 86% opacity

    # Feathered region (y=720..1020)
    fade_len = 300
    for i in range(fade_len):
        y = 720 + i
        prog = 1.0 - (i / float(fade_len))
        alpha = int(220 * (prog ** 1.6))
        rgba[y, :, :3] = 255
        rgba[y, :, 3] = alpha

    cv2.imwrite(out_png, rgba)
    print(f"[OK] Generated Top Luma Mask: {out_png}")
    return out_png

def create_curved_cinema_border_png(out_png: str = "temp/curved_border.png") -> str:
    """
    Replicates Style 3 (OoayDYJKkUs): A 1080x1920 black frame with a curved-edge
    transparent cinema cutout in the center (borderRadius=68px).
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    # Cut out a rounded rectangle (margin=36px, corner radius=68px)
    draw.rounded_rectangle([36, 48, 1044, 1872], radius=68, fill=(0, 0, 0, 0), outline=(255, 255, 255, 45), width=3)
    img.save(out_png)
    print(f"[OK] Generated Curved Cinema Border: {out_png}")
    return out_png

def create_torn_newspaper_shoulder_overlay(out_png: str = "temp/newspaper_shoulders.png") -> str:
    """
    Replicates Style 5 (MoVlt-ptxIk at 0:07): Torn newspaper collage pieces framing
    the bottom-left and bottom-right shoulders of the live speaker.
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    w, h = 1080, 1920
    canvas = np.zeros((h, w, 4), dtype=np.uint8)

    np.random.seed(11)
    for x in range(w):
        left_top = int(1360 + (x * 0.70) + np.random.randint(-6, 7))
        right_top = int(1360 + ((w - x) * 0.70) + np.random.randint(-6, 7))
        top_y = min(left_top, right_top)
        if top_y < h:
            canvas[top_y:h, x] = [235, 230, 220, 245]
            # Simulated newspaper text lines
            for ty in range(top_y + 16, h, 20):
                if (x // 12) % 6 != 0:
                    canvas[ty:ty+5, x] = [40, 40, 40, 200]

    cv2.imwrite(out_png, canvas)
    print(f"[OK] Generated Torn Newspaper Shoulder Overlay: {out_png}")
    return out_png

def generate_luxury_pill_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    out_ass: str = "temp/style1_luxury.ass"
) -> str:
    """
    Replicates Style 1 (DetnsvBN1fs): Single-line center-lower captions at y=1460
    with glowing emerald/gold highlight pill around the active spoken keyword.
    """
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: LuxuryPill,Montserrat Bold,84,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H80000000&,-1,0,0,0,100,100,1,0,1,6,3,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    duration = end_t - start_t
    first_start = words[0].get("start", 0.0) if words else 0.0
    is_rel = (first_start < 60.0 and start_t >= 60.0)

    if is_rel:
        clip_words = [w for w in words if 0.0 <= w["start"] <= duration - 0.20]
    else:
        clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.20]

    lines = []
    chunk_size = 3
    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        if is_rel:
            t_s = max(0.0, chunk[0]["start"])
            t_e = min(duration, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = min(duration, chunk[-1]["end"] - start_t)

        if t_e <= t_s:
            t_e = t_s + 0.35

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        words_str = " ".join([w["word"].upper() for w in chunk[:-1]])
        hero_str = chunk[-1]["word"].upper()

        pos = r"{\an5\pos(540,1460)\t(0,60,\fscx112\fscy112)\t(60,120,\fscx100\fscy100)}"
        if words_str:
            line_text = f"{pos}{{\\c&H00D4D4D8&}}{words_str} {{\\c&H0081B910&\\b1}}{hero_str}"
        else:
            line_text = f"{pos}{{\\c&H0081B910&\\b1}}{hero_str}"

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},LuxuryPill,,0,0,0,,{line_text}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Style 1 Luxury Subtitles: {out_ass}")
    return out_ass

def generate_davinci_writeon_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    out_ass: str = "temp/style2_davinci.ass"
) -> str:
    """
    Replicates Style 2 (RXQOmQGJK34): Multi-tile staggered write-on text with stepped
    word zooms (1.0x -> 1.08x -> 1.16x) and Gaussian blur fade-in at y=1440.
    """
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DaVinci,Montserrat Black,92,&H00FFFFFF&,&H0000FFFF&,&H00111111&,&H00000000&,-1,0,0,0,100,100,1,0,1,8,4,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    duration = end_t - start_t
    first_start = words[0].get("start", 0.0) if words else 0.0
    is_rel = (first_start < 60.0 and start_t >= 60.0)

    if is_rel:
        clip_words = [w for w in words if 0.0 <= w["start"] <= duration - 0.20]
    else:
        clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.20]

    lines = []
    chunk_size = 2
    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        if is_rel:
            t_s = max(0.0, chunk[0]["start"])
            t_e = min(duration, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = min(duration, chunk[-1]["end"] - start_t)

        if t_e <= t_s:
            t_e = t_s + 0.35

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        txt = " ".join([w["word"].upper() for w in chunk])
        pos = r"{\an5\pos(540,1440)\t(0,50,\blur4\fscx112\fscy112)\t(50,110,\blur0\fscx100\fscy100)}"
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},DaVinci,,0,0,0,,{pos}{txt}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Style 2 DaVinci Subtitles: {out_ass}")
    return out_ass

def generate_pyramid_softlight_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    out_ass: str = "temp/style3_pyramid.ass"
) -> str:
    """
    Replicates Style 3 (OoayDYJKkUs): Sliding 3-word Pyramid Stack where words
    accumulate line-by-line in a translucent Soft-Light Purple & White palette at y=980.
    """
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pyramid,Montserrat Bold,78,&H20FFFFFF&,&H2000FFFF&,&H50000000&,&H00000000&,-1,0,0,0,100,100,2,0,1,4,3,5,80,80,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    duration = end_t - start_t
    first_start = words[0].get("start", 0.0) if words else 0.0
    is_rel = (first_start < 60.0 and start_t >= 60.0)

    if is_rel:
        clip_words = [w for w in words if 0.0 <= w["start"] <= duration - 0.20]
    else:
        clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.20]

    lines = []
    for i in range(0, len(clip_words), 3):
        chunk = clip_words[i:i + 3]
        if is_rel:
            group_end = min(duration, chunk[-1]["end"])
        else:
            group_end = min(duration, chunk[-1]["end"] - start_t)

        accumulated = []
        for idx, w in enumerate(chunk):
            if is_rel:
                w_start = max(0.0, w["start"])
                w_next = min(duration, chunk[idx + 1]["start"]) if idx + 1 < len(chunk) else group_end
            else:
                w_start = max(0.0, w["start"] - start_t)
                w_next = min(duration, chunk[idx + 1]["start"] - start_t) if idx + 1 < len(chunk) else group_end

            if w_next <= w_start:
                w_next = w_start + 0.25

            color = r"{\c&H15F755A8&}" if idx == len(chunk) - 1 else r"{\c&H15FFFFFF&}"
            accumulated.append(f"{color}{w['word'].upper()}")
            pyramid_text = r"\N".join(accumulated)

            s_fmt = f"{int(w_start//3600):01d}:{int((w_start%3600)//60):02d}:{w_start%60:05.2f}"
            e_fmt = f"{int(w_next//3600):01d}:{int((w_next%3600)//60):02d}:{w_next%60:05.2f}"
            lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},Pyramid,,0,0,0,,{{\\an5\\pos(540,980)\\blur2}}{pyramid_text}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Style 3 Pyramid Subtitles: {out_ass}")
    return out_ass

def generate_vox_editorial_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    chart_windows: list = None,
    out_ass: str = "temp/style4_vox.ass"
) -> str:
    """
    Replicates Style 4 (Vox Data Journalism): Editorial journalism typography
    (Playfair Display Italic + Inter ExtraBold) inside yellow/black strips at y=1520,
    suppressed during full-screen chart takeovers.
    """
    if chart_windows is None:
        chart_windows = []
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VoxEditorial,Georgia,76,&H00141413&,&H00000000&,&H00FFFFFF&,&H0000E6FF&,-1,1,0,0,100,100,1,0,3,8,0,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    duration = end_t - start_t
    first_start = words[0].get("start", 0.0) if words else 0.0
    is_rel = (first_start < 60.0 and start_t >= 60.0)

    if is_rel:
        clip_words = [w for w in words if 0.0 <= w["start"] <= duration - 0.20]
    else:
        clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.20]

    lines = []
    for i in range(0, len(clip_words), 3):
        chunk = clip_words[i:i + 3]
        if is_rel:
            t_s = max(0.0, chunk[0]["start"])
            t_e = min(duration, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = min(duration, chunk[-1]["end"] - start_t)

        mid = (t_s + t_e) / 2.0
        # Hide during full-screen charts
        if any(cw["start"] <= mid <= cw["end"] for cw in chart_windows):
            continue

        if t_e <= t_s:
            t_e = t_s + 0.35

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        txt = " ".join([w["word"].lower() for w in chunk])
        pos = r"{\an5\pos(540,1540)}"
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},VoxEditorial,,0,0,0,,{pos}{txt}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Style 4 Vox Subtitles: {out_ass}")
    return out_ass

def generate_marksoy_minimal_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    takeover_windows: list = None,
    out_ass: str = "temp/style5_marksoy.ass"
) -> str:
    """
    Replicates Style 5 (MoVlt-ptxIk): Single-word lowercase minimal captions
    ('people', 'life', 'timing') at chest level (y=1160) ONLY when the live speaker
    is on screen, hiding automatically during full-screen cream/grid cards!
    """
    if takeover_windows is None:
        takeover_windows = []
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MarkSoyWord,Montserrat,84,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,-1,0,1,3,6,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    red_words = {"die", "wrong", "late", "crushed", "devil", "90%", "fail"}
    duration = end_t - start_t
    first_start = words[0].get("start", 0.0) if words else 0.0
    is_rel = (first_start < 60.0 and start_t >= 60.0)

    if is_rel:
        clip_words = [w for w in words if 0.0 <= w["start"] <= duration - 0.20]
    else:
        clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.20]

    lines = []
    for w in clip_words:
        if is_rel:
            t_s = max(0.0, w["start"])
            t_e = max(t_s + 0.12, min(duration, w["end"]))
        else:
            t_s = max(0.0, w["start"] - start_t)
            t_e = max(t_s + 0.12, min(duration, w["end"] - start_t))

        mid = (t_s + t_e) / 2.0
        # Hide speaker captions when a full-screen kinetic typography card is active
        if any(tw["start"] <= mid <= tw["end"] for tw in takeover_windows):
            continue

        clean = w["word"].lower().strip(".,?!")
        col = r"{\c&H004444EF&}" if clean in red_words else r"{\c&H00FFFFFF&}"
        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},MarkSoyWord,,0,0,0,,{{\\an5\\pos(540,1160)}}{col}{clean}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Style 5 Mark Soy Subtitles: {out_ass}")
    return out_ass
