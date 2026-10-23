import os
import json
import subprocess
import argparse
from faster_whisper import WhisperModel

def extract_audio(input_video, output_audio="temp_audio.wav"):
    cmd = [
        "ffmpeg", "-y", "-i", input_video,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        output_audio
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_audio

def transcribe_cpu(audio_path, output_json="transcript.json"):
    print("[*] Transcribing on CPU using faster-whisper (int8)...")
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=4)
    segments, _ = model.transcribe(audio_path, word_timestamps=True)
    
    words = []
    full_text_segments = []
    for seg in segments:
        full_text_segments.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        for w in seg.words:
            words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})
            
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"segments": full_text_segments, "words": words}, f, indent=2)
    return words

def score_hook(first_sentence):
    """Invokes hookscore.py from the youtube-agent-skill repository."""
    hook_script = ".agents/skills/youtube-agent-skill/skills/yt-script/hookscore.py"
    if os.path.exists(hook_script):
        res = subprocess.run(["python", hook_script, "--hook", first_sentence], capture_output=True, text=True)
        print(f"Hook Evaluation:\n{res.stdout}")

def generate_karaoke_ass(words, clip_start, clip_end, output_ass="subs.ass"):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat,78,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,0,2,80,80,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    clip_words = [w for w in words if w["start"] >= clip_start and w["end"] <= clip_end]
    lines = []
    chunk_size = 3
    for i in range(0, len(clip_words), chunk_size):
        chunk = clip_words[i:i + chunk_size]
        t_start = max(0.0, chunk[0]["start"] - clip_start)
        t_end = max(0.1, chunk[-1]["end"] - clip_start)
        
        s_fmt = f"{int(t_start//3600):01d}:{int((t_start%3600)//60):02d}:{t_start%60:05.2f}"
        e_fmt = f"{int(t_end//3600):01d}:{int((t_end%3600)//60):02d}:{t_end%60:05.2f}"
        
        text_karaoke = ""
        for w in chunk:
            duration_cs = max(1, int((w["end"] - w["start"]) * 100))
            text_karaoke += f"{{\\k{duration_cs}}}{w['word'].upper()} "
            
        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},Default,,0,0,0,,{text_karaoke.strip()}")
        
    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))

def render_vertical_short(video_path, clip_start, duration, output_path="output_short.mp4"):
    print("[*] Rendering vertical short with blurred letterbox and subtitles...")
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(clip_start), "-t", str(duration),
        "-i", video_path,
        "-filter_complex",
        (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[blurred];"
            "[fg]scale=1080:-1[crisp];"
            "[blurred][crisp]overlay=(W-w)/2:(H-h)/2[base];"
            "[base]subtitles=subs.ass[v_out]"
        ),
        "-map", "[v_out]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"[✓] Render finished: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Input podcast MP4 file")
    parser.add_argument("--start", type=float, default=None, help="Clip start timestamp in seconds")
    parser.add_argument("--duration", type=float, default=45.0, help="Clip length in seconds")
    args = parser.parse_args()

    audio = extract_audio(args.video)
    words = transcribe_cpu(audio)
    
    if args.start is not None:
        generate_karaoke_ass(words, args.start, args.start + args.duration)
        render_vertical_short(args.video, args.start, args.duration)
    else:
        print("\n[!] Audio transcribed to transcript.json. Open Antigravity chat to pick the hook.")
