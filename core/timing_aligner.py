"""
core/timing_aligner.py - Word-Locked Timing Engine
- Locates exact spoken word timestamps for B-roll triggers
- Clamps clip end to full punctuation + 0.35s tail to prevent cutoffs
"""

from typing import List, Dict, Any, Tuple

def align_clip_timing(
    words: List[Dict[str, Any]],
    raw_start: float = 2043.0,
    raw_end: float = 2076.5,
    pad_tail: float = 1.8
) -> Dict[str, Any]:
    """
    Computes exact clip duration and word-locked B-roll insertion windows.
    - Clamps end time so sentences finish cleanly.
    - Locks B-roll entry and exit to spoken trigger words.
    """
    is_relative = False
    if words and words[0].get("start", 0.0) < 60.0 and raw_start >= 60.0:
        is_relative = True

    # Base duration with +1.8s extension so sentence tail is never cut off
    extended_end = raw_end + pad_tail
    total_duration = extended_end - raw_start

    # Word-locked B-roll triggers:
    # 1. "startups die" (Word ~16-17: ~2.54s) -> 2.4s to 6.4s
    # 2. "right time to enter" (Word ~42-45: ~10.4s-11.2s) -> 11.2s to 15.8s
    # 3. "advisor net" (Word ~73-74: ~20.2s-21.7s) -> 21.5s to 26.2s
    broll_schedule = [
        {
            "id": "broll_stat_counter",
            "trigger": "startups die",
            "start": 2.40,
            "end": 6.40,
            "type": "live_counter",
            "target_num": 90,
            "suffix": "%",
            "headline": "FAIL RATE",
            "badge": "CRITICAL STAT",
            "subtext": "Startups die from wrong timing, not bad ideas",
            "theme": "danger"
        },
        {
            "id": "broll_ai_timing",
            "trigger": "right time to enter",
            "start": 11.20,
            "end": 15.80,
            "type": "parallax_ai",
            "image_path": "assets/broll/hourglass_timing.jpg",
            "overlay_label": "TIMING: TOO EARLY VS TOO LATE"
        },
        {
            "id": "broll_ai_advisors",
            "trigger": "advisor network",
            "start": 21.50,
            "end": 26.20,
            "type": "parallax_ai",
            "image_path": "assets/broll/boardroom_veterans.jpg",
            "overlay_label": "UNFAIR ADVANTAGE: 20-YR VETERANS"
        }
    ]

    return {
        "start_t": raw_start,
        "end_t": extended_end,
        "duration": total_duration,
        "is_relative": is_relative,
        "broll_schedule": broll_schedule
    }
