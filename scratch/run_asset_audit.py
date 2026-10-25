import os
import sys
sys.path.insert(0, os.path.abspath("."))
import json
from core.asset_fit_auditor import fetch_and_audit_internet_audio

audits = [
    ("deep sub bass drop 40hz cinematic", "sfx", 2.2, "deep_impact", "sub_drop.wav"),
    ("mechanical odometer clock tick", "sfx", 0.15, "crisp_ui", "tick.wav"),
    ("analog tape rewind fast zip", "sfx", 0.8, "crisp_ui", "tape_rewind.wav"),
    ("camera mechanical shutter click", "sfx", 0.25, "crisp_ui", "shutter.wav"),
    ("heavy cardboard paper tear rip", "sfx", 0.6, "foley", "paper_rip.wav"),
    ("vinyl record scratch stop turntable", "sfx", 0.75, "foley", "vinyl_stop.wav"),
    ("cinematic whoosh transition air swipe", "sfx", 0.8, "foley", "whoosh.wav"),
    ("futuristic clean ui notification ping", "sfx", 0.4, "crisp_ui", "ui_ping.wav"),
    ("dark ambient bass drone cinematic", "bgm", 16.0, "dark_pulse", "eerie_sub_drone.mp3"),
    ("authoritative warm hip hop marimba instrumental groove", "bgm", 20.0, "warm_groove", "authoritative_groove.mp3"),
]

results = []
print("="*70)
print("[*] EXECUTING ACTIVE ASSET & ACOUSTIC FIT AUDIT")
print("="*70)

for query, a_type, dur, vibe, filename in audits:
    res = fetch_and_audit_internet_audio(query, a_type, dur, vibe, filename)
    print(f"[{'PASS' if res.get('fit') else 'FAIL'}] {filename}: RMS={res.get('rms_energy')} | DomFreq={res.get('dominant_freq_hz')}Hz | {res.get('audit_notes')}")
    results.append({"filename": filename, **res})

with open("temp/audio_audit_report.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n[OK] Asset & Audio Fit Audit Complete -> temp/audio_audit_report.json")
