"""
Link Guodian Laozi A glyphs to Living Glossary entries.

Adds exemplar glyph paths and provenance data to glossary character entries.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional
from guodian_glyph_mapper import GuodianGlyphMapper


class GuodianGlossaryLinker:
    """Link Guodian glyphs to glossary entries."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.glossary_dir = self.project_root / "data" / "glossary" / "entries"
        self.mapper = GuodianGlyphMapper()

    def get_glossary_entry(self, character: str) -> Optional[Dict]:
        """Load glossary entry for a character."""
        unicode_val = f"U+{ord(character):04X}"
        entry_path = self.glossary_dir / f"{unicode_val}_{character}.json"

        if entry_path.exists():
            with open(entry_path, encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_glossary_entry(self, character: str, entry: Dict):
        """Save updated glossary entry."""
        unicode_val = f"U+{ord(character):04X}"
        entry_path = self.glossary_dir / f"{unicode_val}_{character}.json"

        entry["modified"] = datetime.now(timezone.utc).isoformat()

        with open(entry_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

    def link_chapter_glyphs(self, chapter_num: int) -> Dict[str, int]:
        """
        Link all glyphs from a chapter to their glossary entries.
        Returns count of linked characters.
        """
        mapping = self.mapper.generate_chapter_mapping(chapter_num)
        linked = 0
        skipped = 0

        if not mapping.get("verified"):
            print(f"Chapter {chapter_num} not verified - skipping detailed links")
            return {"linked": 0, "skipped": 0, "reason": "not_verified"}

        for glyph in mapping["glyphs"]:
            # Link to received character (the one we translate)
            rec_char = glyph.get("received_char")
            guo_char = glyph.get("guodian_char")

            if rec_char:
                if self._link_glyph_to_entry(
                    rec_char,
                    glyph["path"],
                    chapter_num,
                    glyph["slip"],
                    glyph["position"],
                    guo_char if guo_char != rec_char else None
                ):
                    linked += 1
                else:
                    skipped += 1

        return {"linked": linked, "skipped": skipped}

    def _link_glyph_to_entry(
        self,
        character: str,
        glyph_path: str,
        chapter: int,
        slip: int,
        position: int,
        loan_form: Optional[str] = None
    ) -> bool:
        """Add glyph link to a glossary entry."""
        entry = self.get_glossary_entry(character)

        if not entry:
            return False

        # Ensure font_data structure exists
        if not entry.get("font_data"):
            entry["font_data"] = {
                "traced": False,
                "vector_path": None,
                "source_images": [],
                "extracted_features": None,
                "tracing_metadata": None
            }

        if not entry["font_data"].get("source_images"):
            entry["font_data"]["source_images"] = []

        # Check if this glyph is already linked
        existing = [
            img for img in entry["font_data"]["source_images"]
            if img.get("path") == glyph_path
        ]
        if existing:
            return True  # Already linked

        # Add new glyph link
        glyph_entry = {
            "path": glyph_path,
            "source": "guodian_laozi_a",
            "slip": slip,
            "position": position,
            "chapter": chapter,
            "is_exemplar": True,
        }

        if loan_form:
            glyph_entry["loan_form"] = loan_form
            glyph_entry["note"] = f"Guodian writes {loan_form} for {character}"

        entry["font_data"]["source_images"].append(glyph_entry)

        # Update exemplar_provenance if this is the first/best example
        if not entry.get("exemplar_provenance") or entry["exemplar_provenance"].get("slip") is None:
            entry["exemplar_provenance"] = {
                "tomb": "Guodian Tomb 1",
                "slip_bundle": "A",
                "slip_number": str(slip),
                "position": position,
                "scribe_id": None
            }

        # Add history entry
        if not entry.get("history"):
            entry["history"] = []

        entry["history"].append({
            "date": datetime.now(timezone.utc).isoformat(),
            "field": "font_data.source_images",
            "from": None,
            "to": f"Added glyph from slip {slip} position {position}",
            "rationale": f"Linked Guodian Laozi A glyph (Chapter {chapter})",
            "author": "guodian_linker"
        })

        self.save_glossary_entry(character, entry)
        return True

    def link_all_verified_chapters(self) -> Dict:
        """Link glyphs from all verified chapters."""
        results = {}
        for chapter in self.mapper.verified_transcriptions.keys():
            result = self.link_chapter_glyphs(chapter)
            results[chapter] = result
            print(f"Chapter {chapter}: {result['linked']} linked, {result['skipped']} skipped")
        return results

    def update_chu_stage_in_glossary(self, character: str):
        """Update the character_evolution.chu field with glyph data."""
        entry = self.get_glossary_entry(character)
        if not entry:
            return False

        # Get glyphs for this character from mapper
        glossary_links = self.mapper.generate_glossary_links()
        char_glyphs = glossary_links.get(character, [])

        if not char_glyphs:
            return False

        # Ensure character_evolution.chu exists
        if not entry.get("character_evolution"):
            entry["character_evolution"] = {}
        if not entry["character_evolution"].get("chu"):
            entry["character_evolution"]["chu"] = {}

        chu = entry["character_evolution"]["chu"]
        chu["attested"] = True
        chu["image_refs"] = [g["path"] for g in char_glyphs]
        chu["analysis"] = f"Found in Guodian Laozi A, {len(char_glyphs)} instances"

        # Add history entry
        entry["history"].append({
            "date": datetime.now(timezone.utc).isoformat(),
            "field": "character_evolution.chu",
            "from": None,
            "to": f"Attested with {len(char_glyphs)} glyph instances",
            "rationale": "Linked from Guodian Laozi A glyph folder",
            "author": "guodian_linker"
        })

        self.save_glossary_entry(character, entry)
        return True


def main():
    linker = GuodianGlossaryLinker()

    print("=== Linking Guodian Glyphs to Glossary ===\n")

    # Link all verified chapters
    results = linker.link_all_verified_chapters()

    total_linked = sum(r.get("linked", 0) for r in results.values())
    print(f"\nTotal characters linked: {total_linked}")

    # Show what characters got linked
    print("\n=== Linked Characters ===")
    for chapter, result in results.items():
        if result.get("linked", 0) > 0:
            print(f"Chapter {chapter}: {result['linked']} character-glyph links added")


if __name__ == "__main__":
    main()
