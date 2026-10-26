---
name: bgm-score-director
description: Analyzes the entire video's vocal energy curve, transcript emotion, and pacing to select, beat-align, EQ-pocket, and sidechain-duck the optimal royalty-free BGM track.
---

# Whole-Video BGM Score Director Skill

Whenever editing a short, ALWAYS execute this 4-step BGM workflow (combining `core/video_bgm_analyzer.py` and `.claude/skills/earshot/SKILL.md`):
1. **Whole-Video Telemetry (`analyze_video_for_bgm`):**
   - Run `analyze_video_for_bgm(video_path, "transcript.json")` to measure the speaker's vocal RMS curve, pause windows, and emotional keyword balance (`tension_score` vs `authority_score`).
2. **Multi-Candidate BGM Audition (`fetch_and_score_best_bgm_candidate`):**
   - Download at least 3 royalty-free BGM candidates from Openverse CC0 / Internet Archive / Freesound.
   - Audit every candidate with `librosa` (BPM `90–135`, Spectral Centroid `<2500Hz` so it doesn't clash with human speech).
3. **Vocal-Pocket EQ & Beat-Drop Alignment:**
   - Apply a `-6dB` parametric EQ dip at `2200Hz` (`equalizer=f=2200:width_type=o:width=2.0:g=-6`) on the BGM so the speaker's voice sits inside a crystal-clear frequency pocket.
4. **Broadcast Sidechain Ducking & `earshot` Verification:**
   - Route the BGM through `sidechaincompress` keyed by `[voice_sc]` (`mix_master_audio_with_sidechain`), then run `python -m earshot measure <output.mp4>` to verify `-14 LUFS` integrated loudness and zero clipping.
