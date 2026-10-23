---
name: viral-100m-engine
description: Autonomous 100M+ viral short video studio engine. Combines podcast hook curation, retention heuristics, 5 radical visual compositing architectures (IG Luxury Glass, DaVinci Fusion, Curved Cinema, Vox Data Journalism, Mark Soy Wrapper), Remotion kinetic overlays, and broadcast loudness audio engineering.
---

# 100M+ Viral Short Studio Master Engine

## Purpose & Overview
This skill operates as an autonomous, senior-level viral video director and media systems engineer. It synthesizes all specialized studio skills (`viral-podcast-cutter`, `context-aware-editor`, `elite-video-editor`, `elite-sound-designer`, `remotion-vox-system`, `viral-sound-vfx-director`) into a unified pipeline capable of producing **5 radically distinct viral styles** from any raw video podcast.

It strictly enforces the **Anti-Repetition Law**: every short variation must utilize a unique cut cadence, color grade, subtitle engine, motion curve, BGM genre, and sound design palette.

---

## The 5 Viral Archetype Registry

When generating variations, the agent must deploy all 5 architectures without cross-pollinating templates:

### 1. `style1_luxury_glass` (Instagram Luxury Tech & Speed-Ramp)
- **Reference:** Elite lifestyle & tech founder Reels (`DetnsvBN1fs`)
- **Visuals:** 100% on-speaker, teal/gold contrast LUT (`eq=contrast=1.16:saturation=1.18`), moving B-roll blended into upper 45% dark studio air via feathered luma mask (`temp/top_luma_mask.png`), 3D Apple frosted glass notification pills at $y=140$.
- **Subtitles:** Montserrat Bold single-line at $y=1460$ with smooth emerald/gold morphing highlight pill.
- **Audio:** Luxury deep house / chill-hop (`chill_lofi.mp3`) + iOS glass UI pops, soft air swishes, 40 Hz sub-bass drop.

### 2. `style2_davinci_fusion` (DaVinci Resolve Fusion Editorial)
- **Reference:** Hishaam Ahmed documentary editing (`RXQOmQGJK34`)
- **Visuals:** Textured paper `#ECEAE4` takeovers, tilted vintage Polaroid frames with drop shadows, 4-frame rapid shutter montage (10.8s–12.0s) flashing 5 market images 4 frames apart (0.133s), exclusion color inversion flashes.
- **Subtitles:** Multi-tile staggered write-on text with stepped 3-stage camera punch-ins ($1.0x \rightarrow 1.08x \rightarrow 1.16x$).
- **Audio:** Ambient sub-drone (`eerie_sub_drone.mp3`) + firewood crackle room texture (`firewood.wav`) + camera shutter clicks + cinema impact hit.

### 3. `style3_curved_cinema` (Curved Cinema & Pyramid Text)
- **Reference:** Grow with Alex 1.5M-like cinematic aesthetic (`OoayDYJKkUs`)
- **Visuals:** Permanent curved-edge black cinema border (68px corner radius, `temp/curved_border.png`) framing the entire 9:16 canvas, high-contrast cinema cuts (`eq=contrast=1.24:saturation=1.32`) every 2.2s.
- **Subtitles:** Center 3-word pyramid stack at $y=980$ in translucent Soft-Light Purple (`#A855F7`) and crisp white.
- **Audio:** Emotional cinematic felt piano (`warm_ambient_piano.mp3`) + diegetic scenery foley (real ocean waves at 28s, desert wind at 10.8s).

### 4. `style4_vox_documentary` (Authentic Vox Studio Data Journalism)
- **Reference:** Vox Studio / Johnny Harris explainer journalism
- **Visuals:** Warm newsprint `#F4F1EA`, 32px blueprint grid, subtle film grain (`noise=alls=6`), animated SVG Fig 01 horizontal bar chart with real-time ticking odometer ($0\% \rightarrow 90\%$), animated Fig 02 Bell Curve market timing graph.
- **Subtitles:** Editorial label strips (`Georgia Italic` + `Inter ExtraBold`). **Strictly suppressed** during chart visualizers.
- **Audio:** Investigative marimba / pizzicato plucks (`pizzicato_comedy.mp3`) + mechanical odometer ticks + felt-marker squeaks + paper rips.

