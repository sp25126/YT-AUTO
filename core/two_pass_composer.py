import os
import shutil
import subprocess
from typing import List, Dict, Any

def render_two_pass_master(
    raw_podcast: str,
    start_t: float,
    end_t: float,          # Set to 33.40s (cuts off right after "detail", before "and"!)
    broll_windows: List[Dict[str, Any]],
    ass_path: str,
    output_mp4: str = "outputs/cloned_ai_short.mp4",
    bgm_path: str = "assets/music/dark_synth_drive.mp3"
) -> str:
    """
    Two-Pass Master Compositor:
    - Pass 1: Decode & normalize ONLY the 33.4s podcast slice into 30fps CFR clean base.
      Completely eliminates 100% of the frame-drop stutter on the speaker video!
    - Pass 2: Composite Split-Screen B-Roll, Dynamic Speaker Framing, Dual-Zone Captions,
      Top 8px glowing neon retention bar, audio risers, and Multi-Stem Sound Effects.
    - Clamped cleanly at 33.40s with a 0.25s audio fade-out starting at 33.15s.
    """
    os.makedirs("temp/pro_build", exist_ok=True)
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    duration = round(end_t - start_t, 2)
    clean_base = "temp/clean_base_30fps.mp4"

    # PASS 1: Decode & normalize ONLY the 33.4s podcast slice to 30fps Constant Frame Rate
    print(f"\n[Pass 1/2] Pre-normalizing base speaker clip ({start_t:.2f}s - {end_t:.2f}s, {duration:.2f}s) to 30fps CFR...")
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start_t), "-t", str(duration),
        "-i", raw_podcast,
        "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.12:saturation=1.10",
        "-r", "30", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        clean_base
    ], check=True)
    # Also mirror to temp/pro_build/clean_base_30fps.mp4
    try:
        shutil.copy2(clean_base, "temp/pro_build/clean_base_30fps.mp4")
    except Exception:
        pass
    print(f"[Pass 1/2 OK] Clean base normalized: {clean_base}")

    # PASS 2: Composite Split-Screen B-Roll, Dynamic Speaker Framing, Captions, Retention Bar, and Multi-Stem SFX
    print("\n[Pass 2/2] Compositing multi-cut B-roll, VFX, retention bar, and audio stems...")
    sfx_whoosh = "assets/sfx/whoosh.wav"
    sfx_hit = "assets/sfx/hit.wav"
    sfx_pop = "assets/sfx/pop.wav"
    sfx_riser = "assets/sfx/riser.wav"
    has_bgm = os.path.exists(bgm_path)
    has_riser = os.path.exists(sfx_riser)

    inputs = ["-i", clean_base]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
    inputs.extend(["-i", sfx_whoosh, "-i", sfx_hit, "-i", sfx_pop])
    if has_riser:
        inputs.extend(["-i", sfx_riser])

    whoosh_idx = 2 if has_bgm else 1
    hit_idx = 3 if has_bgm else 2
    pop_idx = 4 if has_bgm else 3
    riser_idx = 5 if has_bgm else 4
    broll_base_idx = (6 if has_riser else 5) if has_bgm else (5 if has_riser else 4)

    for b in broll_windows:
        inputs.extend(["-i", b["file"]])

    split_expr = "+".join([f"between(t,{b['start']:.2f},{b['end']:.2f})" for b in broll_windows])

    filter_parts = [
        "[0:v]split=2[v_full][v_for_bot];",
        "[v_for_bot]crop=1080:960:0:140[v_bot_face];",
        f"[v_full][v_bot_face]overlay=0:960:enable='{split_expr}':eof_action=pass[v_split_base];"
    ]

    last_v = "[v_split_base]"
    for idx, b in enumerate(broll_windows):
        in_idx = broll_base_idx + idx
        b_pts = f"[b_pts_{idx}]"
        next_v = f"[v_comp_{idx}]"
        filter_parts.append(
            f"[{in_idx}:v]fps=30,setpts=PTS-STARTPTS+({b['start']:.2f}/TB){b_pts};"
            f"{last_v}{b_pts}overlay=0:0:enable='between(t,{b['start']:.2f},{b['end']:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v

    # Retention Bar: Top 8px glowing neon bar filling left-to-right across duration
    filter_parts.append(
        f"{last_v}drawbox=x=0:y=0:w=1080:h=8:color=0x10141C@0.85:t=fill,"
        f"drawbox=x=0:y=0:w='min(1080,1080*t/{duration:.2f})':h=8:color=0x2EF773:t=fill[v_bar];"
    )
    last_v = "[v_bar]"

    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    filter_parts.append(f"{last_v}subtitles=filename='{clean_ass}':fontsdir='assets/fonts'[v_out];")

    # Audio Mix + 0.25s clean fade-out before "and" at 33.15s
    fade_start = max(0.0, duration - 0.25)
    audio_stems = ["[voice_clean]"]

    filter_parts.append(
        f"[0:a]highpass=f=85,acompressor=threshold=-16dB:ratio=3:attack=10:release=100:makeup=4dB,"
        f"afade=t=out:st={fade_start:.2f}:d=0.25[voice_clean];"
    )

    if has_bgm:
        filter_parts.append(f"[1:a]volume=0.11,afade=t=out:st={fade_start:.2f}:d=0.25[bgm_low];")
        audio_stems.append("[bgm_low]")

    sfx_id = 0
    for b in broll_windows:
        t_riser = max(0, int((b["start"] - 0.60) * 1000))
        t_in = max(0, int(b["start"] * 1000))
        t_mid = max(0, int(((b["start"] + b["end"]) / 2.0) * 1000))
        t_out = max(0, int((b["end"] - 0.12) * 1000))

        if has_riser and b["start"] >= 0.60:
            r1 = f"[r_{sfx_id}]"
            filter_parts.append(f"[{riser_idx}:a]adelay={t_riser}|{t_riser},volume=0.35{r1};")
            audio_stems.append(r1)

        w1, h1, pm, wo = f"[w_{sfx_id}]", f"[h_{sfx_id}]", f"[pm_{sfx_id}]", f"[wo_{sfx_id}]"
        filter_parts.append(f"[{whoosh_idx}:a]adelay={t_in}|{t_in},volume=0.48{w1};")
        filter_parts.append(f"[{hit_idx}:a]adelay={t_in}|{t_in},volume=0.40{h1};")
        filter_parts.append(f"[{pop_idx}:a]adelay={t_mid}|{t_mid},volume=0.45{pm};")
        filter_parts.append(f"[{whoosh_idx}:a]adelay={t_out}|{t_out},volume=0.35{wo};")
        audio_stems.extend([w1, h1, pm, wo])
        sfx_id += 1

    filter_parts.append(
        f"{''.join(audio_stems)}amix=inputs={len(audio_stems)}:duration=first:dropout_transition=0[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", str(duration),
        "-r", "30", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-threads", "2",
        output_mp4
    ]

    print(f"[*] Rendering Master 2-Pass Short ({duration:.2f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Master 2-Pass Short Rendered: {output_mp4}")

    # Mirror to outputs/master_short_v5.mp4 if output_mp4 is cloned_ai_short.mp4
    alt_out = "outputs/master_short_v5.mp4" if output_mp4 != "outputs/master_short_v5.mp4" else "outputs/cloned_ai_short.mp4"
    try:
        shutil.copy2(output_mp4, alt_out)
        print(f"[OK] Mirrored to {alt_out}")
    except Exception:
        pass

    return output_mp4

