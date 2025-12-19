"""
CHUBS Dataset Analysis
Extracted from HuggingFace viewer: https://huggingface.co/datasets/chen-yingfa/CHUBS

This contains POS-tagged sentences from Chu bamboo slip texts.
Data visible from the viewer (first ~100 rows of training set).
"""

# Data extracted from HuggingFace viewer
# Format: (input_sequence, label_sequence, id)

CHUBS_SAMPLES = [
    (["[", "天", "]", "生", "民", "而", "成", "大", "命", "𴺡"],
     ["B-名词", "I-名词", "I-名词", "B-动词", "B-名词", "B-连词", "B-动词", "B-名词", "I-名词", "O"], 0),

    (["命", ")", "司", "悳", "正", "以", "𵁌", "福", "，"],
     ["B-动词", "I-动词", "B-名词", "I-名词", "B-动词", "B-介词", "B-名词", "I-名词", "O"], 1),

    (["立", "明", "王", "以", "𵁍", "之", "，"],
     ["B-动词", "B-名词", "I-名词", "B-连词", "B-动词", "B-代词", "O"], 2),

    (["曰", "：", """, "大", "命", "又", "𵁎", "，"],
     ["B-动词", "O", "O", "B-名词", "I-名词", "B-动词", "B-形容词", "O"], 3),

    (["少", "命", "日", "𴺡", "成", "𴺡", "則", "敬", "，"],
     ["B-名词", "I-名词", "O", "O", "O", "O", "B-连词", "B-动词", "O"], 4),

    (["又", "尚", "則", "𵁏", "𴺡", "以", "敬", "命", "，", "則", "宅", "【", "一", "】", "亟", "。"],
     ["B-动词", "B-形容词", "B-连词", "O", "O", "B-连词", "B-动词", "B-名词", "O", "B-连词", "B-名词", "O", "O", "O", "B-名词", "O"], 5),

    (["女", "不", "居", "而", "𵁐", "義", "，"],
     ["B-连词", "B-副词", "B-动词", "B-连词", "B-动词", "B-名词", "O"], 8),

    (["則", "宅", "至", "于", "亟", "。"],
     ["B-连词", "B-名词", "B-连词", "I-连词", "B-名词", "O"], 9),

    (["或", "司", "不", "義", "而", "𵁑", "之", "𵁌", "𴺡"],
     ["B-连词", "B-动词", "B-形容词", "I-形容词", "B-连词", "B-动词", "B-代词", "O", "O"], 10),

    (["禍", "）", "𵁒", "才", "人", "𴺡"],
     ["B-名词", "O", "B-动词", "B-介词", "O", "O"], 11),

    (["人", "）", "[", "能", "]", "母", "𵁓", "𵁔", "？"],
     ["B-名词", "O", "B-副词", "I-副词", "I-副词", "I-副词", "B-动词", "B-语气词", "O"], 12),

    (["女", "𵁓", "而", "𵁕", "𵁒", "，", "則", "宅", "至", "于", "亟", "。"],
     ["B-连词", "B-动词", "B-连词", "B-动词", "I-动词", "O", "B-连词", "B-名词", "B-连词", "I-连词", "B-名词", "O"], 13),

    (["夫", "民", "生", "而", "佴", "不", "明", "，"],
     ["B-助词", "B-名词", "B-动词", "B-连词", "B-名词", "B-副词", "B-动词", "O"], 14),

    (["𵁖", "以", "明", "之", "，"],
     ["B-名词", "B-连词", "B-动词", "B-代词", "O"], 15),

    (["能", "亡", "佴", "𵁔", "？"],
     ["B-副词", "I-副词", "B-名词", "B-语气词", "O"], 16),

    (["夫", "民", "生", "而", "樂", "生", "𵁗", "，"],
     ["B-助词", "B-名词", "B-连词", "B-连词", "B-动词", "B-名词", "I-名词", "O"], 18),

    (["上", "以", "𵁗", "之", "，"],
     ["B-名词", "B-连词", "B-动词", "B-代词", "O"], 19),

    (["能", "母", "懽", "𵁔", "？"],
     ["B-副词", "I-副词", "B-动词", "B-语气词", "O"], 20),

    (["夫", "民", "生", "而", "痌", "死", "𵁙", "，"],
     ["B-助词", "B-名词", "B-动词", "B-连词", "B-动词", "B-名词", "I-名词", "O"], 22),

    (["上", "以", "𵁚", "之", "，"],
     ["B-名词", "B-连词", "B-动词", "B-代词", "O"], 23),

    (["王", "才", "蒿", "京", "，"],
     ["B-名词", "B-动词", "B-名词", "I-名词", "O"], 27),

    (["各", "于", "大", "室", "，"],
     ["B-动词", "B-介词", "B-名词", "I-名词", "O"], 28),

    (["卽", "立", "，"],
     ["B-动词", "B-名词", "O"], 29),

    (["咸", "。"],
     ["B-动词", "O"], 30),

    (["王", "曰", "："],
     ["B-名词", "B-动词", "O"], 35),

    (["人", "有", "言", "多", "，"],
     ["B-名词", "B-动词", "B-名词", "B-形容词", "O"], 37),

    (["隹", "我", "鮮", "。"],
     ["B-副词", "B-代词", "B-形容词", "O"], 38),

    (["余", "隹", "亦", "𴽈", "乍", "女", "，"],
     ["B-代词", "B-连词", "B-连词", "B-动词", "I-动词", "B-代词", "O"], 40),

    (["有", "女", "隹", "𴽑", "子", "，"],
     ["B-动词", "B-代词", "B-动词", "B-名词", "I-名词", "O"], 42),

    (["隹", "㝅", "眔", "非", "㝅", "。", """],
     ["B-助词", "B-形容词", "B-连词", "B-形容词", "I-形容词", "O", "O"], 44),

    (["凡", "人", "有", "獄", "有", "𴽆", "，"],
     ["B-副词", "B-名词", "B-名词", "B-名词", "B-动词", "B-名词", "O"], 59),

    (["女", "勿", "受", "𴽟", "，"],
     ["B-代词", "B-副词", "B-动词", "I-动词", "O"], 60),

    (["不", "明", "于", "民", "="],
     ["B-副词", "B-动词", "B-介词", "O", "O"], 61),

    (["民", "）", "其", "聖", "女", "，"],
     ["B-名词", "I-名词", "B-助词", "B-动词", "B-代词", "O"], 62),

    (["凡", "人", "無", "獄", "亡", "𴽆", "，"],
     ["B-副词", "B-名词", "B-动词", "B-名词", "B-动词", "B-名词", "O"], 65),

    (["是", "亦", "引", "休", "，"],
     ["B-代词", "B-副词", "B-动词", "I-动词", "O"], 68),

    (["乃", "智", "隹", "子", "不", "隹", "之", "頌", "，"],
     ["B-连词", "B-动词", "B-助词", "B-名词", "B-副词", "B-助词", "B-助词", "B-动词", "O"], 72),

    (["是", "亦", "尚", "弗", "𴽚", "乃", "彝", "。"],
     ["B-代词", "B-连词", "B-副词", "B-副词", "B-动词", "B-代词", "B-名词", "O"], 73),

    (["隹", "𴽛", "威", "義", "，"],
     ["B-助词", "B-动词", "B-名词", "I-名词", "O"], 75),

    (["隹", "人", "乃", "亦", "無", "智", "亡", "𴽗", "于", "民", "若", "否", "。"],
     ["B-连词", "B-名词", "B-连词", "B-连词", "B-副词", "B-动词", "B-副词", "B-动词", "B-介词", "B-名词", "B-形容词", "I-形容词", "O"], 79),

    (["乃", "身", "𴽜", "隹", "明", "隹", "𴽝", "，"],
     ["B-代词", "B-名词", "B-连词", "B-助词", "B-动词", "B-助词", "B-动词", "O"], 80),

    (["余", "辟", "相", "隹", "卸", "事", "，"],
     ["B-代词", "B-动词", "B-名词", "B-动词", "B-名词", "I-名词", "O"], 84),

    (["不", "𴽕", "則", "𴽖", "于", "余", "。"],
     ["B-副词", "B-动词", "B-连词", "B-动词", "B-介词", "B-代词", "O"], 86),

    (["少", "大", "乃", "有", "𴽗", "智", "𴽘", "恙", "。"],
     ["B-名词", "I-名词", "B-代词", "B-助词", "B-动词", "B-动词", "B-动词", "B-动词", "O"], 89),

    (["余", "既", "埶", "【", "十", "六", "】", "乃", "服", "，"],
     ["B-代词", "B-副词", "B-动词", "O", "O", "O", "O", "B-代词", "B-名词", "O"], 93),

    (["女", "毋", "敢", "朋", "𴽒", "于", "酉", "，"],
     ["B-代词", "B-副词", "B-助词", "B-动词", "B-动词", "B-介词", "B-名词", "O"], 94),

    (["勿", "教", "人", "悳", "我", "。", """],
     ["B-副词", "B-动词", "B-名词", "B-动词", "B-代词", "O", "O"], 95),

    (["是", "隹", "君", "子", "秉", "心", "，"],
     ["B-代词", "B-动词", "B-名词", "I-名词", "B-动词", "B-名词", "O"], 113),

    (["女", "有", "退", "進", "於", "朕", "命", "，"],
     ["B-代词", "B-连词", "B-动词", "I-动词", "B-介词", "B-代词", "B-名词", "O"], 117),

    (["則", "或", "，", "卽", "命", "朕", "。"],
     ["B-连词", "B-动词", "O", "B-连词", "B-动词", "B-代词", "O"], 119),

    (["女", "有", "告", "于", "余", "事", "，"],
     ["B-代词", "B-连词", "B-动词", "B-介词", "B-代词", "B-名词", "O"], 120),

    (["女", "有", "命", "正", "，"],
     ["B-代词", "B-动词", "B-名词", "I-名词", "O"], 121),

    (["有", "卽", "正", "，"],
     ["B-动词", "B-连词", "B-动词", "O"], 122),
]

def analyze_character_pos():
    """Analyze POS distribution for each character across the corpus."""
    char_pos = {}

    for chars, labels, _ in CHUBS_SAMPLES:
        for char, label in zip(chars, labels):
            # Skip punctuation and brackets
            if char in "，。？：""【】[]()）=、〈〉" or label == "O":
                continue

            # Extract POS (remove B-/I- prefix)
            pos = label[2:] if label.startswith(("B-", "I-")) else label

            if char not in char_pos:
                char_pos[char] = {}
            if pos not in char_pos[char]:
                char_pos[char][pos] = 0
            char_pos[char][pos] += 1

    return char_pos

def find_key_characters():
    """Find characters relevant to DDJ/RSM analysis."""
    key_chars = {
        # Structural operators
        "以": "RSM: connector/means operator",
        "之": "RSM: possessive/demonstrative",
        "而": "RSM: sequential connector",
        "則": "RSM: conditional/consequential",
        "于": "RSM: locative/directional",
        "於": "RSM: locative/directional (variant)",

        # Negation/absence
        "不": "RSM: negation operator",
        "無": "RSM: absence/without",
        "亡": "RSM: absence/lack",
        "非": "RSM: negation/not-X",
        "勿": "RSM: prohibition",
        "毋": "RSM: prohibition (variant)",
        "弗": "RSM: negation (object-specific)",

        # DDJ core concepts
        "悳": "RSM: de (accumulated pattern) - archaic form",
        "德": "RSM: de (accumulated pattern)",
        "道": "RSM: dao (path/process)",
        "生": "RSM: emergence/birth",
        "成": "RSM: completion/achievement",
        "命": "RSM: mandate/pattern-assignment",
        "明": "RSM: clarity/illumination",

        # Modal/aspectual
        "能": "RSM: capacity/ability",
        "可": "RSM: possibility",
        "其": "RSM: modal/pronominal",
        "隹": "RSM: emphasis/modal (Chu form)",

        # Pronouns
        "我": "1st person",
        "余": "1st person (formal)",
        "朕": "1st person (royal)",
        "女": "2nd person",

        # Key nouns
        "民": "people",
        "王": "king",
        "天": "heaven/sky",
        "心": "heart-mind",
        "身": "body/self",
        "義": "righteousness/fitting",
    }

    return key_chars

def main():
    print("=" * 60)
    print("CHUBS DATASET ANALYSIS")
    print("Chu Bamboo Slip POS-Tagged Data")
    print("=" * 60)

    # Analyze POS distribution
    char_pos = analyze_character_pos()

    # Get key characters
    key_chars = find_key_characters()

    print("\n" + "=" * 60)
    print("KEY CHARACTERS: POS DISTRIBUTION")
    print("=" * 60)

    for char, description in key_chars.items():
        if char in char_pos:
            print(f"\n{char} - {description}")
            total = sum(char_pos[char].values())
            for pos, count in sorted(char_pos[char].items(), key=lambda x: -x[1]):
                pct = count / total * 100
                print(f"  {pos}: {count} ({pct:.1f}%)")
        else:
            print(f"\n{char} - {description}")
            print("  (not found in sample)")

    print("\n" + "=" * 60)
    print("悳 (DE) ANALYSIS - Critical for RSM")
    print("=" * 60)

    # Find all sentences containing 悳
    de_sentences = []
    for chars, labels, id in CHUBS_SAMPLES:
        if "悳" in chars:
            de_sentences.append((chars, labels, id))

    print(f"\nFound {len(de_sentences)} sentences containing 悳:")
    for chars, labels, id in de_sentences:
        print(f"\n  ID {id}: {''.join(chars)}")
        # Find position and POS of 悳
        for i, (c, l) in enumerate(zip(chars, labels)):
            if c == "悳":
                print(f"  悳 at position {i}, tagged as: {l}")

    print("\n" + "=" * 60)
    print("STRUCTURAL OPERATORS: GRAMMATICAL CONSTRAINTS")
    print("=" * 60)

    structural_ops = ["以", "之", "而", "則", "于", "不", "無", "亡"]

    for op in structural_ops:
        if op in char_pos:
            print(f"\n{op}:")
            for pos, count in sorted(char_pos[op].items(), key=lambda x: -x[1]):
                print(f"  {pos}: {count}")

if __name__ == "__main__":
    main()
