import json

for cid in ['clip_01', 'clip_02', 'clip_03', 'clip_04', 'clip_05']:
    path = f'temp/clips_test/{cid}_transcript.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    words = data['words']
    title = data['clip_info']['title']
    print(f"=== {cid}: {title} ===")
    print(f"Total words: {len(words)}, Duration: {data['clip_info']['end'] - data['clip_info']['start']:.1f}s")
    print("First 8 words:", [(w['word'], round(w['start'], 2)) for w in words[:8]])
    print("Last 5 words:", [(w['word'], round(w['start'], 2)) for w in words[-5:]])
    print()
