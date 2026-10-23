---
name: ai-shorts-generator
description: Generates short viral cinematic videos from a single idea using OpenMontage free pipelines or cloud video endpoints.
---

# AI Shorts Generator

## Workflow:
1. Accept a 1-sentence prompt idea from the user.
2. Expand the idea into a dramatic visual prompt (high camera-shake, gritty, realistic lighting, punchy dialogue).
3. Generate title strictly under 25 characters + append targeted hashtags (`#shorts #viral`).
4. Generate 9:16 vertical thumbnail prompt for Antigravity's native image generator.
5. Delegate video assembly to `core/openmontage` for offline asset rendering, or emit task payload for external video generation.
