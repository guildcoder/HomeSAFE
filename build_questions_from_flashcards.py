#!/usr/bin/env python3
"""Generate a basic multiple-choice question bank from flashcards.

This creates two MCQs per flashcard:
1) term -> definition
2) definition -> term

Usage:
  python scripts/build_questions_from_flashcards.py
"""
import json, random, pathlib

FLASH = pathlib.Path("data/flashcards.json")
OUT = pathlib.Path("data/questions.json")

def pick_wrong(deck, correct_idx, field, k=3):
    idxs = list(range(len(deck)))
    idxs.remove(correct_idx)
    random.shuffle(idxs)
    return [deck[i][field] for i in idxs[:k]]

def main():
    deck = json.loads(FLASH.read_text(encoding="utf-8"))
    random.shuffle(deck)

    qs = []
    for i, c in enumerate(deck):
        # term -> definition
        wrongs = pick_wrong(deck, i, "definition")
        choices = [c["definition"], *wrongs]
        random.shuffle(choices)
        ans = choices.index(c["definition"])
        qs.append({
            "id": f"fc-{i}-t2d",
            "category": "general",  # edit later
            "type": "mcq",
            "prompt": f"What is the definition of: “{c['term']}”?",
            "choices": choices,
            "answerIndex": ans,
            "explanation": c["definition"]
        })

        # definition -> term
        wrongs = pick_wrong(deck, i, "term")
        choices = [c["term"], *wrongs]
        random.shuffle(choices)
        ans = choices.index(c["term"])
        qs.append({
            "id": f"fc-{i}-d2t",
            "category": "general",  # edit later
            "type": "mcq",
            "prompt": "Which term matches this definition?",
            "stem": c["definition"],
            "choices": choices,
            "answerIndex": ans,
            "explanation": c["term"]
        })

    OUT.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(qs)} questions → {OUT}")

if __name__ == "__main__":
    main()
