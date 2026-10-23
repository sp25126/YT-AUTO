import os
import json
import subprocess
import cv2
import numpy as np
import scipy.io.wavfile as wav
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from faster_whisper import WhisperModel

def download_reference_short(url: str, out_dir: str = "temp/ref_analysis"):
    os.makedirs(out_dir, exist_ok=True)
    video_path = os.path.join(out_dir, "ref_short.mp4")
    audio_path = os.path.join(out_dir, "ref_audio.wav")

    # Support passing local file path or web URL
    if os.path.exists(url):
        import shutil
        shutil.copyfile(url, video_path)
    else:
        subprocess.run([
            "yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "--merge-output-format", "mp4", "-o", video_path, url
        ], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    return video_path, audio_path

def detect_camera_motion(cap, start_frame: int, end_frame: int) -> str:
    """Uses OpenCV Dense Optical Flow on CPU to classify B-roll animation style."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, prev = cap.read()
    if not ret:
        return "static"
    
    h, w = prev.shape[:2]
    prev_gray = cv2.cvtColor(cv2.resize(prev, (180, 320)), cv2.COLOR_BGR2GRAY)
    
    # Sample midpoint frame of the scene
    mid_frame = start_frame + max(1, (end_frame - start_frame) // 2)
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
    ret, curr = cap.read()
    if not ret:
        return "static"
    curr_gray = cv2.cvtColor(cv2.resize(curr, (180, 320)), cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    fx, fy = flow[..., 0], flow[..., 1]
    
    # Check radial divergence from center (Zoom-In vs Zoom-Out)
    cy, cx = 160, 90
    y_grid, x_grid = np.mgrid[0:320, 0:180]
    rx, ry = x_grid - cx, y_grid - cy
    radial_dot = np.mean(fx * rx + fy * ry)

    mean_fx, mean_fy = np.mean(fx), np.mean(fy)
    mag = np.mean(np.sqrt(fx**2 + fy**2))

    if mag < 0.4:
        return "static_or_subtle_float"
    if radial_dot > 15.0:
        return "ken_burns_zoom_in"
    if radial_dot < -15.0:
        return "ken_burns_zoom_out"
    if abs(mean_fx) > abs(mean_fy):
        return "pan_right" if mean_fx < 0 else "pan_left"
    return "tilt_or_shake_vfx"

def analyze_scenes_and_keyframes(video_path: str, out_dir: str = "temp/ref_analysis"):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=22.0, min_scene_len=8))
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    keyframes_dir = os.path.join(out_dir, "keyframes")
    os.makedirs(keyframes_dir, exist_ok=True)

    scenes_data = []
    thumbs = []

    for idx, (start, end) in enumerate(scene_list):
        s_frame, e_frame = start.get_frames(), end.get_frames()
        s_sec, e_sec = round(start.get_seconds(), 2), round(end.get_seconds(), 2)
        mid_frame = s_frame + (e_frame - s_frame) // 2

        # Classify B-Roll animation
        motion_type = detect_camera_motion(cap, s_frame, e_frame)

        # Save midpoint keyframe for Antigravity Vision inspection
        cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
        ret, frame = cap.read()
        kf_path = os.path.join(keyframes_dir, f"scene_{idx+1:02d}.jpg")
        if ret:
            cv2.imwrite(kf_path, frame)
            # Add timestamp label onto thumbnail for contact sheet
            thumb = cv2.resize(frame, (270, 480))
            cv2.putText(thumb, f"S{idx+1}: {s_sec}s ({motion_type[:10]})", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
            thumbs.append(thumb)

        scenes_data.append({
            "scene_index": idx + 1,
            "start_time": s_sec,
            "end_time": e_sec,
            "duration": round(e_sec - s_sec, 2),
            "detected_animation": motion_type,
            "keyframe_image": kf_path
        })

    cap.release()

    # Build a single Contact Sheet Grid so Antigravity can see all scenes in 1 image
    if thumbs:
        cols = 4
        while len(thumbs) % cols != 0:
            thumbs.append(np.zeros((480, 270, 3), dtype=np.uint8))
        rows = [np.hstack(thumbs[i:i+cols]) for i in range(0, len(thumbs), cols)]
        contact_sheet = np.vstack(rows)
        cv2.imwrite(os.path.join(out_dir, "contact_sheet.jpg"), contact_sheet)

    return scenes_data

def analyze_voiceover_and_sfx(audio_path: str):
    model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=4)
    segments, info = model.transcribe(audio_path, word_timestamps=True)

    words = []
    for seg in segments:
        for w in seg.words:
            words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})

    total_dur = words[-1]["end"] - words[0]["start"] if len(words) > 1 else 1.0
    wpm = round((len(words) / total_dur) * 60, 1)

    # Detect sharp transient spikes (SFX whooshes / impacts)
    sr, data = wav.read(audio_path)
    data = data.astype(float)
    data = data / (np.max(np.abs(data)) or 1.0)
    hop = int(sr * 0.1)
    sfx_spikes = []
    for i in range(1, len(data) // hop):
        prev_rms = np.sqrt(np.mean(data[(i-1)*hop : i*hop]**2))
        curr_rms = np.sqrt(np.mean(data[i*hop : (i+1)*hop]**2))
        if curr_rms > 0.45 and (curr_rms - prev_rms) > 0.25:
            sfx_spikes.append(round(i * 0.1, 2))

    return {
        "language": info.language,
        "words_per_minute": wpm,
        "recommended_tts_speed": "+15%" if wpm > 175 else "+5%",
        "sfx_transient_timestamps": sfx_spikes[:12],
        "transcript": " ".join([w["word"] for w in words]),
        "words": words
    }

def reverse_engineer_short(url: str):
    out_dir = "temp/ref_analysis"
    print(f"[*] Downloading & dissecting viral short: {url}")
    v_path, a_path = download_reference_short(url, out_dir)
    scenes = analyze_scenes_and_keyframes(v_path, out_dir)
    audio_metrics = analyze_voiceover_and_sfx(a_path)

    avg_cut = round(np.mean([s["duration"] for s in scenes]), 2) if scenes else 0
    report = {
        "source_url": url,
        "editing_telemetry": {
            "total_scenes": len(scenes),
            "average_shot_duration_sec": avg_cut,
            "cuts_per_minute": round(60 / avg_cut, 1) if avg_cut > 0 else 0,
            "contact_sheet_path": os.path.join(out_dir, "contact_sheet.jpg")
        },
        "voiceover_telemetry": {
            "wpm": audio_metrics["words_per_minute"],
            "recommended_edge_tts_rate": audio_metrics["recommended_tts_speed"],
            "sfx_hit_timestamps": audio_metrics["sfx_transient_timestamps"],
            "full_script": audio_metrics["transcript"]
        },
        "scene_breakdown": scenes
    }

    report_path = os.path.join(out_dir, "deconstruction_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Reverse-engineering complete! Report: {report_path}")
    print(f"[OK] Visual Contact Sheet saved to: {out_dir}/contact_sheet.jpg")
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        reverse_engineer_short(sys.argv[1])
    else:
        print("Usage: python core/reverse_engineer.py <URL_OR_LOCAL_PATH>")
