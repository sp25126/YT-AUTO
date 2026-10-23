import os
from core.pro_utils import clean_spoken_words

def generate_pro_subtitles(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    out_ass: str = "temp/pro_subs.ass"
) -> str:
    """
    Generates high-impact, readable subtitles placed at chest/lower-third level (\\pos(540,1480))
    over the smooth feathered bottom gradient.
    - Setup line: 68pt Crisp White
    - Hero keyword: 108pt Montserrat Black with pop-scale bounce
    - Trigger colors: Bright Crimson (&H004C2EFF&), Bright Emerald (&H0081B910&), Gold (&H0000E6FF&)
    - Zero horizontal drawbox seam, zero stutter mistakes ('net.' -> 'NETWORK').
    """
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    words = clean_spoken_words(words)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ProGlow,Montserrat Black,102,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,1,0,1,10,6,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    red_triggers = {"DIE", "DIES", "WRONG", "LATE", "CRUSHED", "DEVIL", "DEVIL'S", "90%", "FAIL", "FAILURE", "DEATHS"}
    green_triggers = {"TIMING", "EARLY", "RIGHT", "SPACE", "BUSINESS", "ADVISOR", "NETWORK", "ROSY", "DETAIL", "DETAILS", "VETERANS", "VETERAN"}

    if not words:
        clip_words = []
        duration = end_t - start_t
        is_relative = False
    else:
        first_start = words[0].get("start", 0.0)
        is_relative = (first_start < 60.0 and start_t >= 60.0)
        duration = round(end_t - start_t, 2)
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
            t_e = t_s + 0.35

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        # Clean "a advisor" -> "AN ADVISOR"
        chunk_clean = []
        for idx, w in enumerate(chunk):
            w_text = w["word"].strip()
            if w_text.lower() == "a" and idx + 1 < len(chunk) and "advisor" in chunk[idx + 1]["word"].lower():
                chunk_clean.append("AN")
            elif "net" in w_text.lower() and idx > 0 and "advisor" in chunk[idx - 1]["word"].lower():
                chunk_clean.append("NETWORK")
            else:
                chunk_clean.append(w_text.upper())

        if len(chunk_clean) >= 2:
            setup = " ".join(chunk_clean[:-1])
            hero = chunk_clean[-1]
        else:
            setup = ""
            hero = chunk_clean[0]

        clean_h = hero.strip(".,?!\"'")
        if clean_h in red_triggers or any(c.isdigit() for c in clean_h):
            h_col = "&H004C2EFF&"  # Bright Crimson
        elif clean_h in green_triggers:
            h_col = "&H0081B910&"  # Bright Emerald
        else:
            h_col = "&H0000E6FF&"  # Bright Gold

        pos = r"{\an5\pos(540,1480)\t(0,60,\fscx115\fscy115)\t(60,130,\fscx100\fscy100)}"
        if setup:
            text = f"{pos}{{\\fs68\\c&H00FFFFFF&}}{setup}\\N{{\\fs108\\c{h_col}}}{hero}"
        else:
            text = f"{pos}{{\\fs112\\c{h_col}}}{hero}"

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},ProGlow,,0,0,0,,{text}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated High-Impact Subtitles ({len(lines)} lines): {out_ass}")
    return out_ass
