from core.presets import ARCHETYPE_PRESETS

def generate_styled_ass(words, start_t, end_t, archetype="comedy_banter", output_file="captions.ass"):
    cfg = ARCHETYPE_PRESETS.get(archetype, ARCHETYPE_PRESETS["comedy_banter"])
    
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{cfg['font_name']},{cfg['font_size']},{cfg['primary_color']},{cfg['highlight_color']},{cfg['outline_color']},&H80000000,-1,0,0,0,100,100,0,{cfg['tilt_angle']},1,{cfg['outline_width']},{cfg['shadow_depth']},2,60,60,460,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    clip_words = [w for w in words if w["start"] >= start_t and w["end"] <= end_t]
    lines = []
    chunk_size = 3

    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        line_start = max(0.0, chunk[0]["start"] - start_t)
        line_end = max(0.1, chunk[-1]["end"] - start_t)

        s_fmt = f"{int(line_start//3600):01d}:{int((line_start%3600)//60):02d}:{line_start%60:05.2f}"
        e_fmt = f"{int(line_end//3600):01d}:{int((line_end%3600)//60):02d}:{line_end%60:05.2f}"

        # Build word line with pop-in bounce animation
        text_payload = ""
        for w in chunk:
            dur_cs = max(1, int((w["end"] - w["start"]) * 100))
            word_str = w['word'].upper()
            
            # For comedy/hustle: pop scale to 115% then settle to 100% on the spoken frame
            if archetype in ["comedy_banter", "hustle_alpha"]:
                anim = r"{\t(0,100,\fscx115\fscy115)\t(100,200,\fscx100\fscy100)}"
                text_payload += f"{{\\k{dur_cs}}}{anim}{word_str} "
            else:
                text_payload += f"{{\\k{dur_cs}}}{word_str} "

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},Main,,0,0,0,,{text_payload.strip()}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

def make_ass_subtitles(words, start_t, end_t, output_file="captions.ass", archetype="comedy_banter"):
    return generate_styled_ass(words, start_t, end_t, archetype=archetype, output_file=output_file)
