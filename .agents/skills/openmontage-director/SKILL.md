---
name: openmontage-director
description: Scene & B-Roll orchestrator that coordinates automated B-roll asset fetching and timeline integration.
---

# OpenMontage Director Directives

## Primary Objective
Direct scene generation, transcript entity extraction, and B-roll alignment using `core/broll_fetcher.py` and OpenMontage video composition pipelines.

## Workflow:
1. Scan transcript segments for visualizable entities (technology, money, AI, office, mobile apps).
2. Invoke `core/broll_fetcher.py` to retrieve vertical B-roll assets.
3. Align visual cutaways with the Edit Decision List (EDL) and provide transition markers for the video composer.
