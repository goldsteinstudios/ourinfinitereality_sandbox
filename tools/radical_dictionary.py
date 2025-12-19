"""
Comprehensive radical decomposition dictionary for Dao De Jing characters
Focus on topological/transformational radicals rather than just semantic classification
"""

from typing import List, Dict, Set

# Priority radical categories based on topological operations
RADICAL_CATEGORIES = {
    "motion": {
        "radicals": ["辶", "走", "足", "行"],
        "description": "Continuous motion through space",
        "color": "#ef4444"
    },
    "fluid": {
        "radicals": ["水", "氵", "冫", "雨"],
        "description": "Flow and fluid dynamics",
        "color": "#06b6d4"
    },
    "constraint": {
        "radicals": ["尸", "厂", "广", "宀"],
        "description": "External constraints/boundaries being applied",
        "color": "#f59e0b"
    },
    "boundary": {
        "radicals": ["口", "門", "戶", "囗"],
        "description": "Defined boundaries and enclosures",
        "color": "#10b981"
    },
    "thread": {
        "radicals": ["糸", "纟"],
        "description": "Continuous connection patterns",
        "color": "#8b5cf6"
    },
    "cloth": {
        "radicals": ["巾", "衣", "布"],
        "description": "Woven/flexible structures",
        "color": "#ec4899"
    },
    "agent": {
        "radicals": ["人", "亻", "夫", "子"],
        "description": "Acting entities",
        "color": "#3b82f6"
    },
    "internal": {
        "radicals": ["心", "忄", "思", "意"],
        "description": "Internal states and processes",
        "color": "#f59e0b"
    },
    "action": {
        "radicals": ["手", "扌", "寸", "支"],
        "description": "Action and manipulation",
        "color": "#14b8a6"
    },
    # === NEW CATEGORIES (from "other" analysis) ===
    "structure": {
        "radicals": ["一", "丶", "八", "土", "木", "⺮"],
        "description": "Basic structural elements, earth, plants, foundation",
        "color": "#78350f"
    },
    "magnitude": {
        "radicals": ["大", "小", "少", "多"],
        "description": "Size, quantity, degree, scale",
        "color": "#7c3aed"
    },
    "transformation": {
        "radicals": ["火", "為", "無"],
        "description": "Change, becoming, doing/not-doing, transformation",
        "color": "#dc2626"
    },
    "perception": {
        "radicals": ["目", "見", "示", "矢"],
        "description": "Seeing, showing, manifesting, awareness, knowing",
        "color": "#0891b2"
    },
    "communication": {
        "radicals": ["言", "訁"],
        "description": "Speech, language, expression",
        "color": "#a855f7"
    },
    "temporal": {
        "radicals": ["日", "月", "夕"],
        "description": "Time, sun, moon, temporal markers",
        "color": "#f59e0b"
    },
    "direction": {
        "radicals": ["方", "正", "反"],
        "description": "Directional markers, orientation, alignment",
        "color": "#10b981"
    },
    "entity": {
        "radicals": ["老", "牛", "馬", "鳥"],
        "description": "Living beings, creatures, entities",
        "color": "#ec4899"
    },
    "connection": {
        "radicals": ["而", "丿", "乙"],
        "description": "Connecting elements, relationships, conjunctions",
        "color": "#a855f7"
    },
    "material": {
        "radicals": ["金", "玉", "石"],
        "description": "Physical materials, precious substances",
        "color": "#facc15"
    },
}

