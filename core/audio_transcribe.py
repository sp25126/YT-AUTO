import json
import subprocess
from faster_whisper import WhisperModel

def extract_and_transcribe(video_path: str, output_json: str = "transcript.json"):
    temp_wav = "temp_mono.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        temp_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 4 CPU threads, int8 quantization: minimal RAM and no GPU needed
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=4)
    segments, _ = model.transcribe(temp_wav, word_timestamps=True)

    result = []
    for segment in segments:
        for word in segment.words:
            result.append({
                "word": word.word.strip(),
                "start": round(word.start, 2),
                "end": round(word.end, 2)
            })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result
