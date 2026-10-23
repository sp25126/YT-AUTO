import os
import subprocess
from core.presets import ARCHETYPE_PRESETS

def compose_editor_short(
    video_path: str,
    start_t: float,
    end_t: float,
    archetype: str = "comedy_banter",
    sfx_markers: list = None,
    silence_windows: list = None,   # e.g., [{"start": 14.2, "end": 15.1}] for punchlines
    output_path: str = "outputs/short.mp4",
    ass_path: str = "captions.ass"
):
    if sfx_markers is None:
        sfx_markers = []
    if silence_windows is None:
        silence_windows = []

    duration = end_t - start_t
    cfg = ARCHETYPE_PRESETS.get(archetype, ARCHETYPE_PRESETS["comedy_banter"])
    bgm_path = os.path.join("assets/music", cfg["bgm_style"])
    if not os.path.exists(bgm_path):
        bgm_path = "assets/music/chill_lofi.mp3"

    has_bgm = os.path.exists(bgm_path)
    inputs = [
        "-ss", str(start_t), "-t", str(duration), "-i", video_path
    ]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])

    # Map archetype SFX
    sfx_library = {
        "record_scratch": "assets/sfx/record_scratch.wav",
        "crickets": "assets/sfx/crickets.wav",
        "braam_hit": "assets/sfx/braam.wav",
        "snap_pop": "assets/sfx/pop.wav",
        "pop": "assets/sfx/pop.wav",
        "whoosh": "assets/sfx/whoosh.wav",
        "hit": "assets/sfx/hit.wav",
        "vinyl_stop": "assets/sfx/vinyl_stop.wav"
    }

    sfx_inputs_map = {}
    idx = 2 if has_bgm else 1
    for item in sfx_markers:
        name = item.get("effect")
        if name in sfx_library and os.path.exists(sfx_library[name]) and name not in sfx_inputs_map:
            inputs.extend(["-i", sfx_library[name]])
            sfx_inputs_map[name] = idx
            idx += 1

    # 1. Video Processing: 9:16 blurred background + archetype color grade
    fg_filter = f"[fg_raw]scale=1080:-1,{cfg['color_filter']}[fg_graded];"
    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    filter_graph = [
        "[0:v]split=2[bg_raw][fg_raw];",
        "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg_blur];",
        fg_filter,
        "[bg_blur][fg_graded]overlay=(W-w)/2:(H-h)/2[base_canvas];",
        f"[base_canvas]subtitles=filename='{clean_ass}'[v_out];"
    ]

    # 2. Dynamic Audio: Build silence windows into BGM (Punchline Cuts)
    if has_bgm:
        bgm_vol = cfg["ducking_depth"]
        if silence_windows:
            vol_conditions = " * ".join(
                [f"(1-between(t,{w['start']-start_t:.2f},{w['end']-start_t:.2f}))" for w in silence_windows]
            )
            bgm_filter = f"[1:a]volume=eval=frame:volume='{bgm_vol}*{vol_conditions}'[bgm_processed];"
        else:
            bgm_filter = f"[1:a]volume={bgm_vol}[bgm_processed];"
        filter_graph.append(bgm_filter)
        filter_graph.append("[0:a][bgm_processed]amix=inputs=2:duration=first[speech_bgm];")
    else:
        filter_graph.append("[0:a]acopy[speech_bgm];")

    # 3. Lay down SFX with millisecond offsets
    audio_branches = ["[speech_bgm]"]
    for i, sfx in enumerate(sfx_markers):
        name = sfx.get("effect")
        if name in sfx_inputs_map:
            input_idx = sfx_inputs_map[name]
            delay_ms = max(0, int((sfx["time"] - start_t) * 1000))
            branch = f"[sfx_{i}]"
            filter_graph.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},volume=0.45{branch};")
            audio_branches.append(branch)

    if len(audio_branches) > 1:
        filter_graph.append(f"{''.join(audio_branches)}amix=inputs={len(audio_branches)}:duration=first[a_out]")
    else:
        filter_graph.append("[speech_bgm]acopy[a_out]")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_graph),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True)

def render_short_video(
    video_path: str,
    start_t: float,
    end_t: float,
    sfx_markers: list,
    output_path: str = "outputs/short.mp4",
    bgm_path: str = "assets/music/chill_lofi.mp3",
    archetype: str = "comedy_banter",
    silence_windows: list = None
):
    compose_editor_short(
        video_path=video_path,
        start_t=start_t,
        end_t=end_t,
        archetype=archetype,
        sfx_markers=sfx_markers,
        silence_windows=silence_windows or [],
        output_path=output_path
    )