# Comprehensive character-to-radical mapping
# Expanded from existing TypeScript mapping with focus on TTC frequency
RADICAL_MAP: Dict[str, List[str]] = {
    # === MOTION RADICALS (辶, 走, 足, 行) ===
    # 辶 (walking radical) - marks continuous motion through space
    "道": ["辶"], "達": ["辶"], "近": ["辶"], "遠": ["辶"], "過": ["辶"],
    "迎": ["辶"], "退": ["辶"], "進": ["辶"], "遇": ["辶"], "運": ["辶"],
    "還": ["辶"], "邊": ["辶"], "逆": ["辶"], "從": ["辶"], "復": ["辶"],
    "往": ["辶"], "返": ["辶"], "造": ["辶"], "遵": ["辶"], "遊": ["辶"],
    "遁": ["辶"], "逃": ["辶"], "逝": ["辶"], "遲": ["辶"], "速": ["辶"],

    # 足 (foot) - grounded motion
    "足": ["足"], "踐": ["足"], "跡": ["足"], "跨": ["足"],

    # 行 (go/walk) - action of moving
    "行": ["行"], "衍": ["行"],

    # === FLUID RADICALS (水/氵, 冫, 雨) ===
    # 水/氵 (water) - flow, fluidity, transformation
    "水": ["水"], "江": ["氵"], "河": ["氵"], "海": ["氵"], "淵": ["氵"],
    "淳": ["氵"], "治": ["氵"], "清": ["氵"], "流": ["氵"], "沖": ["氵"],
    "沒": ["氵"], "法": ["氵"], "泛": ["氵"], "泮": ["氵"], "波": ["氵"],
    "泥": ["氵"], "洋": ["氵"], "洛": ["氵"], "渾": ["氵"], "混": ["氵"],
    "深": ["氵"], "涉": ["氵"], "溪": ["氵"], "谿": ["氵"], "淡": ["氵"],
    "湛": ["氵"], "濁": ["氵"], "澹": ["氵"], "源": ["氵"], "溺": ["氵"],
    "漸": ["氵"], "潮": ["氵"], "滌": ["氵"], "滿": ["氵"], "漢": ["氵"],

    # 冫 (ice) - frozen/suspended fluid
    "冰": ["冫"], "冷": ["冫"], "凍": ["冫"],

    # 雨 (rain) - descending fluid
    "雨": ["雨"], "雪": ["雨"], "雲": ["雨"], "霧": ["雨"],

    # === CONSTRAINT RADICALS (尸, 厂, 广, 宀) ===
    # 尸 (corpse/lid) - external constraint applied to something
    "尸": ["尸"], "尾": ["尸"], "屍": ["尸"], "居": ["尸"], "屋": ["尸"],
    "局": ["尸"], "屬": ["尸"], "展": ["尸"], "屏": ["尸"],

    # 厂 (cliff) - external boundary/constraint
    "厂": ["厂"], "原": ["厂"], "厚": ["厂"], "厭": ["厂"],

    # 广 (shelter) - protective constraint
    "广": ["广"], "廣": ["广"], "度": ["广"], "庫": ["广"], "庭": ["广"],
    "廢": ["广"], "廳": ["广"], "廉": ["广"],

    # 宀 (roof) - covering/containing constraint
    "宀": ["宀"], "宅": ["宀"], "宇": ["宀"], "安": ["宀"], "宗": ["宀"],
    "宙": ["宀"], "定": ["宀"], "宜": ["宀"], "客": ["宀"], "室": ["宀"],
    "家": ["宀"], "容": ["宀"], "寂": ["宀"], "寒": ["宀"], "富": ["宀"],
    "寧": ["宀"], "寶": ["宀"], "實": ["宀"], "寵": ["宀"],

    # === BOUNDARY RADICALS (口, 門, 戶, 囗) ===
    # 口 (mouth) - opening/boundary/portal
    "口": ["口"], "名": ["口"], "命": ["口"], "和": ["口"], "唯": ["口"],
    "善": ["口"], "器": ["口"], "吾": ["口"], "君": ["口"], "知": ["口"],
    "品": ["口"], "哀": ["口"], "嗚": ["口"], "呼": ["口"], "否": ["口"],
    "吉": ["口"], "同": ["口"], "合": ["口"], "含": ["口"], "告": ["口"],
    "味": ["口"], "呵": ["口"], "可": ["口"], "各": ["口"], "谷": ["口", "口"],
    "員": ["口"], "唱": ["口"], "吞": ["口"], "吐": ["口"], "咎": ["口"],
    "喧": ["口"], "嘆": ["口"], "嘉": ["口"], "噎": ["口"],

    # 門 (gate) - threshold/transition boundary
    "門": ["門"], "開": ["門"], "閉": ["門"], "間": ["門"], "閣": ["門"],
    "關": ["門"], "閱": ["門"], "闕": ["門"],

    # 戶 (door) - entrance/exit boundary
    "戶": ["戶"], "房": ["戶"], "所": ["戶"], "扇": ["戶"],

    # 囗 (enclosure) - complete boundary
    "囗": ["囗"], "四": ["囗"], "回": ["囗"], "因": ["囗"], "困": ["囗"],
    "固": ["囗"], "國": ["囗"], "園": ["囗"], "圓": ["囗"], "圍": ["囗"],
    "圖": ["囗"],

    # === THREAD RADICALS (糸/纟) ===
    # 糸/纟 (thread) - continuous connection
    "糸": ["糸"], "紀": ["糸"], "約": ["糸"], "紅": ["糸"], "紋": ["糸"],
    "納": ["糸"], "純": ["糸"], "紛": ["糸"], "素": ["糸"], "索": ["糸"],
    "累": ["糸"], "絕": ["糸"], "統": ["糸"], "絲": ["糸"], "經": ["糸"],
    "綿": ["糸"], "緊": ["糸"], "維": ["糸"], "綱": ["糸"], "網": ["糸"],
    "緣": ["糸"], "編": ["糸"], "緩": ["糸"], "縛": ["糸"], "繁": ["糸"],
    "繩": ["糸"], "繼": ["糸"], "纏": ["糸"],

    # === CLOTH RADICALS (巾, 衣, 布) ===
    # 巾 (cloth/napkin) - woven flexible structure
    "巾": ["巾"], "布": ["巾"], "帝": ["巾"], "師": ["巾"], "帶": ["巾"],
    "帆": ["巾"], "幅": ["巾"], "幕": ["巾"], "幣": ["巾"], "幫": ["巾"],

    # 衣 (clothing) - covering/wrapping structure
    "衣": ["衣"], "表": ["衣"], "裏": ["衣"], "裂": ["衣"], "裝": ["衣"],
    "裕": ["衣"], "補": ["衣"], "裸": ["衣"], "製": ["衣"],

    # === AGENT RADICALS (人/亻, 夫, 子) ===
    # 人/亻 (person) - human agent
    "人": ["人"], "仁": ["亻"], "今": ["人"], "仙": ["亻"], "代": ["亻"],
    "仕": ["亻"], "他": ["亻"], "付": ["亻"], "仙": ["亻"], "以": ["人"],
    "件": ["亻"], "任": ["亻"], "企": ["人"], "伏": ["亻"], "伐": ["亻"],
    "休": ["亻"], "伯": ["亻"], "估": ["亻"], "伴": ["亻"], "伸": ["亻"],
    "似": ["亻"], "位": ["亻"], "住": ["亻"], "佐": ["亻"], "何": ["亻"],
    "余": ["人"], "作": ["亻"], "你": ["亻"], "佔": ["亻"], "使": ["亻"],
    "來": ["人"], "例": ["亻"], "供": ["亻"], "依": ["亻"], "侯": ["亻"],
    "侵": ["亻"], "便": ["亻"], "俗": ["亻"], "保": ["亻"], "信": ["亻"],
    "修": ["亻"], "俱": ["亻"], "俾": ["亻"], "倍": ["亻"], "們": ["亻"],
    "倫": ["亻"], "偏": ["亻"], "做": ["亻"], "停": ["亻"], "健": ["亻"],
    "側": ["亻"], "偵": ["亻"], "偶": ["亻"], "偽": ["亻"], "傅": ["亻"],
    "傑": ["亻"], "備": ["亻"], "傳": ["亻"], "僅": ["亻"], "僧": ["亻"],
    "億": ["亻"], "儀": ["亻"], "儉": ["亻"], "儒": ["亻"], "儲": ["亻"],

    # 夫 (adult man/husband) - mature agent
    "夫": ["大"], "扶": ["夫"], "膚": ["夫"],

    # 子 (child) - nascent agent
    "子": ["子"], "孔": ["子"], "存": ["子"], "孝": ["子"], "孟": ["子"],
    "孤": ["子"], "孫": ["子"], "學": ["子"], "孩": ["子"],

    # === INTERNAL RADICALS (心/忄, 思, 意) ===
    # 心/忄 (heart) - internal state/emotion
    "心": ["心"], "忠": ["心"], "思": ["心"], "志": ["心"], "忘": ["心"],
    "性": ["忄"], "情": ["忄"], "慎": ["忄"], "慈": ["忄"], "慧": ["忄"],
    "悲": ["忄"], "恐": ["忄"], "恃": ["忄"], "恬": ["忄"], "恍": ["忄"],
    "惚": ["忄"], "惟": ["忄"], "惠": ["忄"], "惡": ["忄"], "惜": ["忄"],
    "惑": ["忄"], "慌": ["忄"], "慮": ["忄"], "憂": ["忄"], "憎": ["忄"],
    "懼": ["忄"], "懷": ["忄"], "態": ["忄"], "怒": ["忄"], "怨": ["忄"],
    "恨": ["忄"], "悅": ["忄"], "悟": ["忄"], "患": ["忄"], "恩": ["忄"],
    "息": ["心"], "恭": ["心"], "悉": ["忄"], "想": ["心"], "意": ["心"],
    "愁": ["心"], "愛": ["心"], "感": ["心"], "愚": ["心"], "慕": ["心"],
    "慢": ["忄"], "慰": ["忄"], "憤": ["忄"], "憐": ["忄"], "憲": ["心"],
    "應": ["心"], "懂": ["忄"], "懇": ["忄"], "懲": ["忄"], "懶": ["忄"],

    # === ACTION RADICALS (手/扌, 寸, 支) ===
    # 手/扌 (hand) - manipulation/action
    "手": ["手"], "持": ["扌"], "拱": ["扌"], "拔": ["扌"], "拾": ["扌"],
    "挾": ["扌"], "振": ["扌"], "指": ["扌"], "推": ["扌"], "揚": ["扌"],
    "握": ["扌"], "揮": ["扌"], "援": ["扌"], "損": ["扌"], "搖": ["扌"],
    "摩": ["扌"], "撲": ["扌"], "擊": ["扌"], "操": ["扌"], "擅": ["扌"],
    "擾": ["扌"], "攝": ["扌"], "拿": ["手"], "拜": ["手"], "掌": ["手"],
    "投": ["扌"], "抱": ["扌"], "揣": ["扌"], "撫": ["扌"], "拓": ["扌"],
    "執": ["扌"], "擴": ["扌"], "打": ["扌"], "扶": ["扌"], "扼": ["扌"],
    "抗": ["扌"], "攻": ["扌"], "掘": ["扌"], "抑": ["扌"], "招": ["扌"],
    "捨": ["扌"], "捐": ["扌"], "控": ["扌"], "採": ["扌"], "接": ["扌"],
    "掃": ["扌"], "授": ["扌"], "掩": ["扌"], "探": ["扌"], "措": ["扌"],
    "掛": ["扌"], "排": ["扌"], "掠": ["扌"], "據": ["扌"], "捉": ["扌"],
    "挑": ["扌"], "提": ["扌"], "揭": ["扌"], "換": ["扌"], "撥": ["扌"],
    "撤": ["扌"], "播": ["扌"], "擇": ["扌"], "擔": ["扌"], "擬": ["扌"],
    "支": ["手"], "抹": ["扌"], "按": ["扌"], "挫": ["扌"], "捕": ["扌"],
    "描": ["扌"], "插": ["扌"], "搏": ["扌"], "搜": ["扌"], "摘": ["扌"],
    "摧": ["扌"], "摸": ["扌"], "撒": ["扌"], "撞": ["扌"], "撮": ["扌"],
    "撰": ["扌"], "撿": ["扌"], "擁": ["扌"], "擂": ["扌"], "擄": ["扌"],
    "擋": ["扌"], "擎": ["扌"], "擒": ["扌"], "擠": ["扌"], "擰": ["扌"],
    "擱": ["扌"], "擲": ["扌"], "擷": ["扌"], "擺": ["扌"], "擻": ["扌"],
    "擼": ["扌"], "攀": ["扌"], "攏": ["扌"], "攔": ["扌"], "攙": ["扌"],
    "攛": ["扌"], "攜": ["扌"], "攢": ["扌"], "攣": ["扌"], "攤": ["扌"],
    "攪": ["扌"], "攫": ["扌"], "攬": ["扌"], "攮": ["扌"], "收": ["扌"],
    "攷": ["扌"], "取": ["又"], "拜": ["扌"],

    # 寸 (thumb/inch) - precision action
    "寸": ["寸"], "寺": ["寸"], "封": ["寸"], "射": ["寸"], "將": ["寸"],
    "專": ["寸"], "尊": ["寸"], "導": ["寸"], "對": ["寸"],

    # === OTHER IMPORTANT TTC RADICALS ===
    # 大 (great/large) - expansion
    "大": ["大"], "天": ["大"], "太": ["大"], "失": ["大"], "奇": ["大"],
    "奈": ["大"], "套": ["大"], "奉": ["大"], "奏": ["大"], "奔": ["大"],

    # 女 (woman) - yin/receptive principle
    "女": ["女"], "好": ["女"], "如": ["女"], "妙": ["女"], "妃": ["女"],
    "姓": ["女"], "始": ["女"], "婴": ["女"], "要": ["女"], "妥": ["女"],

    # 言/訁 (speech) - communication/naming
    "言": ["言"], "信": ["言"], "詐": ["訁"], "詞": ["訁"], "誠": ["訁"],
    "說": ["訁"], "話": ["訁"], "語": ["訁"], "謂": ["訁"], "諸": ["訁"],
    "識": ["訁"], "論": ["訁"], "議": ["訁"], "記": ["訁"], "詩": ["訁"],
    "訓": ["訁"], "許": ["訁"], "設": ["訁"], "証": ["訁"], "譽": ["訁"],
    "譏": ["訁"], "讁": ["訁"], "謀": ["訁"], "謙": ["訁"], "警": ["訁"],
    "詳": ["訁"], "試": ["訁"], "詔": ["訁"], "計": ["訁"], "訴": ["訁"],

    # 土 (earth) - grounding/foundation
    "土": ["土"], "地": ["土"], "在": ["土"], "坐": ["土"], "坤": ["土"],
    "型": ["土"], "城": ["土"], "域": ["土"], "執": ["土"], "培": ["土"],
    "基": ["土"], "堂": ["土"], "堅": ["土"], "堆": ["土"], "報": ["土"],
    "場": ["土"], "塊": ["土"], "塵": ["土"], "境": ["土"], "墜": ["土"],

    # 木 (wood/tree) - growth/structure
    "木": ["木"], "本": ["木"], "朱": ["木"], "朴": ["木"], "材": ["木"],
    "村": ["木"], "杜": ["木"], "束": ["木"], "林": ["木"], "枝": ["木"],
    "析": ["木"], "松": ["木"], "板": ["木"], "果": ["木"], "柔": ["木"],
    "柱": ["木"], "查": ["木"], "栗": ["木"], "校": ["木"], "根": ["木"],
    "格": ["木"], "桃": ["木"], "案": ["木"], "梁": ["木"], "棄": ["木"],
    "棋": ["木"], "森": ["木"], "植": ["木"], "極": ["木"], "楚": ["木"],
    "業": ["木"], "樂": ["木"], "樹": ["木"], "橋": ["木"], "機": ["木"],

    # 火 (fire) - transformation/energy
    "火": ["火"], "灰": ["火"], "灯": ["火"], "災": ["火"], "炎": ["火"],
    "為": ["火"], "烈": ["火"], "烏": ["火"], "烹": ["火"], "焉": ["火"],
    "無": ["火"], "然": ["火"], "煮": ["火"], "照": ["火"], "熱": ["火"],
    "燃": ["火"], "爆": ["火"], "爐": ["火"],

    # 金 (metal) - hardness/value
    "金": ["金"], "針": ["金"], "釘": ["金"], "銅": ["金"], "銘": ["金"],
    "銳": ["金"], "銀": ["金"], "鋒": ["金"], "錄": ["金"], "錢": ["金"],
    "鍵": ["金"], "鎖": ["金"], "鐵": ["金"], "鑄": ["金"],

    # 玉 (jade) - preciousness
    "玉": ["玉"], "玩": ["玉"], "玲": ["玉"], "珍": ["玉"], "珠": ["玉"],
    "現": ["玉"], "理": ["玉"], "琴": ["玉"], "瑩": ["玉"], "璧": ["玉"],

    # 示 (show/spirit) - manifestation
    "示": ["示"], "社": ["示"], "神": ["示"], "祀": ["示"], "祈": ["示"],
    "祖": ["示"], "祝": ["示"], "祥": ["示"], "票": ["示"], "祭": ["示"],
    "禁": ["示"], "禮": ["示"], "禍": ["示"], "福": ["示"],

    # 竹 (bamboo) - flexibility/writing
    "竹": ["⺮"], "笑": ["⺮"], "笛": ["⺮"], "符": ["⺮"], "第": ["⺮"],
    "筆": ["⺮"], "等": ["⺮"], "筋": ["⺮"], "策": ["⺮"], "算": ["⺮"],
    "管": ["⺮"], "箱": ["⺮"], "節": ["⺮"], "範": ["⺮"], "篇": ["⺮"],
    "築": ["⺮"], "簡": ["⺮"], "簽": ["⺮"], "籌": ["⺮"], "籍": ["⺮"],

    # 見 (see) - perception
    "見": ["見"], "規": ["見"], "視": ["見"], "親": ["見"], "覺": ["見"],
    "覽": ["見"], "觀": ["見"],

    # 車 (vehicle/wheel) - circular motion/transport
    "車": ["車"], "軍": ["車"], "軌": ["車"], "軟": ["車"], "較": ["車"],
    "載": ["車"], "輔": ["車"], "輕": ["車"], "輛": ["車"], "輝": ["車"],
    "輩": ["車"], "輪": ["車"], "輯": ["車"], "輸": ["車"], "轉": ["車"],
    "轍": ["車"], "轎": ["車"],

    # 食 (food/eat) - consumption/nourishment
    "食": ["食"], "飢": ["食"], "飯": ["食"], "飲": ["食"], "飽": ["食"],
    "餌": ["食"], "養": ["食"], "餘": ["食"], "餓": ["食"], "館": ["食"],

    # 馬 (horse) - power/speed
    "馬": ["馬"], "馳": ["馬"], "駐": ["馬"], "駒": ["馬"], "駕": ["馬"],
    "駛": ["馬"], "駿": ["馬"], "騎": ["馬"], "騙": ["馬"], "騰": ["馬"],
    "騷": ["馬"], "驅": ["馬"], "驕": ["馬"], "驗": ["馬"], "驚": ["馬"],

    # KEY TTC CHARACTERS - ensure coverage
    "無": ["火"],  # Critical character - "nothing/without"
    "為": ["火"],  # Critical character - "do/act/make"
    "道": ["辶"],  # Already covered - "the Way"
    "德": ["彳"],  # Virtue/power - walking radical variant
    "天": ["大"],  # Heaven/sky
    "下": ["一"],  # Under/below
    "不": ["一"],  # Not/negation
    "有": ["月"],  # Have/exist
    "物": ["牛"],  # Things/beings
    "常": ["巾"],  # Constant/eternal
    "自": ["目"],  # Self
    "然": ["火"],  # Nature/natural
    "知": ["矢", "口"],  # Know - arrow + mouth
    "者": ["老"],  # One who/that which
    "之": ["丶"],  # Possessive particle
    "以": ["人"],  # By means of/use
    "其": ["八"],  # Its/that
    "於": ["方"],  # At/in
    "而": ["而"],  # And/yet
    "也": ["乙"],  # Final particle
    "與": ["臼"],  # Give/with
    "若": ["艸"],  # Like/as if
    "所": ["戶"],  # Place/that which
}

