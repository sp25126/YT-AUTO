import os
import wave
import struct
import numpy as np

def generate_pro_foley_pack():
    os.makedirs("assets/sfx", exist_ok=True)
    sr = 44100

    # 1. Shutter Click (shutter.wav) - mechanical dual-blade snap
    shutter_len = int(sr * 0.18)
    shutter = np.zeros(shutter_len, dtype=np.float32)
    # Click 1
    t1 = np.linspace(0, 0.04, int(sr * 0.04))
    click1 = np.sin(2 * np.pi * 1400 * t1) * np.exp(-t1 * 120) * 0.8
    shutter[:len(click1)] += click1
    # Click 2 (blade release)
    t2 = np.linspace(0, 0.05, int(sr * 0.05))
    click2 = np.sin(2 * np.pi * 950 * t2) * np.exp(-t2 * 90) * 0.7
    st2 = int(sr * 0.06)
    shutter[st2:st2+len(click2)] += click2
    write_wav("assets/sfx/shutter.wav", shutter, sr)

    # 2. Paper Rip (paper_rip.wav) - high frequency tearing noise
    rip_len = int(sr * 0.35)
    t_rip = np.linspace(0, 0.35, rip_len)
    noise = np.random.uniform(-1, 1, rip_len).astype(np.float32)
    env = np.sin(np.pi * t_rip / 0.35) ** 1.5
    rip = noise * env * 0.65
    write_wav("assets/sfx/paper_rip.wav", rip, sr)

    # 3. Ocean Waves (ocean_waves.wav) - rolling swell for Style 3
    wave_len = int(sr * 6.0)
    t_w = np.linspace(0, 6.0, wave_len)
    pink = np.cumsum(np.random.randn(wave_len)).astype(np.float32)
    pink -= np.mean(pink)
    pink /= np.max(np.abs(pink)) + 1e-6
    mod = 0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t_w)
    waves = pink * mod * 0.4
    write_wav("assets/sfx/ocean_waves.wav", waves, sr)

    # 4. Wind Ambience (wind.wav)
    wind_len = int(sr * 6.0)
    t_wind = np.linspace(0, 6.0, wind_len)
    noise_w = np.convolve(np.random.uniform(-1, 1, wind_len), np.ones(80)/80, mode='same').astype(np.float32)
    wind = noise_w * (0.6 + 0.3 * np.sin(2 * np.pi * 0.15 * t_wind)) * 0.45
    write_wav("assets/sfx/wind.wav", wind, sr)

    # 5. Firewood Crackle (firewood.wav) - random snaps
    fire_len = int(sr * 6.0)
    fire = np.zeros(fire_len, dtype=np.float32)
    np.random.seed(42)
    pop_indices = np.random.randint(0, fire_len, 40)
    for idx in pop_indices:
        p_len = min(int(sr * 0.015), fire_len - idx)
        tp = np.linspace(0, 0.015, p_len)
        pop = np.sin(2 * np.pi * 2200 * tp) * np.exp(-tp * 300) * 0.5
        fire[idx:idx+p_len] += pop
    # Add subtle low rumble
    rumble = np.sin(2 * np.pi * 65 * np.linspace(0, 6.0, fire_len)) * 0.08
    fire += rumble
    write_wav("assets/sfx/firewood.wav", fire, sr)

    # 6. Sub Drop (sub_drop.wav) - 40Hz deep bass impact
    sub_len = int(sr * 1.2)
    t_sub = np.linspace(0, 1.2, sub_len)
    freq = 75.0 * np.exp(-t_sub * 2.5) + 38.0
    sub = np.sin(2 * np.pi * freq * t_sub) * np.exp(-t_sub * 2.2) * 0.95
    write_wav("assets/sfx/sub_drop.wav", sub, sr)

def write_wav(filename: str, audio: np.ndarray, sr: int):
    audio = np.clip(audio, -1.0, 1.0)
    int_data = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(int_data.tobytes())
    print(f"[OK] Generated SFX: {filename}")

if __name__ == "__main__":
    generate_pro_foley_pack()
