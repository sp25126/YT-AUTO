import json
import sys
import os

sys.path.append(".agents/skills/youtube-agent-skill/skills/yt-script")
import hookscore

with open("transcript.json", "r", encoding="utf-8") as f:
    words = json.load(f)

# Candidate windows and opening sentences
candidates = [
    (10.4, 43.0, "Get client feedback on the live page, not in screenshots."),
    (17.6, 48.8, "Your client clicks where something is wrong and writes what they mean."),
    (67.7, 100.0, "Website feedback is lost before it reaches the developer."),
    (67.7, 110.0, "Website feedback is lost before it reaches the developer."),
    (69.4, 100.0, "Your team then spends hours working out which page or screen the person meant."),
    (78.4, 119.0, "Screenshots do not say which page or device."),
    (82.9, 122.0, "Chat threads bury the decision."),
    (85.6, 126.0, "Vague notes cause extra rounds of changes."),
    (339.6, 370.0, "This feels like wasted space."),
    (346.7, 375.0, "I do not want to come up with a title, I just want to give my feedback.")
]

for start, end, hook in candidates:
    parts, score, formula, hits = hookscore.score(hook)
    print(f"[{start}s - {end}s] ({end-start:.1f}s) Hook: \"{hook}\"")
    print(f"Score: {score} | Formula: {formula} | Props: {parts}\n")
