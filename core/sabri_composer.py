import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from core.ae_motion_engine import render_ae_ui_card_image
from core.sabri_captions import generate_sabri_subtitles

def build_sabri_style_short(
    source_video: str,
    start_t: float,
    end_t: float,
    words: list,
    ui_cards: list,  # [{"start_offset": 2.5, "duration": 4.5, "headline": "90% FAIL RATE", "badge": "❌ CRITICAL STAT", "subtext": "...", "type": "loser"}]
    output_mp4: str = "outputs/cloned_ai_short.mp4",
    bgm_path: str = "assets/music/dark_synth_drive.mp3"
):
    """
    Renders Sabri Suby 3-Layer Hybrid Architecture on CPU:
    - Layer 1: 100% Original Human Voice with Broadcast EQ/Comp + Ducked BGM + SFX
    - Layer 2: 9:16 Talking-head with top-half 1080x960 animated After-Effects UI Proof Cards
    - Layer 3: Center-Stacked Sabri Subtitles at MarginV=840 with electric green pop highlights
    """
    os.makedirs("temp/sabri_build", exist_ok=True)
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    duration = end_t - start_t

    # 1. Pre-extract clean source clip via instant stream-copy (bypasses 2-hour container parsing)
    clean_source = "temp/clean_source_clip.mp4"
    print(f"[*] Pre-extracting source clip ({start_t}s - {end_t}s)...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_t), "-t", str(duration),
        "-i", source_video, "-c", "copy", clean_source
    ], check=True)

    # 2. Generate center-stacked Sabri Suby style captions
    ass_path = "temp/sabri_build/sabri_subs.ass"
    generate_sabri_subtitles(words, start_t, end_t, ass_path)
    clean_ass = os.path.relpath(ass_path).replace("\\", "/")

    # 3. Render Glassmorphic UI Card PNGs
    card_overlays = []
    card_inputs = []
    for idx, card in enumerate(ui_cards):
        card_png = f"temp/sabri_build/card_{idx}.png"
        render_ae_ui_card_image(
            headline=card["headline"],
            metric_badge=card["badge"],
            subtext=card["subtext"],
            card_type=card.get("type", "winner"),
            out_png=card_png
        )
        c_start = card["start_offset"]
        c_end = c_start + card["duration"]
        card_inputs.extend(["-i", card_png])
        card_overlays.append((c_start, c_end))

    # 4. Base Inputs: Video, BGM, Whoosh SFX, Pop SFX
    sfx_whoosh = "assets/sfx/whoosh.wav"
    sfx_pop = "assets/sfx/pop.wav"
    has_bgm = os.path.exists(bgm_path)

    inputs = ["-i", clean_source]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
    inputs.extend(["-i", sfx_whoosh, "-i", sfx_pop])

    base_card_input_idx = 4 if has_bgm else 3
    inputs.extend(card_inputs)

    # 5. Video Filtergraph: Memory-optimized crop before scale + Top-Half Card Overlays + Subtitles
    filter_parts = [
        "[0:v]crop=608:1080:(in_w-608)/2:0,scale=1080:1920,"
        "eq=contrast=1.14:saturation=1.12:brightness=-0.01,unsharp=5:5:1.1:5:5:0.0[v_base];"
    ]

    last_v = "[v_base]"
    for idx, (c_start, c_end) in enumerate(card_overlays):
        card_stream_idx = base_card_input_idx + idx
        next_v = f"[v_card_{idx}]"
        
        # Snappy Cubic-Out Slide-in over 0.35s
        # y = -280 * (1 - (t - c_start)/0.35)^3 when entering, then locks at y=0
        slide_y = (
            f"if(lt(t,{c_start:.2f}),-960,"
            f"if(lt(t,{c_start + 0.35:.2f}),-280*pow(1-(t-{c_start:.2f})/0.35,3),0))"
        )

        filter_parts.append(
            f"{last_v}[{card_stream_idx}:v]overlay=x=0:y='{slide_y}':"
            f"enable='between(t,{c_start:.2f},{c_end:.2f})':repeatlast=1{next_v};"
        )
        last_v = next_v

    filter_parts.append(f"{last_v}subtitles=filename='{clean_ass}':fontsdir='assets/fonts'[v_out];")

    # 6. Audio Pipeline: Original Voice + Broadcast Highpass/Compression + Ducked BGM + SFX
    whoosh_idx = 2 if has_bgm else 1
    pop_idx = 3 if has_bgm else 2

    audio_branches = ["[voice_clean]"]
    filter_parts.append(
        "[0:a]highpass=f=85,acompressor=threshold=-16dB:ratio=3:attack=10:release=100:makeup=4dB[voice_clean];"
    )

    if has_bgm:
        filter_parts.append("[1:a]volume=0.12[bgm_low];")
        audio_branches.append("[bgm_low]")

    # Trigger whoosh & pop on each card entry
    for idx, (c_start, _) in enumerate(card_overlays):
        w_delay = max(0, int(c_start * 1000))
        p_delay = max(0, int((c_start + 0.22) * 1000))
        w_branch = f"[sfx_w_{idx}]"
        p_branch = f"[sfx_p_{idx}]"
        filter_parts.append(f"[{whoosh_idx}:a]adelay={w_delay}|{w_delay},volume=0.45{w_branch};")
        filter_parts.append(f"[{pop_idx}:a]adelay={p_delay}|{p_delay},volume=0.40{p_branch};")
        audio_branches.extend([w_branch, p_branch])

    filter_parts.append(
        f"{''.join(audio_branches)}amix=inputs={len(audio_branches)}:duration=first:dropout_transition=0[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-threads", "2",
        output_mp4
    ]

    print(f"\n[*] Rendering Sabri-Style Hybrid Short ({duration:.1f}s) to {output_mp4}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered Sabri-Style Hybrid Short: {output_mp4}")
    return output_mp4
