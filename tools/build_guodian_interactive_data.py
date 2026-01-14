"""
Build Guodian Bundle A Interactive Data

Combines data from multiple sources to create a comprehensive
character-by-character dataset for the interactive web display.

Sources:
- guodian_bundle_a_data.csv: Slip-level data with pinyin
- radicals.yaml: Radical decomposition
- verified_transcriptions.json: Character positions on slips
- glossary entries: Character-level details
"""

import json
import csv
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent


def load_radicals_yaml() -> Dict:
    """Load radical decomposition data."""
    yaml_path = PROJECT_ROOT / "data" / "ddj" / "radicals.yaml"
    if not yaml_path.exists():
        return {}
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_verified_transcriptions() -> Dict:
    """Load verified transcriptions with position data."""
    json_path = PROJECT_ROOT / "data" / "ddj" / "verified_transcriptions.json"
    if not json_path.exists():
        return {}
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def load_guodian_csv() -> List[Dict]:
    """Load the Guodian Bundle A CSV data."""
    csv_path = PROJECT_ROOT / "guodian_bundle_a_data.csv"
    if not csv_path.exists():
        return []
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_glossary_entries() -> Dict[str, Dict]:
    """Load all glossary JSON entries."""
    entries_dir = PROJECT_ROOT / "data" / "glossary" / "entries"
    if not entries_dir.exists():
        return {}

    entries = {}
    for json_file in entries_dir.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
            char = data.get("character")
            if char:
                entries[char] = data
    return entries


def build_radical_lookup(radicals_data: Dict) -> Dict[str, Dict]:
    """Build character -> radical decomposition lookup."""
    lookup = {}

    # Process substrates
    for substrate, data in radicals_data.get("substrates", {}).items():
        for char, char_data in data.get("characters", {}).items():
            lookup[char] = {
                "substrate": substrate,
                "substrate_meaning": data.get("meaning", ""),
                "operator": char_data.get("operator", ""),
                "meaning": char_data.get("meaning", ""),
                "breakdown": char_data.get("breakdown", ""),
                "pinyin": char_data.get("pinyin", ""),
            }

    return lookup


def build_pinyin_lookup(csv_data: List[Dict]) -> Dict[str, str]:
    """Build character -> pinyin lookup from CSV."""
    lookup = {}
    for row in csv_data:
        chinese = row.get("chinese", "")
        pinyin = row.get("pinyin", "")
        if chinese and pinyin:
            # Split into characters and pinyin syllables
            chars = list(chinese)
            pinyins = pinyin.split()
            # Match as best we can
            for i, char in enumerate(chars):
                if char not in lookup and i < len(pinyins):
                    lookup[char] = pinyins[i]
    return lookup


def build_slip_data(
    transcriptions: Dict,
    radical_lookup: Dict,
    pinyin_lookup: Dict,
    glossary: Dict
) -> Dict[int, List[Dict]]:
    """Build slip-by-slip character data."""
    slips = {}

    for chapter_str, chapter_data in transcriptions.items():
        positions = chapter_data.get("positions", {})

        for pos_key, (guo_char, rec_char) in positions.items():
            # Parse position key: "37_5" -> slip 37, position 5
            parts = pos_key.split("_")
            if len(parts) != 2:
                continue

            slip_num = int(parts[0])
            position = int(parts[1])

            if slip_num not in slips:
                slips[slip_num] = []

            # Get character info
            char = guo_char if guo_char and guo_char != "○" else rec_char
            display_char = char if char else "□"

            # Get pinyin
            pinyin = ""
            if char:
                pinyin = pinyin_lookup.get(char, "")
                # Also check glossary
                if not pinyin and char in glossary:
                    p = glossary[char].get("pinyin", "")
                    if p:
                        # Convert "dao4" to "dào" format if needed
                        pinyin = p

            # Get radicals
            radicals = radical_lookup.get(char, {})

            # Get glossary data
            gloss = glossary.get(char, {})
            decomposition = gloss.get("radical_decomposition", {}).get("standard", {}).get("components", [])

            char_data = {
                "position": position,
                "guodian": guo_char,
                "received": rec_char,
                "display": display_char,
                "pinyin": pinyin,
                "is_variant": guo_char != rec_char and guo_char and rec_char,
                "radicals": decomposition if decomposition else [],
                "substrate": radicals.get("substrate", ""),
                "operator": radicals.get("operator", ""),
                "meaning": radicals.get("meaning", ""),
                "breakdown": radicals.get("breakdown", ""),
            }

            slips[slip_num].append(char_data)

    # Sort each slip by position
    for slip_num in slips:
        slips[slip_num].sort(key=lambda x: x["position"])

    return slips


