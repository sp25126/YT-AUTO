import os
from typing import List, Dict, Any

def generate_capcut_glow_ass(
    words: List[Dict[str, Any]],
    start_t: float = 2043.0,
    end_t: float = 2076.40,
    output_ass: str = "temp/capcut_glow.ass"
) -> str:
    """
    Replicates the Videotrix (4VqvzS7OQj4) & Winter Media (OwuTc_mzyo8) subtitle style:
    - Chest-level position (x=540, y=1290)
    - 2-Font stacked layout: Thin Italic Serif setup line + Giant Bold Neon-Glow keyword line
    - Dual-layer ASS rendering: Layer 0 = Soft outer neon bloom (\blur16), Layer 1 = Crisp core
    - Zero solid background boxes
    - Clamped strictly before 33.02s (eliminates trailing 'AND')
    """
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: GlowBloom,Montserrat Black,88,&H00FFFFFF&,&H0000FFFF&,&H002BF746&,&H00000000&,-1,0,0,0,100,100,1,0,1,14,0,5,60,60,60,1
Style: CrispCore,Montserrat Black,88,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H80000000&,-1,0,0,0,100,100,1,0,1,3,2,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    red_words = {"DIE", "DIES", "DYING", "WRONG", "LATE", "CRUSHED", "DEVIL", "DEVIL'S", "90%", "FAIL", "COLLAPSE"}
    green_words = {"TIMING", "EARLY", "RIGHT", "SPACE", "BUSINESS", "ADVISOR", "NETWORK", "ROSY", "DETAIL", "DETAILS", "VETERANS"}

    duration = round(end_t - start_t, 2)
    if not words:
        clip_words = []
    else:
        first_start = words[0].get("start", 0.0)
        is_relative = (first_start < 60.0 and start_t >= 60.0)
        max_rel_time = min(duration - 0.20, 33.02)
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

        s_fmt = f"{int(t_s//3600):01d}:{int((t_s%3600)//60):02d}:{t_s%60:05.2f}"
        e_fmt = f"{int(t_e//3600):01d}:{int((t_e%3600)//60):02d}:{t_e%60:05.2f}"

        # Split chunk into top setup words (Thin Italic Serif) and bottom hero word (Giant Bold Sans)
        if len(chunk) >= 2:
            top_words = " ".join([w["word"].lower().strip(".,?!\"'") for w in chunk[:-1]])
            hero_word = chunk[-1]["word"].upper().strip(".,?!\"'")
        else:
            top_words = ""
            hero_word = chunk[0]["word"].upper().strip(".,?!\"'")

        clean_hero = hero_word.strip(".,?!\"'")
        if clean_hero in red_words:
            hero_color = r"&H004B2AFF&"   # Vibrant Crimson (BGR)
            glow_color = r"&H002A15B0&"
        elif clean_hero in green_words:
            hero_color = r"&H0073F72E&"   # Neon Emerald (BGR)
            glow_color = r"&H00459E1B&"
        else:
            hero_color = r"&H0000E6FF&"   # Warm Cyber Yellow (BGR)
            glow_color = r"&H000088B0&"

        # Position at chest level (y=1290) with subtle pop scale spring
        pos_pop = r"{\an5\pos(540,1290)\t(0,65,\fscx114\fscy114)\t(65,140,\fscx100\fscy100)}"

        if top_words:
            # 2-Line Stacked: Top line in 56pt Georgia Italic, Bottom line in 96pt Montserrat Black
            core_payload = (
                f"{pos_pop}"
                r"{\fnGeorgia\fs56\b0\i1\c&H00E4E4E7&}" + top_words + r"\N"
                r"{\fnMontserrat Black\fs96\b1\i0\c" + hero_color + r"}" + hero_word
            )
            bloom_payload = (
                f"{pos_pop}"
                r"{\blur16\3c" + glow_color + r"\fnGeorgia\fs56\b0\i1}" + top_words + r"\N"
                r"{\fnMontserrat Black\fs96\b1\i0}" + hero_word
            )
        else:
            core_payload = f"{pos_pop}" + r"{\fnMontserrat Black\fs96\b1\c" + hero_color + r"}" + hero_word
            bloom_payload = f"{pos_pop}" + r"{\blur16\3c" + glow_color + r"\fnMontserrat Black\fs96\b1}" + hero_word

        # Layer 0: Soft Neon Glow Bloom behind text
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},GlowBloom,,0,0,0,,{bloom_payload}")
        # Layer 1: Crisp Core Text on top
        lines.append(f"Dialogue: 1,{s_fmt},{e_fmt},CrispCore,,0,0,0,,{core_payload}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated CapCut Glow Subtitles ({len(lines)} dialogue events): {output_ass}")
    return output_ass

if __name__ == "__main__":
    import json
    t_path = "temp/clips_test/clip_03_transcript.json"
    if os.path.exists(t_path):
        with open(t_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        generate_capcut_glow_ass(data.get("words", []))
