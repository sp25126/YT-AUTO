"""sound_mixer.py - Multi-track sonic pacing and sidechain ducking engine.
"""

def generate_ducking_filter(
    dialogue_label: str = "0:a",
    bgm_label: str = "1:a",
    output_label: str = "a_ducked"
) -> str:
    """Builds sidechain compression filtergraph for dialogue-ducked background music."""
    return (
        f"[{bgm_label}]volume=0.14[bgm_base];"
        f"[{dialogue_label}][bgm_base]sidechaincompress="
        f"threshold=0.08:ratio=6:attack=15:release=250[{output_label}]"
    )

def generate_sfx_chain(
    sfx_cues: list,
    base_audio_label: str = "speech_bgm",
    output_label: str = "a_out"
) -> tuple:
    """Builds delayed SFX overlay chain."""
    filter_lines = []
    labels = [f"[{base_audio_label}]"]
    
    for i, cue in enumerate(sfx_cues):
        input_idx = cue.get("input_idx", 2)
        delay_ms = cue.get("delay_ms", 100)
        vol = cue.get("volume", 0.35)
        sfx_lbl = f"[sfx_{i}]"
        filter_lines.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},volume={vol}{sfx_lbl};")
        labels.append(sfx_lbl)
        
    filter_lines.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=first[{output_label}]")
    return "\n".join(filter_lines), output_label

if __name__ == "__main__":
    print(generate_ducking_filter())
