---
name: context-aware-editor
description: Evaluates transcript alongside acoustic energy curves and visual background profiles to orchestrate beat-by-beat dynamic styling.
---

# Context-Aware Editor Skill

## Inputs
1. `transcript.json`: Millisecond-accurate word boundaries.
2. `context_profile.json`:
   - `visual_profile`: Tells you whether the scene is dark, moody, or brightly lit.
   - `energy_curve`: Logs speaker RMS intensity and volume spikes.

## Editing Directives (Beat-by-Beat Narrative Alignment)

Divide the clip into distinct emotional beats rather than treating it uniformly:

1. **Intimate / Secret / Conspiracy Beat:**
   - **Trigger:** Low RMS energy (`whisper_or_pause`) + words like "secret", "never told anyone", "truth".
   - **Typography:** Sentence-case, smaller font (64pt), muted pale silver (`&H00D0D0D0`), zero bounce.
   - **Audio/VFX:** Smooth 110% slow push-in, low-pass filter on BGM, high-pass on dialogue.

2. **Shock / Revelation / High-Stakes Beat:**
   - **Trigger:** High RMS spike (`high_intensity`) + contrarian claims or intense delivery.
   - **Typography:** Uppercase, 92pt font, high-contrast electric color (Neon Lime or Crimson), explosive scale bounce (`\t(\fscx120\fscy120)`).
   - **Audio/VFX:** Snap zoom (120%), 808 sub impact, camera shake.

3. **Comedic Deflation / Deadpan Punchline Beat:**
   - **Trigger:** Sarcastic remark, deadpan delivery, or an extended silence pause following a statement.
   - **Typography:** Rotated tilt (`\frz-4`), warm butter yellow, black outline.
   - **Audio/VFX:** Full music drop (0.0 volume) for the silence duration, vinyl stop or record scratch SFX, snap punch-in on speaker's facial reaction.

4. **Background Adaptation:**
   - If `visual_tone == "bright_background"`: Add solid dark outline depth (`Outline=8`) or shadow backing so text doesn't wash out.
   - If `visual_tone == "dark_background"`: Use clean neon or crisp white typography with minimal shadow.
