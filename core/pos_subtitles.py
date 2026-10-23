import os
from typing import List, Dict, Any

def generate_pos_locked_ass(
    words: List[Dict[str, Any]],
    start_t: float,
    end_t: float,
    split_windows: List[Dict[str, float]],  # [{"start": 2.4, "end": 6.0}, ...]
    output_ass: str = "temp/locked_subs.ass"
) -> str:
    """
    Hard-Coordinate Subtitle Engine:
    - Split-Screen Mode: Locked to split border seam at y=960 using {\an5\pos(540,960)}
    - Full-Screen Mode: Locked to lower-third below chin at y=1580 using {\an5\pos(540,1580)}
    - Words strictly clamped to avoid any trailing text after "detail."
    - Dynamic kinetic pop bounce and neon emerald keyword highlighting
    """
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: FullLower,Montserrat Black,78,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,1,0,1,9,5,5,60,60,60,1
Style: SplitCenter,Montserrat Black,76,&H00FFFFFF&,&H0000FFFF&,&H00141010&,&HD0000000&,-1,0,0,0,100,100,1,0,3,14,0,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    power_words = {
        "TIMING", "STARTUPS", "DIE", "DIES", "DYING", "EARLY", "LATE",
        "ADVISOR", "NETWORK", "ROSY", "DEVIL", "DEVIL'S", "DETAIL", "DETAILS",
        "WRONG", "ENTER", "VETERANS", "SPACE", "BUSINESS", "90%", "CRUSHED"
    }

    duration = round(end_t - start_t, 2)
    if not words:
        clip_words = []
    else:
        first_start = words[0].get("start", 0.0)
        is_relative = (first_start < 60.0 and start_t >= 60.0)
        
        # Strictly clamp words: end right after "...in the detail." (33.02s) and BEFORE "AND" (33.68s)
        max_rel_time = min(duration - 0.20, 33.20)
        if is_relative:
            clip_words = [w for w in words if 0.0 <= w["start"] <= max_rel_time]
        else:
            clip_words = [w for w in words if start_t <= w["start"] and (w["start"] - start_t) <= max_rel_time]

    lines = []
    chunk_size = 3

    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        if is_relative:
            t_s = max(0.0, chunk[0]["start"])
            t_e = min(duration, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = min(duration, chunk[-1]["end"] - start_t)

        if t_e <= t_s:
            t_e = t_s + 0.30

        mid_t = (t_s + t_e) / 2.0

        # Check if split-screen is active at this moment
        in_split = any(sw["start"] <= mid_t <= sw["end"] for sw in split_windows)
        if in_split:
            style = "SplitCenter"
            pos_tag = r"{\an5\pos(540,960)}"   # Locked exactly to the split border seam
        else:
            style = "FullLower"
            pos_tag = r"{\an5\pos(540,1580)}"  # Locked to lower-third below chin, off speaker's face!

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        tokens = []
        for w in chunk:
            clean = w["word"].upper().strip(".,?!\"'")
            raw = w["word"].upper()
            if clean in power_words or any(c.isdigit() for c in clean):
                tokens.append(r"{\c&H0073F72E&\fscx116\fscy116}" + raw + r"{\c&H00FFFFFF&\fscx100\fscy100}")
            else:
                tokens.append(raw)

        bounce = r"{\t(0,65,\fscx114\fscy114)\t(65,140,\fscx100\fscy100)}"
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},{style},,0,0,0,,{pos_tag}{bounce}{' '.join(tokens)}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated Hard \\pos(x,y) Subtitles ({len(lines)} lines): {output_ass}")
    return output_ass
