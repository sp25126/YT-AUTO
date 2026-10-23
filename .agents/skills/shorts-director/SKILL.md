---
name: shorts-director
description: Detects genre archetype, locates comedic timing cutouts, tags emphasis moments, and outputs stylized manifest.
---

# Human-Grade Shorts Director Skill

When analyzing `transcript.json`:
1. **Detect Genre Archetype:** Classify into one of:
   - `comedy_banter` (humorous/awkward/sarcastic)
   - `hustle_alpha` (motivational/business/high intensity)
   - `dark_mystery` (crime/unsolved/shocking discoveries)
   - `tech_intellectual` (philosophical/explanatory/thoughtful)

2. **Locate Comedic Silence Windows (`silence_windows`):**
   - If the clip has a punchline, sarcastic pause, or awkward silence, tag the exact interval (`start` to `end`). The BGM will mute entirely here.

3. **Curate Deliberate SFX:**
   - On comedic cuts: inject `record_scratch`, `crickets`, or `vinyl_stop`.
   - On profound/heavy claims: inject `braam_hit`.
   - Avoid sound clutter. Maximum 2–3 SFX per 40-second clip.

## Manifest Output:
```json
{
  "archetype": "comedy_banter",
  "start_time": 112.5,
  "end_time": 154.2,
  "silence_windows": [
    {"start": 131.0, "end": 132.4}
  ],
  "sfx_markers": [
    {"time": 131.0, "effect": "record_scratch"},
    {"time": 131.8, "effect": "crickets"}
  ],
  "title": "When the joke doesn't land... #shorts",
  "tags": ["#shorts", "#comedy", "#podcastclips"],
  "thumbnail_prompt": "Awkward close-up portrait of the speaker looking sideways with wide eyes, split screen showing an empty chair, warm comedic lighting, 9:16 vertical ratio."
}
```
