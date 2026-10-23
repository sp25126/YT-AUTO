import os
import subprocess
from typing import List, Dict, Any

def compose_zero_lag_short(
    source_video: str,
    start_t: float,
    end_t: float,          # Clamped to 33.85s right after "in the detail."
    broll_windows: List[Dict[str, Any]],   # [{"file": "temp/seq1.mp4", "start": 2.4, "end": 6.0}, ...]
    ass_path: str,
    output_mp4: str = "outputs/cloned_ai_short.mp4",
    bgm_path: str = "assets/music/dark_synth_drive.mp3"
) -> str:
    """
    Renders butter-smooth 30fps CFR video with:
    - Zero framesync lag: internal PTS shifting (setpts=PTS-STARTPTS+(START/TB)) with eof_action=pass
    - True face reframing (crop=1080:960:0:140 shifted to y=960 during B-roll)
    - Dual-Zone safe-area ASS captions (MarginV=310 fullcam, MarginV=895 splitseam)
    - Full multi-stem audio design with ducked BGM, entry whoosh/hit, mid-sequence cut pops, and exit swooshes
    - Exact sentence clamping at 33.85s with 0.25s audio fade-out
    """
    duration = round(end_t - start_t, 2)
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    os.makedirs("temp/pro_build", exist_ok=True)

    # 1. Pre-extract clean source clip via fast stream-copy
    clean_source = "temp/pro_build/clean_source.mp4"
    print(f"[*] Pre-extracting clean source clip ({start_t:.2f}s - {end_t:.2f}s, duration: {duration:.2f}s)...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_t), "-t", str(duration),
        "-i", source_video, "-c", "copy", clean_source
    ], check=True)

    # 2. Setup inputs
    sfx_whoosh = "assets/sfx/whoosh.wav"
    sfx_hit = "assets/sfx/hit.wav"
    sfx_pop = "assets/sfx/pop.wav"
    has_bgm = os.path.exists(bgm_path)

    inputs = ["-i", clean_source]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
    inputs.extend(["-i", sfx_whoosh, "-i", sfx_hit, "-i", sfx_pop])

    broll_base_idx = 5 if has_bgm else 4
    for b in broll_windows:
        inputs.extend(["-i", b["file"]])

    # 3. Normalize main video to rock-solid 30fps CFR and create fullcam & face-split streams
    filter_parts = [
        "[0:v]fps=30,setpts=PTS-STARTPTS,crop=608:1080:(in_w-608)/2:0,scale=1080:1920,"
        "eq=contrast=1.14:saturation=1.12:brightness=-0.01,unsharp=5:5:1.0:5:5:0.0,"
        "split=2[v_full_cfr][v_for_bottom];",
        "[v_for_bottom]crop=1080:960:0:140[v_face_bottom];"
    ]

    # 4. Place speaker's face in bottom half (y=960) ONLY when a B-roll window is active
    split_expr = "+".join([f"between(t,{b['start']:.2f},{b['end']:.2f})" for b in broll_windows])
    filter_parts.append(
        f"[v_full_cfr][v_face_bottom]overlay=0:960:enable='{split_expr}':eof_action=pass[v_base_split];"
    )

    # 5. Shift each B-roll clip's PTS to its exact start timestamp and overlay at y=0
    last_v = "[v_base_split]"
    for idx, b in enumerate(broll_windows):
        in_idx = broll_base_idx + idx
        b_label = f"[broll_pts_{idx}]"
        next_v = f"[v_comp_{idx}]"
        filter_parts.append(
            f"[{in_idx}:v]fps=30,setpts=PTS-STARTPTS+({b['start']:.2f}/TB)[broll_pts_{idx}];"
            f"{last_v}{b_label}overlay=0:0:enable='between(t,{b['start']:.2f},{b['end']:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v

    # 6. Burn dual-zone captions cleanly (No full-frame gray brightness flash!)
    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    filter_parts.append(f"{last_v}subtitles=filename='{clean_ass}':fontsdir='assets/fonts'[v_out];")

    # 7. Audio Mix: Broadcast Voice + Ducked BGM + Multi-Stem Whooshes & Mid-Sequence Cut Pops
    fade_start = max(0.0, duration - 0.25)
    filter_parts.append(
        "[0:a]aresample=async=1,highpass=f=85,acompressor=threshold=-16dB:ratio=3:attack=10:release=100:makeup=4dB[voice_pro];"
    )

    audio_stems = ["[voice_pro]"]
    whoosh_idx = 2 if has_bgm else 1
    hit_idx = 3 if has_bgm else 2
    pop_idx = 4 if has_bgm else 3

    if has_bgm:
        filter_parts.append("[1:a]volume=0.11[bgm_low];")
        audio_stems.append("[bgm_low]")

    sfx_id = 0
    for b in broll_windows:
        t_in_ms = max(0, int(b["start"] * 1000))
        t_mid_ms = max(0, int(((b["start"] + b["end"]) / 2.0) * 1000))
        t_out_ms = max(0, int((b["end"] - 0.12) * 1000))

        w1, h1, p_mid, w_out = f"[w_{sfx_id}]", f"[h_{sfx_id}]", f"[pm_{sfx_id}]", f"[wo_{sfx_id}]"
        filter_parts.append(f"[{whoosh_idx}:a]adelay={t_in_ms}|{t_in_ms},volume=0.45{w1};")
        filter_parts.append(f"[{hit_idx}:a]adelay={t_in_ms}|{t_in_ms},volume=0.38{h1};")
        # Mid-sequence sub-cut SFX pop!
        filter_parts.append(f"[{pop_idx}:a]adelay={t_mid_ms}|{t_mid_ms},volume=0.42{p_mid};")
        filter_parts.append(f"[{whoosh_idx}:a]adelay={t_out_ms}|{t_out_ms},volume=0.32{w_out};")
        audio_stems.extend([w1, h1, p_mid, w_out])
        sfx_id += 1

    filter_parts.append(
        f"{''.join(audio_stems)}amix=inputs={len(audio_stems)}:duration=first:dropout_transition=0,"
        f"afade=t=out:st={fade_start:.2f}:d=0.25[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", str(duration),
        "-fps_mode", "cfr", "-r", "30",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-threads", "2",
        output_mp4
    ]

    print(f"\n[*] Rendering Zero-Lag 30fps CFR Short ({duration:.2f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Zero-Lag 30fps CFR Short Rendered: {output_mp4}")
    return output_mp4
