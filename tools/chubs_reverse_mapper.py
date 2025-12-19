"""
CHUBS Reverse Mapper: Extract character assignments from CHUBS glyph folders.

For each Guodian Laozi A glyph file, determines:
1. guodian_char: The actual form on the bamboo slip
2. received_char: The standard/received text equivalent
3. confidence: How certain the identification is

Uses CHUBS folder naming convention:
- Simple: "道" = character is 道
- Variant: "返（反）" = actual form is 返, standard meaning is 反
- Undefined: "○（難）" = unidentified glyph, likely means 難
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class ChubsReverseMapper:
    """Extract character assignments from CHUBS folder structure."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.chubs_glyphs = self.project_root / "data" / "CHUBS_repo" / "glyphs"
        self.laozi_glyphs = self.project_root / "data" / "ddj" / "Guodian Strip Glyphs"
        self.mappings_path = self.project_root / "data" / "CHUBS_repo" / "twelve_book_glyph_mappings.json"

        self._mappings = None
        self._glyph_index = None

    @property
    def mappings(self) -> Dict:
        """Load CHUBS character mappings."""
        if self._mappings is None:
            if self.mappings_path.exists():
                with open(self.mappings_path, encoding='utf-8') as f:
                    self._mappings = json.load(f)
            else:
                self._mappings = {}
        return self._mappings

    def parse_folder_name(self, folder_name: str) -> Tuple[str, str]:
        """
        Parse CHUBS folder name to extract actual and standard characters.

        Examples:
            "道" → ("道", "道")
            "返（反）" → ("返", "反")
            "○（難）" → ("○", "難")
            "亓（其）" → ("亓", "其")

        Returns:
            (actual_form, standard_char)
        """
        # Check for variant pattern: X（Y）
        match = re.match(r'^(.+?)（(.+?)）$', folder_name)
        if match:
            actual = match.group(1)
            standard = match.group(2)
            return (actual, standard)

        # Simple case: character is both actual and standard
        return (folder_name, folder_name)

    def build_glyph_index(self) -> Dict[str, Dict]:
        """
        Build index mapping each Laozi A glyph filename to its character assignment.

        Returns:
            {
                "郭店簡_01A-老子甲_37_01A-37-05.png": {
                    "slip": 37,
                    "position": 5,
                    "guodian_char": "返",
                    "received_char": "反",
                    "folder": "返（反）",
                    "is_variant": True,
                    "is_undefined": False,
                    "confidence": "high"
                }
            }
        """
        if self._glyph_index is not None:
            return self._glyph_index

        self._glyph_index = {}

        # Track files found in multiple folders (ambiguous)
        file_assignments = defaultdict(list)

        # Scan all CHUBS glyph folders
        for folder in self.chubs_glyphs.iterdir():
            if not folder.is_dir():
                continue

            folder_name = folder.name
            actual_char, standard_char = self.parse_folder_name(folder_name)

            # Find all Laozi A images in this folder
            for img in folder.glob("*.png"):
                if "老子甲" not in img.name:
                    continue

                # Parse slip and position from filename
                # Pattern: 郭店簡_01A-老子甲_37_01A-37-05.png
                match = re.search(r'老子甲_(\d+)_01A-\d+-(\d+)', img.name)
                if not match:
                    continue

                slip = int(match.group(1))
                position = int(match.group(2))

                file_assignments[img.name].append({
                    "slip": slip,
                    "position": position,
                    "guodian_char": actual_char,
                    "received_char": standard_char,
                    "folder": folder_name,
                    "is_variant": actual_char != standard_char,
                    "is_undefined": actual_char == "○",
                    "path": str(img)
                })

        # Resolve assignments (prefer non-ambiguous)
        for filename, assignments in file_assignments.items():
            if len(assignments) == 1:
                entry = assignments[0]
                entry["confidence"] = "high"
                entry["ambiguous"] = False
            else:
                # Multiple assignments - flag as ambiguous
                # Use first non-undefined assignment if available
                non_undefined = [a for a in assignments if not a["is_undefined"]]
                if non_undefined:
                    entry = non_undefined[0]
                else:
                    entry = assignments[0]
                entry["confidence"] = "low"
                entry["ambiguous"] = True
                entry["other_assignments"] = [a["folder"] for a in assignments if a["folder"] != entry["folder"]]

            self._glyph_index[filename] = entry

        return self._glyph_index

    def get_slip_transcription(self, slip_num: int) -> List[Dict]:
        """
        Get position-ordered character sequence for a slip.

        Returns list of glyph entries sorted by position.
        """
        index = self.build_glyph_index()

        slip_glyphs = [
            entry for entry in index.values()
            if entry["slip"] == slip_num
        ]

        return sorted(slip_glyphs, key=lambda x: x["position"])

    def get_coverage_stats(self) -> Dict:
        """Calculate coverage statistics."""
        index = self.build_glyph_index()

        # Count all Laozi A glyphs in our folder
        laozi_files = list(self.laozi_glyphs.glob("*.png"))

        total = len(laozi_files)
        identified = len(index)
        undefined = sum(1 for e in index.values() if e["is_undefined"])
        variants = sum(1 for e in index.values() if e["is_variant"] and not e["is_undefined"])
        ambiguous = sum(1 for e in index.values() if e.get("ambiguous", False))

        # Find files not in CHUBS
        indexed_files = set(index.keys())
        laozi_filenames = set(f.name for f in laozi_files)
        missing = laozi_filenames - indexed_files

        return {
            "total_laozi_glyphs": total,
            "identified_by_chubs": identified,
            "undefined_placeholder": undefined,
            "variant_forms": variants,
            "ambiguous": ambiguous,
            "missing_from_chubs": len(missing),
            "coverage_pct": 100 * identified / total if total > 0 else 0,
            "missing_files": sorted(missing)[:20]  # First 20
        }

    def export_index(self, output_path: Optional[Path] = None) -> Path:
        """Export glyph index to JSON file."""
        if output_path is None:
            output_path = self.project_root / "data" / "ddj" / "chubs_glyph_index.json"

        index = self.build_glyph_index()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        return output_path

    def validate_against_chapter_40(self) -> Dict:
        """
        Validate against known Chapter 40 transcription.

        Chapter 40 (slip 37) verified transcription:
        - Guodian: 返也者道僮也溺也者道之甬也天下之勿生於又生於亡
        - Received: 反者道之動弱者道之用天下萬物生於有有生於無
        """
        expected = {
            5: ("返", "反"),
            6: ("也", "也"),
            7: ("者", "者"),
            8: ("道", "道"),
            9: ("僮", "動"),
            10: ("也", "也"),
            11: ("溺", "弱"),
            12: ("也", "也"),
            13: ("者", "者"),
            14: ("道", "道"),
            15: ("之", "之"),
            16: ("甬", "用"),
            17: ("也", "也"),
            18: ("天", "天"),
            19: ("下", "下"),
            20: ("之", "萬"),  # Note: 之 used for 萬 in position 20
            21: ("勿", "物"),
            22: ("生", "生"),
            23: ("於", "於"),
            24: ("又", "有"),
            25: ("生", "有"),  # Note: 生 vs second 有
            26: ("於", "於"),
            27: ("亡", "無"),
        }

        slip_37 = self.get_slip_transcription(37)

        results = {
            "correct": [],
            "wrong": [],
            "missing": [],
            "extra": []
        }

        found_positions = {g["position"] for g in slip_37}

        for pos, (exp_guo, exp_rec) in expected.items():
            matches = [g for g in slip_37 if g["position"] == pos]
            if not matches:
                results["missing"].append({
                    "position": pos,
                    "expected_guodian": exp_guo,
                    "expected_received": exp_rec
                })
            else:
                g = matches[0]
                if g["guodian_char"] == exp_guo:
                    results["correct"].append({
                        "position": pos,
                        "char": exp_guo,
                        "received_match": g["received_char"] == exp_rec
                    })
                else:
                    results["wrong"].append({
                        "position": pos,
                        "expected": exp_guo,
                        "got": g["guodian_char"]
                    })

        # Check for extra positions
        for pos in found_positions:
            if pos not in expected:
                g = [x for x in slip_37 if x["position"] == pos][0]
                results["extra"].append({
                    "position": pos,
                    "char": g["guodian_char"]
                })

        results["accuracy"] = len(results["correct"]) / len(expected) if expected else 0
        return results


