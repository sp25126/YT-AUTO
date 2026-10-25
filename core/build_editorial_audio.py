import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.abspath("."))
from core.pro_sound_director import (
    generate_earshot_sound_kit,
    search_openverse_sfx_or_bgm,
    compute_real_sfx_frame_cues,
)

def build_editorial_soundtrack(
    clean_base_mp4: str = "temp/clean_base_30fps.mp4",
    output_audio_wav: str = "temp/editorial_master_audio.wav",
    duration_sec: float = 33.4,
    fps: int = 30
) -> str:
    print("[*] Generating studio-calibrated sound kit via Earshot...")
    kit = generate_earshot_sound_kit("assets/sfx/earshot_kit")

    # Define all timeline events specified in prompt
    raw_events = [
        {"type": "whoosh_fast", "time_sec": 0.05, "volume": 0.38, "reason": "Intro reveal swipe"},
        {"type": "counter_tick", "time_sec": 0.55, "volume": 0.22, "reason": "Counter tick 1"},
        {"type": "counter_tick", "time_sec": 0.85, "volume": 0.22, "reason": "Counter tick 2"},
        {"type": "counter_tick", "time_sec": 1.15, "volume": 0.22, "reason": "Counter tick 3"},
        {"type": "counter_tick", "time_sec": 1.40, "volume": 0.22, "reason": "Counter tick 4"},
        {"type": "counter_tick", "time_sec": 1.70, "volume": 0.22, "reason": "Counter tick 5"},
        {"type": "counter_tick", "time_sec": 1.95, "volume": 0.22, "reason": "Counter tick 6"},
        {"type": "cursor_click", "time_sec": 1.40, "volume": 0.42, "reason": "Filter pill highlights"},
        {"type": "ui_pop", "time_sec": 1.60, "volume": 0.48, "reason": "90% callout pops out"},
        {"type": "sub_hit", "time_sec": 1.60, "volume": 0.35, "reason": "90% callout impact"},
        {"type": "whoosh_fast", "time_sec": 6.30, "volume": 0.38, "reason": "Mode C speaker punch-in"},
        {"type": "whoosh_fast", "time_sec": 10.60, "volume": 0.40, "reason": "Mode B dual comparison in"},
        {"type": "ui_pop", "time_sec": 10.60, "volume": 0.42, "reason": "Comparison card 1 spring"},
        {"type": "ui_pop", "time_sec": 12.10, "volume": 0.42, "reason": "Comparison card 2 spring"},
        {"type": "card_land", "time_sec": 12.10, "volume": 0.35, "reason": "Card 2 land impact"},
        {"type": "whoosh_fast", "time_sec": 15.40, "volume": 0.38, "reason": "Mode C speaker punch-in"},
        {"type": "whoosh_fast", "time_sec": 20.80, "volume": 0.40, "reason": "Mode A floating studio return"},
        {"type": "cursor_click", "time_sec": 22.20, "volume": 0.42, "reason": "Advisor filter click"},
        {"type": "ui_pop", "time_sec": 22.20, "volume": 0.35, "reason": "Pill tag reveal"},
        {"type": "whoosh_fast", "time_sec": 26.20, "volume": 0.38, "reason": "Mode C speaker punch-in"},
        {"type": "whoosh_fast", "time_sec": 28.00, "volume": 0.40, "reason": "Mode B dual comparison in"},
        {"type": "ui_pop", "time_sec": 28.00, "volume": 0.42, "reason": "Outside Rosy card spring"},
        {"type": "ui_pop", "time_sec": 29.50, "volume": 0.42, "reason": "Devil Details card spring"},
        {"type": "card_land", "time_sec": 29.50, "volume": 0.35, "reason": "Details card impact"},
    ]

    print("[*] Computing Real-SFX frame-offset cues (-2 frames for clicks, -1.5 for pops, -3 for whooshes)...")
    calibrated_cues = compute_real_sfx_frame_cues(raw_events, fps=fps)

    sr = 44100
    total_samples = int(duration_sec * sr)
    sfx_track = np.zeros(total_samples, dtype=np.float32)

    for cue in calibrated_cues:
        sfx_type = cue["type"]
        wav_file = kit.get(sfx_type)
        if not wav_file or not os.path.exists(wav_file):
            continue
        try:
            data, file_sr = sf.read(wav_file)
            if len(data.shape) > 1:
                data = data.mean(axis=1) # to mono
            if file_sr != sr:
                # simple resampling
                indices = np.round(np.linspace(0, len(data) - 1, int(len(data) * sr / file_sr))).astype(int)
                data = data[indices]
            
            vol = cue.get("volume", 0.4)
            data = data * vol

            start_idx = int((cue["time_ms"] / 1000.0) * sr)
            if start_idx < total_samples:
                end_idx = min(total_samples, start_idx + len(data))
                sfx_track[start_idx:end_idx] += data[:end_idx - start_idx]
        except Exception as e:
            print(f"[!] Error mixing {sfx_type}: {e}")

    # Clip protect SFX track
    sfx_track = np.clip(sfx_track, -0.95, 0.95)
    sfx_wav = "temp/editorial_sfx_stem.wav"
    sf.write(sfx_wav, sfx_track, sr)
    print(f"[OK] Rendered calibrated SFX stem: {sfx_wav}")

    # Step 2: Extract and level speaker voice to -14 LUFS using dynaudnorm
    voice_wav = "temp/editorial_voice_leveled.wav"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", clean_base_mp4,
        "-vn",
        "-af", "dynaudnorm=f=150:g=15:m=10.0:r=0.9,loudnorm=I=-14:TP=-1.5:LRA=7",
        "-ar", "44100", "-ac", "2",
        voice_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Leveled speaker voice to -14 LUFS: {voice_wav}")

    # Step 3: Check for BGM bed or search Openverse
    bgm_wav = "assets/sfx/openverse_bgm.wav"
    if not os.path.exists(bgm_wav):
        search_openverse_sfx_or_bgm("dark ambient synth bed", max_duration_sec=duration_sec, license_filter="cc0", out_path=bgm_wav)

    # Step 4: Final broadcast mix via FFmpeg with amix=normalize=0 and alimiter
    print("[*] Mixing voice, calibrated SFX stem, and ambient bed into master audio...")
    inputs = ["-i", voice_wav, "-i", sfx_wav]
    filter_complex = "[0:a]volume=1.0[v];[1:a]volume=1.1[sfx];"
    
    if os.path.exists(bgm_wav) and os.path.getsize(bgm_wav) > 1000:
        inputs.extend(["-i", bgm_wav])
        filter_complex += f"[2:a]aloop=loop=-1:size=2e+09,atrim=0:{duration_sec},volume=0.14,afade=t=out:st={duration_sec - 0.4}:d=0.4[bgm];"
        filter_complex += "[v][sfx][bgm]amix=inputs=3:duration=first:normalize=0,alimiter=limit=-1.5dB[out]"
    else:
        filter_complex += "[v][sfx]amix=inputs=2:duration=first:normalize=0,alimiter=limit=-1.5dB[out]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "44100", "-ac", "2",
        output_audio_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Generated Master Audio (-14 LUFS): {output_audio_wav}")
    return output_audio_wav

if __name__ == "__main__":
    build_editorial_soundtrack()
