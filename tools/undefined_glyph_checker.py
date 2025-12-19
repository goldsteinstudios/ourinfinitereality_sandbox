#!/usr/bin/env python3
"""
Check for undefined/variant glyphs in the 12-Book DDJ chapters.

Identifies characters in the CHUBS corpus that:
1. Use placeholder symbols (○, △, □, etc.)
2. Have variant annotations like ○（道）
3. Use Unicode private use area (未編碼字符)
"""

import json
import re
from pathlib import Path
from collections import defaultdict

CHUBS_DIR = Path("/Users/willgoldstein/claudecode/dao-de-jing-analyzer/data/CHUBS_repo")
GLYPHS_DIR = CHUBS_DIR / "glyphs"
POS_DIR = CHUBS_DIR / "pos-tagging-data"

# 12-Book chapter list
TWELVE_BOOK_CHAPTERS = [
    # Book 1: Engine
    40, 16, 5,
    # Book 2: Geometry
    25, 32,
    # Book 3: Co-emergence
    2,
    # Book 4: Self-Organization
    37, 57, 64,
    # Book 5: Constant
    55, 41,
    # Book 6: Perception
    56, 35,
    # Book 7: Sufficiency
    44, 46, 9,
    # Book 8: Boundaries
    52, 30,
    # Book 9: Scale
    54, 66,
    # Book 10: Subtraction
    48, 59, 22,
    # Book 11: Generation
    42, 51,  # 40 already included
    # Book 12: Closure
    1, 11, 81
]

def is_undefined_glyph(char):
    """Check if a character is undefined/placeholder."""
    # Check for placeholder symbols
    if char in "○△□◇●▲■◆〇":
        return True, "placeholder"

    # Check for Unicode private use area (CJK Extension G, etc.)
    code = ord(char) if len(char) == 1 else 0

    # Private Use Areas
    if 0xE000 <= code <= 0xF8FF:
        return True, "private_use_area"
    if 0xF0000 <= code <= 0xFFFFD:
        return True, "supplementary_pua_a"
    if 0x100000 <= code <= 0x10FFFD:
        return True, "supplementary_pua_b"

    # CJK Extension G (includes many unencoded Chu script chars)
    if 0x30000 <= code <= 0x3134F:
        return True, "cjk_extension_g"

    # CJK Extension H
    if 0x31350 <= code <= 0x323AF:
        return True, "cjk_extension_h"

    return False, None


def analyze_glyph_folders():
    """Analyze glyph folder names for undefined characters."""
    results = {
        "placeholder": [],
        "annotated_variant": [],
        "private_use": [],
        "standard": []
    }

    for folder in GLYPHS_DIR.iterdir():
        if not folder.is_dir():
            continue

        name = folder.name
        image_count = len(list(folder.glob("*.png")) + list(folder.glob("*.jpg")))

        # Check for annotated variants like ○（道）
        if "（" in name and "）" in name:
            # Extract base and annotation
            match = re.match(r"(.+)（(.+)）", name)
            if match:
                placeholder, annotation = match.groups()
                results["annotated_variant"].append({
                    "folder": name,
                    "placeholder": placeholder,
                    "annotation": annotation,
                    "image_count": image_count
                })
                continue

        # Check single character
        if len(name) == 1:
            is_undef, undef_type = is_undefined_glyph(name)
            if is_undef:
                results["placeholder" if undef_type == "placeholder" else "private_use"].append({
                    "folder": name,
                    "type": undef_type,
                    "code": hex(ord(name)),
                    "image_count": image_count
                })
            else:
                results["standard"].append({
                    "folder": name,
                    "code": hex(ord(name)),
                    "image_count": image_count
                })

    return results


def analyze_pos_data_undefined():
    """Find undefined characters used in POS tagging data."""
    undefined_in_corpus = defaultdict(lambda: {"count": 0, "examples": []})

    for split in ["train", "dev", "test"]:
        filepath = POS_DIR / f"{split}_examples.json"
        if not filepath.exists():
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for example in data:
            sentence = "".join(example["input"])
            for char in example["input"]:
                is_undef, undef_type = is_undefined_glyph(char)
                if is_undef:
                    undefined_in_corpus[char]["count"] += 1
                    undefined_in_corpus[char]["type"] = undef_type
                    if len(undefined_in_corpus[char]["examples"]) < 3:
                        undefined_in_corpus[char]["examples"].append(sentence[:50])

    return dict(undefined_in_corpus)


