"""
Corrections Manager for Guodian Laozi Glyph Mappings.

Provides:
1. Load/save corrections from JSON
2. Apply corrections to transcriptions
3. CLI interface for manual corrections
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class CorrectionsManager:
    """Manage manual corrections to auto-generated glyph mappings."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.corrections_file = self.project_root / "data" / "ddj" / "corrections.json"
        self._corrections = None

    @property
    def corrections(self) -> Dict:
        """Lazy-load corrections from JSON."""
        if self._corrections is None:
            self._corrections = self._load_corrections()
        return self._corrections

    def _load_corrections(self) -> Dict:
        """Load corrections from JSON file."""
        if not self.corrections_file.exists():
            return {"_metadata": {}, "corrections": {}}

        with open(self.corrections_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_corrections(self):
        """Save corrections to JSON file."""
        self.corrections["_metadata"]["updated"] = datetime.now().isoformat()
        self.corrections_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.corrections_file, 'w', encoding='utf-8') as f:
            json.dump(self.corrections, f, ensure_ascii=False, indent=2)

    def get_correction(self, slip: int, position: int) -> Optional[Dict]:
        """Get correction for a specific slip/position."""
        key = f"{slip}_{position}"
        return self.corrections.get("corrections", {}).get(key)

    def set_correction(self, slip: int, position: int,
                       guodian_char: str, received_char: Optional[str],
                       note: str = "") -> None:
        """Set or update a correction."""
        key = f"{slip}_{position}"
        self.corrections.setdefault("corrections", {})[key] = {
            "guodian": guodian_char,
            "received": received_char,
            "note": note,
            "added": datetime.now().isoformat()
        }
        self.save_corrections()

    def remove_correction(self, slip: int, position: int) -> bool:
        """Remove a correction. Returns True if removed."""
        key = f"{slip}_{position}"
        if key in self.corrections.get("corrections", {}):
            del self.corrections["corrections"][key]
            self.save_corrections()
            return True
        return False

    def get_all_corrections(self) -> Dict[Tuple[int, int], Dict]:
        """Get all corrections as {(slip, position): data} dict."""
        result = {}
        for key, data in self.corrections.get("corrections", {}).items():
            if "_" in key:
                slip, pos = key.split("_")
                result[(int(slip), int(pos))] = data
        return result

    def apply_to_transcription(self, slip: int, position: int,
                                auto_guodian: str, auto_received: str) -> Tuple[str, str, bool]:
        """
        Apply correction if exists, otherwise return auto values.
        Returns: (guodian_char, received_char, was_corrected)
        """
        correction = self.get_correction(slip, position)
        if correction:
            return (
                correction["guodian"],
                correction.get("received"),
                True
            )
        return (auto_guodian, auto_received, False)

    def import_from_review(self, review_json_path: Path) -> int:
        """
        Import corrections from a manual review JSON file.
        Returns number of corrections imported.
        """
        with open(review_json_path, 'r', encoding='utf-8') as f:
            review_data = json.load(f)

        count = 0
        for correction in review_data.get("corrections", []):
            slip = correction["slip"]
            position = correction["position"]
            corrected_char = correction["corrected_char"]
            note = correction.get("note", "Imported from manual review")

            # The corrected_char is what the user identified - that's the Guodian char
            # We need to figure out the received char (standard form)
            self.set_correction(
                slip, position,
                guodian_char=corrected_char,
                received_char=None,  # Will need separate lookup
                note=note
            )
            count += 1

        return count

    def get_stats(self) -> Dict:
        """Get correction statistics."""
        corrections = self.get_all_corrections()
        slips = set(slip for slip, _ in corrections.keys())

        return {
            "total_corrections": len(corrections),
            "slips_affected": len(slips),
            "slips_list": sorted(slips)
        }


def main():
    """CLI for corrections management."""
    import sys

    manager = CorrectionsManager()

    if len(sys.argv) < 2:
        print("Corrections Manager CLI")
        print("-" * 40)
        stats = manager.get_stats()
        print(f"Total corrections: {stats['total_corrections']}")
        print(f"Slips affected: {stats['slips_affected']}")
        print("\nUsage:")
        print("  python corrections_manager.py list")
        print("  python corrections_manager.py add <slip> <position> <guodian_char> [received_char] [note]")
        print("  python corrections_manager.py remove <slip> <position>")
        print("  python corrections_manager.py import <review_json_path>")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        corrections = manager.get_all_corrections()
        if not corrections:
            print("No corrections recorded.")
            return

        print(f"Total corrections: {len(corrections)}\n")
        for (slip, pos), data in sorted(corrections.items()):
            rec = data.get('received') or '(particle)'
            note = data.get('note', '')
            print(f"  Slip {slip:02d}, Position {pos:02d}: {data['guodian']} -> {rec}")
            if note:
                print(f"    Note: {note}")

    elif cmd == "add":
        if len(sys.argv) < 5:
            print("Usage: add <slip> <position> <guodian_char> [received_char] [note]")
            return

        slip = int(sys.argv[2])
        pos = int(sys.argv[3])
        guodian = sys.argv[4]
        received = sys.argv[5] if len(sys.argv) > 5 else None
        note = sys.argv[6] if len(sys.argv) > 6 else ""

        manager.set_correction(slip, pos, guodian, received, note)
        print(f"Added correction: Slip {slip}, Pos {pos}: {guodian} -> {received or '(particle)'}")

    elif cmd == "remove":
        if len(sys.argv) < 4:
            print("Usage: remove <slip> <position>")
            return

        slip = int(sys.argv[2])
        pos = int(sys.argv[3])

        if manager.remove_correction(slip, pos):
            print(f"Removed correction for Slip {slip}, Position {pos}")
        else:
            print(f"No correction found for Slip {slip}, Position {pos}")

    elif cmd == "import":
        if len(sys.argv) < 3:
            print("Usage: import <review_json_path>")
            return

        path = Path(sys.argv[2])
        if not path.exists():
            print(f"File not found: {path}")
            return

        count = manager.import_from_review(path)
        print(f"Imported {count} corrections from {path}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
