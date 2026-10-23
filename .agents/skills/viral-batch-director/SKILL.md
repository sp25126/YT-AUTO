---
name: viral-batch-director
description: Cross-references transcript.json, scout_report.json, and channel_profile.json to generate a batch of 5 to 10 viral clip manifests.
---

# Viral Batch Director Protocol

## Mission
Analyze a full podcast recording and extract **5 to 10 high-retention vertical clips** tailored to the brand DNA in `channel_profile.json`.

## Clip Selection Rules
1. **Dynamic Quantity Formula:**
   - Duration < 45 mins: Generate **5 clips**
   - Duration 45–90 mins: Generate **7 clips**
   - Duration > 90 mins: Generate **8–10 clips**
2. **Prioritization Hierarchy:**
   - **Tier 1:** Segments overlapping with `heat_peaks` (intensity > 0.70) in `scout_report.json`.
   - **Tier 2:** Topics matching keywords from top-viewed items in `existing_viral_shorts`.
   - **Tier 3:** Narrative arcs fulfilling one of the 21 viral hook formulas with a hook score > 75.
3. **Pacing & Constraints:**
   - Duration must be strictly between 28 and 54 seconds.
   - Non-overlapping: Clips must be separated by at least 90 seconds.
   - Self-contained: The premise must resolve cleanly without external context.
4. **Style Assignment:** Assign each clip one archetype (`comedy_banter`, `hustle_alpha`, `dark_mystery`, or `tech_intellectual`).
5. **Comedic / Tension Drops:** Locate 1–2 silence windows (`start` and `end`) where background audio cuts completely out.

## Output Schema
Always output `batch_manifest.json` wrapped in a markdown code fence:
```json
{
  "source_video_id": "dQw4w9WgXcQ",
  "total_clips": 6,
  "clips": [
    {
      "clip_id": "clip_01",
      "archetype": "hustle_alpha",
      "start_time": 242.4,
      "end_time": 284.1,
      "hook_text": "The reason most creators fail within 90 days...",
      "hook_score": 91,
      "silence_windows": [
        {"start": 268.0, "end": 269.1}
      ],
      "sfx_markers": [
        {"time": 242.4, "effect": "whoosh"},
        {"time": 269.1, "effect": "braam_hit"}
      ],
      "title": "Why 99% Quit in 90 Days #shorts",
      "tags": ["#creator", "#motivation", "#growth", "#shorts"],
      "thumbnail_prompt": "Cinematic vertical split: high contrast dramatic portrait of guest looking stressed on top, rising red stock chart breaking on bottom, hyper-detailed, studio rim lighting, 9:16."
    }
  ]
}
```
