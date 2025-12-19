#!/usr/bin/env python3
"""
Translation Verifier using CHUBS POS Data

Compares grammatical interpretations in translations against
empirical POS distributions from Chu bamboo slip corpus.

CHUBS dataset: https://huggingface.co/datasets/chen-yingfa/CHUBS
Source: THUNLP (Tsinghua University NLP Lab), Apache 2.0
"""

import json
from collections import defaultdict
from pathlib import Path

# Paths
CHUBS_DIR = Path("/Users/willgoldstein/claudecode/dao-de-jing-analyzer/data/CHUBS_repo")
POS_DIR = CHUBS_DIR / "pos-tagging-data"

# POS tag translations (Chinese -> English)
POS_LABELS = {
    "名词": "noun",
    "动词": "verb",
    "形容词": "adjective",
    "副词": "adverb",
    "代词": "pronoun",
    "介词": "preposition",
    "连词": "conjunction",
    "助词": "particle",
    "数量词": "numeral",
    "语气词": "modal particle",
}

def load_pos_data():
    """Load all POS tagging data from CHUBS."""
    char_pos = defaultdict(lambda: defaultdict(int))
    char_contexts = defaultdict(list)

    for split in ["train", "dev", "test"]:
        filepath = POS_DIR / f"{split}_examples.json"
        if not filepath.exists():
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for example in data:
            chars = example["input"]
            labels = example["label"]

            for i, (char, label) in enumerate(zip(chars, labels)):
                if label == "O" or len(char) != 1:
                    continue

                # Extract POS (remove B-/I- prefix)
                pos = label[2:] if label.startswith(("B-", "I-")) else label
                char_pos[char][pos] += 1

                # Store context (surrounding characters)
                context = {
                    "prev": chars[i-1] if i > 0 else None,
                    "next": chars[i+1] if i < len(chars)-1 else None,
                    "pos": pos,
                    "sentence": "".join(chars)
                }
                if len(char_contexts[char]) < 10:  # Limit examples
                    char_contexts[char].append(context)

    return dict(char_pos), dict(char_contexts)


def get_primary_pos(char_pos_data, char):
    """Get the most common POS for a character."""
    if char not in char_pos_data:
        return None, 0

    pos_counts = char_pos_data[char]
    total = sum(pos_counts.values())

    if total == 0:
        return None, 0

    primary = max(pos_counts.items(), key=lambda x: x[1])
    return primary[0], primary[1] / total


