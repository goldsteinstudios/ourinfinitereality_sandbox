#!/usr/bin/env python3
"""
CHUBS Glyph Mapper for 12-Book DDJ Project

Maps key characters from the 12-Book RSM structure to available
Guodian bamboo slip glyph images in the CHUBS dataset.

Output: Character inventory with glyph counts and source manuscripts.
"""

import os
import json
from collections import defaultdict
from pathlib import Path

# Base paths
# CHUBS dataset cloned from: https://huggingface.co/datasets/chen-yingfa/CHUBS
# Source: THUNLP (Tsinghua University NLP Lab)
# License: Apache 2.0
CHUBS_DIR = Path("/Users/willgoldstein/claudecode/dao-de-jing-analyzer/data/CHUBS_repo")
GLYPHS_DIR = CHUBS_DIR / "glyphs"
POS_DIR = CHUBS_DIR / "pos-tagging-data"

# 12-Book key characters from RSM ordering
TWELVE_BOOKS = {
    1: {
        "title": "The Engine",
        "chapters": [40, 16, 5],
        "theme": "Oscillation and Yielding Mechanics",
        "key_characters": ["反", "弱", "動", "用", "復", "歸", "根", "虛", "屈", "出",
                          "道", "之", "者", "天", "下", "萬", "物", "生", "於", "有", "無",
                          "致", "極", "守", "靜", "篤", "並", "作", "吾", "觀", "芸", "各",
                          "曰", "命", "常", "明", "妄", "凶", "容", "乃", "公", "王", "久",
                          "沒", "身", "殆", "地", "仁", "以", "為", "芻", "狗", "聖", "人",
                          "百", "姓", "間", "其", "猶", "橐", "籥", "乎", "而", "愈", "多",
                          "言", "數", "窮", "如", "中"]
    },
    2: {
        "title": "The Geometry",
        "chapters": [25, 32],
        "theme": "Sphere Proof and Uncarved Block",
        "key_characters": ["混", "成", "大", "潰", "遠", "法", "自", "然", "樸", "止",
                          "谷", "先", "寂", "寥", "獨", "改", "母", "字", "強", "國", "居",
                          "恆", "微", "臣", "賓", "會", "露", "甘", "均", "制", "譬", "江", "海"]
    },
    3: {
        "title": "Co-emergence",
        "chapters": [2],
        "theme": "The Mechanics of Distinction",
        "key_characters": ["美", "惡", "善", "相", "難", "易", "長", "短", "形", "盈",
                          "音", "聲", "和", "後", "隨", "事", "教", "始", "恃", "功", "去",
                          "皆", "已"]
    },
    4: {
        "title": "Self-Organization",
        "chapters": [37, 57, 64],
        "theme": "The 無為 Operational Definition",
        "key_characters": ["化", "欲", "鎮", "定", "正", "富", "輔", "敢", "執", "敗",
                          "慎", "累", "仞", "忌", "諱"]
    },
    5: {
        "title": "The Constant",
        "chapters": [55, 41],
        "theme": "Epistemological Cascade and Frame Operator",
        "key_characters": ["含", "厚", "赤", "骨", "筋", "柔", "握", "固", "益", "祥",
                          "氣", "壯", "老", "士", "聞", "若", "笑", "昧", "進", "退", "辱",
                          "偷", "隅", "器", "象"]
    },
    6: {
        "title": "Perception",
        "chapters": [56, 35],
        "theme": "The Six Operations and Imperceptibility",
        "key_characters": ["知", "塞", "兌", "閉", "門", "挫", "銳", "解", "紛", "光",
                          "塵", "玄", "同", "親", "疏", "貴", "賤", "往", "害", "安", "平",
                          "樂", "餌", "過", "淡", "味", "視", "既"]
    },
    7: {
        "title": "Sufficiency",
        "chapters": [44, 46, 9],
        "theme": "The Two Knowings",
        "key_characters": ["名", "貨", "得", "亡", "病", "甚", "費", "藏", "足", "卻",
                          "走", "馬", "糞", "戎", "郊", "罪", "禍", "憯", "持", "已", "揣",
                          "保", "金", "玉", "滿", "堂", "驕", "遺", "遂"]
    },
    8: {
        "title": "Boundaries",
        "chapters": [52, 30],
        "theme": "Mother Recursion and Completion Protocol",
        "key_characters": ["子", "勤", "啓", "濟", "救", "小", "殃", "習", "佐", "兵",
                          "還", "師", "荊", "棘", "果", "伐", "矜"]
    },
    9: {
        "title": "Scale",
        "chapters": [54, 66],
        "theme": "Scale-Invariant Cultivation",
        "key_characters": ["修", "德", "真", "鄉", "邦", "博", "建", "拔", "抱", "脫",
                          "孫", "祭", "祀", "輟", "餘", "豐", "上", "民", "前", "推", "厭",
                          "爭", "莫"]
    },
    10: {
        "title": "Subtraction",
        "chapters": [48, 59, 22],
        "theme": "The Clearing Principle",
        "key_characters": ["損", "至", "嗇", "柢", "積", "曲", "全", "枉", "窪", "敝",
                          "惑", "式", "見", "是", "彰", "學", "取", "治", "備", "克", "深",
                          "少"]
    },
    11: {
        "title": "Generation",
        "chapters": [42, 51, 40],
        "theme": "The Dimensional Proof",
        "key_characters": ["一", "二", "三", "負", "陰", "陽", "沖", "孤", "寡", "畜",
                          "勢", "尊", "育", "亭", "毒", "養", "覆", "宰"]
    },
    12: {
        "title": "Closure",
        "chapters": [1, 11, 81],
        "theme": "Coordinate System, Void Examples, Self-Validation",
        "key_characters": ["可", "非", "妙", "徼", "兩", "出", "異", "謂", "又", "眾",
                          "十", "輻", "共", "轂", "當", "車", "埏", "埴", "鑿", "戶", "牖",
                          "室", "利", "信", "辯", "己", "與"]
    }
}


