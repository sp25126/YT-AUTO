import os
import sys
import requests
import subprocess
import numpy as np
import scipy.io.wavfile as wav

# Curated Direct CC0 / Royalty-Free Dark Synth & Electronic Pulse Streams
CURATED_VIRAL_BGMS = [
    # Pixabay / Wikimedia Commons / CC0 Driving Electronic & Dark Synth Pulses
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3",
    "https://cdn.pixabay.com/download/audio/2022/10/25/audio_946b0939c8.mp3",
]

def build_guaranteed_viral_bgm(duration: float = 34.0, out_mp3: str = "assets/music/viral_pulse_116bpm.mp3") -> str:
    """
    1. Tries downloading a curated driving Dark Synthwave / Electronic Pulse track (no sleepy cello!).
    2. Fallback: Synthesizes a studio-grade 116 BPM Dark Analog Synthwave Arpeggio + Sub-Bass Pulse
       (Rezz / Iman Gadzhi documentary style) so you are 100% guaranteed a hard-hitting viral beat!
    """
    os.makedirs(os.path.dirname(out_mp3) or ".", exist_ok=True)
    for url in CURATED_VIRAL_BGMS:
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if r.status_code == 200 and len(r.content) > 100000:
                raw_mp3 = out_mp3 + ".raw.mp3"
                with open(raw_mp3, "wb") as f:
                    f.write(r.content)
                subprocess.run([
                    "ffmpeg", "-y", "-i", raw_mp3,
                    "-af", (
                        "silenceremove=start_periods=1:start_threshold=-32dB,"
                        "equalizer=f=65:width_type=o:width=1.2:g=5,"
                        "equalizer=f=2200:width_type=o:width=2.0:g=-6,"
                        "dynaudnorm=f=150:g=11"
                    ),
                    "-t", str(duration),
                    "-b:a", "192k", out_mp3
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                if os.path.exists(raw_mp3):
                    os.remove(raw_mp3)
                print(f"[Viral BGM] Loaded curated dark electronic pulse -> {out_mp3}")
                return out_mp3
        except Exception:
            pass

    # Fallback: Procedural 116 BPM Dark Synthwave Pluck + Deep 808 Sub-Pulse (Zero Copyright!)
    print("[Viral BGM] Generating 116 BPM Dark Analog Synthwave Pulse...")
    sr = 44100
    total_samples = int(duration * sr)
    bpm = 116.0
    beat_sec = 60.0 / bpm
    sixteenth_sec = beat_sec / 4.0

    # Minor progression root notes (D2 -> Bb1 -> G1 -> A1)
    progression = [73.42, 58.27, 49.00, 55.00]
    audio = np.zeros(total_samples, dtype=np.float32)

    for step in range(int(duration / sixteenth_sec)):
        s_idx = int(step * sixteenth_sec * sr)
        e_idx = min(total_samples, int((step + 1) * sixteenth_sec * sr))
        seg_len = e_idx - s_idx
        if seg_len <= 0:
            break
        bar_idx = (step // 16) % 4
        root_f = progression[bar_idx]
        # Arpeggio intervals (1x, 1.5x fifth, 2x octave, 1.2x minor third)
        arp_mult = [1.0, 1.5, 2.0, 1.2][step % 4]
        freq = root_f * arp_mult
        seg_t = np.linspace(0, sixteenth_sec, seg_len, False)
        # Warm analog saw-pluck envelope
        env = np.exp(-seg_t * 18.0)
        wave = (np.sin(2 * np.pi * freq * seg_t) + 0.5 * np.sin(2 * np.pi * freq * 2 * seg_t)) * env

        # Add deep kick transient on every quarter beat (step % 4 == 0)
        if step % 4 == 0:
            k_freq = np.linspace(115, 36, seg_len)
            kick = np.sin(2 * np.pi * k_freq * seg_t) * np.exp(-seg_t * 14.0) * 1.4
            wave += kick

        audio[s_idx:e_idx] += wave

    # Warm lowpass filter via FFmpeg so it sounds like a dark Moog synth bed
    raw_wav = out_mp3.replace(".mp3", "_raw.wav")
    audio = np.clip(audio * 0.35, -0.95, 0.95)
    wav.write(raw_wav, sr, (audio * 32767).astype(np.int16))
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_wav,
        "-af", "lowpass=f=1800,aecho=0.8:0.88:120:0.25,equalizer=f=60:width_type=o:width=1:g=4",
        "-b:a", "192k", out_mp3
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(raw_wav):
        os.remove(raw_wav)
    print(f"[Viral BGM] Generated & filtered synth pulse -> {out_mp3}")
    return out_mp3

def apply_pro_sfx_and_bgm_mix(
    video_in: str,
    output_mp4: str = "outputs/three_d_polished_master.mp4",
    voice_source: str = "temp/clean_base_30fps.mp4"
):
    """
    Takes the rendered video and layers:
    1. Loud, clearly audible Earshot SFX synced to every scene cut, color-burst reveal, & 3D flip.
    2. Driving 116 BPM Dark Synth BGM ducked via sidechain compression.
    """
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    bgm_file = build_guaranteed_viral_bgm(33.5)

    # Ensure Earshot kit exists
    from core.pro_sound_director import generate_earshot_sound_kit
    kit = generate_earshot_sound_kit("assets/sfx/earshot_kit")

    # Exact Frame-Locked SFX Cues matching your 32.9s video's exact visual transitions:
    sfx_cues = [
        # 0:00.0 - Cold open Roto 'TIMING' reveal
        {"file": kit["sub_hit"], "ms": 20, "vol": 0.95},
        {"file": kit["whoosh_fast"], "ms": 40, "vol": 0.75},

        # 0:02.2 - 90% Crash Chart Entry + Odometer Ticks
        {"file": kit["whoosh_fast"], "ms": 2120, "vol": 0.85},
        {"file": kit["sub_hit"], "ms": 2200, "vol": 0.85},
        {"file": kit["counter_tick"], "ms": 2450, "vol": 0.70},
        {"file": kit["counter_tick"], "ms": 2750, "vol": 0.70},
        {"file": kit["counter_tick"], "ms": 3050, "vol": 0.70},
        {"file": kit["card_land"], "ms": 3450, "vol": 0.85},

        # 0:06.2 - Cut back to Speaker
        {"file": kit["whoosh_fast"], "ms": 6150, "vol": 0.70},

        # 0:10.6 - Trap #1 'TOO EARLY' 3D Window Entry + Color Burst @ 10.95s + Pill Pops
        {"file": kit["whoosh_fast"], "ms": 10520, "vol": 0.90},
        {"file": kit["ui_pop"], "ms": 10950, "vol": 0.85},
        {"file": kit["cursor_click"], "ms": 11200, "vol": 0.80},

        # 0:12.8 - Trap #2 'CRUSHED' 3D Monolith Slam + Color Burst @ 13.15s
        {"file": kit["whoosh_fast"], "ms": 12720, "vol": 0.90},
        {"file": kit["sub_hit"], "ms": 12800, "vol": 0.95},
        {"file": kit["ui_pop"], "ms": 13150, "vol": 0.85},

        # 0:15.4 - Cut to Guest Speaker ('Number one...')
        {"file": kit["whoosh_fast"], "ms": 15350, "vol": 0.70},

        # 0:20.8 - 'VETERANS' 3D Window Entry + Color Burst + Floating Pills
        {"file": kit["whoosh_fast"], "ms": 20720, "vol": 0.90},
        {"file": kit["card_land"], "ms": 20850, "vol": 0.85},
        {"file": kit["ui_pop"], "ms": 21200, "vol": 0.85},
        {"file": kit["cursor_click"], "ms": 21450, "vol": 0.80},

        # 0:26.0 - Cut to Guest Speaker
        {"file": kit["whoosh_fast"], "ms": 25950, "vol": 0.70},

        # 0:27.9 - 'ALL ROSY' 3D Card Entry
        {"file": kit["whoosh_fast"], "ms": 27820, "vol": 0.88},
        {"file": kit["ui_pop"], "ms": 28150, "vol": 0.80},

        # 0:30.2 - 3D 180-Degree Card Flip ('THE DETAILS')
        {"file": kit["whoosh_fast"], "ms": 30120, "vol": 0.95},
        {"file": kit["sub_hit"], "ms": 30220, "vol": 0.95},
    ]

    v_src = voice_source if os.path.exists(voice_source) else video_in
    inputs = ["-i", video_in, "-i", v_src, "-stream_loop", "-1", "-i", bgm_file]
    for c in sfx_cues:
        inputs.extend(["-i", c["file"]])

    filter_parts = [
        # 1. Clean Speaker Voice from input 1:a (-14 LUFS) + Hard Clamp at 32.85s (mute 'and' at 33.1s)
        "[1:a]highpass=f=85,dynaudnorm=f=150:g=15:p=0.94,"
        "acompressor=threshold=-15dB:ratio=3.5:attack=6:release=70:makeup=5dB,"
        "volume=enable='gte(t,32.85)':volume=0,"
        "afade=t=out:st=32.60:d=0.25,asplit=2[voice_main][voice_sc];",

        # 2. Driving Viral BGM (Volume boosted to 0.34 so you can clearly feel the pulse, sidechained by voice)
        "[2:a]volume=0.34,afade=t=out:st=32.55:d=0.30[bgm_raw];",
        "[bgm_raw][voice_sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=280:makeup=1.3[bgm_ducked];"
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
        output_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Master Polished Short with Audible SFX & Driving BGM -> {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    test_video = "temp/three_d_raw.mp4"
    if not os.path.exists(test_video):
        test_video = "outputs/three_d_master_short.mp4"
    apply_pro_sfx_and_bgm_mix(test_video)
