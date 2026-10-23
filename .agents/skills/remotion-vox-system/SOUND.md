# Procedural Soundscape & Broadcast Loudness Rules
- **Voiceover Spine:** Must be normalized with `dynaudnorm` and mixed with `amix=normalize=0` so volume never dips.
- **Micro-SFX Choreography:**
  - Every spring card pop-in triggers `pop.wav` (`-12dB`).
  - Every counting number or chart draw triggers a rapid mechanical `tick.wav` every 3 frames.
  - Every stamp slam (`90% FAIL`, `DEVIL IN DETAILS`) triggers `hit.wav` (`-8dB`).
  - Every full-screen takeover transition triggers `whoosh.wav` (`-10dB`).