def add_common_pinyin() -> Dict[str, str]:
    """Common character pinyin not in other sources."""
    return {
        "道": "dào", "德": "dé", "之": "zhī", "也": "yě", "者": "zhě",
        "而": "ér", "不": "bù", "以": "yǐ", "為": "wéi", "其": "qí",
        "所": "suǒ", "於": "yú", "是": "shì", "則": "zé", "故": "gù",
        "有": "yǒu", "無": "wú", "萬": "wàn", "物": "wù", "生": "shēng",
        "天": "tiān", "下": "xià", "人": "rén", "民": "mín", "聖": "shèng",
        "大": "dà", "小": "xiǎo", "上": "shàng", "中": "zhōng", "長": "cháng",
        "知": "zhī", "善": "shàn", "名": "míng", "言": "yán", "行": "xíng",
        "事": "shì", "動": "dòng", "靜": "jìng", "強": "qiáng", "弱": "ruò",
        "柔": "róu", "剛": "gāng", "反": "fǎn", "返": "fǎn", "復": "fù",
        "用": "yòng", "功": "gōng", "成": "chéng", "敗": "bài", "始": "shǐ",
        "終": "zhōng", "難": "nán", "易": "yì", "高": "gāo", "和": "hé",
        "音": "yīn", "聲": "shēng", "先": "xiān", "後": "hòu", "相": "xiāng",
        "形": "xíng", "盈": "yíng", "虛": "xū", "實": "shí", "常": "cháng",
        "恆": "héng", "亡": "wáng", "又": "yòu", "古": "gǔ", "今": "jīn",
        "皆": "jiē", "此": "cǐ", "亓": "qí", "已": "yǐ", "居": "jū",
        "弗": "fú", "猶": "yóu", "墮": "suí", "城": "chéng", "型": "xíng",
        "浧": "yíng", "拃": "zuò", "志": "zhì", "僮": "dòng", "溺": "ruò",
        "甬": "yòng", "勿": "wù", "智": "zhì",
    }


def build_interactive_data() -> Dict:
    """Build the complete interactive dataset."""
    print("Loading data sources...")

    radicals = load_radicals_yaml()
    transcriptions = load_verified_transcriptions()
    csv_data = load_guodian_csv()
    glossary = load_glossary_entries()

    print(f"  Radicals: {len(radicals.get('substrates', {}))} substrate families")
    print(f"  Transcriptions: {len(transcriptions)} chapters")
    print(f"  CSV rows: {len(csv_data)}")
    print(f"  Glossary entries: {len(glossary)}")

    # Build lookups
    radical_lookup = build_radical_lookup(radicals)
    pinyin_lookup = build_pinyin_lookup(csv_data)

    # Add common pinyin
    common_pinyin = add_common_pinyin()
    for char, py in common_pinyin.items():
        if char not in pinyin_lookup:
            pinyin_lookup[char] = py

    print(f"  Radical lookup: {len(radical_lookup)} characters")
    print(f"  Pinyin lookup: {len(pinyin_lookup)} characters")

    # Build slip data
    slips = build_slip_data(transcriptions, radical_lookup, pinyin_lookup, glossary)

    print(f"\nBuilt data for {len(slips)} slips")

    # Generate output
    output = {
        "metadata": {
            "bundle": "A",
            "name": "Guodian Laozi A (老子甲)",
            "date": "~300 BCE",
            "slips": len(slips),
            "total_positions": sum(len(s) for s in slips.values()),
        },
        "slips": {}
    }

    # Add slip data with chapter info
    slip_chapters = {
        1: [19], 2: [46], 3: [66], 4: [66], 5: [66],
        6: [46, 30], 7: [30], 8: [15], 9: [15], 10: [15],
        11: [64], 12: [63], 13: [37], 14: [37], 15: [2],
        16: [2], 17: [2], 18: [32], 19: [32], 20: [32],
        21: [25], 22: [25], 23: [25, 5], 24: [16], 25: [64],
        26: [64], 27: [56], 28: [56], 29: [56, 57], 30: [57],
        31: [57], 32: [57], 33: [55], 34: [55], 35: [55, 44],
        36: [44], 37: [40], 38: [9], 39: [9],
    }

    for slip_num in sorted(slips.keys()):
        output["slips"][str(slip_num)] = {
            "slip": slip_num,
            "chapters": slip_chapters.get(slip_num, []),
            "characters": slips[slip_num]
        }

    return output


def main():
    """Build and save interactive data."""
    data = build_interactive_data()

    # Save to public directory for web access
    output_path = PROJECT_ROOT / "public" / "data" / "guodian_interactive.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to: {output_path}")
    print(f"Total characters: {data['metadata']['total_positions']}")

    # Also save to data directory
    data_path = PROJECT_ROOT / "data" / "ddj" / "guodian_interactive.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Also saved to: {data_path}")


if __name__ == "__main__":
    main()
