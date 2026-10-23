import json

transcript_path = r'C:\Users\saumy\.gemini\antigravity-ide\brain\81220eb9-52be-4b9a-b578-1814f56cbf14\.system_generated\steps\385\output.txt'
with open(transcript_path, 'r', encoding='utf-8') as f:
    items = json.load(f)['transcript']

def print_range(label, start_idx, count):
    print(f"\n==================== {label} ====================")
    for i in range(start_idx, min(start_idx + count, len(items))):
        sec = items[i]['offset'] / 1000.0
        dur = items[i].get('duration', 0) / 1000.0
        print(f"[{sec:6.1f}s - {sec+dur:6.1f}s] {items[i]['text']}")

print_range("1. CODERS DISRUPTED BY AI", 785, 45)
