import subprocess
import os

def render_context_short(
    video_path: str,
    start_t: float,
    end_t: float,
    manifest: dict,
    output_path: str = "outputs/context_short.mp4",
    ass_path: str = "context_captions.ass"
):
    duration = end_t - start_t
    beats = manifest.get("beats", [])
    sfx_cues = manifest.get("sfx_cues", [])
    silence_windows = manifest.get("silence_windows", [])

    # Dynamic BGM selection based on primary theme
    bgm_map = {
        "dark": "assets/music/eerie_sub_drone.mp3",
        "comedy": "assets/music/pizzicato_comedy.mp3",
        "hype": "assets/music/dark_synth_drive.mp3",
        "thoughtful": "assets/music/warm_ambient_piano.mp3"
    }
    bgm_file = bgm_map.get(manifest.get("primary_mood", "thoughtful"), "assets/music/warm_ambient_piano.mp3")
    if not os.path.exists(bgm_file):
        bgm_file = "assets/music/chill_lofi.mp3"

    has_bgm = os.path.exists(bgm_file)
    inputs = [
        "-ss", str(start_t), "-t", str(duration), "-i", video_path
    ]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_file])

    # Map SFX files
    sfx_bank = {
        "record_scratch": "assets/sfx/record_scratch.wav",
        "braam": "assets/sfx/braam.wav",
        "whoosh": "assets/sfx/whoosh.wav",
        "sub_drop": "assets/sfx/hit.wav",
        "pop": "assets/sfx/pop.wav"
    }
    
    sfx_index_map = {}
    current_idx = 2 if has_bgm else 1
    for cue in sfx_cues:
        eff = cue.get("effect")
        if eff in sfx_bank and os.path.exists(sfx_bank[eff]) and eff not in sfx_index_map:
            inputs.extend(["-i", sfx_bank[eff]])
            sfx_index_map[eff] = current_idx
            current_idx += 1

    # 1. Video Filter: 9:16 blurred background + dynamic punch-in on shock beats
    punch_conditions = []
    for beat in beats:
        if beat.get("tone") == "shock":
            rel_start = max(0, beat["start"] - start_t)
            rel_end = max(0, beat["end"] - start_t)
            punch_conditions.append(f"between(t,{rel_start:.2f},{rel_end:.2f})")
            
    zoom_expr = "if(" + "+".join(punch_conditions) + ",1.20,1.0)" if punch_conditions else "1.0"
    clean_ass = ass_path.replace("\\", "/")

    filter_graph = [
        "[0:v]split=2[bg_raw][fg_raw];",
        "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg_blur];",
        f"[fg_raw]scale=eval=frame:w='1080*{zoom_expr}':h='-1'[fg_dynamic];",
        "[bg_blur][fg_dynamic]overlay=(W-w)/2:(H-h)/2[base_canvas];",
        f"[base_canvas]subtitles='{clean_ass}'[v_out];"
    ]

    # 2. Dynamic Audio: Mute BGM during silence windows and whispers
    if has_bgm:
        vol_expressions = []
        for sw in silence_windows:
            r_s = max(0, sw["start"] - start_t)
            r_e = max(0, sw["end"] - start_t)
            vol_expressions.append(f"(1-between(t,{r_s:.2f},{r_e:.2f}))")

        base_vol = 0.12
        if vol_expressions:
            vol_formula = f"{base_vol} * " + " * ".join(vol_expressions)
            filter_graph.append(f"[1:a]volume=eval=frame:volume='{vol_formula}'[bgm_processed];")
        else:
            filter_graph.append(f"[1:a]volume={base_vol}[bgm_processed];")

        filter_graph.append("[0:a][bgm_processed]amix=inputs=2:duration=first[dialogue_mix];")
    else:
        filter_graph.append("[0:a]acopy[dialogue_mix];")

    # 4. Lay down SFX
    delayed_labels = ["[dialogue_mix]"]
    for i, cue in enumerate(sfx_cues):
        eff = cue.get("effect")
        if eff in sfx_index_map:
            input_num = sfx_index_map[eff]
            delay_ms = max(0, int((cue["time"] - start_t) * 1000))
            label = f"[sfx_{i}]"
            filter_graph.append(f"[{input_num}:a]adelay={delay_ms}|{delay_ms},volume=0.45{label};")
            delayed_labels.append(label)

    if len(delayed_labels) > 1:
        filter_graph.append(f"{''.join(delayed_labels)}amix=inputs={len(delayed_labels)}:duration=first[a_out]")
    else:
        filter_graph.append("[dialogue_mix]acopy[a_out]")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_graph),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Context-Aware Master Rendered: {output_path}")
