import os

def generate_sabri_subtitles(words: list, start_t: float, end_t: float, output_ass: str = "temp/sabri_subs.ass"):
    """
    Creates Sabri Suby style center-stacked dynamic subtitles:
    - Clean heavy white sans with deep drop shadow at center split line (MarginV=840)
    - Scale pop bounce on every phrase
    - Electric Neon Green / Gold pop highlights behind numbers & power triggers
    """
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SabriClean,Montserrat Black,84,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H95000000&,-1,0,0,0,100,100,1,0,1,9,5,2,70,70,840,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    power_triggers = {
        "90%", "FAIL", "FAILS", "FAILED", "BRUTAL", "RUTHLESS", "TIMING", "TIME",
        "CRUSH", "CONQUER", "MILLION", "BILLION", "NEVER", "SECRET", "CHEAT",
        "STARTUP", "STARTUPS", "DIE", "DIES", "DYING", "WRONG", "DEVIL", "DEVIL'S", "DETAIL"
    }
    
    if not words:
        clip_words = []
    else:
        duration = end_t - start_t
        first_start = words[0].get("start", 0.0)
        # Check if words are already relative (start < 60 while start_t > 60)
        if first_start < 60.0 and start_t >= 60.0:
            is_relative = True
            clip_words = [w for w in words if 0.0 <= w["start"] <= duration]
        else:
            is_relative = False
            clip_words = [w for w in words if w["start"] >= start_t and w["end"] <= end_t]

    lines = []
    chunk_size = 3  # 2-3 words max so text is huge and readable on mobile feeds

    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        if is_relative:
            t_s = max(0.0, chunk[0]["start"])
            t_e = max(t_s + 0.3, chunk[-1]["end"])
        else:
            t_s = max(0.0, chunk[0]["start"] - start_t)
            t_e = max(t_s + 0.3, chunk[-1]["end"] - start_t)

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        formatted_words = []
        for w in chunk:
            clean_w = w["word"].upper().strip(".,?!\"'")
            raw_w = w["word"].upper()
            if clean_w in power_triggers or any(char.isdigit() for char in clean_w):
                # Electric Neon Green highlight for power words and numbers
                formatted_words.append(r"{\c&H0046F72B&}" + raw_w + r"{\c&H00FFFFFF&}")
            else:
                formatted_words.append(raw_w)

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},SabriClean,,0,0,0,,{' '.join(formatted_words)}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Sabri Subtitles: {output_ass}")
    return output_ass
