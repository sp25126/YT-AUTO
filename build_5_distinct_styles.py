import os
import sys
import json
import subprocess
from core.five_style_filters import (
    create_top_luma_mask_png,
    create_curved_cinema_border_png,
    create_torn_newspaper_shoulder_overlay,
    generate_luxury_pill_ass,
    generate_davinci_writeon_ass,
    generate_pyramid_softlight_ass,
    generate_vox_editorial_ass,
    generate_marksoy_minimal_ass
)

def escape_path_for_ffmpeg(p: str) -> str:
    return p.replace("\\", "/").replace(":", "\\:")

# ==============================================================================
# VARIANT 1: 01_IG_Luxury_Glass.mp4
# ==============================================================================
def build_variant_1_luxury(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 1: 01_IG_Luxury_Glass.mp4")
    print("="*70)
    
    top_mask = create_top_luma_mask_png("temp/top_luma_mask.png")
    ass_path = generate_luxury_pill_ass(words, 0.0, 33.40, "temp/style1_luxury.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    # Inputs:
    # 0: clean_base
    # 1: top_mask
    # 2: BGM chill_lofi
    # 3: pop
    # 4: whoosh
    # 5: sub_drop
    # 6..9: broll videos
    # 10..13: pill cards
    inputs = [
        "-i", clean_base,
        "-i", top_mask,
        "-stream_loop", "-1", "-i", "assets/music/chill_lofi.mp3",
        "-i", "assets/sfx/pop.wav",
        "-i", "assets/sfx/whoosh.wav",
        "-i", "assets/sfx/sub_drop.wav",
        "-i", "remotion_studio/public/assets/broll_beat1_crash.mp4",
        "-i", "remotion_studio/public/assets/broll_beat2_early.mp4",
        "-i", "remotion_studio/public/assets/broll_beat3_mentors.mp4",
        "-i", "remotion_studio/public/assets/broll_beat4_rosy.mp4",
        "-i", "temp/style1_pill1.mp4",
        "-i", "temp/style1_pill2.mp4",
        "-i", "temp/style1_pill3.mp4",
        "-i", "temp/style1_pill4.mp4",
    ]
    
    # Filtergraph:
    # Base Speaker: Teal & Gold grade + speed ramp zoom
    # 1.25x -> 1.0x whip zoom in first 14 frames
    zoom_expr = "if(lte(on,14), 1.25 - 0.25*(on/14), 1.02 + 0.02*sin(on*0.06))"
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        f"eq=contrast=1.16:saturation=1.18[v_spk];"
    ]
    
    # Upper Luma B-Roll: Mask each broll clip with top_luma_mask using alphamerge
    brolls = [
        (6, 2.20, 6.00),
        (7, 10.80, 15.20),
        (8, 21.20, 25.80),
        (9, 28.00, 33.00),
    ]
    last_v = "[v_spk]"
    for idx, (in_idx, t_s, t_e) in enumerate(brolls):
        b_label = f"[broll_luma_{idx}]"
        next_v = f"[v_broll_{idx}]"
        filters.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+({t_s:.2f}/TB)[b_raw_{idx}];"
            f"[b_raw_{idx}][1:v]alphamerge{b_label};"
            f"{last_v}{b_label}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Overlay Apple Glass Pills with colorkey black
    pills = [
        (10, 2.20, 6.00),
        (11, 10.80, 15.20),
        (12, 21.20, 25.80),
        (13, 28.00, 33.00),
    ]
    for idx, (in_idx, t_s, t_e) in enumerate(pills):
        p_label = f"[pill_{idx}]"
        next_v = f"[v_pill_{idx}]"
        filters.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+({t_s:.2f}/TB){p_label};"
            f"{last_v}{p_label}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Subtitles
    filters.append(f"{last_v}subtitles='{escaped_ass}'[v_out];")
    
    # Audio Mix: Chill Lofi BGM + Glass UI Pops + Sub Drops
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25[v_voice];"
        "[2:a]volume=0.14,afade=t=out:st=33.15:d=0.25[bgm];"
        "[5:a]adelay=10|10,volume=0.65[sfx_drop];"
        "[3:a]adelay=2200|2200,volume=0.55[sfx_pop1];"
        "[3:a]adelay=10800|10800,volume=0.55[sfx_pop2];"
        "[3:a]adelay=21200|21200,volume=0.55[sfx_pop3];"
        "[3:a]adelay=28000|28000,volume=0.55[sfx_pop4];"
        "[sfx_drop][sfx_pop1][sfx_pop2][sfx_pop3][sfx_pop4]amix=inputs=5:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


# ==============================================================================
# VARIANT 2: 02_DaVinci_Fusion_Editorial.mp4
# ==============================================================================
def build_variant_2_davinci(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 2: 02_DaVinci_Fusion_Editorial.mp4")
    print("="*70)
    
    ass_path = generate_davinci_writeon_ass(words, 0.0, 33.40, "temp/style2_davinci.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    # 4-Frame Rapid Shutter Montage (10.8s - 12.0s):
    # 5 images flashed 4 frames (0.133s) apart:
    # 10.80: hourglass, 10.93: megacity, 11.07: boardroom, 11.20: luxury, 11.33: circuit
    inputs = [
        "-i", clean_base,
        "-stream_loop", "-1", "-i", "assets/music/eerie_sub_drone.mp3",
        "-stream_loop", "-1", "-i", "assets/sfx/firewood.wav",
        "-i", "assets/sfx/shutter.wav",
        "-i", "assets/sfx/hit.wav",
        "-i", "temp/style2_paper1.mp4",        # 5
        "-i", "temp/style2_paper2.mp4",        # 6
        "-loop", "1", "-t", "0.20", "-i", "assets/broll/hourglass_timing.jpg",  # 7
        "-loop", "1", "-t", "0.20", "-i", "assets/broll/cyberpunk_megacity.jpg",# 8
        "-loop", "1", "-t", "0.20", "-i", "assets/broll/boardroom_veterans.jpg", # 9
        "-loop", "1", "-t", "0.20", "-i", "assets/broll/golden_luxury.jpg",     # 10
        "-loop", "1", "-t", "0.20", "-i", "assets/broll/circuit_hardware.jpg",   # 11
    ]
    
    filters = [
        # Stepped zoom jumps
        "[0:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920,"
        "eq=contrast=1.12:saturation=1.05[v_spk];"
    ]
    
    last_v = "[v_spk]"
    # Overlay Paper 1 at 2.20s–6.00s
    filters.append(
        f"[5:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(2.20/TB)[p1];"
        f"{last_v}[p1]overlay=0:0:enable='between(t,2.20,6.00)':eof_action=pass[v_p1];"
    )
    last_v = "[v_p1]"
    
    # 4-frame shutter montage at 10.80..12.00
    montage_imgs = [
        (7, 10.80, 10.94),
        (8, 10.94, 11.08),
        (9, 11.08, 11.22),
        (10, 11.22, 11.36),
        (11, 11.36, 12.00),
    ]
    for idx, (in_idx, t_s, t_e) in enumerate(montage_imgs):
        m_lbl = f"[m_{idx}]"
        next_v = f"[v_m_{idx}]"
        filters.append(
            f"[{in_idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setpts=PTS-STARTPTS+({t_s:.2f}/TB){m_lbl};"
            f"{last_v}{m_lbl}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Overlay Paper 2 at 21.20s–25.80s
    filters.append(
        f"[6:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(21.20/TB)[p2];"
        f"{last_v}[p2]overlay=0:0:enable='between(t,21.20,25.80)':eof_action=pass[v_p2];"
    )
    last_v = "[v_p2]"
    
    # Subtitles
    filters.append(f"{last_v}subtitles='{escaped_ass}'[v_out];")
    
    # Audio Mix: Ambient Drone + Firewood Crackle + Shutter clicks on each montage frame + Deep Hit
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25[v_voice];"
        "[1:a]volume=0.10,afade=t=out:st=33.15:d=0.25[bgm_drone];"
        "[2:a]volume=0.08,afade=t=out:st=33.15:d=0.25[bgm_fire];"
        "[4:a]adelay=2200|2200,volume=0.65[sfx_hit];"
        "[3:a]adelay=10800|10800,volume=0.55[sh1];"
        "[3:a]adelay=10940|10940,volume=0.55[sh2];"
        "[3:a]adelay=11080|11080,volume=0.55[sh3];"
        "[3:a]adelay=11220|11220,volume=0.55[sh4];"
        "[3:a]adelay=11360|11360,volume=0.55[sh5];"
        "[sfx_hit][sh1][sh2][sh3][sh4][sh5]amix=inputs=6:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_drone][bgm_fire][sfx_bus]amix=inputs=4:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


# ==============================================================================
# VARIANT 3: 03_Curved_Cinema_Pyramid.mp4
# ==============================================================================
def build_variant_3_curved_cinema(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 3: 03_Curved_Cinema_Pyramid.mp4")
    print("="*70)
    
    curved_border = create_curved_cinema_border_png("temp/curved_border.png")
    ass_path = generate_pyramid_softlight_ass(words, 0.0, 33.40, "temp/style3_pyramid.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    inputs = [
        "-i", clean_base,
        "-i", curved_border,
        "-stream_loop", "-1", "-i", "assets/music/warm_ambient_piano.mp3",
        "-i", "assets/sfx/ocean_waves.wav",
        "-i", "assets/sfx/wind.wav",
        "-i", "assets/sfx/whoosh.wav",
        "-i", "remotion_studio/public/assets/broll_beat1_crash.mp4",
        "-i", "remotion_studio/public/assets/broll_beat2_early.mp4",
        "-i", "remotion_studio/public/assets/broll_beat3_mentors.mp4",
        "-i", "remotion_studio/public/assets/broll_beat4_rosy.mp4",
    ]
    
    # High-contrast cinema grading
    filters = [
        "[0:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920,"
        "eq=contrast=1.24:saturation=1.32[v_spk];"
    ]
    
    # Full-screen cinema B-roll cuts
    brolls = [
        (6, 2.20, 6.00),
        (7, 10.80, 15.20),
        (8, 21.20, 25.80),
        (9, 28.00, 33.00),
    ]
    last_v = "[v_spk]"
    for idx, (in_idx, t_s, t_e) in enumerate(brolls):
        b_label = f"[broll_cin_{idx}]"
        next_v = f"[v_cin_{idx}]"
        filters.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,eq=contrast=1.24:saturation=1.32,setpts=PTS-STARTPTS+({t_s:.2f}/TB){b_label};"
            f"{last_v}{b_label}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Apply Permanent Curved-Edge Black Cinema Border
    filters.append(
        f"{last_v}[1:v]overlay=0:0[v_border];"
        f"[v_border]subtitles='{escaped_ass}'[v_out];"
    )
    
    # Audio Mix: Warm Piano BGM + Diegetic Wind (at 10.8s) + Diegetic Ocean Waves (at 28.0s)
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25[v_voice];"
        "[2:a]volume=0.15,afade=t=out:st=33.15:d=0.25[bgm_piano];"
        "[4:a]adelay=10800|10800,volume=0.45[sfx_wind];"
        "[3:a]adelay=28000|28000,volume=0.50[sfx_ocean];"
        "[5:a]adelay=2200|2200,volume=0.40[sfx_whoosh];"
        "[sfx_wind][sfx_ocean][sfx_whoosh]amix=inputs=3:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_piano][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


# ==============================================================================
# VARIANT 4: 04_Vox_Pro_Documentary.mp4
# ==============================================================================
def build_variant_4_vox(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 4: 04_Vox_Pro_Documentary.mp4")
    print("="*70)
    
    chart_windows = [
        {"start": 2.20, "end": 6.20},
        {"start": 10.80, "end": 15.40},
        {"start": 21.20, "end": 26.00},
    ]
    ass_path = generate_vox_editorial_ass(words, 0.0, 33.40, chart_windows, "temp/style4_vox.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    inputs = [
        "-i", clean_base,
        "-stream_loop", "-1", "-i", "assets/music/pizzicato_comedy.mp3",
        "-i", "assets/sfx/tick.wav",
        "-i", "assets/sfx/paper_rip.wav",
        "-i", "assets/sfx/hit.wav",
        "-i", "temp/style4_bar.mp4",
        "-i", "temp/style4_curve.mp4",
        "-i", "temp/style4_blue.mp4",
    ]
    
    filters = [
        "[0:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920,"
        "noise=alls=6:allf=t+u[v_spk];"
    ]
    
    # Overlay Vox Charts
    takeovers = [
        (5, 2.20, 6.20),
        (6, 10.80, 15.40),
        (7, 21.20, 26.00),
    ]
    last_v = "[v_spk]"
    for idx, (in_idx, t_s, t_e) in enumerate(takeovers):
        c_label = f"[vox_chart_{idx}]"
        next_v = f"[v_vox_{idx}]"
        filters.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+({t_s:.2f}/TB){c_label};"
            f"{last_v}{c_label}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    filters.append(f"{last_v}subtitles='{escaped_ass}'[v_out];")
    
    # Audio Mix: Pizzicato Loop + Odometer Ticks + Paper Rips
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25[v_voice];"
        "[1:a]volume=0.13,afade=t=out:st=33.15:d=0.25[bgm_pizz];"
        "[2:a]adelay=2400|2400,volume=0.65[tick1];"
        "[2:a]adelay=2700|2700,volume=0.65[tick2];"
        "[2:a]adelay=3000|3000,volume=0.65[tick3];"
        "[3:a]adelay=10800|10800,volume=0.55[rip1];"
        "[4:a]adelay=2200|2200,volume=0.50[hit1];"
        "[tick1][tick2][tick3][rip1][hit1]amix=inputs=5:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_pizz][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


# ==============================================================================
# VARIANT 5: 05_MarkSoy_MixedMedia_Wrapper.mp4
# ==============================================================================
def build_variant_5_marksoy(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 5: 05_MarkSoy_MixedMedia_Wrapper.mp4")
    print("="*70)
    
    newspaper_collar = create_torn_newspaper_shoulder_overlay("temp/newspaper_shoulders.png")
    takeovers = [
        {"start": 2.20, "end": 6.00},
        {"start": 10.50, "end": 15.40},
        {"start": 21.20, "end": 26.00},
        {"start": 28.00, "end": 33.40},
    ]
    ass_path = generate_marksoy_minimal_ass(words, 0.0, 33.40, takeovers, "temp/style5_marksoy.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    inputs = [
        "-i", clean_base,
        "-i", newspaper_collar,
        "-stream_loop", "-1", "-i", "assets/music/dark_synth_drive.mp3",
        "-i", "assets/sfx/paper_rip.wav",
        "-i", "assets/sfx/pop.wav",
        "-i", "assets/sfx/sub_drop.wav",
        "-i", "assets/sfx/whoosh.wav",
        "-i", "temp/style5_card.mp4",       # 7 (2.20-6.00)
        "-i", "temp/style5_blocks.mp4",     # 8 (10.50-15.40)
        "-i", "temp/style5_cream1.mp4",     # 9 (21.20-26.00)
        "-i", "temp/style5_cream2.mp4",     # 10 (28.00-33.40)
    ]
    
    filters = [
        "[0:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920[v_spk];"
    ]
    
    # Overlay Beat B (CardZoom 2.20-6.00)
    filters.append(
        "[7:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(2.20/TB)[v_c7];"
        "[v_spk][v_c7]overlay=0:0:enable='between(t,2.20,6.00)':eof_action=pass[v_b];"
    )
    # Overlay Beat C (CornerBlocks 10.50-15.40)
    filters.append(
        "[8:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(10.50/TB)[v_c8];"
        "[v_b][v_c8]overlay=0:0:enable='between(t,10.50,15.40)':eof_action=pass[v_c];"
    )
    # Overlay Beat D (Torn Newspaper Shoulder Collar wrapping live speaker at 16.00-21.20)
    filters.append(
        "[v_c][1:v]overlay=0:0:enable='between(t,16.00,21.20)':eof_action=pass[v_d];"
    )
    # Overlay Beat E (CreamSerif1 21.20-26.00)
    filters.append(
        "[9:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(21.20/TB)[v_c9];"
        "[v_d][v_c9]overlay=0:0:enable='between(t,21.20,26.00)':eof_action=pass[v_e];"
    )
    # Overlay Beat F (CreamSerif2 28.00-33.40)
    filters.append(
        "[10:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(28.00/TB)[v_c10];"
        "[v_e][v_c10]overlay=0:0:enable='between(t,28.00,33.40)':eof_action=pass[v_f];"
    )
    
    # Subtitles: only appear on live speaker (suppressed during takeovers)
    filters.append(f"[v_f]subtitles='{escaped_ass}'[v_out];")
    
    # Audio Mix: Percussive Drive + Paper Rips + Sub Drop + Whooshes
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25[v_voice];"
        "[2:a]volume=0.13,afade=t=out:st=33.15:d=0.25[bgm_stomp];"
        "[3:a]adelay=16000|16000,volume=0.60[rip_collar];"
        "[5:a]adelay=2200|2200,volume=0.65[drop_card];"
        "[6:a]adelay=10500|10500,volume=0.50[whoosh_blocks];"
        "[4:a]adelay=21200|21200,volume=0.55[pop_cream];"
        "[rip_collar][drop_card][whoosh_blocks][pop_cream]amix=inputs=4:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_stomp][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-r", "30", "-fps_mode", "cfr",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


# ==============================================================================
# MAIN ORCHESTRATOR
# ==============================================================================
def main():
    os.makedirs("outputs/5_viral_styles", exist_ok=True)
    clean_base = "temp/clean_base_30fps.mp4"
    if not os.path.exists(clean_base):
        raise FileNotFoundError(f"Missing {clean_base}")
        
    with open("temp/clips_test/clip_03_transcript.json", "r", encoding="utf-8") as f:
        tdata = json.load(f)
    words = tdata.get("words", [])
    
    # Build each variant into outputs/5_viral_styles/
    build_variant_1_luxury(clean_base, "outputs/5_viral_styles/01_IG_Luxury_Glass.mp4", words)
    build_variant_2_davinci(clean_base, "outputs/5_viral_styles/02_DaVinci_Fusion_Editorial.mp4", words)
    build_variant_3_curved_cinema(clean_base, "outputs/5_viral_styles/03_Curved_Cinema_Pyramid.mp4", words)
    build_variant_4_vox(clean_base, "outputs/5_viral_styles/04_Vox_Pro_Documentary.mp4", words)
    build_variant_5_marksoy(clean_base, "outputs/5_viral_styles/05_MarkSoy_MixedMedia_Wrapper.mp4", words)
    
    print("\n" + "="*70)
    print("[OK] ALL 5 DISTINCT VIRAL STYLES GENERATED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    main()