def main():
    """Run reverse mapper and export index."""
    mapper = ChubsReverseMapper()

    print("=" * 60)
    print("CHUBS REVERSE MAPPER")
    print("=" * 60)

    # Build index
    print("\nBuilding glyph index...")
    index = mapper.build_glyph_index()
    print(f"Indexed {len(index)} glyph files")

    # Coverage stats
    print("\n" + "-" * 40)
    print("COVERAGE STATISTICS")
    print("-" * 40)
    stats = mapper.get_coverage_stats()
    print(f"Total Laozi A glyphs: {stats['total_laozi_glyphs']}")
    print(f"Identified by CHUBS: {stats['identified_by_chubs']} ({stats['coverage_pct']:.1f}%)")
    print(f"  - Variant forms: {stats['variant_forms']}")
    print(f"  - Undefined (○): {stats['undefined_placeholder']}")
    print(f"  - Ambiguous: {stats['ambiguous']}")
    print(f"Missing from CHUBS: {stats['missing_from_chubs']}")

    if stats['missing_files']:
        print(f"\nFirst missing files:")
        for f in stats['missing_files'][:5]:
            print(f"  {f}")

    # Validate against Chapter 40
    print("\n" + "-" * 40)
    print("CHAPTER 40 VALIDATION (Slip 37)")
    print("-" * 40)
    validation = mapper.validate_against_chapter_40()
    print(f"Accuracy: {validation['accuracy']:.1%}")
    print(f"Correct: {len(validation['correct'])}")
    print(f"Wrong: {len(validation['wrong'])}")
    print(f"Missing: {len(validation['missing'])}")

    if validation['wrong']:
        print("\nWrong identifications:")
        for w in validation['wrong']:
            print(f"  Position {w['position']}: expected {w['expected']}, got {w['got']}")

    if validation['missing']:
        print("\nMissing positions:")
        for m in validation['missing']:
            print(f"  Position {m['position']}: {m['expected_guodian']}")

    # Export
    print("\n" + "-" * 40)
    output = mapper.export_index()
    print(f"Exported index to: {output}")

    # Show sample entries
    print("\nSample entries from slip 37:")
    slip_37 = mapper.get_slip_transcription(37)
    for g in slip_37[:5]:
        variant = f" (variant of {g['received_char']})" if g['is_variant'] else ""
        print(f"  Pos {g['position']}: {g['guodian_char']}{variant}")


if __name__ == "__main__":
    main()