def analyze_character(char, char_pos_data, char_contexts, claimed_pos=None):
    """Analyze a single character's grammatical usage."""
    result = {
        "character": char,
        "found": char in char_pos_data,
        "claimed_pos": claimed_pos,
    }

    if not result["found"]:
        result["note"] = "Not found in CHUBS corpus"
        return result

    pos_counts = char_pos_data[char]
    total = sum(pos_counts.values())

    # Calculate distribution
    distribution = []
    for pos, count in sorted(pos_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        distribution.append({
            "pos": pos,
            "pos_english": POS_LABELS.get(pos, pos),
            "count": count,
            "percentage": round(pct, 1)
        })

    result["total_occurrences"] = total
    result["distribution"] = distribution
    result["primary_pos"] = distribution[0]["pos"] if distribution else None
    result["primary_pos_english"] = distribution[0]["pos_english"] if distribution else None

    # Check if claimed POS matches corpus
    if claimed_pos:
        # Map English to Chinese POS
        pos_mapping = {v: k for k, v in POS_LABELS.items()}
        claimed_chinese = pos_mapping.get(claimed_pos.lower(), claimed_pos)

        claimed_pct = 0
        for d in distribution:
            if d["pos"] == claimed_chinese or d["pos_english"].lower() == claimed_pos.lower():
                claimed_pct = d["percentage"]
                break

        result["claimed_percentage"] = claimed_pct
        if claimed_pct >= 50:
            result["verdict"] = "CONFIRMED"
        elif claimed_pct >= 20:
            result["verdict"] = "PLAUSIBLE"
        elif claimed_pct > 0:
            result["verdict"] = "MINORITY_USAGE"
        else:
            result["verdict"] = "NOT_ATTESTED"

    # Add example contexts
    if char in char_contexts:
        result["examples"] = char_contexts[char][:3]

    return result


def verify_translation_choices(translations, char_pos_data, char_contexts):
    """
    Verify a list of translation choices.

    translations: list of dicts with 'character' and 'interpreted_as' keys
    """
    results = []

    for t in translations:
        char = t["character"]
        claimed = t.get("interpreted_as")

        analysis = analyze_character(char, char_pos_data, char_contexts, claimed)
        analysis["translation_note"] = t.get("note", "")
        results.append(analysis)

    return results


def print_verification_report(results):
    """Print a formatted verification report."""
    print("=" * 70)
    print("TRANSLATION VERIFICATION REPORT")
    print("Based on CHUBS Chu Bamboo Slip POS Data")
    print("=" * 70)

    confirmed = []
    plausible = []
    minority = []
    not_attested = []
    not_found = []

    for r in results:
        if not r["found"]:
            not_found.append(r)
        elif "verdict" not in r:
            continue
        elif r["verdict"] == "CONFIRMED":
            confirmed.append(r)
        elif r["verdict"] == "PLAUSIBLE":
            plausible.append(r)
        elif r["verdict"] == "MINORITY_USAGE":
            minority.append(r)
        else:
            not_attested.append(r)

    def print_group(title, items, show_warning=False):
        if not items:
            return
        print(f"\n{'='*70}")
        print(f"{title} ({len(items)})")
        print("-" * 70)
        for r in items:
            char = r["character"]
            claimed = r.get("claimed_pos", "?")
            primary = r.get("primary_pos_english", "?")
            pct = r.get("claimed_percentage", 0)
            total = r.get("total_occurrences", 0)

            if show_warning:
                print(f"  {char}: claimed '{claimed}' but corpus shows:")
                for d in r.get("distribution", [])[:3]:
                    print(f"      {d['pos_english']}: {d['percentage']}%")
            else:
                print(f"  {char}: '{claimed}' = {pct}% of {total} occurrences (primary: {primary})")

    print_group("✓ CONFIRMED (>50% corpus support)", confirmed)
    print_group("~ PLAUSIBLE (20-50% corpus support)", plausible)
    print_group("? MINORITY USAGE (<20% but attested)", minority, show_warning=True)
    print_group("✗ NOT ATTESTED IN CORPUS", not_attested, show_warning=True)
    print_group("— NOT FOUND IN CHUBS", not_found)

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print("-" * 70)
    total = len(results)
    print(f"  Total characters checked: {total}")
    print(f"  Confirmed:     {len(confirmed):3d} ({100*len(confirmed)/total:.1f}%)")
    print(f"  Plausible:     {len(plausible):3d} ({100*len(plausible)/total:.1f}%)")
    print(f"  Minority:      {len(minority):3d} ({100*len(minority)/total:.1f}%)")
    print(f"  Not attested:  {len(not_attested):3d} ({100*len(not_attested)/total:.1f}%)")
    print(f"  Not in corpus: {len(not_found):3d} ({100*len(not_found)/total:.1f}%)")


# ============================================================
# DDJ TRANSLATION VERIFICATION
# ============================================================

# Key interpretive choices from the 12-Book translations
DDJ_INTERPRETATIONS = [
    # Book 1: The Engine (Ch. 40, 16, 5)
    {"character": "反", "interpreted_as": "verb", "note": "reversal as movement"},
    {"character": "弱", "interpreted_as": "adjective", "note": "yielding as function"},
    {"character": "動", "interpreted_as": "noun", "note": "movement of dao"},
    {"character": "用", "interpreted_as": "noun", "note": "function of dao"},
    {"character": "復", "interpreted_as": "verb", "note": "return/cycle back"},
    {"character": "歸", "interpreted_as": "verb", "note": "return home"},
    {"character": "根", "interpreted_as": "noun", "note": "root"},
    {"character": "虛", "interpreted_as": "noun", "note": "emptiness/void"},
    {"character": "屈", "interpreted_as": "verb", "note": "compressed/bent"},
    {"character": "出", "interpreted_as": "verb", "note": "emerge"},

    # Book 2: The Geometry (Ch. 25, 32)
    {"character": "混", "interpreted_as": "adjective", "note": "undifferentiated"},
    {"character": "成", "interpreted_as": "verb", "note": "complete/achieve"},
    {"character": "大", "interpreted_as": "adjective", "note": "great/unbounded"},
    {"character": "潰", "interpreted_as": "verb", "note": "overflow (Guodian variant)"},
    {"character": "遠", "interpreted_as": "adjective", "note": "far/extended"},
    {"character": "法", "interpreted_as": "verb", "note": "model/pattern after"},
    {"character": "自", "interpreted_as": "pronoun", "note": "self"},
    {"character": "然", "interpreted_as": "particle", "note": "so/thus (-ness suffix)"},
    {"character": "樸", "interpreted_as": "noun", "note": "uncarved block"},
    {"character": "止", "interpreted_as": "verb", "note": "stop"},

    # Book 3: Co-emergence (Ch. 2)
    {"character": "美", "interpreted_as": "noun", "note": "beauty"},
    {"character": "惡", "interpreted_as": "noun", "note": "ugliness"},
    {"character": "善", "interpreted_as": "noun", "note": "good/skill"},
    {"character": "相", "interpreted_as": "adverb", "note": "mutually"},
    {"character": "生", "interpreted_as": "verb", "note": "co-emerge/arise"},
    {"character": "形", "interpreted_as": "verb", "note": "shape each other"},
    {"character": "盈", "interpreted_as": "verb", "note": "fill each other"},
    {"character": "和", "interpreted_as": "verb", "note": "harmonize"},
    {"character": "隨", "interpreted_as": "verb", "note": "follow"},

    # Book 4: Self-Organization (Ch. 37, 57, 64)
    {"character": "化", "interpreted_as": "verb", "note": "transform"},
    {"character": "欲", "interpreted_as": "noun", "note": "desire"},
    {"character": "定", "interpreted_as": "verb", "note": "stabilize"},
    {"character": "正", "interpreted_as": "verb", "note": "correct/align"},
    {"character": "輔", "interpreted_as": "verb", "note": "assist"},
    {"character": "敢", "interpreted_as": "verb", "note": "dare"},
    {"character": "執", "interpreted_as": "verb", "note": "grasp/hold"},

    # Book 5: The Constant (Ch. 55, 41)
    {"character": "常", "interpreted_as": "noun", "note": "the constant"},
    {"character": "明", "interpreted_as": "noun", "note": "clarity/illumination"},
    {"character": "若", "interpreted_as": "verb", "note": "appears as (frame operator)"},
    {"character": "笑", "interpreted_as": "verb", "note": "laugh at"},
    {"character": "士", "interpreted_as": "noun", "note": "practitioner/scholar"},
    {"character": "聞", "interpreted_as": "verb", "note": "hear/encounter"},

    # Book 6: Perception (Ch. 56, 35)
    {"character": "知", "interpreted_as": "verb", "note": "know"},
    {"character": "言", "interpreted_as": "verb", "note": "speak"},
    {"character": "塞", "interpreted_as": "verb", "note": "block"},
    {"character": "閉", "interpreted_as": "verb", "note": "close"},
    {"character": "解", "interpreted_as": "verb", "note": "untangle"},
    {"character": "玄", "interpreted_as": "adjective", "note": "mysterious/paradoxical"},
    {"character": "同", "interpreted_as": "noun", "note": "sameness"},

    # Book 7: Sufficiency (Ch. 44, 46, 9)
    {"character": "足", "interpreted_as": "adjective", "note": "sufficient"},
    {"character": "止", "interpreted_as": "verb", "note": "stop"},
    {"character": "得", "interpreted_as": "verb", "note": "gain/obtain"},
    {"character": "亡", "interpreted_as": "verb", "note": "lose/lack"},
    {"character": "病", "interpreted_as": "noun", "note": "sickness/malfunction"},

    # Book 8: Boundaries (Ch. 52, 30)
    {"character": "母", "interpreted_as": "noun", "note": "mother/source"},
    {"character": "子", "interpreted_as": "noun", "note": "child/derivative"},
    {"character": "果", "interpreted_as": "verb", "note": "complete/achieve result"},
    {"character": "伐", "interpreted_as": "verb", "note": "cut down/boast"},
    {"character": "壯", "interpreted_as": "adjective", "note": "forced prime"},

    # Book 9: Scale (Ch. 54, 66)
    {"character": "修", "interpreted_as": "verb", "note": "cultivate"},
    {"character": "德", "interpreted_as": "noun", "note": "alignment/accumulated pattern"},
    {"character": "觀", "interpreted_as": "verb", "note": "observe"},
    {"character": "建", "interpreted_as": "verb", "note": "establish"},
    {"character": "爭", "interpreted_as": "verb", "note": "contend"},

    # Book 10: Subtraction (Ch. 48, 59, 22)
    {"character": "損", "interpreted_as": "verb", "note": "subtract/reduce"},
    {"character": "益", "interpreted_as": "verb", "note": "increase/add"},
    {"character": "學", "interpreted_as": "noun", "note": "learning"},
    {"character": "曲", "interpreted_as": "adjective", "note": "curved/bent"},
    {"character": "全", "interpreted_as": "adjective", "note": "complete/whole"},

    # Book 11: Generation (Ch. 42, 51, 40)
    {"character": "一", "interpreted_as": "numeral", "note": "one/unity"},
    {"character": "二", "interpreted_as": "numeral", "note": "two/polarity"},
    {"character": "三", "interpreted_as": "numeral", "note": "three/closure"},
    {"character": "陰", "interpreted_as": "noun", "note": "receptive aspect"},
    {"character": "陽", "interpreted_as": "noun", "note": "active aspect"},
    {"character": "畜", "interpreted_as": "verb", "note": "accumulate/nurture"},

    # Book 12: Closure (Ch. 1, 11, 81)
    {"character": "道", "interpreted_as": "noun", "note": "dao/pattern"},
    {"character": "可", "interpreted_as": "adjective", "note": "expressible/manifest"},
    {"character": "名", "interpreted_as": "noun", "note": "name/distinction"},
    {"character": "無", "interpreted_as": "noun", "note": "nothing/void"},
    {"character": "有", "interpreted_as": "noun", "note": "something/presence"},
    {"character": "妙", "interpreted_as": "noun", "note": "subtlety/relations"},
    {"character": "信", "interpreted_as": "adjective", "note": "trustworthy"},
    {"character": "辯", "interpreted_as": "adjective", "note": "eloquent"},

    # Critical structural operators
    {"character": "之", "interpreted_as": "particle", "note": "possessive/demonstrative"},
    {"character": "以", "interpreted_as": "preposition", "note": "by means of"},
    {"character": "而", "interpreted_as": "conjunction", "note": "and/yet"},
    {"character": "則", "interpreted_as": "conjunction", "note": "then/therefore"},
    {"character": "於", "interpreted_as": "preposition", "note": "at/in/from"},
    {"character": "不", "interpreted_as": "adverb", "note": "negation"},
    {"character": "弗", "interpreted_as": "adverb", "note": "structural negation"},
    {"character": "其", "interpreted_as": "pronoun", "note": "its/that"},
    {"character": "乃", "interpreted_as": "conjunction", "note": "therefore/then"},
]


def main():
    print("Loading CHUBS POS data...")
    char_pos_data, char_contexts = load_pos_data()
    print(f"Loaded POS data for {len(char_pos_data)} characters")

    print("\nVerifying DDJ translation choices...")
    results = verify_translation_choices(DDJ_INTERPRETATIONS, char_pos_data, char_contexts)

    print_verification_report(results)

    # Export detailed results
    output_file = CHUBS_DIR.parent / "ddj_verification_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed results exported to: {output_file}")


if __name__ == "__main__":
    main()
