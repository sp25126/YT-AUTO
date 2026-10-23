import os
import shutil
import subprocess
from typing import List, Dict, Any
from core.dynamic_audio_curator import render_adaptive_audio_stems

def compose_fullscreen_remotion_short(
    clean_base_30fps: str,      # Pre-sliced 33.40s 1080x1920 30fps speaker clip
    takeover_clips: List[Dict[str, Any]],       # [{"file": "temp/remotion_s1.mp4", "start": 2.2, "end": 6.2}, ...]
    ass_path: str,
    output_mp4: str = "outputs/viral_remotion_short.mp4",
    duration: float = 33.40
) -> str:
    """
    Composites Full-Screen 1080x1920 Remotion Animations directly over the timeline
    during visualization moments (returning to full-screen speaker in between)
    with adaptive tone-shifting audio bed (Hype Synth -> Vinyl Stop -> Analytical Groove -> Tension Riser)
    and collision-free subtitles.
    """
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    # 1. Generate adaptive tone-shifting audio bed (-14 LUFS leveled)
    master_audio = "temp/adaptive_master_audio.wav"
    render_adaptive_audio_stems(clean_base_30fps, duration=duration, out_audio=master_audio)

    # 2. Build Video Overlay Filtergraph
    # Base = 1080x1920 Speaker. When a Remotion scene is active, it takes over the FULL 1080x1920 screen!
    inputs = ["-i", clean_base_30fps, "-i", master_audio]
    for tc in takeover_clips:
        inputs.extend(["-i", tc["file"]])

    filter_parts = ["[0:v]fps=30,setpts=PTS-STARTPTS[v_base];"]
    last_v = "[v_base]"

    for idx, tc in enumerate(takeover_clips):
        in_idx = 2 + idx
        r_label = f"[rem_{idx}]"
        next_v = f"[v_layer_{idx}]"
        filter_parts.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+({tc['start']:.2f}/TB){r_label};"
            f"{last_v}{r_label}overlay=0:0:enable='between(t,{tc['start']:.2f},{tc['end']:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v

    # Retention Bar: Top 8px glowing neon bar along top edge
    filter_parts.append(
        f"{last_v}drawbox=x=0:y=0:w=1080:h=8:color=0x10141C@0.85:t=fill,"
        f"drawbox=x=0:y=0:w='min(1080,1080*t/{duration:.2f})':h=8:color=0x2EF773:t=fill[v_bar];"
    )
    last_v = "[v_bar]"

    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    filter_parts.append(f"{last_v}subtitles=filename='{clean_ass}':fontsdir='assets/fonts'[v_out];")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[v_out]",
        "-map", "1:a",
        "-t", str(duration),
        "-r", "30", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-threads", "2",
        output_mp4
    ]

    print(f"[*] Rendering Full-Screen Remotion Short ({duration:.2f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered Full-Screen Remotion Short with Adaptive Audio: {output_mp4}")

    # Mirror to cloned_ai_short.mp4 and master_short_v5.mp4
    for dest in ["outputs/cloned_ai_short.mp4", "outputs/master_short_v5.mp4"]:
        if dest != output_mp4:
            try:
                shutil.copy2(output_mp4, dest)
                print(f"[OK] Mirrored to {dest}")
            except Exception:
                pass

    return output_mp4

