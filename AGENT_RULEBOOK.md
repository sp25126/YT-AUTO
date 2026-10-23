# Antigravity Autonomous Shorts Studio: Master Rulebook

## 1. Skill Execution Hierarchy & Phased Pipeline
Every incoming podcast or video MUST pass through four strictly sequential phases. Do not skip phases or trigger rendering before metadata audits pass.

### Phase 1: Ingestion & Market Intelligence
- **Tools:** `web-yt-researcher`, `youtube-agent-pack` (tools: `title.py`, `swipe.py`)
- **MCPs:** `youtube-intelligence`, `browser-vision`
- **Execution:**
  1. Extract the YouTube Replay Heatmap (`yt-dlp` info_dict heatmap). Flag segments with intensity >= 0.70.
  2. Search competitor channels to identify already saturated clips vs. unclipped high-retention spikes.
  3. Load `channel_profile.json` to lock target audience tone and pacing constraints.

### Phase 2: Retention Curation & Hook Extraction
- **Tools:** `viral-podcast-cutter`, `viral-batch-director`, `youtube-agent-skill` (tools: `hookscore.py`, `deadair.py`)
- **Execution:**
  1. Detect spoken hooks matching the 21 Viral Hook Formulas.
  2. Run `hookscore.py` on the opening 3-second statement. Reject any candidate with a score < 78/100.
  3. Run `deadair.py`. Flag conversational pauses > 350ms for micro-jumpcut removal.
  4. Ensure duration is strictly between 28s and 54s with a self-contained narrative arc.

### Phase 3: Context-Aware Sensory Design
- **Tools:** `context-aware-editor`, `viral-sound-vfx-director`, `elite-sound-designer`
- **MCPs:** `freesound-audio`
- **Execution:**
  1. Measure background video luminance (bright vs. dark) to set subtitle stroke depth.
  2. Map acoustic RMS intensity curve: flag intimate whispers, vocal peaks, and deadpan silence windows.
  3. Pull missing bespoke sound effects via `freesound-audio` directly into `assets/sfx/`.
  4. Program the **Music Dropout Window**: mute BGM completely (0.0 volume) on comedic punchlines or shocking revelations.

### Phase 4: Master Assembly & Quality Assurance
- **Tools:** `elite-video-editor`, `openmontage-director`, `ai-shorts-generator`
- **MCPs:** `ffmpeg-tools`
- **Execution:**
  1. **Dynamic Framing:** Run CPU face tracking (smooth follow, dual-speaker split stack, or reaction punch).
  2. Generate dynamic `.ass` subtitles with per-word typographic morphing.
  3. Compile FFmpeg filtergraph: 9:16 canvas, color grade, sidechain ducking, audio delays.
  4. Output metadata bundle (`title`, `tags`, `thumbnail_prompt`).

---

## 2. Anti-AI Slop Compliance Checklist (Enforced by Agent)
- [ ] No monolithic yellow karaoke text running identically throughout the entire clip.
- [ ] No generic continuous lo-fi track playing over dramatic pauses or punchlines.
- [ ] Visual stimulus reset applied every 2.2 to 2.8 seconds (scale punch, B-roll, or framing switch).
- [ ] No cartoon whoosh spam: maximum 2–3 meaningful sound effects per 40-second duration.
- [ ] Titles must be strictly under 25 characters (excluding hashtags) to avoid mobile feed truncation.

---

## 3. Researched 2026 Viral Sound & Visual Asset Playbook
Short-form algorithms prioritize watch-time completion and first-second swipe-through rate. These current editing and audio conventions drive top-performing retention:

### A. Core SFX Palette
- **Deep Distorted Sub Impact (808 Braam):** Triggers on the opening contrarian hook or major plot twist.
- **Smooth Whoosh Swish:** Accompanying quick push-in camera zooms and visual B-roll transitions.
- **Subtle Bubble Pop / UI Click:** Clean, organic accent for rapid list items, statistics, and keyword pop-ins.
- **Record Scratch / Awkward Silence Crickets:** Immediate comic relief during deadpan punchlines and host reaction shots.
- **Heartbeat Tension Pulse:** Low sub-bass thudding (40–60 Hz) building suspense before high-stakes revelations.

