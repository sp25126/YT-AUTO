# BEAT_SHEET.md — Master 100M+ Viral Business Short Direction

**Project:** Autonomous 100M+ Viral Studio  
**Clip:** Startup Ideas & Timing (33.4s) | Speaker: Raj Shamani & Guest  
**Resolution:** 1080x1920 (9:16 Vertical) | **CFR:** 30.0 FPS | **Integrated Loudness:** -14.1 dB LUFS  
**Director Easing Standard:** Easing curves only (`cubic-bezier`, `spring`), zero `linear` interpolation  

---

## 1. Retention Mechanics & Visual Beat Architecture

| Beat # | Timestamp | Spoken Dialogue | Spoken Emotion | Visual Direction & Technique (AE / AM / AP / CapCut) | Motion Curve & Camera Rig | Audio & Foley Justification |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **00** | `0:00.0 - 0:02.2` | *"But what about the timing? A lot of people..."* | **Contrarian Shock & Urgency** | **CapCut Roto + AP J-Cut Riser**: At 0:00.0, an instantaneous `1.24x -> 1.0x` speed-ramp pull-back happens on Raj. Feathered alpha gradient at the bottom. Floating 3D metallic badge: `THE TIMING TRAP`. | `cubic-bezier(0.16, 1, 0.3, 1)` smooth snap deceleration (`scale: 1.24 -> 1.0`). | **Pre-visual J-cut riser** triggered 5 frames early (`-160ms`) peaking into a **38Hz deep sub-bass drop**. |
| **01** | `0:02.2 - 0:06.2` | *"...a lot of startups die, not because of trend, they die because of wrong timing."* | **Brutal Reality Check** | **AE Swiss Grid & Live Crash Chart**: Full-screen dark obsidian grid (`#07090E`). Single signal color (`#FF2E4C`). SVG line chart plunging downward into a crash zone while mechanical odometer rolls from `0% -> 90%`. AM screen-shake (`wiggle(10, 16)`) on *"wrong timing"*. | Chart path easing: `cubic-bezier(0.7, 0, 0.2, 1)`. Odometer spring: `{ damping: 12, stiffness: 200 }`. | Analog odometer ticker SFX (`tick.wav`) + heavy CRT sub-thud on 90% impact. |
| **02** | `0:06.2 - 0:10.5` | *"Yeah, either they're too early or too late. So how do you pick up..."* | **Binary Dilemma** | **Speaker Push-In + Over-The-Shoulder Glass Callouts**: Live speaker shot retained. Camera pushes in `1.0x -> 1.14x`. At 0:06.8, left frosted-glass badge pops over left shoulder: `⏪ TOO EARLY`. At 0:07.8, right glass badge pops over right shoulder: `⏩ TOO LATE`. | `spring({ damping: 14, stiffness: 180, mass: 0.8 })` with AM directional blur (`feGaussianBlur stdDeviation="18,0"`). | Tape-rewind zip SFX (`tape_rewind.wav`) at 0:06.8 + low mechanical latch click (`latch.wav`) at 0:07.8. |
| **03** | `0:10.5 - 0:15.4` | *"...the right time to enter a space to learn and then eventually start a business?"* | **Curiosity & Strategic Mystery** | **Mark Soy / Alight Motion 3-Panel Whip-Pan**: 3-step horizontal camera whip-pan (`x: 0 -> -1080 -> -2160`) across an infinite dark canvas with SVG `<feGaussianBlur>` directional blur: **Panel A** (*Empty Barren Desert: 0 Demand*), **Panel B** (*Crowded Metropolis: Crushed by Giants*), **Panel C** (*Precision Launch Window*). | Whip curve: `cubic-bezier(0.85, 0, 0.15, 1)` with dynamic velocity blur vector. | 3 rapid camera whoosh swipes (`whoosh_pan.wav`) synchronized with each 1080px panel shift. |
| **04** | `0:15.4 - 0:21.2` | *"Number one, you can't just be on internet, right? You've got to be able to create a advisor net."* | **Authoritative Playbook** | **Premiere BGM Pivot + Mark Soy Torn-Paper Wrapper**: Tense intro drone halts on a tape-stop. Authoritative warm hip-hop / marimba groove kicks in. Torn-newspaper collar frames the guest's shoulders. Floating cream card (`#F5F2DC`) with classical italic serif (`// TACTICAL PLAYBOOK: create an advisor network`). | Snap-in card: `spring({ damping: 15, stiffness: 160 })`. Speaker camera scale punch: `1.18x`. | Vinyl tape-stop at 0:15.4 (`tape_stop.wav`) transitioning into rhythmic groove + paper slide SFX. |
| **05** | `0:21.2 - 0:26.0` | *"The first thing that you want to do is talk to people who've done this for a while."* | **Mentorship Truth** | **Pro Vox Interactive Blueprint & Framed Video**: Architectural 32px blueprint grid (`#0F172A`). Live animated SVG vector nodes linking 3 veteran pillars (`TECH VETERANS`, `CAPITAL ALLOCATORS`, `OPERATIONAL FOUNDERS`) around a framed moving mentor video. | Node draw-in: `strokeDashoffset` interpolated over `0.6s` with `cubic-bezier(0.4, 0, 0.2, 1)`. | Technical UI ping SFX (`ui_ping.wav`) on each node lock + subtle pen-plotter hum. |
| **06** | `0:26.0 - 0:33.4` | *"Because what happens is outside and it looks all rosy. But once you go, the devil's always in the detail..."* | **The Brutal Truth Climax** | **DaVinci Fusion Luma-Split & 4-Frame Shutter Montage**: Opens on warm golden luxury yacht clip (*"looks all rosy"*). At 0:30.6 (*"once you go in"*), a diagonal paper-tear wipe slices the screen open to reveal a rapid 4-frame camera-shutter montage of financial spreadsheets, legal contracts, and late-night execution. | Diagonal split wipe: `0.25s` linear ramp. Montage cadence: 1 frame every 4 frames (`133ms`). | Sharp paper tear SFX (`paper_rip.wav`) at 0:30.6 + 4 mechanical camera shutter clicks (`shutter.wav`) every 133ms. |

---

## 2. Audio Stem Routing & Loudness Architecture

```
[Voice Stream] ──> dynaudnorm ──> highpass(80Hz) ──> acompressor ──> asplit=2 ──┬──> [Voice Master] ──┐
                                                                                 │                     │
                                                                       [Sidechain Control]             │
                                                                                 │                     │
[BGM Stem 1: Dark Intro (0.0-15.4s)]  ──┬──> atrim / afade ──> sidechaincompress ◄──┘                     │
[BGM Stem 2: Warm Groove (15.4-33.4s)] ──┘                                                             │
                                                                                                       ├──> amix=normalize=0 ──> alimiter ──> Output (-14 LUFS)
[SFX Bus: Sub-hit, Ticks, Whooshes, Shutter, Paper Rip] ──> adelay ──> amix=normalize=0 ──────────────┘
```

- **Voice Stem:** Integrated loudness locked at `-14.1 dB LUFS` via `dynaudnorm=f=150:g=15:p=0.92`.
- **BGM Sidechain:** BGM automatically drops by `-7.5 dB` whenever speech is active (attack: 15ms, release: 220ms).
- **Hard Clamping:** `alimiter=limit=0.95:attack=5:release=50` guarantees zero clipping over mobile speakers.
