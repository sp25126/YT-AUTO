import os
import shutil
import subprocess
from typing import List, Dict, Any
from core.dynamic_audio_curator import render_adaptive_audio_stems

def render_capcut_pro_short(
    clean_base_30fps: str,
    takeover_clips: List[Dict[str, Any]],
    ass_path: str,
    output_mp4: str = "outputs/capcut_pro_short.mp4",
    duration: float = 33.40
) -> str:
    """
    Composites the CapCut / Premiere Pro Collage Short:
    1. Dynamic Speaker Zoom (1.22x -> 1.00x cold-open pull-back via zoompan + subtle drift)
    2. Deep Bottom Vignette Gradient over speaker's lower chest (y=1180..1920) so chest-level subtitles pop
    3. Seamless 3-Layer Depth Remotion Scenes (B&W cutouts + midground metallic text + halftone orbs)
    4. Top 8px Glowing Neon Retention Bar
    5. Dual-Layer 2-Font Glow Subtitles at Chest-Level (y=1290)
    6. Organic Foley Studio Audio Mix (-14.1 dB LUFS with normalize=0)
    """
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    # 1. Render the complete adaptive audio bed with organic foley & cold-open hit
    master_audio = "temp/adaptive_master_audio.wav"
    render_adaptive_audio_stems(clean_base_30fps, duration=duration, out_audio=master_audio)

    # 2. Build Video Filtergraph
    inputs = ["-i", clean_base_30fps, "-i", master_audio]
    for tc in takeover_clips:
        inputs.extend(["-i", tc["file"]])

    # Dynamic camera zoom on speaker + Bottom Black Vignette Gradient (Cosmocuts 0:08 style)
    # The vignette darkens y=1180..1920 smoothly so chest-level glowing subtitles pop with 100% contrast!
    zoom_expr = "if(lte(on,18), 1.22 - 0.22*(on/18), 1.04 + 0.02*sin(on*0.08))"
    filter_parts = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        f"drawbox=x=0:y=1180:w=1080:h=740:color=black@0.65:t=fill[v_speaker_vig];"
    ]

    last_v = "[v_speaker_vig]"
    for idx, tc in enumerate(takeover_clips):
        in_idx = 2 + idx
        c_label = f"[col_{idx}]"
        next_v = f"[v_layer_{idx}]"
        filter_parts.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+({tc['start']:.2f}/TB){c_label};"
            f"{last_v}{c_label}overlay=0:0:enable='between(t,{tc['start']:.2f},{tc['end']:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v

    # Retention Bar: Top 8px glowing neon bar along top edge
    filter_parts.append(
        f"{last_v}drawbox=x=0:y=0:w=1080:h=8:color=0x050608@0.85:t=fill,"
        f"drawbox=x=0:y=0:w='min(1080,1080*t/{duration:.2f})':h=8:color=0x2EF773:t=fill[v_bar];"
    )
    last_v = "[v_bar]"

    # Burn 2-Font Chest-Level Neon Glow Subtitles on top
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

    print(f"[*] Rendering CapCut Pro Collage Short ({duration:.2f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered CapCut Pro Collage Short: {output_mp4}")

    # Mirror to all output targets
    for dest in ["outputs/viral_remotion_short.mp4", "outputs/master_short_v5.mp4", "outputs/cloned_ai_short.mp4"]:
        if dest != output_mp4:
            try:
                shutil.copy2(output_mp4, dest)
                print(f"[OK] Mirrored to {dest}")
            except Exception:
                pass

    return output_mp4
