import json

def build_contextual_ass(
    words: list,
    beats: list,
    bg_profile: dict,
    start_t: float,
    end_t: float,
    output_file: str = "context_captions.ass"
):
    """
    Renders subtitles with per-word typographic morphing.
    beats: list of dicts: [{"start": 12.0, "end": 18.5, "tone": "shock" | "whisper" | "comedy" | "neutral"}]
    """
    # Background contrast compensation
    outline_val = 10 if bg_profile.get("visual_tone") == "bright_background" else 6
    outline_col = "&H00000000&"

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BaseTone,Montserrat ExtraBold,78,&H00FFFFFF&,&H0000FFFF&,{outline_col},&H90000000&,-1,0,0,0,100,100,0,0,1,{outline_val},3,2,60,60,480,1

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
        mid_time = chunk[0]["start"]

        # Determine prevailing tone for this chunk
        current_tone = "neutral"
        for beat in beats:
            if beat["start"] <= mid_time <= beat["end"]:
                current_tone = beat.get("tone", "neutral")
                break

        # Map tone to dynamic ASS override tags
        if current_tone == "whisper":
            tone_tags = r"{\fs64\c&H00D0D0D0&\i1\frz0}"       # Small, silver, italic
        elif current_tone == "shock":
            tone_tags = r"{\fs92\c&H0033FF33&\i0\frz0}"       # Huge, neon green, bold
        elif current_tone == "comedy":
            tone_tags = r"{\fs82\c&H0000D4FF&\i0\frz-4}"      # Tilted comic yellow
        else:
            tone_tags = r"{\fs78\c&H00FFFFFF&\i0\frz0}"       # Clean white

        s_fmt = f"{int(line_start//3600):01d}:{int((line_start%3600)//60):02d}:{line_start%60:05.2f}"
        e_fmt = f"{int(line_end//3600):01d}:{int((line_end%3600)//60):02d}:{line_end%60:05.2f}"

        karaoke_text = ""
        for w in chunk:
            dur_cs = max(1, int((w["end"] - w["start"]) * 100))
            word_str = w['word'].upper()
            
            if current_tone == "shock":
                # Explosive bounce animation on each word
                anim = r"{\t(0,100,\fscx125\fscy125)\t(100,200,\fscx100\fscy100)}"
                karaoke_text += f"{{\\k{dur_cs}}}{anim}{word_str} "
            else:
                karaoke_text += f"{{\\k{dur_cs}}}{word_str} "

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},BaseTone,,0,0,0,,{tone_tags}{karaoke_text.strip()}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Dynamic Contextual Subtitles written to {output_file}")