def get_radicals(char: str) -> List[str]:
    """
    Get list of radicals for a given character.

    Args:
        char: Chinese character

    Returns:
        List of radicals in the character (empty list if not found)
    """
    return RADICAL_MAP.get(char, [])


def get_radical_category(radical: str) -> str:
    """
    Get the category (motion, fluid, constraint, etc.) for a radical.

    Args:
        radical: The radical character

    Returns:
        Category name or "other" if not in priority categories
    """
    for category, info in RADICAL_CATEGORIES.items():
        if radical in info["radicals"]:
            return category
    return "other"


def get_all_radicals() -> Set[str]:
    """Get set of all unique radicals in the dictionary."""
    radicals = set()
    for char_radicals in RADICAL_MAP.values():
        radicals.update(char_radicals)
    return radicals


def get_characters_with_radical(radical: str) -> List[str]:
    """
    Get all characters that contain a specific radical.

    Args:
        radical: The radical to search for

    Returns:
        List of characters containing that radical
    """
    return [char for char, rads in RADICAL_MAP.items() if radical in rads]


def export_dictionary_stats() -> Dict:
    """Export statistics about the radical dictionary."""
    all_radicals = get_all_radicals()

    stats = {
        "total_characters": len(RADICAL_MAP),
        "total_unique_radicals": len(all_radicals),
        "radicals_by_category": {},
        "characters_per_radical": {}
    }

    # Count by category
    for category, info in RADICAL_CATEGORIES.items():
        chars_in_category = []
        for radical in info["radicals"]:
            chars_in_category.extend(get_characters_with_radical(radical))
        stats["radicals_by_category"][category] = len(set(chars_in_category))

    # Count characters per radical
    for radical in all_radicals:
        stats["characters_per_radical"][radical] = len(get_characters_with_radical(radical))

    return stats


if __name__ == "__main__":
    # Print statistics
    stats = export_dictionary_stats()
    print(f"Radical Dictionary Statistics:")
    print(f"  Total characters mapped: {stats['total_characters']}")
    print(f"  Total unique radicals: {stats['total_unique_radicals']}")
    print(f"\nCharacters by category:")
    for category, count in stats["radicals_by_category"].items():
        print(f"  {category}: {count}")

    print(f"\nTop 10 most common radicals:")
    sorted_radicals = sorted(stats["characters_per_radical"].items(),
                            key=lambda x: x[1], reverse=True)[:10]
    for radical, count in sorted_radicals:
        category = get_radical_category(radical)
        print(f"  {radical} ({category}): {count} characters")