def scan_glyphs_directory():
    """Scan the glyphs directory and build character inventory."""
    inventory = {}

    if not GLYPHS_DIR.exists():
        print(f"ERROR: Glyphs directory not found: {GLYPHS_DIR}")
        return inventory

    for folder in GLYPHS_DIR.iterdir():
        if folder.is_dir():
            char_name = folder.name
            images = list(folder.glob("*.png")) + list(folder.glob("*.jpg"))

            # Parse source manuscripts from filenames
            sources = defaultdict(list)
            for img in images:
                # Format: 郭店簡_01A-老子甲_18_01A-18-10.png
                parts = img.stem.split("_")
                if len(parts) >= 2:
                    manuscript = parts[0]  # e.g., 郭店簡
                    if len(parts) >= 3:
                        text = parts[1]  # e.g., 01A-老子甲
                        sources[f"{manuscript}_{text}"].append(img.name)
                    else:
                        sources[manuscript].append(img.name)

            inventory[char_name] = {
                "count": len(images),
                "sources": dict(sources),
                "path": str(folder)
            }

    return inventory


def extract_base_character(folder_name):
    """Extract base character from folder name like ○（道）or 道."""
    # Handle annotated forms like ○（道）
    if "（" in folder_name and "）" in folder_name:
        start = folder_name.index("（") + 1
        end = folder_name.index("）")
        return folder_name[start:end]
    # Handle simple character names
    if len(folder_name) == 1:
        return folder_name
    return None


def map_books_to_glyphs(inventory):
    """Map 12-Book characters to available glyphs."""
    results = {}

    # Build reverse lookup: base_char -> [folder_names]
    char_to_folders = defaultdict(list)
    for folder_name in inventory.keys():
        base = extract_base_character(folder_name)
        if base:
            char_to_folders[base].append(folder_name)
        # Also add exact match
        if len(folder_name) == 1:
            char_to_folders[folder_name].append(folder_name)

    for book_num, book_data in TWELVE_BOOKS.items():
        book_result = {
            "title": book_data["title"],
            "chapters": book_data["chapters"],
            "theme": book_data["theme"],
            "characters": {}
        }

        for char in book_data["key_characters"]:
            folders = char_to_folders.get(char, [])

            if folders:
                # Aggregate all sources
                total_count = 0
                all_sources = {}
                glyph_paths = []

                for folder in folders:
                    if folder in inventory:
                        total_count += inventory[folder]["count"]
                        glyph_paths.append(inventory[folder]["path"])
                        for src, imgs in inventory[folder]["sources"].items():
                            if src not in all_sources:
                                all_sources[src] = []
                            all_sources[src].extend(imgs)

                book_result["characters"][char] = {
                    "found": True,
                    "glyph_count": total_count,
                    "folders": folders,
                    "paths": glyph_paths,
                    "sources": all_sources,
                    "guodian_laozi": any("老子" in src for src in all_sources.keys())
                }
            else:
                book_result["characters"][char] = {
                    "found": False,
                    "glyph_count": 0,
                    "folders": [],
                    "paths": [],
                    "sources": {},
                    "guodian_laozi": False
                }

        results[book_num] = book_result

    return results


