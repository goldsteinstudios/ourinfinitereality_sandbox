"""
Analyze the "other" category radicals and propose new categorizations
"""

import pandas as pd
from collections import Counter, defaultdict
from pathlib import Path

from ttc_parser import parse_ttc_csv
from radical_cooccurrence import RadicalCoOccurrenceMatrix
from radical_dictionary import get_radical_category, get_radicals, RADICAL_MAP

# Load data
csv_path = Path(__file__).parent.parent / "public" / "Just Characters-Table 1.csv"
print("Loading Dao De Jing data...")
characters = parse_ttc_csv(str(csv_path))

print("Building co-occurrence matrix...")
matrix = RadicalCoOccurrenceMatrix(characters, window_size=5)

# Count radical frequencies by category
radical_counts = Counter()
radical_to_chars = defaultdict(list)

for char_obj in characters:
    radicals = get_radicals(char_obj.char)
    for radical in radicals:
        radical_counts[radical] += 1
        radical_to_chars[radical].append(char_obj.char)

# Separate by category
categorized_radicals = defaultdict(list)
for radical in matrix.unique_radicals:
    category = get_radical_category(radical)
    count = radical_counts[radical]
    categorized_radicals[category].append((radical, count))

# Sort by count
for category in categorized_radicals:
    categorized_radicals[category].sort(key=lambda x: x[1], reverse=True)

print("\n" + "="*80)
print("RADICAL FREQUENCY BY CATEGORY")
print("="*80)

for category in ['motion', 'fluid', 'constraint', 'boundary', 'thread', 'cloth',
                 'agent', 'internal', 'action', 'other']:
    radicals = categorized_radicals[category]
    total_count = sum(count for _, count in radicals)
    print(f"\n{category.upper()} ({len(radicals)} radicals, {total_count} occurrences):")

    if category == 'other':
        # For "other", show top 30 with more detail
        print("\nTop 30 'other' radicals:")
        for i, (radical, count) in enumerate(radicals[:30], 1):
            # Get example characters
            example_chars = list(set(radical_to_chars[radical]))[:5]
            example_str = "".join(example_chars)
            print(f"  {i:2d}. {radical}  ({count:4d} occurrences)  Examples: {example_str}")

        if len(radicals) > 30:
            print(f"\n  ... and {len(radicals) - 30} more radicals")
    else:
        # For categorized, show all
        for radical, count in radicals:
            print(f"  {radical}: {count}")

print("\n" + "="*80)
print("PROPOSED NEW CATEGORIES FOR 'OTHER' RADICALS")
print("="*80)

# Analyze the top "other" radicals and propose categories
other_radicals = categorized_radicals['other']

# Define semantic groupings for top radicals
proposed_categories = {
    "Structure/Foundation": {
        "radicals": ["一", "丶", "八", "土", "木", "竹"],
        "description": "Basic structural elements, earth, plants, foundation",
        "color": "#6b4423"
    },
    "Magnitude/Scale": {
        "radicals": ["大", "小", "少", "多"],
        "description": "Size, quantity, degree",
        "color": "#7c3aed"
    },
    "Transformation/Change": {
        "radicals": ["火", "無", "為"],
        "description": "Transformation, becoming, doing/not-doing",
        "color": "#dc2626"
    },
    "Observation/Perception": {
        "radicals": ["目", "見", "示", "矢"],
        "description": "Seeing, showing, manifesting, awareness",
        "color": "#0891b2"
    },
    "Communication/Expression": {
        "radicals": ["言", "訁", "音"],
        "description": "Speech, language, sound",
        "color": "#8b5cf6"
    },
    "Time/Duration": {
        "radicals": ["日", "月", "夕"],
        "description": "Sun, moon, temporal markers",
        "color": "#f59e0b"
    },
    "Direction/Orientation": {
        "radicals": ["方", "正", "反"],
        "description": "Directional markers, alignment",
        "color": "#10b981"
    },
    "Entity/Being": {
        "radicals": ["老", "牛", "馬", "鳥"],
        "description": "Living beings, creatures",
        "color": "#ec4899"
    },
    "Power/Force": {
        "radicals": ["力", "刀", "弓", "戈"],
        "description": "Strength, weapons, force",
        "color": "#ef4444"
    },
    "Containment/Vessel": {
        "radicals": ["器", "皿", "囗"],
        "description": "Containers, vessels, enclosed spaces",
        "color": "#14b8a6"
    },
    "Connection/Relation": {
        "radicals": ["而", "丿", "乙"],
        "description": "Connecting elements, relationships",
        "color": "#a855f7"
    },
    "Material/Substance": {
        "radicals": ["金", "玉", "石"],
        "description": "Physical materials, precious substances",
        "color": "#facc15"
    },
    "Body/Physical": {
        "radicals": ["足", "耳", "肉"],
        "description": "Body parts, physical form",
        "color": "#f97316"
    }
}

