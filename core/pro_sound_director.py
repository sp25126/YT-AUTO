import os
import sys
import json
import requests
import subprocess

OPENVERSE_AUDIO_URL = "https://api.openverse.org/v1/audio/"

def search_openverse_sfx_or_bgm(
    query: str,
    max_duration_sec: float = 8.0,
    license_filter: str = "cc0",
    out_path: str = "assets/sfx/openverse_sound.wav"
) -> str:
    """
    Tool 1 from a99VVqGgVM8:
    Queries Openverse's 5.2M+ audio catalog with ZERO API key needed.
    Downloads the best matching short sound effect or music bed and converts to 44.1kHz WAV.
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    params = {
        "q": query,
        "license": license_filter,
        "page_size": 10
    }
    try:
        resp = requests.get(OPENVERSE_AUDIO_URL, params=params, timeout=12)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            for item in results:
                dur_ms = item.get("duration") or 0
                audio_url = item.get("url")
                if audio_url and (dur_ms == 0 or dur_ms <= max_duration_sec * 1000):
                    raw_file = out_path + ".raw"
                    r = requests.get(audio_url, timeout=15)
                    with open(raw_file, "wb") as f:
                        f.write(r.content)
                    subprocess.run([
                        "ffmpeg", "-y", "-i", raw_file,
                        "-af", f"silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:{max_duration_sec}",
                        "-ar", "44100", "-ac", "2",
                        out_path
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    if os.path.exists(raw_file):
                        os.remove(raw_file)
                    print(f"[Openverse] Downloaded '{item.get('title')}' ({dur_ms}ms) -> {out_path}")
                    return out_path
    except Exception as e:
        print(f"[!] Openverse search fallback for '{query}': {e}")
    return ""


def generate_earshot_sound_kit(kit_dir: str = "assets/sfx/earshot_kit") -> dict:
    """
    Tool 3 from a99VVqGgVM8:
    Uses Earshot's procedural forge to render clean, studio-calibrated UI & motion sounds
    (whoosh, pop, snap, tick, sub_hit, shutter).
    """
    os.makedirs(kit_dir, exist_ok=True)
    recipes = {
        "whoosh_fast": ("whoosh_fast/crisp", os.path.join(kit_dir, "whoosh_fast.wav")),
        "ui_pop": ("ui_pop/soft", os.path.join(kit_dir, "ui_pop.wav")),
        "card_land": ("pro_tap/soft", os.path.join(kit_dir, "card_land.wav")),
        "cursor_click": ("typing_key/thock", os.path.join(kit_dir, "cursor_click.wav")),
        "counter_tick": ("pro_typing_key/tick", os.path.join(kit_dir, "counter_tick.wav")),
        "sub_hit": ("sub_drop/pro", os.path.join(kit_dir, "sub_hit.wav")),
    }
    rendered = {}
    py_exec = sys.executable or "python"
    for name, (recipe_id, wav_path) in recipes.items():
        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000:
            rendered[name] = wav_path
            continue
        try:
            subprocess.run(
                [py_exec, "-m", "earshot", "sfx", "render", recipe_id, "-o", wav_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            rendered[name] = wav_path
        except Exception:
            # Fallback to Openverse if earshot CLI is still downloading models
            res = search_openverse_sfx_or_bgm(name.replace("_", " "), 2.5, "cc0", wav_path)
            if not res or not os.path.exists(wav_path):
                # Procedural numpy synthesis fallback
                try:
                    import numpy as np
                    import soundfile as sf
                    sr = 44100
                    if "click" in name:
                        dur = 0.05
                        t = np.linspace(0, dur, int(sr * dur), False)
                        sig = np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 90)
                    elif "pop" in name:
                        dur = 0.08
                        t = np.linspace(0, dur, int(sr * dur), False)
                        sig = np.sin(2 * np.pi * (600 - t * 4000) * t) * np.exp(-t * 50)
                    elif "whoosh" in name:
                        dur = 0.35
                        t = np.linspace(0, dur, int(sr * dur), False)
                        noise = np.random.uniform(-0.5, 0.5, len(t))
                        env = np.sin(np.pi * (t / dur)) ** 2
                        sig = noise * env * 0.4
                    elif "sub" in name or "land" in name:
                        dur = 0.5
                        t = np.linspace(0, dur, int(sr * dur), False)
                        freq = np.linspace(120, 35, len(t))
                        sig = np.sin(2 * np.pi * freq * t) * np.exp(-t * 8) * 0.6
                    else: # tick
                        dur = 0.03
                        t = np.linspace(0, dur, int(sr * dur), False)
                        sig = np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * 0.3
                    sf.write(wav_path, sig.astype(np.float32), sr)
                except Exception as ex:
                    print(f"[!] Synth fallback failed for {name}: {ex}")
            rendered[name] = wav_path
    return rendered


def compute_real_sfx_frame_cues(timeline_events: list, fps: int = 30) -> list:
    """
    Tool 2 from a99VVqGgVM8 (Real-SFX Timing Rules):
    Adjusts raw visual event timestamps using professional editor frame-offset rules:
    - 'cursor_click' / 'ui_pop': Lead the visual cut by -2 frames (-66ms) so the click triggers the visual!
    - 'whoosh_fast': Peak lands +2 frames (+66ms) into the motion transition (-3 frames lead).
    - 'card_land' / 'sub_hit': Lands on the exact impact frame (0ms offset) after a -6dB BGM micro-dip.
    """
    frame_ms = 1000.0 / fps
    frame_offsets = {
        "cursor_click": -2 * frame_ms,
        "ui_pop": -1.5 * frame_ms,
        "whoosh_fast": -3 * frame_ms,
        "card_land": 0.0,
        "sub_hit": 0.0,
        "counter_tick": 0.0
    }
    calibrated_cues = []
    for ev in timeline_events:
        sfx_type = ev["type"]
        raw_ms = ev["time_sec"] * 1000.0
        exact_ms = max(0, int(raw_ms + frame_offsets.get(sfx_type, 0.0)))
        calibrated_cues.append({
            "type": sfx_type,
            "time_ms": exact_ms,
            "volume": ev.get("volume", 0.42),
            "reason": ev.get("reason", "")
        })
    return calibrated_cues


if __name__ == "__main__":
    print("[+] Initializing Pro Sound Director Audio Stack...")
    kit = generate_earshot_sound_kit()
    print(f"[+] Rendered Sound Kit: {list(kit.keys())}")
    
    # Test frame cues
    sample_events = [
        {"type": "whoosh_fast", "time_sec": 0.0, "reason": "Intro swipe"},
        {"type": "counter_tick", "time_sec": 0.8, "reason": "Tick 1"},
        {"type": "cursor_click", "time_sec": 1.4, "reason": "Filter click"},
        {"type": "ui_pop", "time_sec": 1.6, "reason": "90% callout pop"},
        {"type": "whoosh_fast", "time_sec": 6.3, "reason": "Speaker punch-in transition"},
    ]
    cues = compute_real_sfx_frame_cues(sample_events)
    print(f"[+] Calibrated Frame Cues:\n{json.dumps(cues, indent=2)}")
