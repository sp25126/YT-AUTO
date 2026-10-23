---
name: elite-sound-designer
description: Orchestrates sonic pacing, sidechain compression, emphasis sound effects, and emotional background music.
---

# Elite Sound Design Directives

## Sound Layer Hierarchy
1. **Dialogue (Stem 1):** Main foreground signal. Normalized to -14 LUFS, high-pass filtered at 80Hz.
2. **SFX Markers (Stem 2):**
   - **Riser (0.8s):** Starts at second 2.2 leading into the punchline at second 3.0.
   - **Bass Hit / Braam:** Triggers on key contrarian claims.
   - **Pop / Tap:** Triggers on rapid list items and keyword reveals.
   - **Swoosh:** Triggers on camera push-ins and B-roll transitions.
3. **Background Music (Stem 3):**
   - **Dynamic Sidechain Ducking:** Volume sits at -22dB during speech, immediately rising by +6dB when the speaker pauses for emphasis.

## Output FFmpeg Audio Filter Graph Formula:
`[bgm]volume=0.14[bgm_base];[dialogue][bgm_base]sidechaincompress=threshold=0.08:ratio=6:attack=15:release=250[ducked_mix]`
