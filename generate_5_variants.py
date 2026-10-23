import os
import sys
import json
import subprocess
from core.pro_utils import create_smooth_bottom_gradient_png
from core.high_impact_subs import generate_pro_subtitles

def compose_style_variant(
    variant_name: str,
    clean_base_30fps: str,
    broll_clips: list,     # [{"file": "temp/v1_b1.mp4", "start": 2.2, "end": 6.2}, ...]
    ass_path: str,
    is_pip_mode: bool = False,
    is_chromakey: bool = False
) -> str:
    os.makedirs("outputs/variants", exist_ok=True)
    out_mp4 = f"outputs/variants/{variant_name}.mp4"
    grad_png = create_smooth_bottom_gradient_png("temp/smooth_vignette.png")

    inputs = [
        "-i", clean_base_30fps,
        "-i", grad_png,
        "-stream_loop", "-1", "-i", "assets/music/dark_synth_drive.mp3",
        "-i", "assets/sfx/whoosh.wav",
        "-i", "assets/sfx/pop.wav",
        "-i", "assets/sfx/hit.wav"
    ]
    for bc in broll_clips:
        inputs.extend(["-i", bc["file"]])

    # Dynamic Camera Zoom on Speaker via Zoompan (zero memory violations on Windows)
    # 1.22x cold-open pull-back during first 18 frames + subtle live camera drift
    zoom_expr = "if(lte(on,18), 1.22 - 0.22*(on/18), 1.04 + 0.02*sin(on*0.08))"
    filter_parts = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v_spk];"
    ]

    if is_pip_mode:
        # Variant 5 (PiP Reactor): Keep speaker visible in a 320x320 framed badge at (710, 980)
        filter_parts.append(
            "[v_spk]split=2[v_main][v_pip_raw];"
            "[v_pip_raw]crop=700:700:190:180,scale=320:320,"
            "drawbox=x=0:y=0:w=320:h=320:color=0x10B981@1:t=4[v_pip];"
        )
        last_v = "[v_main]"
    else:
        last_v = "[v_spk]"

    for idx, bc in enumerate(broll_clips):
        in_idx = 6 + idx
        b_lbl = f"[br_{idx}]"
        nxt_v = f"[v_l_{idx}]"
        pre_filter = "chromakey=0x00FF00:0.18:0.10," if is_chromakey else ""
        filter_parts.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,{pre_filter}setpts=PTS-STARTPTS+({bc['start']:.2f}/TB){b_lbl};"
            f"{last_v}{b_lbl}overlay=0:0:enable='between(t,{bc['start']:.2f},{bc['end']:.2f})':eof_action=pass{nxt_v};"
        )
        last_v = nxt_v

    if is_pip_mode:
        pip_enable = "+".join([f"between(t,{b['start']:.2f},{b['end']:.2f})" for b in broll_clips])
        filter_parts.append(f"{last_v}[v_pip]overlay=710:980:enable='{pip_enable}':eof_action=pass[v_with_pip];")
        last_v = "[v_with_pip]"

    # Overlay Smooth Feathered Gradient PNG + Burn Giant 108pt Subtitles
    escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
    filter_parts.append(
        f"{last_v}[1:v]overlay=0:0[v_grad];"
        f"[v_grad]subtitles='{escaped_ass}'[v_out];"
    )

    # Studio Audio Pipeline: Dynamic normalization, compressor, SFX impacts, and limiter
    filter_parts.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,"
        "acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,"
        "afade=t=out:st=33.15:d=0.25[voice_loud];"
        "[2:a]volume=0.12,afade=t=out:st=33.15:d=0.25[bgm_bed];"
        "[5:a]adelay=10|10,volume=0.55[sfx_open];"
    )

    sfx_labels = ["[sfx_open]"]
    for idx, bc in enumerate(broll_clips):
        t_in = max(0, int(bc["start"] * 1000))
        t_mid = max(0, int(((bc["start"] + bc["end"]) / 2.0) * 1000))
        t_out = max(0, int((bc["end"] - 0.14) * 1000))
        w_in, p_mid, w_out = f"[wi_{idx}]", f"[pm_{idx}]", f"[wo_{idx}]"
        filter_parts.append(f"[3:a]adelay={t_in}|{t_in},volume=0.48{w_in};")
        filter_parts.append(f"[4:a]adelay={t_mid}|{t_mid},volume=0.52{p_mid};")
        filter_parts.append(f"[3:a]adelay={t_out}|{t_out},volume=0.40{w_out};")
        sfx_labels.extend([w_in, p_mid, w_out])

    filter_parts.append(
        f"{''.join(sfx_labels)}amix=inputs={len(sfx_labels)}:duration=longest:normalize=0[sfx_bus];"
        f"[voice_loud][bgm_bed][sfx_bus]amix=inputs=3:duration=first:normalize=0,"
        f"alimiter=limit=0.95:attack=5:release=50[a_out]"
    )

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]

    print(f"[*] Compositing {variant_name}...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Built Style Variant: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")
    return out_mp4

