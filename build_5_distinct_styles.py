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
# VARIANT 1: 01_IG_Luxury_Glass.mp4 (Instagram Luxury & Speed-Ramp DetnsvBN1fs)
# ==============================================================================
def build_variant_1_luxury(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 1: 01_IG_Luxury_Glass.mp4 (PRO DIRECTOR CUT)")
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
    
    # Dynamic Camera Scale Punches (The 2.4s Cognitive Reset):
    z_expr = (
        "if(between(t,2.2,6.5), 1.18, "
        "if(between(t,8.5,15.5), 1.18, "
        "if(between(t,15.5,21.5), 1.08, "
        "if(between(t,21.5,27.5), 1.20, "
        "if(between(t,27.5,33.4), 1.14, 1.0)))))"
    )
    
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"crop=w='1080/{z_expr}':h='1920/{z_expr}':x='(1080-out_w)/2':y='(1920-out_h)/2',"
        f"scale=1080:1920,eq=contrast=1.16:saturation=1.18[v_spk];"
    ]
    
    # Upper Luma B-Roll: Moving HD video blended into dark studio ceiling
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
        
    # Overlay Apple Glass Notification Pills with colorkey black
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
    
    # Audio Engineering: Voice + Sidechain Ducked Chill Lofi BGM with silence drop + Sub Drop + Pops
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25,asplit=2[v_voice][v_voice_sc];"
        "[2:a]volume='if(between(t,2.0,2.22),0,0.22)':eval=frame[bgm_raw];"
        "[bgm_raw][v_voice_sc]sidechaincompress=threshold=0.06:ratio=5:attack=15:release=200,afade=t=out:st=33.15:d=0.25[bgm_ducked];"
        "[5:a]adelay=2220|2220,volume=0.85[sfx_drop];"
        "[4:a]adelay=2200|2200,volume=0.50[sw1];"
        "[4:a]adelay=8500|8500,volume=0.50[sw2];"
        "[4:a]adelay=15500|15500,volume=0.50[sw3];"
        "[4:a]adelay=21500|21500,volume=0.50[sw4];"
        "[4:a]adelay=27500|27500,volume=0.50[sw5];"
        "[3:a]adelay=2200|2200,volume=0.60[pop1];"
        "[3:a]adelay=10800|10800,volume=0.60[pop2];"
        "[3:a]adelay=21200|21200,volume=0.60[pop3];"
        "[3:a]adelay=28000|28000,volume=0.60[pop4];"
        "[sfx_drop][sw1][sw2][sw3][sw4][sw5][pop1][pop2][pop3][pop4]amix=inputs=10:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
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
# VARIANT 2: 02_DaVinci_Fusion_Editorial.mp4 (DaVinci Resolve Fusion RXQOmQGJK34)
# ==============================================================================
def build_variant_2_davinci(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 2: 02_DaVinci_Fusion_Editorial.mp4 (PRO DIRECTOR CUT)")
    print("="*70)
    
    ass_path = generate_davinci_writeon_ass(words, 0.0, 33.40, "temp/style2_davinci.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    # 4-Frame Rapid Shutter Montage (10.8s - 12.0s):
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
    
    # Stepped zoom punches on live speaker:
    z_expr = (
        "if(between(t,6.0,10.8), 1.14, "
        "if(between(t,12.0,21.2), 1.08, "
        "if(between(t,25.8,33.4), 1.16, 1.0)))"
    )
    
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"crop=w='1080/{z_expr}':h='1920/{z_expr}':x='(1080-out_w)/2':y='(1920-out_h)/2',"
        f"scale=1080:1920,eq=contrast=1.14:saturation=1.08[v_spk];"
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
        "[1:a]volume=0.12,afade=t=out:st=33.15:d=0.25[bgm_drone];"
        "[2:a]volume=0.09,afade=t=out:st=33.15:d=0.25[bgm_fire];"
        "[4:a]adelay=2200|2200,volume=0.75[sfx_hit1];"
        "[4:a]adelay=21200|21200,volume=0.75[sfx_hit2];"
        "[3:a]adelay=10800|10800,volume=0.65[sh1];"
        "[3:a]adelay=10940|10940,volume=0.65[sh2];"
        "[3:a]adelay=11080|11080,volume=0.65[sh3];"
        "[3:a]adelay=11220|11220,volume=0.65[sh4];"
        "[3:a]adelay=11360|11360,volume=0.65[sh5];"
        "[sfx_hit1][sfx_hit2][sh1][sh2][sh3][sh4][sh5]amix=inputs=7:duration=longest:normalize=0[sfx_bus];"
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
# VARIANT 3: 03_Curved_Cinema_Pyramid.mp4 (Grow with Alex OoayDYJKkUs)
# ==============================================================================
def build_variant_3_curved_cinema(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 3: 03_Curved_Cinema_Pyramid.mp4 (PRO DIRECTOR CUT)")
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
        "-i", "assets/broll/stock_hourglass.mp4",
        "-i", "assets/broll/stock_senior_execs.mp4",
        "-i", "assets/broll/stock_luxury.mp4",
    ]
    
    # High-contrast cinema grading with alternating cinema drift & punch
    z_expr = (
        "if(between(t,6.0,10.8), 1.15, "
        "if(between(t,15.2,21.2), 1.08, "
        "if(between(t,25.8,28.0), 1.18, 1.02)))"
    )
    
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"crop=w='1080/{z_expr}':h='1920/{z_expr}':x='(1080-out_w)/2':y='(1920-out_h)/2',"
        f"scale=1080:1920,eq=contrast=1.24:saturation=1.32[v_spk];"
    ]
    
    # Full-screen cinema B-roll cuts
    brolls = [
        (6, 2.20, 6.00),    # Financial crash
        (7, 10.80, 15.20),  # Stock hourglass
        (8, 21.20, 25.80),  # Senior executives
        (9, 28.00, 33.00),  # Luxury yacht celebration
    ]
    last_v = "[v_spk]"
    for idx, (in_idx, t_s, t_e) in enumerate(brolls):
        b_label = f"[broll_cin_{idx}]"
        next_v = f"[v_cin_{idx}]"
        filters.append(
            f"[{in_idx}:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"eq=contrast=1.24:saturation=1.32,setpts=PTS-STARTPTS+({t_s:.2f}/TB){b_label};"
            f"{last_v}{b_label}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Apply Permanent Curved-Edge Black Cinema Border
    filters.append(
        f"{last_v}[1:v]overlay=0:0[v_border];"
        f"[v_border]subtitles='{escaped_ass}'[v_out];"
    )
    
    # Audio Mix: Warm Piano BGM (ducked) + Diegetic Wind (at 10.8s) + Diegetic Ocean Waves (at 28.0s)
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25,asplit=2[v_voice][v_voice_sc];"
        "[2:a]volume=0.20[bgm_raw];"
        "[bgm_raw][v_voice_sc]sidechaincompress=threshold=0.06:ratio=5:attack=15:release=200,afade=t=out:st=33.15:d=0.25[bgm_ducked];"
        "[4:a]adelay=10800|10800,volume=0.55[sfx_wind];"
        "[3:a]adelay=28000|28000,volume=0.60[sfx_ocean];"
        "[5:a]adelay=2200|2200,volume=0.50[whoosh1];"
        "[5:a]adelay=10800|10800,volume=0.50[whoosh2];"
        "[5:a]adelay=21200|21200,volume=0.50[whoosh3];"
        "[sfx_wind][sfx_ocean][whoosh1][whoosh2][whoosh3]amix=inputs=5:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
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
# VARIANT 4: 04_Vox_Pro_Documentary.mp4 (Authentic Vox Studio Data Journalism)
# ==============================================================================
def build_variant_4_vox(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 4: 04_Vox_Pro_Documentary.mp4 (PRO DIRECTOR CUT)")
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
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25,asplit=2[v_voice][v_voice_sc];"
        "[1:a]volume=0.18[bgm_raw];"
        "[bgm_raw][v_voice_sc]sidechaincompress=threshold=0.06:ratio=5:attack=15:release=200,afade=t=out:st=33.15:d=0.25[bgm_ducked];"
        "[2:a]adelay=2400|2400,volume=0.70[tick1];"
        "[2:a]adelay=2700|2700,volume=0.70[tick2];"
        "[2:a]adelay=3000|3000,volume=0.70[tick3];"
        "[3:a]adelay=10800|10800,volume=0.65[rip1];"
        "[4:a]adelay=2200|2200,volume=0.60[hit1];"
        "[tick1][tick2][tick3][rip1][hit1]amix=inputs=5:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
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
# VARIANT 5: 05_MarkSoy_MixedMedia_Wrapper.mp4 (Mark Soy / Vinh Giang MoVlt-ptxIk)
# ==============================================================================
def build_variant_5_marksoy(clean_base: str, out_mp4: str, words: list):
    print("\n" + "="*70)
    print("[*] BUILDING VARIANT 5: 05_MarkSoy_MixedMedia_Wrapper.mp4 (PRO DIRECTOR CUT)")
    print("="*70)
    
    newspaper_collar = create_torn_newspaper_shoulder_overlay("temp/newspaper_shoulders.png")
    takeovers = [
        {"start": 2.20, "end": 6.20},      # 3D Card Zoom Beat
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
        "-i", "temp/style5_card.mp4",       # 7 (3D zoom card 2.20-6.20)
        "-i", "temp/style5_blocks.mp4",     # 8 (Corner blocks transparent overlay 10.50-15.40)
        "-i", "temp/style5_cream1.mp4",     # 9 (Floating cream banner 21.20-26.00)
        "-i", "temp/style5_cream2.mp4",     # 10 (Floating cream banner 28.00-33.40)
    ]
    
    # Live Speaker with dynamic camera scale punches:
    z_expr = (
        "if(between(t,6.2,10.5), 1.16, "
        "if(between(t,10.5,15.4), 1.06, "
        "if(between(t,15.4,21.2), 1.18, "
        "if(between(t,21.2,27.5), 1.08, "
        "if(between(t,27.5,33.4), 1.15, 1.0)))))"
    )
    
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"crop=w='1080/{z_expr}':h='1920/{z_expr}':x='(1080-out_w)/2':y='(1920-out_h)/2',"
        f"scale=1080:1920,eq=contrast=1.12:saturation=1.10[v_spk];"
    ]
    
    # 1. Overlay Beat B (CardZoom 2.20-6.20)
    filters.append(
        "[7:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(2.20/TB)[v_c7];"
        "[v_spk][v_c7]overlay=0:0:enable='between(t,2.20,6.20)':eof_action=pass[v_b];"
    )
    
    # 2. Overlay Beat C (Transparent Corner Blocks AROUND live speaker 10.50-15.40)
    filters.append(
        "[8:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(10.50/TB)[v_c8];"
        "[v_b][v_c8]overlay=0:0:enable='between(t,10.50,15.40)':eof_action=pass[v_c];"
    )
    
    # 3. Overlay Beat D (Torn Newspaper Shoulder Collar wrapping live speaker at 15.40-21.20)
    filters.append(
        "[v_c][1:v]overlay=0:0:enable='between(t,15.40,21.20)':eof_action=pass[v_d];"
    )
    
    # 4. Overlay Beat E (Floating Cream Banner 1 at bottom third 21.20-26.00)
    filters.append(
        "[9:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(21.20/TB)[v_c9];"
        "[v_d][v_c9]overlay=0:0:enable='between(t,21.20,26.00)':eof_action=pass[v_e];"
    )
    
    # 5. Overlay Beat F (Floating Cream Banner 2 at bottom third 28.00-33.40)
    filters.append(
        "[10:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(28.00/TB)[v_c10];"
        "[v_e][v_c10]overlay=0:0:enable='between(t,28.00,33.40)':eof_action=pass[v_f];"
    )
    
    # Subtitles: Minimal 1-word lowercase captions on live speaker
    filters.append(f"[v_f]subtitles='{escaped_ass}'[v_out];")
    
    # Audio Mix: Percussive Stomp Drive + Paper Rips + Sub Drop + Whooshes
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25,asplit=2[v_voice][v_voice_sc];"
        "[2:a]volume=0.20[bgm_raw];"
        "[bgm_raw][v_voice_sc]sidechaincompress=threshold=0.06:ratio=5:attack=15:release=200,afade=t=out:st=33.15:d=0.25[bgm_ducked];"
        "[3:a]adelay=15400|15400,volume=0.65[rip_collar];"
        "[5:a]adelay=2200|2200,volume=0.75[drop_card];"
        "[6:a]adelay=10500|10500,volume=0.55[whoosh_blocks];"
        "[6:a]adelay=21200|21200,volume=0.55[whoosh_cream1];"
        "[6:a]adelay=28000|28000,volume=0.55[whoosh_cream2];"
        "[4:a]adelay=21200|21200,volume=0.60[pop_cream];"
        "[rip_collar][drop_card][whoosh_blocks][whoosh_cream1][whoosh_cream2][pop_cream]amix=inputs=6:duration=longest:normalize=0[sfx_bus];"
        "[v_voice][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
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
    print("[OK] ALL 5 DISTINCT VIRAL STYLES RE-RENDERED WITH PRO DIRECTOR CUTS!")
    print("="*70)

if __name__ == "__main__":
    main()
