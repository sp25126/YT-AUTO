import os
import shutil
import subprocess
from typing import List, Dict, Any
from core.dynamic_audio_curator import render_adaptive_audio_stems

def compose_10m_viral_short(
    clean_base_30fps: str,
    takeover_clips: List[Dict[str, Any]],
    ass_path: str,
    output_mp4: str = "outputs/viral_10m_short.mp4",
    duration: float = 33.40
) -> str:
    """
    Composites the 10M-View Top 1% Viral Short:
    1. Cold-Open Snap Pull-Back (1.22x -> 1.0x over first 0.6s) + Deep Sub-Boom Impact at 0:00.0
    2. Continuous Dynamic Camera Drift on Speaker segments (never static) via Zoompan
    3. Seamless Dark-Studio 3D Remotion Canvases (#090B10 matching black studio)
    4. Top 8px glowing neon progress retention bar
    5. Real organic studio foley mix (whooshes, pops, hits, tape-stop, riser) with normalize=0
    6. Safe-zone subtitles locked to lower-third with clean clamp before trailing 'AND'
    """
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    # Step 1: Render the complete master audio bed with cold-open hit, organic foley, and tone shifts
    master_audio = "temp/adaptive_master_audio.wav"
    render_adaptive_audio_stems(clean_base_30fps, duration=duration, out_audio=master_audio)

    # Step 2: Build Video Filtergraph
    # Input 0: Base speaker video (1080x1920 30fps)
    # Input 1: Master audio (adaptive_master_audio.wav)
    # Input 2..N+1: Remotion takeover clips
    inputs = ["-i", clean_base_30fps, "-i", master_audio]
    for tc in takeover_clips:
        inputs.extend(["-i", tc["file"]])

    # Dynamic camera zoom on speaker:
    # 0 to 18 frames (0.6s): Fast Cold-Open Pull-Back from 1.22x down to 1.00x
    # Frame 18+: Subtle continuous camera drift (1.04 +/- 0.02)
    zoom_expr = "if(lte(on,18), 1.22 - 0.22*(on/18), 1.04 + 0.02*sin(on*0.08))"
    filter_parts = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v_speaker_dynamic];"
    ]

    last_v = "[v_speaker_dynamic]"
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
        f"{last_v}drawbox=x=0:y=0:w=1080:h=8:color=0x090B10@0.85:t=fill,"
        f"drawbox=x=0:y=0:w='min(1080,1080*t/{duration:.2f})':h=8:color=0x2EF773:t=fill[v_bar];"
    )
    last_v = "[v_bar]"

    # Subtitles
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

    print(f"[*] Compositing 10M-View Viral Short ({duration:.2f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered 10M-View Viral Short: {output_mp4}")

    # Mirror to all output targets
    for dest in ["outputs/viral_remotion_short.mp4", "outputs/master_short_v5.mp4", "outputs/cloned_ai_short.mp4"]:
        if dest != output_mp4:
            try:
                shutil.copy2(output_mp4, dest)
                print(f"[OK] Mirrored to {dest}")
            except Exception:
                pass

    return output_mp4