def render_remotion_scene(comp_id: str, out_file: str, concurrency: int = 6):
    """Renders a single Remotion composition to MP4."""
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
        print(f"[OK] Already rendered: {out_file}")
        return out_file

    os.makedirs(os.path.dirname(out_file) or ".", exist_ok=True)
    print(f"[*] Rendering {comp_id} -> {out_file}...")
    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", comp_id,
        os.path.relpath(out_file, "remotion_studio"),
        f"--concurrency={concurrency}"
    ]
    subprocess.run(cmd, cwd="remotion_studio", shell=True, check=True)
    return out_file

def main():
    clean_base = "temp/clean_base_30fps.mp4"
    if not os.path.exists(clean_base):
        print(f"[*] Slicing clean base 30fps...")
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", "2043.0", "-t", "33.40",
            "-i", "inputs/startup_raj_shamani.mp4",
            "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.12:saturation=1.10",
            "-r", "30", "-fps_mode", "cfr",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            clean_base
        ], check=True)

    # 1. Generate Subtitles
    transcript_file = "temp/clips_test/clip_03_transcript.json"
    with open(transcript_file, "r", encoding="utf-8") as f:
        tdata = json.load(f)
    words = tdata.get("words", [])
    ass_path = generate_pro_subtitles(words, start_t=0.0, end_t=33.40, out_ass="temp/pro_subs.ass")

    # 2. Render all 16 composition clips
    # Clip windows
    windows = [
        {"start": 2.20, "end": 6.20},
        {"start": 10.50, "end": 15.40},
        {"start": 21.20, "end": 26.00},
        {"start": 28.00, "end": 33.40}
    ]

    style_configs = {
        "Variant_1_Iman_Documentary": {
            "comp_prefix": "Iman",
            "is_pip": False,
            "is_chromakey": False,
        },
        "Variant_2_Hormozi_HUD": {
            "comp_prefix": "Hormozi",
            "is_pip": False,
            "is_chromakey": True,
        },
        "Variant_3_Apple_Bento": {
            "comp_prefix": "Bento",
            "is_pip": False,
            "is_chromakey": False,
        },
        "Variant_4_Magnates_Dossier": {
            "comp_prefix": "Magnates",
            "is_pip": False,
            "is_chromakey": False,
        },
        "Variant_5_PiP_Reactor": {
            "comp_prefix": "Iman",  # Uses full-bleed documentary visuals with floating PiP badge
            "is_pip": True,
            "is_chromakey": False,
        }
    }

    # Render Remotion clips needed
    for prefix in ["Iman", "Hormozi", "Bento", "Magnates"]:
        for idx in range(1, 5):
            comp_id = f"{prefix}-Beat{idx}"
            out_file = f"temp/{prefix.lower()}_b{idx}.mp4"
            render_remotion_scene(comp_id, out_file)

    # 3. Compose all 5 variants
    rendered_variants = {}
    for var_name, cfg in style_configs.items():
        prefix = cfg["comp_prefix"]
        clips = [
            {"file": f"temp/{prefix.lower()}_b{idx}.mp4", **windows[idx - 1]}
            for idx in range(1, 5)
        ]
        out_v = compose_style_variant(
            variant_name=var_name,
            clean_base_30fps=clean_base,
            broll_clips=clips,
            ass_path=ass_path,
            is_pip_mode=cfg["is_pip"],
            is_chromakey=cfg.get("is_chromakey", False)
        )
        rendered_variants[var_name] = out_v

    # Mirror primary output to master files
    primary = "outputs/variants/Variant_1_Iman_Documentary.mp4"
    if os.path.exists(primary):
        import shutil
        shutil.copyfile(primary, "outputs/master_short_v5_2.mp4")
        shutil.copyfile(primary, "outputs/capcut_pro_short.mp4")
        print(f"[OK] Mirrored Variant 1 to outputs/master_short_v5_2.mp4 and outputs/capcut_pro_short.mp4")

if __name__ == "__main__":
    main()