### B. Trending BGM Profiles
- **Industrial Cyberpunk / Dark Phonk:** High-energy business, hustle, and contrarian philosophy clips.
- **Jaunty Pizzicato Strings (*Curb Your Enthusiasm* Vibe):** Sarcastic podcast banter, relationship roasts, and self-deprecating humor.
- **Warm Ambient Felt Piano:** Intimate storytelling, mental health discussions, and high-empathy insights.
- **Minimalist Sub-Bass Cello Drone:** Crime breakdowns, scientific mysteries, and high-tension exposes.

### C. Visual Rhythm & Framing
- **The 2.4-Second Visual Reset:** Alter camera scale (100% to 118%), angle, or visual asset at least once every 2.4 seconds to reset viewer cognitive attention.
- **Dual-Speaker Split Stack:** Top half framed on speaker, bottom half framed on listener's reaction (maintains conversational context without rapid, jarring cuts).
- **High-Pass Contrast Grade:** Lift shadows by +8%, apply an unsharp mask (5:5:1.2), and crush midtone mud to make mobile phone displays pop.

---

## 4. Real-Time Viral Short Production Package Reference

### A. Master Clip Manifest Pattern (`outputs/dopamine_trap/manifest.json`)
```json
{
  "clip_id": "short_dopamine_bankruptcy",
  "topic": "The 5-Minute Morning Habit Ruining Your Brain",
  "archetype": "hustle_alpha",
  "timeline": {
    "start_time": 412.30,
    "end_time": 454.80,
    "duration": 42.50
  },
  "framing_mode": "smooth_follow",
  "visual_tone": "dark_background",
  "hook_evaluation": {
    "formula_type": "The Contrarian Shock",
    "hook_text": "If you check your phone within 10 minutes of waking up, you are medically bankrupting your dopamine.",
    "hook_score": 94
  },
  "narrative_beats": [
    {
      "start": 412.30,
      "end": 418.50,
      "tone": "shock",
      "description": "The Hook: Contrarian statement on phone habits"
    },
    {
      "start": 418.50,
      "end": 432.00,
      "tone": "neutral",
      "description": "The Mechanism: Cortisol spike and baseline receptor crash"
    },
    {
      "start": 432.00,
      "end": 444.00,
      "tone": "whisper",
      "description": "The Threat: Why you feel anxious and unmotivated by 2 PM"
    },
    {
      "start": 444.00,
      "end": 454.80,
      "tone": "shock",
      "description": "The Solution & Loop: Delay screen time by 60 minutes"
    }
  ],
  "silence_windows": [
    {
      "start": 431.20,
      "end": 432.40,
      "note": "Dead silence dropout before revealing brain impact"
    }
  ],
  "sfx_cues": [
    {
      "time": 412.30,
      "effect": "braam",
      "volume": 0.45
    },
    {
      "time": 418.50,
      "effect": "whoosh",
      "volume": 0.35
    },
    {
      "time": 431.20,
      "effect": "sub_drop",
      "volume": 0.50
    },
    {
      "time": 444.00,
      "effect": "whoosh",
      "volume": 0.35
    }
  ],
  "packaging": {
    "title": "Stop Doing This At 7 AM 🛑 #shorts",
    "tags": [
      "#dopamine",
      "#neuroscience",
      "#habits",
      "#productivity",
      "#shorts"
    ],
    "thumbnail_prompt": "Cinematic vertical 9:16 composition: Split perspective. Top half: hyper-realistic close up of a tired man in bed staring into an intensely glowing blue smartphone screen in dark room. Bottom half: glowing holographic brain displaying depleted neuro-pathways. Cold moody lighting, 8k detail."
  }
}
```

