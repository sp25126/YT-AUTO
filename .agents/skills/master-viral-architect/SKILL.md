---
name: master-viral-architect
description: The ultimate end-to-end orchestration skill for viral short-form content. Combines clipper, scene-understanding, 3D WebGL motion graphics, sidechain audio mixing, and automated YouTube/IG uploading.
---

# Master Viral Architect: Autonomous 10M+ View Engine

When invoked to produce daily shorts, execute this strict sequential pipeline:

**1. Sourcing & Clipping (`.claude/skills/clipper`)**
- Ingest the target long-form podcast URL.
- Extract the highest-retention 30-to-40 second segments using transcript hook analysis.
- Output raw `30s_clip.mp4` and `transcript.json`.

**2. Scene Understanding & Asset Gate (`core/scene_understanding.py`)**
- Run `analyze_speaker_cuts_and_faces()` to lock facial coordinates for eye-anchored zooms.
- Extract `rembg` transparent speaker frames for the opening 3D hook.
- Fetch Pexels/Pixabay B-roll candidate grids, inspect them visually, and generate `_fg_cutout.png` depth layers for the selected clips.

**3. Visual Rendering (`remotion_studio/src/ThreeDMotionDirector.tsx`)**
- Render the 5-layer 3.5D depth sandwich:
  - Layer 0: Three.js 3D WebGL Backdrops (Wireframes, Monoliths).
  - Layer 1: 3D-Tilted Glass Cinema Cards holding Color-Burst B-Roll.
  - Layer 2: 2.5D Parallax Foreground Cutouts.
  - Layer 3: EffectCraft scanlines & glowing particle orbs.
  - Layer 4: Clause-aware (`core/clause_subtitles.py`) borderless typography at chest level.

**4. Audio Sidechain & Foley (`core/surgical_audio_polish.py` + `bgm-score-director`)**
- Generate Earshot UI/Motion SFX (`whoosh_fast`, `sub_hit`, `ui_pop`).
- Fetch 116 BPM Dark Synthwave / Cinematic BGM, carve a vocal EQ pocket, and apply `sidechaincompress` ducking against the normalized `-14 LUFS` vocal track.

**5. QA & Future Upload Hand-off**
- Run `core/frame_inspector.py` to extract and verify contact sheet frames.
- [PENDING INTEGRATION]: Hand off the validated MP4 to the browser-automation agent for scheduled multi-platform publishing via the user's authenticated profiles.
