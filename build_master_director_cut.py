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
from core.frame_inspector import generate_qa_inspection_sheet

def escape_path_for_ffmpeg(p: str) -> str:
    return p.replace("\\", "/").replace(":", "\\:")

def generate_master_kinetic_ass(
    words: list,
    start_t: float = 0.0,
    end_t: float = 33.40,
    out_ass: str = "temp/master_kinetic_subs.ass"
) -> str:
    """
    Generates CapCut Pro Kinetic Subtitles with 80% central safe-zone,
    1-4 words per group, 6-frame scale pop overshoot, and single electric-yellow / green
    signal keyword highlighting.
    Suppresses subtitles during full-screen chart takeovers (2.2s-6.2s, 13.5s-15.4s, 21.2s-26.0s).
    """
    os.makedirs(os.path.dirname(out_ass) or ".", exist_ok=True)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MasterPop,Montserrat ExtraBold,84,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,1,0,1,6,4,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Suppress lower-third speech subtitles whenever a full-screen chart,
    # corner block kinetic overlay, or floating cream sticker card is active.
    suppress_windows = [
        (2.20, 6.20),   # Vox Bar Chart & 90% Odometer
        (6.20, 10.50),  # Sliding Corner Blocks + Center kinetic text
        (13.50, 15.40), # Vox Market Timing Bell Curve
        (15.40, 21.20), # Advisor Network Cream Card + Torn Newspaper
        (21.20, 26.00), # Vox Blueprint Architectural Takeover
        (26.00, 30.60), # Luxury Yacht + Outside Rosy Cream Card
    ]

    clip_words = [w for w in words if start_t <= w["start"] <= end_t - 0.15]
    lines = []
    
    i = 0
    while i < len(clip_words):
        chunk = clip_words[i:i + 2]
        w_start = chunk[0]["start"] - start_t
        w_end = chunk[-1]["end"] - start_t
        
        # Check if overlaps with chart takeovers
        suppressed = False
        for s_w, e_w in suppress_windows:
            if s_w <= w_start < e_w or s_w < w_end <= e_w:
                suppressed = True
                break
        
        if not suppressed and w_end > w_start + 0.10:
            s_fmt = f"{int(w_start//3600):01d}:{int((w_start%3600)//60):02d}:{w_start%60:05.2f}"
            e_fmt = f"{int(w_end//3600):01d}:{int((w_end%3600)//60):02d}:{w_end%60:05.2f}"
            
            # Format text with power keyword highlight on last word
            if len(chunk) == 1:
                txt = f"{{\\c&H0034D399&\\b1}}{chunk[0]['word'].upper()}"
            else:
                txt = f"{{\\c&H00F4F4F5&}}{chunk[0]['word'].upper()} {{\\c&H0034D399&\\b1}}{chunk[1]['word'].upper()}"
            
            # CapCut 6-frame scale overshoot: 115% -> 100%
            anim = r"{\an5\pos(540,1480)\t(0,60,\fscx115\fscy115)\t(60,120,\fscx100\fscy100)}"
            lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},MasterPop,,0,0,0,,{anim}{txt}")
            
        i += len(chunk)

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"[OK] Generated Master Kinetic Subtitles: {out_ass}")
    return out_ass

