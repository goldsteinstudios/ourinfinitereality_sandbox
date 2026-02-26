"""
Primitive Annotator: CLI tool for building the primitives database.

Usage:
  python primitive_annotator.py add-primitive <id> <name> <category>
  python primitive_annotator.py add-exemplar <primitive_id> <image_path> [--slip N] [--pos N]
  python primitive_annotator.py decompose <glyph_path> <char> <primitive_ids...>
  python primitive_annotator.py list
  python primitive_annotator.py search <primitive_id>  # Find in CHUBS
  python primitive_annotator.py stats
"""

import json
import sys
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
PRIMITIVES_FILE = PROJECT_ROOT / "data" / "primitives" / "primitives.json"
CHUBS_INDEX = PROJECT_ROOT / "data" / "ddj" / "chubs_glyph_index.json"


def load_primitives() -> dict:
    """Load the primitives database."""
    if not PRIMITIVES_FILE.exists():
        return {"version": "0.1.0", "primitives": [], "decompositions": []}
    with open(PRIMITIVES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_primitives(data: dict):
    """Save the primitives database."""
    PRIMITIVES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PRIMITIVES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {PRIMITIVES_FILE}")


def add_primitive(id: str, name: str, category: str, description: str = ""):
    """Add a new primitive to the database."""
    data = load_primitives()

    # Check if exists
    for p in data["primitives"]:
        if p["id"] == id:
            print(f"Primitive '{id}' already exists")
            return

    data["primitives"].append({
        "id": id,
        "name": name,
        "category": category,
        "description": description,
        "exemplars": [],
        "variants": [],
        "structural_role": "",
        "frequency": None
    })

    save_primitives(data)
    print(f"Added primitive: {id} ({name})")


def add_exemplar(primitive_id: str, image_path: str, slip: int = None, position: int = None):
    """Add an exemplar image to a primitive."""
    data = load_primitives()

    for p in data["primitives"]:
        if p["id"] == primitive_id:
            p["exemplars"].append({
                "image_path": image_path,
                "source_glyph": Path(image_path).name,
                "slip": slip,
                "position": position
            })
            save_primitives(data)
            print(f"Added exemplar to {primitive_id}: {image_path}")
            return

    print(f"Primitive '{primitive_id}' not found")


def decompose_glyph(glyph_path: str, character: str, primitive_ids: List[str]):
    """Record which primitives compose a glyph."""
    data = load_primitives()

    # Parse slip/position from filename
    # Pattern: 郭店簡_01A-老子甲_37_01A-37-08.png
    filename = Path(glyph_path).name
    slip = None
    position = None

    import re
    match = re.search(r'_(\d+)_01A-\d+-(\d+)\.png', filename)
    if match:
        slip = int(match.group(1))
        position = int(match.group(2))

    decomposition = {
        "glyph_id": filename,
        "character": character,
        "slip": slip,
        "position": position,
        "primitives": [{"primitive_id": pid, "position": ""} for pid in primitive_ids],
        "notes": ""
    }

    # Remove existing decomposition for this glyph if present
    data["decompositions"] = [d for d in data["decompositions"] if d["glyph_id"] != filename]
    data["decompositions"].append(decomposition)

    save_primitives(data)
    print(f"Decomposed {character} ({filename}) into: {', '.join(primitive_ids)}")


def list_primitives():
    """List all primitives."""
    data = load_primitives()

    print(f"\n=== Primitives ({len(data['primitives'])}) ===\n")

    by_category = {}
    for p in data["primitives"]:
        cat = p["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)

    for cat, prims in sorted(by_category.items()):
        print(f"{cat.upper()}:")
        for p in prims:
            exemplar_count = len(p.get("exemplars", []))
            print(f"  {p['id']}: {p['name']} ({exemplar_count} exemplars)")
        print()

    print(f"=== Decompositions: {len(data['decompositions'])} glyphs ===")


def search_chubs(primitive_id: str):
    """Search CHUBS for glyphs containing a primitive (future: needs ML)."""
    print(f"\nSearching CHUBS for primitive: {primitive_id}")
    print("(This requires the primitives to be trained - placeholder for now)")

    # For now, just show which decomposed glyphs use this primitive
    data = load_primitives()

    matches = []
    for d in data["decompositions"]:
        for p in d["primitives"]:
            if p["primitive_id"] == primitive_id:
                matches.append(d)
                break

    if matches:
        print(f"\nKnown glyphs with {primitive_id}:")
        for m in matches:
            print(f"  {m['character']} (slip {m['slip']}, pos {m['position']})")
    else:
        print(f"No decomposed glyphs contain {primitive_id} yet")


def show_stats():
    """Show database statistics."""
    data = load_primitives()

    print("\n=== Primitives Database Stats ===\n")
    print(f"Total primitives: {len(data['primitives'])}")
    print(f"Total decompositions: {len(data['decompositions'])}")

    # Count by category
    categories = {}
    for p in data["primitives"]:
        cat = p["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\nBy category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Count exemplars
    total_exemplars = sum(len(p.get("exemplars", [])) for p in data["primitives"])
    print(f"\nTotal exemplar images: {total_exemplars}")

    # Primitives without exemplars
    no_exemplars = [p["id"] for p in data["primitives"] if not p.get("exemplars")]
    if no_exemplars:
        print(f"\nNeeding exemplars: {', '.join(no_exemplars)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "add-primitive" and len(sys.argv) >= 5:
        add_primitive(sys.argv[2], sys.argv[3], sys.argv[4],
                      sys.argv[5] if len(sys.argv) > 5 else "")

    elif cmd == "add-exemplar" and len(sys.argv) >= 4:
        slip = None
        pos = None
        for i, arg in enumerate(sys.argv):
            if arg == "--slip" and i + 1 < len(sys.argv):
                slip = int(sys.argv[i + 1])
            if arg == "--pos" and i + 1 < len(sys.argv):
                pos = int(sys.argv[i + 1])
        add_exemplar(sys.argv[2], sys.argv[3], slip, pos)

    elif cmd == "decompose" and len(sys.argv) >= 5:
        decompose_glyph(sys.argv[2], sys.argv[3], sys.argv[4:])

    elif cmd == "list":
        list_primitives()

    elif cmd == "search" and len(sys.argv) >= 3:
        search_chubs(sys.argv[2])

    elif cmd == "stats":
        show_stats()

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