def analyze_pos_data():
    """Analyze POS tagging data for key characters."""
    train_file = POS_DIR / "train_examples.json"

    if not train_file.exists():
        return {}

    with open(train_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    char_pos = defaultdict(lambda: defaultdict(int))

    for example in data:
        for char, label in zip(example["input"], example["label"]):
            if label != "O" and len(char) == 1:
                # Extract POS (remove B-/I- prefix)
                pos = label[2:] if label.startswith(("B-", "I-")) else label
                char_pos[char][pos] += 1

    return dict(char_pos)


def generate_report(book_results, pos_data):
    """Generate comprehensive report."""

    print("=" * 70)
    print("CHUBS GLYPH MAPPING REPORT")
    print("12-Book DDJ Key Characters → Guodian Bamboo Slip Images")
    print("=" * 70)

    total_chars = 0
    found_chars = 0
    guodian_laozi_chars = 0
    total_glyphs = 0

    for book_num in sorted(book_results.keys()):
        book = book_results[book_num]
        print(f"\n{'='*70}")
        print(f"BOOK {book_num}: {book['title']}")
        print(f"Chapters: {book['chapters']}")
        print(f"Theme: {book['theme']}")
        print("-" * 70)

        book_found = 0
        book_total = len(book["characters"])
        book_glyphs = 0
        book_laozi = 0

        # Group by found status
        found_list = []
        missing_list = []

        for char, data in book["characters"].items():
            total_chars += 1
            if data["found"]:
                found_chars += 1
                book_found += 1
                book_glyphs += data["glyph_count"]
                total_glyphs += data["glyph_count"]

                if data["guodian_laozi"]:
                    guodian_laozi_chars += 1
                    book_laozi += 1

                # Get POS info
                pos_info = ""
                if char in pos_data:
                    top_pos = sorted(pos_data[char].items(), key=lambda x: -x[1])[:2]
                    pos_info = ", ".join([f"{p}({c})" for p, c in top_pos])

                laozi_marker = "★" if data["guodian_laozi"] else " "
                found_list.append((char, data["glyph_count"], laozi_marker, pos_info))
            else:
                missing_list.append(char)

        print(f"\nFOUND ({book_found}/{book_total}, {book_glyphs} total glyphs, {book_laozi} with Laozi images):")
        print("-" * 70)

        # Print in columns
        col_width = 35
        for i in range(0, len(found_list), 2):
            row = ""
            for j in range(2):
                if i + j < len(found_list):
                    char, count, laozi, pos = found_list[i + j]
                    entry = f"{laozi}{char}: {count:3d} glyphs"
                    if pos:
                        entry += f" [{pos[:20]}]"
                    row += entry.ljust(col_width)
            print(row)

        if missing_list:
            print(f"\nMISSING ({len(missing_list)}):")
            print(" ".join(missing_list))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total key characters across 12 books: {total_chars}")
    print(f"Characters with glyphs:               {found_chars} ({100*found_chars/total_chars:.1f}%)")
    print(f"Characters with Guodian Laozi images: {guodian_laozi_chars} ({100*guodian_laozi_chars/total_chars:.1f}%)")
    print(f"Total glyph images available:         {total_glyphs}")

    # Priority characters (high glyph count + Laozi source)
    print("\n" + "=" * 70)
    print("PRIORITY CHARACTERS FOR CALLIGRAPHY (Guodian Laozi source)")
    print("=" * 70)

    priority = []
    for book_num, book in book_results.items():
        for char, data in book["characters"].items():
            if data["guodian_laozi"] and data["glyph_count"] >= 3:
                priority.append((char, data["glyph_count"], book_num))

    priority.sort(key=lambda x: -x[1])

    print(f"\n{'Char':<6} {'Glyphs':<8} {'Book':<6}")
    print("-" * 25)
    for char, count, book in priority[:50]:
        print(f"{char:<6} {count:<8} {book:<6}")

    return {
        "total_chars": total_chars,
        "found_chars": found_chars,
        "guodian_laozi_chars": guodian_laozi_chars,
        "total_glyphs": total_glyphs
    }


def export_glyph_paths(book_results, output_file):
    """Export character -> glyph path mappings for use in other tools."""
    export_data = {}

    for book_num, book in book_results.items():
        for char, data in book["characters"].items():
            if data["found"] and char not in export_data:
                export_data[char] = {
                    "glyph_count": data["glyph_count"],
                    "paths": data["paths"],
                    "guodian_laozi": data["guodian_laozi"],
                    "sources": {k: len(v) for k, v in data["sources"].items()}
                }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"\nExported glyph mappings to: {output_file}")


def main():
    print("Scanning CHUBS glyphs directory...")
    inventory = scan_glyphs_directory()
    print(f"Found {len(inventory)} character folders")

    print("\nAnalyzing POS tagging data...")
    pos_data = analyze_pos_data()
    print(f"Found POS data for {len(pos_data)} characters")

    print("\nMapping 12-Book characters to glyphs...")
    book_results = map_books_to_glyphs(inventory)

    # Generate report
    stats = generate_report(book_results, pos_data)

    # Export mappings
    output_file = CHUBS_DIR / "twelve_book_glyph_mappings.json"
    export_glyph_paths(book_results, output_file)

    return book_results, stats


if __name__ == "__main__":
    main()
