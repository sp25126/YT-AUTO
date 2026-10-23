import os
import subprocess

def render_adaptive_audio_stems(
    voice_track: str,
    duration: float = 33.40,
    out_audio: str = "temp/adaptive_master_audio.wav"
) -> str:
    """
    Assembles a tone-shifting background audio bed with timed risers, 
    vinyl stops, cold-open impacts, and organic foley without volume drop bugs.
    - 0:00: Cold-Open Deep Sub-Boom (stops the scroll!)
    - 0:00 - 0:15.5: Hype Dark Synth
    - 0:02.2: 808 Sub Impact on 90% Fail Stamp
    - 0:10.5: Organic Air Whoosh into Stickman Stage
    - 0:15.2: 0.4s Vinyl Stop Transition
    - 0:15.5 - 0:27.5: Low-Fi Analytical Strategic Groove
    - 0:21.2: Organic Air Whoosh into Veteran Shield
    - 0:27.5 - 0:33.4: Tension Riser into Dead Silence
    - 0:28.0: Transition Whoosh into Yacht/Devil Rip
    - 33.15s: 0.25s Clean Fade-Out before "AND"
    """
    os.makedirs(os.path.dirname(out_audio) or ".", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    fade_start = max(0.0, duration - 0.25)
    clean_voice = "temp/clean_voice_leveled.wav"
    
    # 1. Normalize voice to -14 LUFS with zero drift and clean fade out before "AND"
    cmd_clean_voice = [
        "ffmpeg", "-y", "-i", voice_track,
        "-af", f"highpass=f=80,dynaudnorm=f=120:g=15:p=0.95,acompressor=threshold=-14dB:ratio=3:attack=10:release=80:makeup=4dB,afade=t=out:st={fade_start:.2f}:d=0.25",
        "-c:a", "pcm_s16le",
        clean_voice
    ]
    subprocess.run(cmd_clean_voice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 2. Complex audio filtergraph: Swapping BGM and placing procedural organic SFX
    riser_sfx = "assets/sfx/riser.wav" if os.path.exists("assets/sfx/riser.wav") else "assets/sfx/whoosh.wav"
    filtergraph = (
        "[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.12,atrim=0:15.5,asetpts=PTS-STARTPTS[bgm_hype];"
        "[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.11,atrim=0:12.0,asetpts=PTS-STARTPTS[bgm_intellect];"
        "[bgm_hype][bgm_intellect]concat=n=2:v=0:a=1[bgm_chained];"
        "[4:a]adelay=10|10,volume=0.60[sfx_cold_open];"
        "[4:a]adelay=2200|2200,volume=0.55[sfx_sub808];"
        "[5:a]adelay=10500|10500,volume=0.38[sfx_whoosh2];"
        "[3:a]adelay=15200|15200,volume=0.45[sfx_tapestop];"
        "[5:a]adelay=21200|21200,volume=0.38[sfx_whoosh3];"
        "[6:a]adelay=27500|27500,volume=0.50[sfx_tension_riser];"
        "[5:a]adelay=28000|28000,volume=0.38[sfx_whoosh4];"
        "[0:a][bgm_chained]amix=inputs=2:duration=first:normalize=0[dialogue_music];"
        "[dialogue_music][sfx_cold_open][sfx_sub808][sfx_whoosh2][sfx_tapestop][sfx_whoosh3][sfx_tension_riser][sfx_whoosh4]"
        "amix=inputs=8:duration=first:normalize=0,"
        "alimiter=limit=0.95:attack=5:release=50[final_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", clean_voice,
        "-stream_loop", "-1", "-i", "assets/music/dark_synth_drive.mp3",
        "-stream_loop", "-1", "-i", "assets/music/pizzicato_comedy.mp3",
        "-i", "assets/sfx/vinyl_stop.wav",
        "-i", "assets/sfx/hit.wav",
        "-i", "assets/sfx/whoosh.wav",
        "-i", riser_sfx,
        "-filter_complex", filtergraph,
        "-map", "[final_out]",
        "-t", str(duration),
        out_audio
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered Adaptive Tone-Shifting Audio Bed: {out_audio}")
    return out_audio

if __name__ == "__main__":
    render_adaptive_audio_stems("temp/clean_base_30fps.mp4", duration=33.40)
