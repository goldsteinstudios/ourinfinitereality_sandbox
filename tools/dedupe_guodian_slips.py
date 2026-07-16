"""
Dedupe chapter-boundary slips in guodian_interactive.json

Slips 6, 23, 29 and 35 straddle a chapter boundary and are transcribed in full
under both adjoining chapters. build_guodian_interactive_data.py appended each
copy, so those four slips carry every character twice.

This repairs the committed JSON in place rather than rebuilding it. The builder
is currently unreproducible: radicals.yaml, guodian_bundle_a_data.csv and
data/glossary/entries are gitignored and no longer on disk, so a rebuild would
drop the radical decompositions, substrates and breakdowns that only survive in
this file. See the sibling fix in build_guodian_interactive_data.py for when
those inputs come back.

Duplicate entries are byte-identical, so keeping the first is lossless.
Idempotent: running it on already-deduped data is a no-op.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGETS = [
    PROJECT_ROOT / "public" / "data" / "guodian_interactive.json",
    PROJECT_ROOT / "data" / "ddj" / "guodian_interactive.json",
]


def dedupe_slip(characters):
    """Keep the first entry per position. Raises if copies disagree."""
    seen = {}
    for char in characters:
        position = char["position"]
        if position in seen:
            if seen[position] != char:
                raise ValueError(
                    f"position {position} appears twice with different content; "
                    "refusing to guess which is authoritative"
                )
            continue
        seen[position] = char
    return [seen[p] for p in sorted(seen)]


def dedupe(data):
    removed = 0
    for slip in data["slips"].values():
        before = len(slip["characters"])
        slip["characters"] = dedupe_slip(slip["characters"])
        dropped = before - len(slip["characters"])
        if dropped:
            print(f"  slip {slip['slip']:2d}: {before} -> {len(slip['characters'])} characters")
            removed += dropped

    data["metadata"]["total_positions"] = sum(
        len(s["characters"]) for s in data["slips"].values()
    )
    return removed


def main():
    for path in TARGETS:
        if not path.exists():
            print(f"skipping (absent): {path}")
            continue

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        print(f"{path.relative_to(PROJECT_ROOT)}:")
        removed = dedupe(data)

        if not removed:
            print("  already deduped, nothing to do")
            continue

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

        print(f"  removed {removed} duplicate characters; "
              f"total_positions now {data['metadata']['total_positions']}\n")


if __name__ == "__main__":
    main()
