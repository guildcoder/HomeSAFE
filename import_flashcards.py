#!/usr/bin/env python3
"""Convert a CSV/TSV export into data/flashcards.json.

Expected columns:
- term, definition

Usage:
  python scripts/import_flashcards.py input.csv
  python scripts/import_flashcards.py input.tsv --tsv
"""
import csv, json, argparse, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--tsv", action="store_true", help="Input is TSV instead of CSV")
    ap.add_argument("--out", default="data/flashcards.json")
    args = ap.parse_args()

    in_path = pathlib.Path(args.input)
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    dialect = 'excel-tab' if args.tsv else 'excel'
    cards = []
    with in_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            term = (row.get("term") or row.get("Term") or "").strip()
            definition = (row.get("definition") or row.get("Definition") or "").strip()
            if term and definition:
                cards.append({"term": term, "definition": definition})

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(cards)} cards → {out_path}")

if __name__ == "__main__":
    main()
