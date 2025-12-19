#!/usr/bin/env python3
"""
Migrate validated_characters.json to Living Glossary format.

This script converts the existing validated_characters.json to the new
glossary format with full schema support, including:
- Individual JSON files per character
- Dual-hypothesis radical decomposition
- History tracking
- CHUBS validation placeholders
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from python_analysis.glossary.manager import GlossaryManager


def parse_structure(structure: str) -> dict:
    """
    Parse structure string like "禾(grain) + 刀(knife) = paths cut through distributed resource"
    into component list.
    """
    if not structure:
        return {"components": []}

    components = []

    # Split on ' + ' or ' = '
    if ' = ' in structure:
        parts_section = structure.split(' = ')[0]
    else:
        parts_section = structure

    parts = parts_section.split(' + ')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Parse "禾(grain)" format
        if '(' in part and ')' in part:
            char_part = part.split('(')[0].strip()
            meaning = part.split('(')[1].rstrip(')').strip()
            components.append({
                "component": char_part,
                "meaning": meaning,
                "position": "unknown"
            })
        else:
            components.append({
                "component": part,
                "meaning": "",
                "position": "unknown"
            })

    return {"components": components}


def determine_tier(character: str) -> int:
    """Determine tier level for a character."""
    tier_1 = ["道", "德", "自", "反", "弱", "者"]
    tier_2 = ["水", "川", "田", "井", "禾", "米", "用", "動", "強", "柔"]

    if character in tier_1:
        return 1
    elif character in tier_2:
        return 2
    else:
        return 3


def create_entry(character: str, data: dict) -> dict:
    """Create a full glossary entry from legacy data."""
    now = datetime.utcnow().isoformat() + "Z"

    # Parse structure into components
    structure_data = parse_structure(data.get("structure", ""))

    entry = {
        "character": character,
        "unicode": f"U+{ord(character):04X}",
        "pinyin": "",  # Will need to be added manually or from another source

        "current_translation": {
            "primary": data.get("geometric", "").split(',')[0].strip() if data.get("geometric") else "",
            "structural": data.get("geometric", ""),
            "traditional": data.get("traditional", ""),
            "notes": data.get("note", "")
        },

        "confidence": "provisional",
        "confidence_score": 0.5,

        "radical_decomposition": {
            "standard": structure_data,
            "agricultural": {"components": []},  # To be filled during analysis
            "preferred": None,
            "preference_rationale": "Pending Tier 1 analysis" if determine_tier(character) == 1 else None
        },

        "character_evolution": {
            "oracle_bone": {"attested": None, "image_refs": [], "analysis": None},
            "bronze": {"attested": None, "image_refs": [], "analysis": None},
            "chu": {"attested": None, "image_refs": [], "analysis": None},
            "seal": {"attested": None, "image_refs": [], "analysis": None}
        },

        "agricultural_hypothesis": {
            "claim": None,
            "predictions": [],
            "falsification_threshold": None
        },

        "counter_evidence": [],

        "chubs_validation": None,

        "guodian_attestation": None,

        "font_data": {
            "traced": False,
            "vector_path": None,
            "source_images": [],
            "extracted_features": None,
            "tracing_metadata": None
        },

        "semantic_field": None,
        "pictographic_analysis": None,
        "exemplar_provenance": None,

        "cross_references": {
            "related_characters": [],
            "ddj_chapters": [],
            "lexicon_category": None,
            "rsm_mapping": None
        },

        "history": [
            {
                "date": now,
                "field": "created",
                "from": None,
                "to": "migrated_from_validated_characters.json",
                "rationale": f"Migration from legacy format. Original validation: {data.get('validation', 'unknown')}",
                "author": "migration_script"
            }
        ],

        "created": now,
        "modified": now
    }

    # Add radical family to cross-references
    radical_family = data.get("radical_family", "")
    if radical_family:
        entry["cross_references"]["lexicon_category"] = "substrate"  # Default, may need adjustment

    return entry


def migrate():
    """Run the migration."""
    # Paths
    source_path = project_root / "translations" / "analysis" / "validated_characters.json"
    gm = GlossaryManager()

    print(f"Migrating from: {source_path}")
    print(f"Migrating to: {gm.entries_dir}")

    # Load source data
    with open(source_path, encoding='utf-8') as f:
        source_data = json.load(f)

    print(f"Found {len(source_data)} characters to migrate")

    # Track results
    created = 0
    skipped = 0
    errors = []

    for character, data in source_data.items():
        try:
            if gm.exists(character):
                print(f"  Skipping {character} - already exists")
                skipped += 1
                continue

            entry = create_entry(character, data)
            gm.create(entry, author="migration_script")
            print(f"  Created {character}")
            created += 1

        except Exception as e:
            print(f"  ERROR on {character}: {e}")
            errors.append((character, str(e)))

    print(f"\nMigration complete:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for char, err in errors:
            print(f"  {char}: {err}")

    # Save combined glossary
    combined_path = gm.save_combined()
    print(f"\nCombined glossary saved to: {combined_path}")


if __name__ == "__main__":
    migrate()