def build_master_100m_director_cut():
    print("="*75)
    print("[*] BUILDING UNIFIED MASTER 100M+ VIRAL DIRECTOR CUT")
    print("="*75)
    
    clean_base = "temp/clean_base_30fps.mp4"
    transcript_path = "temp/clips_test/clip_03_transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
    words = transcript_data.get("words", [])

    ass_path = generate_master_kinetic_ass(words, 0.0, 33.40, "temp/master_kinetic_subs.ass")
    escaped_ass = escape_path_for_ffmpeg(ass_path)
    
    out_mp4 = "outputs/master_100m_director_cut.mp4"
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    
    top_mask = create_top_luma_mask_png("temp/top_luma_mask.png")
    newspaper_collar = create_torn_newspaper_shoulder_overlay("temp/newspaper_shoulders.png")
    
    # Inputs list:
    # 0: clean_base (33.4s)
    # 1: top_luma_mask
    # 2: newspaper_collar
    # 3: BGM 1: chill_lofi.mp3 (0.0-15.4s)
    # 4: BGM 2: warm_ambient_piano.mp3 (15.4-33.4s)
    # 5: SFX: sub_drop.wav
    # 6: SFX: tick.wav
    # 7: SFX: tape_rewind.wav
    # 8: SFX: hit.wav
    # 9: SFX: whoosh.wav
    # 10: SFX: vinyl_stop.wav
    # 11: SFX: ui_ping.wav
    # 12: SFX: paper_rip.wav
    # 13: SFX: shutter.wav
    # 14: Remotion: style1_pill1.mp4
    # 15: Remotion: style4_bar.mp4 (Vox Bar Chart)
    # 16: Remotion: style5_blocks.mp4 (Corner Blocks)
    # 17: Video: stock_hourglass.mp4
    # 18: Video: stock_senior_execs.mp4
    # 19: Remotion: style4_curve.mp4 (Vox Bell Curve)
    # 20: Remotion: style5_cream1.mp4 (Advisor Banner)
    # 21: Remotion: style4_blue.mp4 (Vox Blueprint)
    # 22: Video: stock_luxury.mp4
    # 23: Remotion: style5_cream2.mp4 (Rosy Banner)
    # 24..27: Shutter montage images
    inputs = [
        "-i", clean_base,
        "-i", top_mask,
        "-i", newspaper_collar,
        "-stream_loop", "-1", "-i", "assets/music/chill_lofi.mp3",
        "-stream_loop", "-1", "-i", "assets/music/warm_ambient_piano.mp3",
        "-i", "assets/sfx/sub_drop.wav",
        "-i", "assets/sfx/tick.wav",
        "-i", "assets/sfx/tape_rewind.wav",
        "-i", "assets/sfx/hit.wav",
        "-i", "assets/sfx/whoosh.wav",
        "-i", "assets/sfx/vinyl_stop.wav",
        "-i", "assets/sfx/ui_ping.wav",
        "-i", "assets/sfx/paper_rip.wav",
        "-i", "assets/sfx/shutter.wav",
        "-i", "temp/style1_pill1.mp4",
        "-i", "temp/style4_bar.mp4",
        "-i", "temp/style5_blocks.mp4",
        "-i", "assets/broll/stock_hourglass.mp4",
        "-i", "assets/broll/stock_senior_execs.mp4",
        "-i", "temp/style4_curve.mp4",
        "-i", "temp/style5_cream1.mp4",
        "-i", "temp/style4_blue.mp4",
        "-i", "assets/broll/stock_luxury.mp4",
        "-i", "temp/style5_cream2.mp4",
        "-i", "remotion_studio/public/assets/broll_beat4_devil.mp4",
        "-i", "assets/broll/stock_stressed_analyst.mp4",
        "-i", "remotion_studio/public/assets/broll_beat3_mentors.mp4",
        "-i", "remotion_studio/public/assets/broll_beat2_late.mp4",
    ]
    
    # Dynamic Camera Scale Punches (AE / AP 2.4s Cognitive Reset):
    # 0.0-2.2: 1.22 -> 1.0 (Hook pull-back)
    # 6.2-10.5: 1.0 -> 1.15 (Beat 2 push-in)
    # 15.4-21.2: 1.18 (Beat 4 authority)
    # 26.0-30.6: 1.05
    # 30.6-33.4: 1.20 (Climax tight punch)
    z_expr = (
        "if(between(t,0,2.2), 1.22 - (t/2.2)*0.22, "
        "if(between(t,6.2,10.5), 1.0 + ((t-6.2)/4.3)*0.15, "
        "if(between(t,15.4,21.2), 1.18, "
        "if(between(t,26.0,30.6), 1.05, "
        "if(between(t,30.6,33.4), 1.20, 1.0)))))"
    )
    
    filters = [
        f"[0:v]fps=30,setpts=PTS-STARTPTS,"
        f"crop=w='1080/{z_expr}':h='1920/{z_expr}':x='(1080-out_w)/2':y='(1920-out_h)/2',"
        f"scale=1080:1920,eq=contrast=1.18:saturation=1.20[v_spk];"
    ]
    
    last_v = "[v_spk]"
    
    # 1. Overlay Beat 0 Glass Pill (0.0s - 2.2s)
    filters.append(
        f"[14:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(0.0/TB)[pill0];"
        f"{last_v}[pill0]overlay=0:0:enable='between(t,0.0,2.20)':eof_action=pass[v_pill0];"
    )
    last_v = "[v_pill0]"
    
    # 2. Overlay Beat 1: Vox Bar Chart + Odometer (2.20s - 6.20s)
    filters.append(
        f"[15:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(2.20/TB)[vox_bar];"
        f"{last_v}[vox_bar]overlay=0:0:enable='between(t,2.20,6.20)':eof_action=pass[v_bar];"
    )
    last_v = "[v_bar]"
    
    # 3. Overlay Beat 2: Alight Motion Sliding Corner Blocks (6.20s - 10.50s)
    filters.append(
        f"[16:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(6.20/TB)[blocks];"
        f"{last_v}[blocks]overlay=0:0:enable='between(t,6.20,10.50)':eof_action=pass[v_blocks];"
    )
    last_v = "[v_blocks]"
    
    # 4. Beat 3: 3-Panel Whip-Pan (10.50s - 15.40s)
    # Panel A: Hourglass (10.50 - 12.00)
    # Panel B: Megacity Executives (12.00 - 13.50)
    # Panel C: Vox Bell Curve (13.50 - 15.40)
    filters.append(
        f"[17:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.16:saturation=1.18,setpts=PTS-STARTPTS+(10.50/TB)[b3_pA];"
        f"{last_v}[b3_pA]overlay=0:0:enable='between(t,10.50,12.00)':eof_action=pass[v_b3_a];"
        f"[18:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.16:saturation=1.18,setpts=PTS-STARTPTS+(12.00/TB)[b3_pB];"
        f"[v_b3_a][b3_pB]overlay=0:0:enable='between(t,12.00,13.50)':eof_action=pass[v_b3_b];"
        f"[19:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(13.50/TB)[b3_pC];"
        f"[v_b3_b][b3_pC]overlay=0:0:enable='between(t,13.50,15.40)':eof_action=pass[v_b3];"
    )
    last_v = "[v_b3]"
    
    # 5. Beat 4: Torn Newspaper Collar + Floating Cream Banner (15.40s - 21.20s)
    filters.append(
        f"{last_v}[2:v]overlay=0:0:enable='between(t,15.40,21.20)'[v_paper_spk];"
        f"[20:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(15.40/TB)[cream1];"
        f"[v_paper_spk][cream1]overlay=0:0:enable='between(t,15.40,21.20)':eof_action=pass[v_b4];"
    )
    last_v = "[v_b4]"
    
    # 6. Beat 5: Vox Architectural Blueprint Takeover (21.20s - 26.00s)
    filters.append(
        f"[21:v]fps=30,scale=1080:1920,setpts=PTS-STARTPTS+(21.20/TB)[vox_blue];"
        f"{last_v}[vox_blue]overlay=0:0:enable='between(t,21.20,26.00)':eof_action=pass[v_b5];"
    )
    last_v = "[v_b5]"
    
    # 7. Beat 6: Golden Luxury Yacht (26.00s - 30.60s) + Floating Cream Banner
    filters.append(
        f"[22:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.18:saturation=1.24,setpts=PTS-STARTPTS+(26.00/TB)[luxury];"
        f"{last_v}[luxury]overlay=0:0:enable='between(t,26.00,30.60)':eof_action=pass[v_lux];"
        f"[23:v]fps=30,scale=1080:1920,colorkey=0x000000:0.12:0.06,setpts=PTS-STARTPTS+(26.00/TB)[cream2];"
        f"[v_lux][cream2]overlay=0:0:enable='between(t,26.00,30.60)':eof_action=pass[v_b6_pre];"
    )
    last_v = "[v_b6_pre]"
    
    # 8. Beat 6 Climax: Rapid 4-Frame Shutter Montage (30.60s - 33.40s)
    montage = [
        (24, 30.60, 31.00), # Financial charts
        (25, 31.00, 31.40), # Stressed founder
        (26, 31.40, 31.80), # Boardroom mentors
        (27, 31.80, 33.40), # Late night execution
    ]
    for idx, (in_idx, t_s, t_e) in enumerate(montage):
        m_lbl = f"[m_{idx}]"
        next_v = f"[v_m_{idx}]"
        filters.append(
            f"[{in_idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.28:saturation=0.4,fps=30,setpts=PTS-STARTPTS+({t_s:.2f}/TB){m_lbl};"
            f"{last_v}{m_lbl}overlay=0:0:enable='between(t,{t_s:.2f},{t_e:.2f})':eof_action=pass{next_v};"
        )
        last_v = next_v
        
    # Subtitles layer
    filters.append(f"{last_v}subtitles='{escaped_ass}'[v_out];")
    
    # Audio Engineering:
    # Stem 1: Voice with dynaudnorm + split for sidechain ducking
    # Stem 2: BGM 1 (chill lofi 0.0-15.4s) + BGM 2 (warm piano 15.4-33.4s)
    # Stem 3: SFX Bus (sub-drop at 0.0s, tick at 2.4s, rewind at 6.8s, hit at 7.8s, whoosh at 10.5/12.0/13.5, vinyl stop at 15.4s, ui ping at 21.4s, paper rip at 30.6s, shutter clicks at 30.6/31.0/31.4/31.8s)
    filters.append(
        "[0:a]highpass=f=80,dynaudnorm=f=150:g=15:p=0.92,acompressor=threshold=-14dB:ratio=3:attack=8:release=80:makeup=5dB,afade=t=out:st=33.15:d=0.25,asplit=2[v_voice][v_voice_sc];"
        
        # BGM 1 (0.0s - 15.4s)
        "[3:a]atrim=0:15.40,afade=t=out:st=15.20:d=0.20,volume=0.18[bgm1];"
        # BGM 2 (15.4s - 33.4s)
        "[4:a]atrim=0:18.00,afade=t=in:st=0:d=0.30,afade=t=out:st=17.75:d=0.25,volume=0.20[bgm2];"
        "[bgm1][bgm2]concat=n=2:v=0:a=1[bgm_raw];"
        "[bgm_raw][v_voice_sc]sidechaincompress=threshold=0.06:ratio=5:attack=15:release=220[bgm_ducked];"
        
        # SFX Delays
        "[5:a]adelay=0|0,volume=0.85[sfx_sub];"
        "[6:a]adelay=2400|2400,volume=0.60[sfx_tick1];"
        "[6:a]adelay=3200|3200,volume=0.60[sfx_tick2];"
        "[6:a]adelay=4000|4000,volume=0.60[sfx_tick3];"
        "[7:a]adelay=6800|6800,volume=0.65[sfx_rewind];"
        "[8:a]adelay=7800|7800,volume=0.70[sfx_thud];"
        "[9:a]adelay=10500|10500,volume=0.55[sfx_w1];"
        "[9:a]adelay=12000|12000,volume=0.55[sfx_w2];"
        "[9:a]adelay=13500|13500,volume=0.55[sfx_w3];"
        "[10:a]adelay=15400|15400,volume=0.80[sfx_tape_stop];"
        "[11:a]adelay=21400|21400,volume=0.65[sfx_ping];"
        "[12:a]adelay=30600|30600,volume=0.85[sfx_rip];"
        "[13:a]adelay=30600|30600,volume=0.70[sh1];"
        "[13:a]adelay=31000|31000,volume=0.70[sh2];"
        "[13:a]adelay=31400|31400,volume=0.70[sh3];"
        "[13:a]adelay=31800|31800,volume=0.70[sh4];"
        
        "[sfx_sub][sfx_tick1][sfx_tick2][sfx_tick3][sfx_rewind][sfx_thud][sfx_w1][sfx_w2][sfx_w3][sfx_tape_stop][sfx_ping][sfx_rip][sh1][sh2][sh3][sh4]amix=inputs=16:duration=longest:normalize=0[sfx_bus];"
        
        # Master Mix: Voice + Ducked BGM + SFX Bus
        "[v_voice][bgm_ducked][sfx_bus]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:attack=5:release=50[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filters),
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", "33.40",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    
    print("\n[+] Launching FFmpeg render for Master 100M+ Director Cut...")
    subprocess.run(cmd, check=True)
    print(f"\n[OK] Generated: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")
    
    # Stage 4: Visual QA Frame Inspection Sheet
    print("\n[*] GENERATING QA INSPECTION SHEET & BEAT FRAMES...")
    timestamps = [0.5, 2.5, 4.5, 8.0, 11.5, 14.0, 18.0, 22.5, 24.5, 29.0, 31.5]
    sheet_path, frames = generate_qa_inspection_sheet(out_mp4, timestamps, "temp/qa_frames")
    print(f"[OK] QA Contact Sheet Ready: {sheet_path}")
    return out_mp4

if __name__ == "__main__":
    build_master_100m_director_cut()
