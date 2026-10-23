import os
import subprocess
from typing import List, Dict, Any

def compose_pro_hybrid_short(
    source_video: str,
    start_t: float,
    end_t: float,
    broll_inserts: List[Dict[str, Any]],  # [{"file": "temp/b1.mp4", "start": 2.4, "end": 6.4}, ...]
    ass_path: str,
    output_mp4: str = "outputs/cloned_ai_short.mp4",
    bgm_path: str = "assets/music/dark_synth_drive.mp3"
) -> str:
    """
    Renders the Pro Hybrid Short with:
    - True Split-Reframing (crop=1080:960:0:140 shifted to y=960 during B-roll so face is 100% visible)
    - 3-Frame White Luma Flash VFX on entries and exits
    - Multi-Stem Audio mixing (Broadcast Voice, Ducked BGM, Entry Whoosh + Hit, Exit Swoosh)
    - Dual-Zone safe-area ASS subtitles
    """
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    os.makedirs("temp/pro_build", exist_ok=True)
    duration = end_t - start_t

    # 1. Pre-extract clean source clip via fast stream-copy
    clean_source = "temp/pro_build/clean_source.mp4"
    print(f"[*] Pre-extracting source clip ({start_t}s - {end_t}s, {duration:.1f}s)...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_t), "-t", str(duration),
        "-i", source_video, "-c", "copy", clean_source
    ], check=True)

    # 2. Prepare Base Inputs
    sfx_whoosh = "assets/sfx/whoosh.wav"
    sfx_hit = "assets/sfx/hit.wav"
    sfx_pop = "assets/sfx/pop.wav"
    has_bgm = os.path.exists(bgm_path)

    inputs = ["-i", clean_source]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
    inputs.extend(["-i", sfx_whoosh, "-i", sfx_hit, "-i", sfx_pop])

    broll_base_idx = 5 if has_bgm else 4
    for b in broll_inserts:
        inputs.extend(["-itsoffset", f"{b['start']:.2f}", "-i", b["file"]])

    # 3. Video Filtergraph: Full-screen vs Face-Centered Bottom Split
    # [0:v] is 1920x1080. Crop 9:16 slice first (608:1080), then upscale to 1080:1920
    filter_chain = [
        "[0:v]crop=608:1080:(in_w-608)/2:0,scale=1080:1920,"
        "eq=contrast=1.14:saturation=1.12:brightness=-0.01,unsharp=5:5:1.1:5:5:0.0,"
        "split=2[v_full_raw][v_for_split];",
        # Crop head & shoulders from upper section (0 to 960 with offset y=140)
        "[v_for_split]crop=1080:960:0:140[v_face_bottom];"
    ]

    # Shift face to bottom half (y=960) whenever ANY B-roll is active
    split_enable_expr = "+".join([f"between(t,{b['start']:.2f},{b['end']:.2f})" for b in broll_inserts])
    filter_chain.append(
        f"[v_full_raw][v_face_bottom]overlay=0:960:enable='{split_enable_expr}'[v_reframed];"
    )

    # Overlay each top B-roll clip (1080x960) at y=0
    last_v = "[v_reframed]"
    for idx, b in enumerate(broll_inserts):
        in_idx = broll_base_idx + idx
        next_v = f"[v_broll_{idx}]"
        filter_chain.append(
            f"{last_v}[{in_idx}:v]overlay=0:0:enable='between(t,{b['start']:.2f},{b['end']:.2f})'{next_v};"
        )
        last_v = next_v

    # 4. 3-Frame White Camera Flash VFX at every B-Roll Entry & Exit timestamp
    flash_times = []
    for b in broll_inserts:
        flash_times.append(f"between(t,{b['start']:.2f},{b['start']+0.09:.2f})")
        flash_times.append(f"between(t,{b['end']-0.08:.2f},{b['end']:.2f})")
    flash_expr = "+".join(flash_times)

    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    filter_chain.append(
        f"{last_v}eq=eval=frame:brightness='if({flash_expr},0.32,0.0)',"
        f"subtitles=filename='{clean_ass}':fontsdir='assets/fonts'[v_out];"
    )

    # 5. Multi-Stem Audio: Broadcast Voice + Ducked BGM + Entry Whoosh/Hit + Exit Swoosh
    audio_branches = ["[voice_clean]"]
    filter_chain.append(
        "[0:a]highpass=f=85,acompressor=threshold=-16dB:ratio=3:attack=10:release=100:makeup=4dB[voice_clean];"
    )

    whoosh_idx = 2 if has_bgm else 1
    hit_idx = 3 if has_bgm else 2
    pop_idx = 4 if has_bgm else 3

    if has_bgm:
        filter_chain.append("[1:a]volume=0.11[bgm_ducked];")
        audio_branches.append("[bgm_ducked]")

    sfx_counter = 0
    for b in broll_inserts:
        entry_ms = max(0, int(b["start"] * 1000))
        exit_ms = max(0, int((b["end"] - 0.15) * 1000))

        w_in = f"[win_{sfx_counter}]"
        h_in = f"[hin_{sfx_counter}]"
        p_out = f"[pout_{sfx_counter}]"

        filter_chain.append(f"[{whoosh_idx}:a]adelay={entry_ms}|{entry_ms},volume=0.48{w_in};")
        filter_chain.append(f"[{hit_idx}:a]adelay={entry_ms}|{entry_ms},volume=0.40{h_in};")
        filter_chain.append(f"[{pop_idx}:a]adelay={exit_ms}|{exit_ms},volume=0.38{p_out};")
        audio_branches.extend([w_in, h_in, p_out])
        sfx_counter += 1

    filter_chain.append(
        f"{''.join(audio_branches)}amix=inputs={len(audio_branches)}:duration=first:dropout_transition=0[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_chain),
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-threads", "2",
        output_mp4
    ]

    print(f"\n[*] Rendering Master Hybrid Short ({duration:.1f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Master Hybrid Short Rendered: {output_mp4}")
    return output_mp4
