---
name: viral-reverse-engineer
description: Inspects extracted keyframes, contact sheets, and editing telemetry from viral AI shorts to reverse-engineer prompts, B-roll animations, voiceover cadence, and VFX.
---

# Viral Short Reverse-Engineer Skill

## Execution Protocol
When the user provides a reference Short URL or asks to reverse-engineer a video:
1. Run `python core/reverse_engineer.py "<YOUTUBE_SHORTS_URL>"` via terminal.
2. Load `temp/ref_analysis/deconstruction_report.json` AND visually inspect `temp/ref_analysis/contact_sheet.jpg`.
3. Analyze the 5 Core Pillars from the reference video:
   - **Visual Style & Image Prompts:** Inspect every frame in `contact_sheet.jpg`. Identify the exact art style (e.g., Dark Baroque Oil Painting, 3D Unreal Render, Gritty Cyberpunk, High-Contrast Documentary) and write a matching generation prompt for each scene.
   - **B-Roll Animation Mapping:** Read `detected_animation` from each scene (`ken_burns_zoom_in`, `ken_burns_zoom_out`, `pan_right`, `tilt_or_shake_vfx`) and preserve the exact shot duration cadence (`average_shot_duration_sec`).
   - **VFX & Color Pipeline:** Identify overlays visible on the frames (e.g., Chromatic Aberration RGB split, VHS scanlines, heavy dark vignette, glowing text).
   - **Voiceover Profile:** Match the `words_per_minute` velocity using `edge-tts` voices (`en-US-ChristopherNeural` for deep authority, `en-US-SteffanNeural` for fast explainer, `hi-IN-MadhurNeural` for Hindi).
   - **Audio & SFX Triggers:** Map `whoosh.wav` to scene transitions and `braam.wav` / `pop.wav` to the `sfx_hit_timestamps`.

4. Output `clone_manifest.json` in the workspace root following this schema:
```json
{
  "voiceover": {
    "voice": "en-US-ChristopherNeural",
    "rate": "+12%",
    "pitch": "-4Hz",
    "script": "Your new viral script matching the exact syllable cadence..."
  },
  "vfx_preset": "chromatic_dark_vignette",
  "bgm_track": "dark_synth_drive.mp3",
  "scenes": [
    {
      "scene_id": 1,
      "duration": 2.1,
      "image_prompt": "Hyper-detailed cinematic close-up of...",
      "animation": "ken_burns_zoom_in",
      "transition": "flash_cut",
      "sfx": "braam"
    }
  ]
}
```
