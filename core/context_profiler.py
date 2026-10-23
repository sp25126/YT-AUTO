import cv2
import numpy as np
import scipy.io.wavfile as wav
import json

def analyze_audio_energy(wav_path: str, hop_duration: float = 0.2):
    """Calculates RMS (Root Mean Square) energy across 200ms audio windows on CPU."""
    sample_rate, data = wav.read(wav_path)
    if data.ndim > 1:
        data = data.mean(axis=1) # downmix to mono
    
    # Normalize amplitude
    max_val = np.max(np.abs(data)) if len(data) > 0 else 0
    if max_val > 0:
        data = data.astype(np.float32) / max_val
    else:
        data = data.astype(np.float32)
    
    window_samples = int(sample_rate * hop_duration)
    if window_samples == 0:
        return []
    total_windows = len(data) // window_samples
    
    energy_timeline = []
    for i in range(total_windows):
        segment = data[i * window_samples : (i + 1) * window_samples]
        rms = float(np.sqrt(np.mean(segment**2)))
        t = round(i * hop_duration, 2)
        
        # Categorize acoustic tone
        if rms > 0.35:
            state = "high_intensity"
        elif rms < 0.08:
            state = "whisper_or_pause"
        else:
            state = "normal_conversational"
            
        energy_timeline.append({"time": t, "rms": round(rms, 3), "state": state})
        
    return energy_timeline

def analyze_background_visuals(video_path: str, start_s: float, duration_s: float):
    """
    Measures frame luminance and color temperature to prevent 
    subtitles from blending into the scene background.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.set(cv2.CAP_PROP_POS_MSEC, start_s * 1000)
    
    luminance_samples = []
    total_frames = int(duration_s * fps)
    step = max(1, int(fps))
    
    for i in range(0, total_frames, step): # Sample 1 frame per second
        ret, frame = cap.read()
        if not ret:
            break
        # Convert to grayscale to evaluate overall scene brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        luminance_samples.append(float(np.mean(gray)))
        
    cap.release()
    avg_luminance = np.mean(luminance_samples) if luminance_samples else 128.0
    
    # 0 = Pitch Black, 255 = Pure White
    bg_style = "bright_background" if avg_luminance > 150 else "dark_background"
    
    return {
        "avg_luminance": round(float(avg_luminance), 2),
        "visual_tone": bg_style
    }

def run_context_profile(video_path: str, wav_path: str, start_s: float, duration_s: float, output_json="context_profile.json"):
    print("[*] Profiling acoustic intensity and visual scene tone...")
    audio_profile = analyze_audio_energy(wav_path)
    visual_profile = analyze_background_visuals(video_path, start_s, duration_s)
    
    report = {
        "visual_profile": visual_profile,
        "energy_curve": audio_profile
    }
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report
