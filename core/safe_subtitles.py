import os
from typing import List, Dict, Any

def generate_collision_free_ass(
    words: List[Dict[str, Any]],
    start_t: float = 2043.0,
    end_t: float = 2076.40,
    takeover_windows: List[Dict[str, float]] = None,
    output_ass: str = "temp/collision_free_subs.ass"
) -> str:
    """
    Lower-Third Safe Zone Subtitle Engine:
    - During Full-Screen Takeovers: Locked strictly to y=1740 (\\pos(540,1740)) to eliminate badge collision.
    - During Full-Screen Speaker Shots: Locked to lower third at y=1560 (\\pos(540,1560)) below chin.
    - Clamped strictly at 33.02s before trailing "AND".
    """
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)
    if takeover_windows is None:
        takeover_windows = [
            {"start": 2.20, "end": 6.20},
            {"start": 10.50, "end": 15.40},
            {"start": 21.20, "end": 26.00},
            {"start": 28.00, "end": 33.40}
        ]

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SpeakerSub,Montserrat Black,76,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,1,0,1,8,4,5,60,60,60,1
Style: TakeoverSub,Montserrat Black,74,&H00FFFFFF&,&H0000FFFF&,&H00141010&,&HD0000000&,-1,0,0,0,100,100,1,0,3,12,0,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    emphasis = {
        "TIMING", "STARTUPS", "DIE", "DIES", "DYING", "EARLY", "LATE",
        "ADVISOR", "NETWORK", "ROSY", "DEVIL", "DEVIL'S", "DETAIL", "DETAILS",
        "WRONG", "ENTER", "VETERANS", "SPACE", "BUSINESS", "90%", "CRUSHED", "COLLAPSE"
    }

    duration = round(end_t - start_t, 2)
    if not words:
        clip_words = []
    else:
        first_start = words[0].get("start", 0.0)
        is_relative = (first_start < 60.0 and start_t >= 60.0)
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
        is_takeover = any(w["start"] <= mid_t <= w["end"] for w in takeover_windows)

        # Position captions at y=1740 (well below badges) during takeovers; y=1560 on talking-head shots
        pos_tag = r"{\an5\pos(540,1740)}" if is_takeover else r"{\an5\pos(540,1560)}"
        style = "TakeoverSub" if is_takeover else "SpeakerSub"

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        styled = []
        for w in chunk:
            clean = w["word"].upper().strip(".,?!\"'")
            raw = w["word"].upper()
            if clean in emphasis or any(c.isdigit() for c in clean):
                styled.append(r"{\c&H0073F72E&\fscx114\fscy114}" + raw + r"{\c&H00FFFFFF&\fscx100\fscy100}")
            else:
                styled.append(raw)

        pop = r"{\t(0,60,\fscx112\fscy112)\t(60,130,\fscx100\fscy100)}"
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},{style},,0,0,0,,{pos_tag}{pop}{' '.join(styled)}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated Safe Zone Subtitles ({len(lines)} lines): {output_ass}")
    return output_ass

if __name__ == "__main__":
    import json
    with open("temp/clips_test/clip_03_transcript.json", "r", encoding="utf-8") as f:
        words = json.load(f).get("words", [])
    generate_collision_free_ass(words, 2043.0, 2076.40)
