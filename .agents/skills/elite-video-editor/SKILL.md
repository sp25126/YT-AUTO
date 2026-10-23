---
name: elite-video-editor
description: Directs high-retention video pacing, kinetic scale changes, dynamic camera punch-ins, and color grading.
---

# Elite Video Editor Directives (Top 1% Algorithmic Retention)

## 1. Pacing & Cut Cadence
- **Visual Stimulus Rule:** The viewer's brain must register visual change every **2.2 to 2.8 seconds**.
- **Dynamic Scale Punch-ins:** Switch between 100% and 115% scale on emphasized arguments. Never stay on a static 9:16 crop for longer than 3 seconds.
- **Micro-Jumpcuts:** When `deadair.py` flags pauses > 350ms, trim the quiet frame window to maintain conversational velocity.

## 2. Cinematic Color Grade (FFmpeg Native CPU)
- Standardize podcast webcams and studio footage with vibrant, high-contrast grading:
  - Contrast: `+12%`
  - Saturation: `+18%`
  - Sharpness unsharp mask: `luma_msize_x=5:luma_msize_y=5:luma_amount=1.2`
  - Filter string: `eq=contrast=1.12:saturation=1.18:brightness=-0.02,unsharp=5:5:1.2:5:5:0.0`

## 3. Visual B-Roll Placement
- When the speaker references an entity (e.g., "money", "AI", "time", "brain"), inject a 1.2s B-roll overlay with a 15-frame cross-dissolve.
