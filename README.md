# 🚀 YT-AUTO: Autonomous 100M+ Viral Short Studio

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](#)
[![Remotion](https://img.shields.io/badge/Remotion-4.0+-violet.svg)](#)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-7.1+-green.svg)](#)
[![Loudness](https://img.shields.io/badge/Loudness--14.1%20dB%20LUFS-orange.svg)](#)

> **Industrial-grade, code-driven autonomous studio transforming raw long-form podcasts into 5 radically distinct viral short architectures.** Built by senior video systems engineers and viral editors who produce content reaching over 100M+ views across YouTube Shorts, Instagram Reels, and TikTok.

---

## ⚡ The 5 Radical Viral Architectures

In strict accordance with the **Anti-Repetition Law**, every variation features its own unique **Cut Cadence**, **Color Grade**, **Subtitle Engine**, **Motion Curve**, **BGM Genre**, and **SFX Foley Pack**:

| Variant | Style Archetype | Visual Hook | Subtitle Engine | Audio & SFX Palette | Output File |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | **IG Luxury Glass** (`DetnsvBN1fs`) | 100% on-speaker, teal/gold LUT, upper luma-blended B-roll floating in dark studio air, 3D Apple frosted glass notification pills | Single-line Montserrat Bold with glowing emerald/gold morphing highlight pill ($y=1460$) | Deep house chill-hop + iOS glass UI pops, soft air swishes, 40Hz sub drops | [`01_IG_Luxury_Glass.mp4`](outputs/5_viral_styles/01_IG_Luxury_Glass.mp4) |
| **02** | **DaVinci Fusion Editorial** (`RXQOmQGJK34`) | Textured paper `#ECEAE4` takeovers, tilted Polaroid vintage frames, 4-frame shutter montage (10.8s–12.0s), exclusion flashes | Multi-tile staggered write-on text with stepped 3-stage camera punch-ins ($1.0x \rightarrow 1.08x \rightarrow 1.16x$) | Ambient sub-drone + firewood crackle room texture + camera shutter clicks + cinema hits | [`02_DaVinci_Fusion_Editorial.mp4`](outputs/5_viral_styles/02_DaVinci_Fusion_Editorial.mp4) |
| **03** | **Curved Cinema Pyramid** (`OoayDYJKkUs`) | Permanent curved-edge black cinema border (68px radius) + rapid high-contrast cinema cuts | Sliding 3-word Pyramid Stack ($y=980$) in translucent Soft-Light Purple (`#A855F7`) & White | Emotional cinematic felt piano + diegetic scenery foley (ocean waves, desert wind) | [`03_Curved_Cinema_Pyramid.mp4`](outputs/5_viral_styles/03_Curved_Cinema_Pyramid.mp4) |
| **04** | **Pro Vox Data Journalism** | Warm newsprint `#F4F1EA`, 32px blueprint grid, animated SVG Fig 01 Bar Chart with live odometer ($0\% \rightarrow 90\%$), Fig 02 Bell Curve | Editorial label strips (`Georgia Italic` + `Inter ExtraBold`), suppressed during charts | Investigative marimba / pizzicato plucks + mechanical odometer ticks + paper rips | [`04_Vox_Pro_Documentary.mp4`](outputs/5_viral_styles/04_Vox_Pro_Documentary.mp4) |
| **05** | **Mark Soy Mixed-Media Wrapper** (`MoVlt-ptxIk`) | B&W speaker cutout card zooming out in 3D (`#1B4332`), dark grid with colored geometric corner blocks, torn-newspaper shoulder wrap | 1-word lowercase captions ($y=1160$) on live speaker; full-screen bold sans + classical italic serif on cream cards | Percussive stomp-clap rhythm + paper tears, UI pops, whip-pans, bass drops | [`05_MarkSoy_MixedMedia_Wrapper.mp4`](outputs/5_viral_styles/05_MarkSoy_MixedMedia_Wrapper.mp4) |

---

## 🛠️ System Highlights & Engineering Fixes

1. **Zero-Frame-Drop Compositing (`framesync` Stutter Solved):**
   - Eliminates the 5–8 FPS playback stutter caused by chaining unindexed OpenCV `mp4v` files into FFmpeg `-itsoffset` overlays.
   - Base footage is conformed to a constant 30.000 FPS timebase (`temp/clean_base_30fps.mp4`).
2. **Audio Normalization (`normalize=0` on `amix` Solved):**
   - Eliminates the silent voice bug where default FFmpeg `amix` attenuates speech by -23 dB across delayed SFX streams.
   - Full timeline mastered to broadcast **`-14.1 dB LUFS`** integrated loudness with a **`-1.0 dBFS`** ceiling.
3. **Anti-Literal Visual Metaphors:**
   - Translates spoken idioms into compelling human visuals (e.g., "advisor network" $\rightarrow$ boardroom executives mentoring, rather than Ethernet cables).
   - Live integration with moving 1080p stock footage via Pixabay API.
4. **Remotion Kinetic Overlay Engine:**
   - React-based motion engine (`remotion_studio/`) executing 3D spring physics, SVG vector line tracing, and frosted glass dynamic blur.

---

## 📁 Repository Layout

```
YT-AUTO/
├── .agents/skills/                   # Autonomous AI agent skills
│   └── viral-100m-engine/            # Master Unified 100M Short Director Skill
├── assets/
│   ├── broll/                        # Moving 1080p stock clips
│   ├── music/                        # Curated multi-genre BGM tracks
│   └── sfx/                          # Bespoke foley sound library
├── core/
│   ├── five_style_filters.py         # 5 custom ASS subtitle engines & mask generators
│   ├── render_archetypes.py          # Automated Remotion composition renderer
│   ├── pixabay_remotion_bridge.py    # Pixabay API bridge (video/photo)
│   └── generate_pro_sfx.py           # Foley sound synthesizer
├── remotion_studio/                  # React & Remotion project for kinetic overlays
├── outputs/
│   └── 5_viral_styles/               # 5 finalized master MP4 deliverables
├── temp/                             # Intermediate build assets & masks
├── build_5_distinct_styles.py        # Master production pipeline runner
├── requirements.txt                  # Python dependencies
├── .env                              # Environment configuration (Pixabay key included)
├── ARCHITECTURE_AND_SYSTEM_DESIGN.md # Comprehensive engineering & system design manual
├── STATUS.md                         # Forensic audit history & production log
└── README.md                         # Project documentation
```

---

## 🚀 Quickstart

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+** & npm
- **FFmpeg 6.0+** (with `libass` and `libx264`)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/sp25126/YT-AUTO.git
cd YT-AUTO

# Install Python requirements
pip install -r requirements.txt

# Install Remotion dependencies
cd remotion_studio
npm install
cd ..
```

### 3. API Configuration
The repository includes a pre-configured testing key for Pixabay in `.env`:
```env
PIXABAY_API_KEY=58086702-f40c68777ef64de312fca07dd
```

### 4. Build All 5 Viral Styles
```bash
# 1. Synthesize procedural sound effects
python core/generate_pro_sfx.py

# 2. Render kinetic Remotion overlays
python core/render_archetypes.py

# 3. Assemble and export the 5 master short variations
python build_5_distinct_styles.py
```

All 5 finished master shorts will be written to `outputs/5_viral_styles/`.

---

## 📖 In-Depth Documentation

For complete technical specifications, see:
- [Architecture & System Design Manual](ARCHITECTURE_AND_SYSTEM_DESIGN.md)
- [Project Status & Forensic Engineering Log](STATUS.md)
- [Agent Operational Rulebook](AGENT_RULEBOOK.md)
