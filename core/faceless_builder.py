"""
core/faceless_builder.py - Master Production Engine for High-Velocity Shorts (V5 Polish)
Integrates:
1. TWO-PASS ZERO-LAG CFR MASTER COMPOSITOR:
   - Pass 1: Pre-slices 33.40s podcast slice into 30fps CFR MP4 first to guarantee zero frame drops.
   - Pass 2: Composites multi-cut moving stock videos, VFX, and multi-stem audio.
2. SEMANTIC METAPHOR STOCK VIDEOS & SUB-PIXEL VFX B-ROLL:
   - Window 1 (2.4s-6.0s): Live 30fps Counter Card (0% -> 90% FAIL RATE).
   - Window 2 (10.8s-15.4s): 2-Cut Sequence (Barren Desert Hourglass -> Cyberpunk Megacity Rush).
   - Window 3 (21.5s-26.0s): 2-Cut Sequence (Boardroom Meeting -> Real Moving Senior Executives Stock Video).
   - Window 4 (28.4s-33.4s): 2-Cut Sequence (Real Moving Luxury Yacht Celebration -> Real Moving Stressed Founder Analyzing Data).
3. HARD-COORDINATE \\pos(x,y) DUAL-ZONE SUBTITLES:
   - Split-screen: {\\an5\\pos(540,960)} locked to split seam.
   - Full-screen: {\\an5\\pos(540,1580)} locked to lower-third below chin, off speaker's face.
4. EXACT WORD BOUNDARY CLAMPING:
   - Clamped at 33.40s right after "...detail", before "and".
   - 0.25s clean audio fade-out starting at 33.15s.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath("."))
from core.broll_vfx_engine import render_live_counter_card
from core.vfx_broll_builder import render_vfx_broll_subclip, build_multicut_broll_sequence
from core.pos_subtitles import generate_pos_locked_ass
from core.two_pass_composer import render_two_pass_master

def build_cloned_short(
    source_video: str = "inputs/startup_raj_shamani.mp4",
    start_t: float = 2043.0,
    end_t: float = 2076.40,  # Clamped exactly to 33.40s (cuts off after "detail" before "and")
    output_mp4: str = "outputs/cloned_ai_short.mp4"
) -> str:
    """Builds the 2-pass zero-lag high-velocity short with moving stock video and locked subtitles."""
    os.makedirs("temp/pro_build", exist_ok=True)
    os.makedirs(os.path.dirname(output_mp4) or ".", exist_ok=True)
    duration = end_t - start_t

    # 1. Load transcript words
    transcript_file = "temp/clips_test/clip_03_transcript.json"
    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as f:
            tdata = json.load(f)
        raw_words = tdata.get("words", [])
    else:
        from core.audio_transcribe import extract_and_transcribe
        raw_words = extract_and_transcribe(source_video, "temp/transcript.json")

    print(f"[*] Pipeline locked to word boundary: {start_t:.2f}s to {end_t:.2f}s ({duration:.2f}s)")

    # 2. Window 1 B-Roll (2.4s - 6.0s, 3.6s): Live Animated Counter Card
    w1_file = render_live_counter_card(
        badge="CRITICAL STAT",
        target_num=90,
        suffix="%",
        headline="FAIL RATE",
        subtext="Startups die from wrong timing, not bad ideas",
        theme="danger",
        duration=3.60,
        fps=30,
        out_mp4="temp/pro_build/w1_counter.mp4"
    )

    # 3. Window 2 B-Roll (10.8s - 15.4s, 4.6s): 2-Cut Sequence with Sub-Pixel Motion & RGB Split
    # Sub-clip 2A (2.3s): Barren Desert Hourglass
    c2a = render_vfx_broll_subclip(
        source_path="assets/broll/hourglass_timing.jpg",
        hud_text="TOO EARLY = ZERO MARKET",
        accent_rgb=(255, 68, 68),
        duration=2.30,
        fps=30,
        out_mp4="temp/pro_build/w2_subclip_a.mp4"
    )
    # Sub-clip 2B (2.3s): Cyberpunk Megacity Rush
    c2b = render_vfx_broll_subclip(
        source_path="assets/broll/cyberpunk_megacity.jpg",
        hud_text="TOO LATE = CRUSHED BY GIANTS",
        accent_rgb=(46, 247, 115),
        duration=2.30,
        fps=30,
        out_mp4="temp/pro_build/w2_subclip_b.mp4"
    )
    w2_file = build_multicut_broll_sequence([c2a, c2b], "temp/pro_build/w2_timing_sequence.mp4")

    # 4. Window 3 B-Roll (21.5s - 26.0s, 4.5s): 2-Cut Sequence with REAL MOVING STOCK VIDEO
    # Sub-clip 3A (2.25s): Executive Boardroom
    c3a = render_vfx_broll_subclip(
        source_path="assets/broll/boardroom_veterans.jpg",
        hud_text="STEP 1: ADVISOR NETWORK",
        accent_rgb=(46, 247, 115),
        duration=2.25,
        fps=30,
        out_mp4="temp/pro_build/w3_subclip_a.mp4"
    )
    # Sub-clip 3B (2.25s): Senior Executives Planning & Mentoring (REAL HD MOVING VIDEO!)
    exec_source = "assets/broll/stock_senior_execs.mp4"
    c3b = render_vfx_broll_subclip(
        source_path=exec_source,
        hud_text="TALK TO 20-YR VETERANS",
        accent_rgb=(46, 247, 115),
        duration=2.25,
        fps=30,
        out_mp4="temp/pro_build/w3_subclip_b.mp4"
    )
    w3_file = build_multicut_broll_sequence([c3a, c3b], "temp/pro_build/w3_advisors_sequence.mp4")

    # 5. Window 4 B-Roll (28.4s - 33.4s, 5.0s): 2-Cut Sequence with REAL MOVING STOCK VIDEOS
    # Sub-clip 4A (2.4s): Luxury Yacht Celebration (REAL HD MOVING VIDEO!)
    luxury_source = "assets/broll/stock_luxury.mp4"
    c4a = render_vfx_broll_subclip(
        source_path=luxury_source,
        hud_text="OUTSIDE: LOOKS ALL ROSY",
        accent_rgb=(255, 185, 40),
        duration=2.40,
        fps=30,
        out_mp4="temp/pro_build/w4_subclip_a.mp4"
    )
    # Sub-clip 4B (2.6s): Stressed Entrepreneur Analyzing Late Night (REAL HD MOVING VIDEO!)
    stressed_source = "assets/broll/stock_stressed_analyst.mp4"
    c4b = render_vfx_broll_subclip(
        source_path=stressed_source,
        hud_text="INSIDE: DEVIL IN THE DETAILS",
        accent_rgb=(255, 68, 68),
        duration=2.60,
        fps=30,
        out_mp4="temp/pro_build/w4_subclip_b.mp4"
    )
    w4_file = build_multicut_broll_sequence([c4a, c4b], "temp/pro_build/w4_details_sequence.mp4")

    # 6. Schedule B-roll Windows
    broll_windows = [
        {"file": w1_file, "start": 2.40, "end": 6.00},
        {"file": w2_file, "start": 10.80, "end": 15.40},
        {"file": w3_file, "start": 21.50, "end": 26.00},
        {"file": w4_file, "start": 28.40, "end": 33.40}
    ]

    # 7. Generate Hard-Coordinate \pos(x,y) Subtitles
    split_windows = [{"start": b["start"], "end": b["end"]} for b in broll_windows]
    ass_path = generate_pos_locked_ass(
        words=raw_words,
        start_t=start_t,
        end_t=end_t,
        split_windows=split_windows,
        output_ass="temp/pro_build/pos_locked_subs.ass"
    )

    # 8. Render Master Two-Pass Zero-Lag 30fps CFR Video
    return render_two_pass_master(
        raw_podcast=source_video,
        start_t=start_t,
        end_t=end_t,
        broll_windows=broll_windows,
        ass_path=ass_path,
        output_mp4=output_mp4
    )

if __name__ == "__main__":
    build_cloned_short()
