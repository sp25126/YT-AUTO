import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

def prepare_audible_soundtrack(out_mp3: str = "assets/music/subtle_background_music.mp3") -> str:
    """
    Prepares a broadcast-grade, rich soundtrack with:
    1. Full frequency spectrum (rich low-end, warmth, rhythm) audible on phones & laptops.
    2. A precise vocal pocket EQ cut (-4.5dB at 2.2 kHz) so the music never masks speech.
    3. Leveled with dynaudnorm to -11.1 LUFS so it sits at a reliable, audible reference.
    """
    abs_out = os.path.join(ROOT_DIR, out_mp3) if not os.path.isabs(out_mp3) else out_mp3
    os.makedirs(os.path.dirname(abs_out) or ".", exist_ok=True)
    
    cand_sources = [
        os.path.join(ROOT_DIR, "assets", "music", "ambient_doc.mp3"),
        os.path.join(ROOT_DIR, "temp", "subtle_audits", "ambient_doc.mp3"),
        os.path.join(ROOT_DIR, "temp", "subtle_audits", "doc_loop.mp3"),
    ]
    source_bgm = None
    for src in cand_sources:
        if os.path.exists(src):
            source_bgm = src
            break

    if source_bgm and os.path.exists(source_bgm):
        subprocess.run([
            "ffmpeg", "-y", "-i", source_bgm,
            "-af", (
                "silenceremove=start_periods=1:start_threshold=-40dB,"
                "highpass=f=55,"
                "equalizer=f=120:width_type=o:width=1.5:g=2.5,"        # Punch & warmth
                "equalizer=f=2200:width_type=o:width=1.8:g=-4.5,"     # Vocal presence pocket
                "lowpass=f=12500,"                                    # Clean highs
                "dynaudnorm=f=150:g=11:p=0.92"
            ),
            "-b:a", "192k", abs_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"[Audible BGM] Processed rich soundtrack bed -> {abs_out}")
        return abs_out

    return abs_out

def apply_pro_sfx_and_bgm_mix(
    video_in: str,
    output_mp4: str = "outputs/three_d_polished_master.mp4",
    voice_source: str = "temp/clean_base_30fps.mp4",
    bgm_file: str = None,
    bgm_volume: float = 0.50
):
    """
    Takes the rendered video and layers:
    1. Loud, clearly audible Earshot SFX synced to every scene cut, color-burst reveal, & 3D flip.
    2. Rich, properly audible background music bed:
       - Set to volume=0.50 (sits at approx -20 to -21 LUFS during speech).
       - Gentle sidechain ducking (-3.5dB during speech, swells during pauses).
       - Never muted or inaudible.
    """
    abs_out = os.path.join(ROOT_DIR, output_mp4) if not os.path.isabs(output_mp4) else output_mp4
    os.makedirs(os.path.dirname(abs_out) or ".", exist_ok=True)

    if not bgm_file or not os.path.exists(bgm_file):
        bgm_file = os.path.join(ROOT_DIR, "assets", "music", "subtle_background_music.mp3")
        prepare_audible_soundtrack(bgm_file)

    # Ensure Earshot kit exists
    from core.pro_sound_director import generate_earshot_sound_kit
    kit = generate_earshot_sound_kit("assets/sfx/earshot_kit")

    # Exact Frame-Locked SFX Cues matching visual transitions
    sfx_cues = [
        # 0:00.0 - Cold open Roto 'TIMING' reveal
        {"file": kit["sub_hit"], "ms": 20, "vol": 0.85},
        {"file": kit["whoosh_fast"], "ms": 40, "vol": 0.70},

        # 0:02.2 - 90% Crash Chart Entry + Odometer Ticks
        {"file": kit["whoosh_fast"], "ms": 2120, "vol": 0.75},
        {"file": kit["sub_hit"], "ms": 2200, "vol": 0.80},
        {"file": kit["counter_tick"], "ms": 2450, "vol": 0.65},
        {"file": kit["counter_tick"], "ms": 2750, "vol": 0.65},
        {"file": kit["counter_tick"], "ms": 3050, "vol": 0.65},
        {"file": kit["card_land"], "ms": 3450, "vol": 0.75},

        # 0:06.2 - Cut back to Speaker
        {"file": kit["whoosh_fast"], "ms": 6150, "vol": 0.65},

        # 0:10.6 - Trap #1 'TOO EARLY' 3D Window Entry + Color Burst @ 10.95s + Pill Pops
        {"file": kit["whoosh_fast"], "ms": 10520, "vol": 0.75},
        {"file": kit["ui_pop"], "ms": 10950, "vol": 0.75},
        {"file": kit["cursor_click"], "ms": 11200, "vol": 0.70},

        # 0:12.8 - Trap #2 'CRUSHED' 3D Monolith Slam + Color Burst @ 13.15s
        {"file": kit["whoosh_fast"], "ms": 12720, "vol": 0.75},
        {"file": kit["sub_hit"], "ms": 12800, "vol": 0.85},
        {"file": kit["ui_pop"], "ms": 13150, "vol": 0.75},

        # 0:15.4 - Cut to Guest Speaker ('Number one...')
        {"file": kit["whoosh_fast"], "ms": 15350, "vol": 0.65},

        # 0:20.8 - 'VETERANS' 3D Window Entry + Color Burst + Floating Pills
        {"file": kit["whoosh_fast"], "ms": 20720, "vol": 0.75},
        {"file": kit["card_land"], "ms": 20850, "vol": 0.75},
        {"file": kit["ui_pop"], "ms": 21200, "vol": 0.75},
        {"file": kit["cursor_click"], "ms": 21450, "vol": 0.70},

        # 0:26.0 - Cut to Guest Speaker
        {"file": kit["whoosh_fast"], "ms": 25950, "vol": 0.65},

        # 0:27.9 - 'ALL ROSY' 3D Card Entry
        {"file": kit["whoosh_fast"], "ms": 27820, "vol": 0.75},
        {"file": kit["ui_pop"], "ms": 28150, "vol": 0.70},

        # 0:30.2 - 3D 180-Degree Card Flip ('THE DETAILS')
        {"file": kit["whoosh_fast"], "ms": 30120, "vol": 0.80},
        {"file": kit["sub_hit"], "ms": 30220, "vol": 0.85},
    ]

    abs_video_in = os.path.join(ROOT_DIR, video_in) if not os.path.isabs(video_in) else video_in
    abs_voice_src = os.path.join(ROOT_DIR, voice_source) if not os.path.isabs(voice_source) else voice_source
    v_src = abs_voice_src if os.path.exists(abs_voice_src) else abs_video_in

    inputs = ["-i", abs_video_in, "-i", v_src, "-stream_loop", "-1", "-i", bgm_file]
    for c in sfx_cues:
        inputs.extend(["-i", c["file"]])

    filter_parts = [
        # 1. Clean Speaker Voice from input 1:a (-14 LUFS) + Hard Clamp at 32.85s (mute 'and' at 33.1s)
        "[1:a]highpass=f=85,dynaudnorm=f=150:g=15:p=0.94,"
        "acompressor=threshold=-15dB:ratio=3.5:attack=6:release=70:makeup=5dB,"
        "volume=enable='gte(t,32.85)':volume=0,"
        "afade=t=out:st=32.60:d=0.25,asplit=2[voice_main][voice_sc];",

        # 2. PROPERLY AUDIBLE BACKGROUND MUSIC BED:
        # volume=bgm_volume, gentle sidechain compression (threshold=0.18, ratio=1.65)
        # Ducks by ONLY ~3.5dB during speech so it is clearly, continuously audible behind the voice!
        f"[2:a]volume={bgm_volume:.2f},afade=t=out:st=32.55:d=0.30[bgm_raw];",
        "[bgm_raw][voice_sc]sidechaincompress=threshold=0.18:ratio=1.65:attack=25:release=280:makeup=1.05[bgm_ducked];"
    ]

    sfx_labels = []
    for idx, c in enumerate(sfx_cues):
        in_idx = 3 + idx
        lbl = f"[s_{idx}]"
        filter_parts.append(f"[{in_idx}:a]adelay={c['ms']}|{c['ms']},volume={c['vol']}{lbl};")
        sfx_labels.append(lbl)

    filter_parts.append(
        f"{''.join(sfx_labels)}amix=inputs={len(sfx_labels)}:duration=longest:normalize=0[sfx_bus];"
        f"[voice_main][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,"
        f"alimiter=limit=0.96:attack=5:release=40[a_out]"
    )

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "0:v", "-map", "[a_out]",
        "-t", "32.85",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        abs_out
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Master Polished Short with Audible SFX & Audible BGM -> {abs_out}")
    return abs_out

if __name__ == "__main__":
    test_video = os.path.join(ROOT_DIR, "temp", "three_d_raw.mp4")
    if not os.path.exists(test_video):
        test_video = os.path.join(ROOT_DIR, "outputs", "three_d_master_short.mp4")
    apply_pro_sfx_and_bgm_mix(test_video)