### 5. `style5_marksoy_wrapper` (Mark Soy Code-Driven Motion Wrapper)
- **Reference:** Mark Soy / Vinh Giang motion wrapper (`MoVlt-ptxIk`)
- **Visuals:** 1-word lowercase captions on live speaker (`y=1160`), speaker cutout card zooming out in 3D ($rotateY: -14^\circ, rotateX: 8^\circ$) inside an emerald card (`#1B4332`), dark navy grid `#040814` with sliding geometric blocks, torn-newspaper shoulder wrap (`temp/newspaper_shoulders.png`), warm cream `#F5F2DC` editorial typography snaps.
- **Audio:** Punchy percussive stomp-clap rhythm (`dark_synth_drive.mp3`) + paper tears, UI pops, whip-pans, bass drops.

---

## Operational Workflow

```
[Phase 1: Ingest & Audio Prep]
  ├── Normalize voice audio to -14.1 dB LUFS with speechnorm & 75Hz highpass
  └── Pre-render source video to 30.000 FPS constant timebase: temp/clean_base_30fps.mp4

[Phase 2: Transcript & Hook Scoring]
  ├── Run faster-whisper for word-level timestamps (transcript.json)
  └── Score opening 3s hook against 21 Hook Formulas (reject score < 78/100)

[Phase 3: Visual Metaphor Resolution]
  ├── Map transcript idioms to narrative human visuals (via core/pixabay_remotion_bridge.py)
  └── Fetch moving 1080p stock clips via Pixabay API (PIXABAY_API_KEY)

[Phase 4: Remotion Motion Synthesis]
  ├── Render 13 kinetic overlay compositions: python core/render_archetypes.py
  └── Generate PNG alpha masks (curved border, luma mask, newspaper shoulder overlay)

[Phase 5: Subtitle & Audio Assembly]
  ├── Compile bespoke .ass subtitle files for each style (core/five_style_filters.py)
  ├── Synthesize custom foley SFX (core/generate_pro_sfx.py)
  └── Execute master FFmpeg filtergraph with normalize=0 on amix

[Phase 6: Quality Assurance Audit]
  ├── Verify 0 frame drops (constant 30 FPS)
  ├── Verify -14.1 dB LUFS integrated loudness
  └── Extract and inspect verification keyframes
```

---

## Non-Negotiable Engineering Rules

1. **The Audio Normalization Rule:**
   Never call `amix` without `normalize=0`. Standard FFmpeg `amix` divides voice volume by $1/N$ active inputs, destroying vocal presence.
   ```bash
   amix=inputs=N:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.92:attack=5:release=50
   ```
2. **The Framesync Rule:**
   Never chain unindexed OpenCV `mp4v` files into FFmpeg `-itsoffset` overlays. Always conform base video to a rock-solid 30.0 FPS stream (`temp/clean_base_30fps.mp4`).
3. **The Anti-Literal Metaphor Rule:**
   Never search stock libraries with literal spoken nouns. Translate phrases into emotional and human narrative metaphors (e.g., "advisor network" $\rightarrow$ "boardroom mentors").
4. **The Cognitive Load Subtitle Rule:**
   When full-screen data charts or 3D cards are animating on screen, suppress lower-third subtitles to eliminate competing eye paths.

---

## Standard Execution Commands

To execute the entire 5-variant suite autonomously:
```bash
# 1. Foley synthesis
python core/generate_pro_sfx.py

# 2. Remotion composition render
python core/render_archetypes.py

# 3. Master 5-style compositing & export
python build_5_distinct_styles.py
```
Output files are written to: `outputs/5_viral_styles/`
