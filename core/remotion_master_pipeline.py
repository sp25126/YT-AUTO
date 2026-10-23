"""
core/remotion_master_pipeline.py - Orchestrates Full-Screen Remotion Takeovers & Fixed -14 LUFS Audio
Directs:
1. Four Full-Screen 1080x1920 Remotion Takeovers (Vox/RoboNuggets style):
   - Scene 1 (2.2s - 6.2s): 90% FAIL RATE Counter + Vox Bar Chart + Highlighter Sweep
   - Scene 2 (10.5s - 15.4s): Torn-Paper Comparison (Too Early vs Too Late)
   - Scene 3 (21.2s - 26.0s): Node Graph + Moving Senior Mentors HD Video Card
   - Scene 4 (28.0s - 33.4s): Outside Rosy (Yacht Video) -> Inside Devil in Details (Stressed Founder Video)
2. Full-Screen Speaker Cuts in between (0:00-0:02.2, 0:06.2-0:10.5, 0:15.4-0:21.2, 0:26.0-0:28.0)
3. Fixed Broadcast Audio Pipeline:
   - dynaudnorm + acompressor on voice
   - normalize=0 on all amix filters (eliminates the quiet-at-start bug!)
   - alimiter for solid -14 LUFS broadcast loudness
   - 0.25s audio fade-out at 33.15s (zero trailing "AND")
4. Hard Lower-Third Subtitles (\pos(540,1620)) leaving faces and Remotion cards clear.
"""

import os
import sys
import json
import subprocess

sys.path.insert(0, os.path.abspath("."))
from core.fullscreen_remotion_composer import compose_fullscreen_remotion_short

def generate_remotion_subs(
    words: list,
    start_t: float = 2043.0,
    end_t: float = 2076.40,
    output_ass: str = "temp/remotion_subs.ass"
) -> str:
    os.makedirs(os.path.dirname(output_ass) or ".", exist_ok=True)
    duration = round(end_t - start_t, 2)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VoxSub,Montserrat Black,76,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,1,0,1,9,5,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    power_words = {
        "TIMING", "STARTUPS", "DIE", "DIES", "DYING", "EARLY", "LATE",
        "ADVISOR", "NETWORK", "ROSY", "DEVIL", "DEVIL'S", "DETAIL", "DETAILS",
        "WRONG", "ENTER", "VETERANS", "SPACE", "BUSINESS", "90%", "CRUSHED"
    }

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

        pos_tag = r"{\an5\pos(540,1620)}"
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
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},VoxSub,,0,0,0,,{pos_tag}{bounce}{' '.join(tokens)}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

    print(f"[OK] Generated Vox Subtitles ({len(lines)} lines): {output_ass}")
    return output_ass

from core.cinema_composer import compose_10m_viral_short

def run_remotion_master(
    source_video: str = "inputs/startup_raj_shamani.mp4",
    start_t: float = 2043.0,
    end_t: float = 2076.40,
    output_mp4: str = "outputs/viral_remotion_short.mp4"
) -> str:
    duration = round(end_t - start_t, 2)
    clean_base = "temp/clean_base_30fps.mp4"

    # Step 1: Ensure clean base exists
    if not os.path.exists(clean_base):
        print(f"[*] Pre-slicing clean 30fps CFR base: {clean_base}...")
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(start_t), "-t", str(duration),
            "-i", source_video,
            "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.12:saturation=1.10",
            "-r", "30", "-fps_mode", "cfr",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            clean_base
        ], check=True)

    # Step 2: Define Takeover Windows
    takeover_clips = [
        {"file": "temp/remotion_s1.mp4", "start": 2.20, "end": 6.20},
        {"file": "temp/remotion_s2.mp4", "start": 10.50, "end": 15.40},
        {"file": "temp/remotion_s3.mp4", "start": 21.20, "end": 26.00},
        {"file": "temp/remotion_s4.mp4", "start": 28.00, "end": 33.40}
    ]

    # Step 3: Load transcript and build subtitles
    transcript_file = "temp/clips_test/clip_03_transcript.json"
    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as f:
            tdata = json.load(f)
        raw_words = tdata.get("words", [])
    else:
        raw_words = []

    from core.capcut_glow_subs import generate_capcut_glow_ass
    ass_path = generate_capcut_glow_ass(
        words=raw_words,
        start_t=start_t,
        end_t=end_t,
        output_ass="temp/capcut_glow.ass"
    )

    # Step 4: Run CapCut / Premiere Pro Master Compositor
    from core.capcut_master_composer import render_capcut_pro_short
    return render_capcut_pro_short(
        clean_base_30fps=clean_base,
        takeover_clips=takeover_clips,
        ass_path=ass_path,
        output_mp4=output_mp4,
        duration=duration
    )

if __name__ == "__main__":
    run_remotion_master()
