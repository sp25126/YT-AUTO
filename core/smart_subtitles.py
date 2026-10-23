import os
from typing import List, Dict, Any

def generate_dual_zone_ass(
    words: List[Dict[str, Any]],
    start_t: float,
    end_t: float,
    split_windows: List[Dict[str, float]],  # [{"start": 2.4, "end": 6.4}, ...] (relative to clip start)
    output_ass: str = "temp/smart_subs.ass"
) -> str:
    """
    Generates Dual-Zone Safe-Area Subtitles:
    - Full-Screen Mode (FullCam): Lower-third below the speaker's chin (MarginV=310)
    - Split-Screen Mode (SplitSeam): Sits right on the y=960 split border (MarginV=895) with high-contrast box
    """
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: FullCam,Montserrat Black,76,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,1,0,1,8,4,2,70,70,310,1
Style: SplitSeam,Montserrat Black,80,&H00FFFFFF&,&H0000FFFF&,&H00141010&,&HD0000000&,-1,0,0,0,100,100,1,0,3,12,0,2,70,70,895,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    emphasis = {
        "TIMING", "STARTUPS", "DIE", "DIES", "DYING", "EARLY", "LATE", "ADVISOR",
        "NETWORK", "DEVIL", "DEVIL'S", "DETAIL", "DETAILS", "90%", "CRUSHED",
        "WRONG", "ENTER", "VETERANS", "SPACE", "BUSINESS"
    }

    if not words:
        clip_words = []
    else:
        duration = end_t - start_t
        first_start = words[0].get("start", 0.0)
        is_relative = (first_start < 60.0 and start_t >= 60.0)
        if is_relative:
            clip_words = [w for w in words if 0.0 <= w["start"] <= min(duration, 33.20)]
        else:
            clip_words = [w for w in words if w["start"] >= start_t and (w["start"] - start_t) <= min(duration, 33.20)]

    lines = []
    chunk_size = 3

    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        if is_relative:
            t_s = max(0.0, chunk[0]["start"])
            t_e = max(t_s + 0.25, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = max(t_s + 0.25, chunk[-1]["end"] - start_t)

        mid_t = (t_s + t_e) / 2.0

        # Check if a top B-roll split is active at this exact second
        in_split = any(sw["start"] <= mid_t <= sw["end"] for sw in split_windows)
        style_name = "SplitSeam" if in_split else "FullCam"

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        styled_tokens = []
        for w in chunk:
            clean = w["word"].upper().strip(".,?!\"'")
            raw = w["word"].upper()
            if clean in emphasis or any(char.isdigit() for char in clean):
                styled_tokens.append(r"{\c&H0046F72B&}" + raw + r"{\c&H00FFFFFF&}")
            else:
                styled_tokens.append(raw)

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},{style_name},,0,0,0,,{' '.join(styled_tokens)}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated Dual-Zone Subtitles: {output_ass}")
    return output_ass