print("\nProposed new categories (for top 'other' radicals):\n")

# Show which radicals would go where
for cat_name, cat_info in proposed_categories.items():
    print(f"{cat_name.upper()}")
    print(f"  Description: {cat_info['description']}")
    print(f"  Radicals: {', '.join(cat_info['radicals'])}")

    # Calculate total occurrences
    total = sum(radical_counts[r] for r in cat_info['radicals'] if r in radical_counts)
    print(f"  Total occurrences: {total}")
    print()

# Calculate what would remain as "other"
all_proposed = set()
for cat_info in proposed_categories.values():
    all_proposed.update(cat_info['radicals'])

# Also include already-categorized radicals
already_categorized = set()
for category in ['motion', 'fluid', 'constraint', 'boundary', 'thread', 'cloth',
                 'agent', 'internal', 'action']:
    already_categorized.update(r for r, _ in categorized_radicals[category])

all_categorized = already_categorized | all_proposed

remaining_other = [(r, c) for r, c in other_radicals if r not in all_proposed]
remaining_count = sum(c for _, c in remaining_other)

print("="*80)
print(f"SUMMARY")
print("="*80)
print(f"Original 'other' category: {len(other_radicals)} radicals, {sum(c for _, c in other_radicals)} occurrences")
print(f"Proposed to recategorize: {len(all_proposed)} radicals")
print(f"Would remain as 'other': {len(remaining_other)} radicals, {remaining_count} occurrences")
print(f"\nReduction: {100 * (1 - remaining_count / sum(c for _, c in other_radicals)):.1f}%")

print("\n" + "="*80)
print("TOP 20 RADICALS THAT WOULD REMAIN AS 'OTHER'")
print("="*80)
for i, (radical, count) in enumerate(remaining_other[:20], 1):
    example_chars = "".join(list(set(radical_to_chars[radical]))[:5])
    print(f"  {i:2d}. {radical}  ({count:4d})  Examples: {example_chars}")

# Export to CSV
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# Export full radical analysis
radical_analysis = []
for radical in matrix.unique_radicals:
    current_category = get_radical_category(radical)
    count = radical_counts[radical]
    example_chars = "".join(list(set(radical_to_chars[radical]))[:10])

    # Check proposed category
    proposed_category = current_category
    for cat_name, cat_info in proposed_categories.items():
        if radical in cat_info['radicals']:
            proposed_category = cat_name
            break

    radical_analysis.append({
        'radical': radical,
        'current_category': current_category,
        'proposed_category': proposed_category,
        'frequency': count,
        'example_characters': example_chars
    })

df = pd.DataFrame(radical_analysis)
df = df.sort_values('frequency', ascending=False)
df.to_csv(str(output_dir / "radical_categorization_analysis.csv"), index=False)
print(f"\n✓ Exported detailed analysis to output/radical_categorization_analysis.csv")
