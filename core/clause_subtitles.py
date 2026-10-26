import os
import json

def build_clause_aware_phrases(words: list, max_time: float = 32.85) -> list:
    """
    1. Fixes podcast stutters ('net.' -> 'network', removes 'cat', etc.).
    2. Splits captions strictly at punctuation (?, ., ,, !) so 'the timing? A' never happens!
    3. Guarantees no phrase bleeds across sentence boundaries.
    """
    token_fixes = {
        "net.": "network.",
        "net": "network",
        "cat": "",
        "umm": "",
        "uh": ""
    }
    cleaned_words = []
    for w in words:
        if w["start"] >= max_time:
            break
        raw = w["word"].strip()
        low = raw.lower()
        if low in token_fixes:
            if not token_fixes[low]:
                continue
            raw = token_fixes[low]
        cleaned_words.append({
            "word": raw,
            "start": round(w["start"], 3),
            "end": min(round(w["end"], 3), max_time)
        })

    phrases = []
    current = []
    for w in cleaned_words:
        current.append(w)
        ends_clause = any(w["word"].endswith(p) for p in ("?", ".", ",", "!"))
        if len(current) >= 3 or ends_clause:
            phrases.append({
                "start": current[0]["start"],
                "end": current[-1]["end"],
                "words": current
            })
            current = []

    if current:
        phrases.append({
            "start": current[0]["start"],
            "end": current[-1]["end"],
            "words": current
        })

    return phrases

def generate_clause_phrases_file(
    words_input_path: str = "remotion_studio/public/assets/words.json",
    output_path: str = "remotion_studio/public/assets/clause_phrases.json",
    max_time: float = 32.85
) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(words_input_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    phrases = build_clause_aware_phrases(words, max_time)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)

    print(f"[Clause Subtitles] Generated {len(phrases)} clause-aware phrases -> {output_path}")
    return output_path

if __name__ == "__main__":
    generate_clause_phrases_file()