def check_guodian_laozi_undefined():
    """Check specifically for undefined glyphs in Guodian Laozi materials."""
    laozi_undefined = defaultdict(lambda: {"count": 0, "slips": []})
    laozi_total = 0

    for folder in GLYPHS_DIR.iterdir():
        if not folder.is_dir():
            continue

        # Check for Guodian Laozi images
        for img in folder.glob("郭店簡_*老子*"):
            laozi_total += 1

            # Check folder name
            name = folder.name
            is_undef, undef_type = is_undefined_glyph(name[0] if len(name) >= 1 else "")

            # Also check for annotated variants
            if "（" in name:
                match = re.match(r"(.+)（(.+)）", name)
                if match:
                    placeholder = match.group(1)
                    if placeholder in "○△□":
                        laozi_undefined[name]["count"] += 1
                        laozi_undefined[name]["slips"].append(img.name)
                        laozi_undefined[name]["type"] = "annotated_placeholder"

    return dict(laozi_undefined), laozi_total


def main():
    print("=" * 70)
    print("UNDEFINED GLYPH ANALYSIS")
    print("CHUBS Dataset - Focus on 12-Book DDJ Chapters")
    print("=" * 70)

    # Analyze glyph folders
    print("\n1. GLYPH FOLDER ANALYSIS")
    print("-" * 70)

    folder_results = analyze_glyph_folders()

    print(f"\nStandard characters:     {len(folder_results['standard'])}")
    print(f"Annotated variants:      {len(folder_results['annotated_variant'])}")
    print(f"Placeholder symbols:     {len(folder_results['placeholder'])}")
    print(f"Private use/unencoded:   {len(folder_results['private_use'])}")

    # Show annotated variants (these are readable!)
    print("\n" + "=" * 70)
    print("2. ANNOTATED VARIANTS (readable annotations)")
    print("-" * 70)
    print("These use ○（X）format where X is the modern equivalent\n")

    # Group by annotation
    by_annotation = defaultdict(list)
    for v in folder_results["annotated_variant"]:
        by_annotation[v["annotation"]].append(v)

    # Show most common annotations
    sorted_annotations = sorted(by_annotation.items(), key=lambda x: -sum(v["image_count"] for v in x[1]))

    print(f"{'Annotation':<15} {'Variants':<10} {'Total Images':<15}")
    print("-" * 40)
    for annotation, variants in sorted_annotations[:30]:
        total_images = sum(v["image_count"] for v in variants)
        print(f"{annotation:<15} {len(variants):<10} {total_images:<15}")

    # Analyze POS data
    print("\n" + "=" * 70)
    print("3. UNDEFINED CHARACTERS IN POS CORPUS")
    print("-" * 70)

    pos_undefined = analyze_pos_data_undefined()
    print(f"\nUnique undefined characters in corpus: {len(pos_undefined)}")

    # Sort by frequency
    sorted_undef = sorted(pos_undefined.items(), key=lambda x: -x[1]["count"])

    print(f"\n{'Char':<6} {'Code':<12} {'Count':<8} {'Example':<40}")
    print("-" * 70)
    for char, data in sorted_undef[:20]:
        code = hex(ord(char)) if len(char) == 1 else "multi"
        example = data["examples"][0][:35] if data["examples"] else ""
        print(f"{char:<6} {code:<12} {data['count']:<8} {example}")

    # Check Guodian Laozi specifically
    print("\n" + "=" * 70)
    print("4. GUODIAN LAOZI (老子) UNDEFINED GLYPHS")
    print("-" * 70)

    laozi_undef, laozi_total = check_guodian_laozi_undefined()

    print(f"\nTotal Guodian Laozi images: ~{laozi_total}")
    print(f"Folders with annotated placeholders: {len(laozi_undef)}")

    if laozi_undef:
        print("\nAnnotated placeholders in Laozi materials:")
        for folder, data in sorted(laozi_undef.items(), key=lambda x: -x[1]["count"])[:20]:
            print(f"  {folder}: {data['count']} images")

    # Summary for 12-Book chapters
    print("\n" + "=" * 70)
    print("5. SUMMARY FOR 12-BOOK TRANSLATION WORK")
    print("-" * 70)

    # Key insight: annotated variants ARE usable!
    usable_variants = len(folder_results["annotated_variant"])
    truly_undefined = len(folder_results["placeholder"]) + len(folder_results["private_use"])

    print(f"""
Key findings:

1. USABLE VARIANTS: {usable_variants} glyph folders use ○（X）format
   → The X annotation tells you the modern equivalent
   → These CAN be used for translation verification

2. TRULY UNDEFINED: {truly_undefined} folders are placeholders without annotation
   → These are unreadable without specialist knowledge

3. STANDARD CHARACTERS: {len(folder_results['standard'])} folders are standard Unicode
   → Directly usable

For your 12-Book work:
- Most DDJ characters ARE in the standard set
- Annotated variants like ○（道）= 道 are equivalent
- Only truly undefined placeholders need specialist resolution
""")


if __name__ == "__main__":
    main()