### B. Kinetic Subtitle Engine Specification (`outputs/dopamine_trap/captions.ass`)
```ini
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ShockBeat,Montserrat Black,92,&H00FFFFFF&,&H002BF746&,&H00000000&,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,60,60,480,1
Style: NeutralBeat,Montserrat ExtraBold,76,&H00FFFFFF&,&H0000D4FF&,&H00000000&,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,480,1
Style: WhisperBeat,Montserrat,64,&H00D0D0D0&,&H00FFFFFF&,&H001A1A1A&,&H80000000,0,-1,0,0,100,100,0,0,1,4,1,2,60,60,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
; Beat 1: Shock Hook
Dialogue: 0,0:00:00.00,0:00:02.10,ShockBeat,,0,0,0,,{\t(0,100,\fscx120\fscy120)\t(100,200,\fscx100\fscy100)}{\k40}IF {\k35}YOU {\k45}CHECK {\k90}YOUR
Dialogue: 0,0:00:02.10,0:00:04.30,ShockBeat,,0,0,0,,{\t(0,100,\fscx120\fscy120)\t(100,200,\fscx100\fscy100)}{\k55}PHONE {\k40}WITHIN {\k45}TEN {\k80}MINUTES
Dialogue: 0,0:00:04.30,0:00:06.20,ShockBeat,,0,0,0,,{\t(0,100,\fscx125\fscy125)\t(100,200,\fscx100\fscy100)}{\k35}OF {\k45}WAKING {\k110}UP...
; Beat 2: Explanation
Dialogue: 0,0:00:06.20,0:00:09.10,NeutralBeat,,0,0,0,,{\k30}You {\k35}are {\k45}medically {\k70}bankrupting
Dialogue: 0,0:00:09.10,0:00:12.40,NeutralBeat,,0,0,0,,{\k35}your {\k50}dopamine {\k45}receptors {\k40}for
Dialogue: 0,0:00:12.40,0:00:15.80,NeutralBeat,,0,0,0,,{\k35}the {\k40}entire {\k75}rest {\k30}of {\k45}the {\k65}day.
; Beat 3: Whisper / Threat
Dialogue: 0,0:00:19.70,0:00:23.20,WhisperBeat,,0,0,0,,{\k35}Notice {\k35}how {\k40}by {\k35}two {\k45}p.m.
Dialogue: 0,0:00:23.20,0:00:27.10,WhisperBeat,,0,0,0,,{\k30}you {\k40}feel {\k65}completely {\k85}paralyzed?
; Beat 4: Resolution & Call to Action
Dialogue: 0,0:00:31.70,0:00:35.80,ShockBeat,,0,0,0,,{\t(0,100,\fscx115\fscy115)\t(100,200,\fscx100\fscy100)}{\k40}WAIT {\k45}SIXTY {\k75}MINUTES.
Dialogue: 0,0:00:35.80,0:00:42.50,ShockBeat,,0,0,0,,{\t(0,100,\fscx115\fscy115)\t(100,200,\fscx100\fscy100)}{\k35}SAVE {\k40}YOUR {\k65}BRAIN {\k35}BEFORE {\k50}IT {\k80}STARTS.
```

### C. Master FFmpeg Composite Pipeline
```bash
ffmpeg -y \
  -ss 412.30 -t 42.50 -i temp/source.mp4 \
  -stream_loop -1 -i assets/music/dark_synth_drive.mp3 \
  -i assets/sfx/braam.wav \
  -i assets/sfx/whoosh.wav \
  -i assets/sfx/hit.wav \
  -filter_complex "
    [0:v]split=2[bg_raw][fg_raw];
    [bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg_blur];
    [fg_raw]scale=1080:-1,eq=contrast=1.16:saturation=1.14:brightness=-0.02,unsharp=5:5:1.2:5:5:0.0[fg_graded];
    [bg_blur][fg_graded]overlay=(W-w)/2:(H-h)/2[base_canvas];
    [base_canvas]subtitles=outputs/dopamine_trap/captions.ass[v_out];
    [1:a]volume=eval=frame:volume='0.12*(1-between(t,18.90,20.10))'[bgm_ducked];
    [0:a][bgm_ducked]amix=inputs=2:duration=first[dialogue_bgm];
    [2:a]adelay=0|0,volume=0.45[sfx_braam];
    [3:a]adelay=6200|6200,volume=0.35[sfx_whoosh];
    [4:a]adelay=18900|18900,volume=0.50[sfx_sub];
    [dialogue_bgm][sfx_braam]amix=inputs=2:duration=first[a_stem1];
    [a_stem1][sfx_whoosh]amix=inputs=2:duration=first[a_stem2];
    [a_stem2][sfx_sub]amix=inputs=2:duration=first[a_out]
  " \
  -map "[v_out]" \
  -map "[a_out]" \
  -c:v libx264 -preset veryfast -crf 22 \
  -c:a aac -b:a 192k \
  outputs/dopamine_trap/final_viral_short.mp4
```

---

## 5. Curated Sound Design Reference
- [Top 40 Viral TikTok Meme Sound Effects](https://youtu.be/QRQEHtIiuDc?si=xGlLaLfTNRXZu1nU): Reference for pacing and timing cues that keep audience retention high.
