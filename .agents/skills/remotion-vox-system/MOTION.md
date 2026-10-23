# Remotion Physics & Animation Rules
- **Never use linear interpolation for UI entry.** Always use `spring({ frame, fps, config: { damping: 14, stiffness: 160, mass: 0.8 } })`.
- **Staggered Choreography:**
  - Frame 0–8: Background grid & section header badge slide in.
  - Frame 6–18: Main Pixabay video/image cutout pops in with spring scale (`0.7 -> 1.0`) and tilt (`-6deg -> -2deg`).
  - Frame 12–45: Data bars, line charts, or counters animate using `interpolate(frame, [12, 45], [0, targetValue], { extrapolateRight: 'clamp' })`.
  - Highlighter Sweep: Yellow/Red highlight bars behind key words wipe left-to-right (`width: 0% -> 100%`) over 10 frames right as the word is spoken.
