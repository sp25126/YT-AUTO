---
name: viral-sound-vfx-director
description: Plans high-retention audio-visual assets, sound effect layers, music timing drops, and visual effects per archetype.
---

# Viral Sound & VFX Directives

## Sound Design Archetypes (Zero Clutter Rule)
1. **The Comedic Beat:**
   - **VFX:** Snap punch-in (125% zoom) on awkward pauses or punchlines.
   - **Audio Drop:** Cut background music entirely for 0.7–1.2s. Insert `record_scratch.wav` or `crickets.wav`.
   - **Subtitles:** Angled rotation (`\frz-3`), warm yellow primary, bold black outline, spring bounce on adjectives.

2. **The High-Stakes / Business Hook:**
   - **VFX:** Flash transition on opening sentence, subtle directional camera shake (`0.1s`), film unsharp mask.
   - **Audio Drop:** Muffled low-pass filter on BGM leading into the contrarian claim, resolved with an 808 `braam_hit.wav`.
   - **Subtitles:** High-contrast lime green keywords, condensed heavy sans font (`Montserrat Black`), center-aligned.

3. **The Deep Narrative / Mystery:**
   - **VFX:** 35mm grain overlay, 60% desaturated shadows, slow push-in zoom (+5% across clip duration).
   - **Audio:** Continuous low-frequency cello or binaural drone, zero cartoon sound effects, natural room reverberation.
   - **Subtitles:** Elegant serif (`Cinzel`), sentence-case capitalization, wide tracking, subtle cross-fades.

## Tool Integration:
- Query `freesound-audio` via MCP to fetch missing SFX directly into `assets/sfx/`.
- Validate keyword contrast using `youtube-intelligence`.
