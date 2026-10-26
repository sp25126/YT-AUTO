---
name: pro-depth-editor
description: Combines Jad M.H's Editor-V1 (rotoscoped word-behind-head & 3-layer depth cutouts) with Eddie's Clipper Skill (face-anchored zooms, camera-cut tracking, and visual candidate inspection).
---

# Pro Depth Editor Skill (Editor-V1 + Clipper Unified)

Whenever the user asks to clip or edit a video with `pro-depth-editor`:
1. **Run Scene Understanding First (`core/scene_understanding.py`):**
   - Run `analyze_speaker_cuts_and_faces()` to log camera cuts and `[face_cx_pct, face_cy_pct]` coordinates.
   - Run `extract_speaker_roto_frames()` on the opening 2.2s hook (`0.0s -> 2.2s`) so the speaker is rotoscoped into transparent PNG frames (`remotion_studio/public/assets/roto_hook/frame_XXXX.png`) and giant 3D text (`TIMING`) can rise behind their head.
2. **Visual B-Roll Candidate Inspection & Foreground Cutout Generation:**
   - For every B-roll scene, call `fetch_and_inspect_broll_candidates()` to download 3 Pexels/Pixabay candidate videos, extract their midpoint frames, and automatically generate a **transparent foreground cutout (`_fg_cutout.png`)** of the subject inside that B-roll video using `rembg`.
   - **Visually view `*_INSPECTION_GRID.jpg` using your image-reading tool** to verify which candidate video actually depicts the spoken metaphor cleanly (rejecting any bad crops, padlocks, or decapitated frames).
3. **Render the 3-Layer Depth Sandwich (`remotion_studio/src/ProDepthEditor.tsx`):**
   - Every B-roll takeover MUST have 3 depth layers:
     - Layer 0 (Back): Moving B-roll video.
     - Layer 1 (Midground): Animated 2D SVG vector graphics (radars, curves, node triangles) + Giant Typography (`TOO EARLY`, `CRUSHED`, `VETERANS`, `ALL ROSY`, `DETAILS`).
     - Layer 2 (Foreground): The `_fg_cutout.png` subject layered **in front of** the giant text and 2D vectors for real parallax depth.
4. **Sidechain Audio Mix & QA Inspection:**
   - Mix with `core/viral_bgm_engine.py` (`sidechaincompress` + `clamp_end_sec=32.85`) and inspect `temp/qa_frames/QA_CONTACT_SHEET.jpg` before finishing.
