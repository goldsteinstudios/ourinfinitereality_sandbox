"""
Compare original vs. improved categorization to show reduction in "other"
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Configure Chinese fonts
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'Heiti SC', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# Data
original_categories = {
    "motion": 968,
    "fluid": 440,
    "constraint": 406,
    "boundary": 2289,
    "thread": 100,
    "cloth": 221,
    "agent": 2096,
    "internal": 417,
    "action": 403,
    "other": 7614  # Original massive "other"
}

improved_categories = {
    "motion": 968,
    "fluid": 440,
    "constraint": 406,
    "boundary": 2289,
    "thread": 100,
    "cloth": 221,
    "agent": 2096,
    "internal": 417,
    "action": 403,
    # NEW CATEGORIES
    "structure": 4748,
    "magnitude": 1264,
    "transformation": 1453,
    "perception": 933,
    "communication": 475,
    "temporal": 477,
    "direction": 300,
    "entity": 849,
    "connection": 761,
    "material": 50,
    "other": 1052  # Dramatically reduced!
}

# Calculate totals
orig_total = sum(original_categories.values())
improved_total = sum(improved_categories.values())

print("="*80)
print("CATEGORY IMPROVEMENT ANALYSIS")
print("="*80)
print(f"\nOriginal 'other' category: {original_categories['other']:,} co-occurrences")
print(f"Improved 'other' category: {improved_categories['other']:,} co-occurrences")
print(f"Reduction: {original_categories['other'] - improved_categories['other']:,} co-occurrences")
print(f"Reduction percentage: {100 * (1 - improved_categories['other'] / original_categories['other']):.1f}%")

print(f"\n'Other' as % of total:")
print(f"  Original: {100 * original_categories['other'] / orig_total:.1f}%")
print(f"  Improved: {100 * improved_categories['other'] / improved_total:.1f}%")

# Create visualization
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Pie charts
orig_values = list(original_categories.values())
orig_labels = list(original_categories.keys())
orig_colors = ['#ef4444', '#06b6d4', '#f59e0b', '#10b981', '#8b5cf6',
               '#ec4899', '#3b82f6', '#f59e0b', '#14b8a6', '#cccccc']

ax1.pie(orig_values, labels=orig_labels, autopct='%1.1f%%', startangle=90, colors=orig_colors)
ax1.set_title('Original Categorization\n(10 categories, 45.8% "other")', fontweight='bold', fontsize=11)

improved_values = list(improved_categories.values())
improved_labels = list(improved_categories.keys())
improved_colors = ['#ef4444', '#06b6d4', '#f59e0b', '#10b981', '#8b5cf6',
                   '#ec4899', '#3b82f6', '#f59e0b', '#14b8a6',
                   '#78350f', '#7c3aed', '#dc2626', '#0891b2', '#a855f7',
                   '#f59e0b', '#10b981', '#ec4899', '#a855f7', '#facc15', '#999999']

ax2.pie(improved_values, labels=improved_labels, autopct='%1.0f%%', startangle=90,
        colors=improved_colors, textprops={'fontsize': 8})
ax2.set_title('Improved Categorization\n(20 categories, 6.3% "other")', fontweight='bold', fontsize=11)

# Plot 3: Bar comparison
categories_to_compare = ['original\n"other"', 'improved\n"other"']
other_values = [original_categories['other'], improved_categories['other']]
bars = ax3.bar(categories_to_compare, other_values, color=['#cccccc', '#999999'], edgecolor='black', linewidth=2)

ax3.set_ylabel('Co-occurrence Count', fontsize=11, fontweight='bold')
ax3.set_title('"Other" Category Reduction', fontsize=12, fontweight='bold', pad=15)
ax3.set_ylim(0, 8000)

# Add value labels on bars
for bar, val in zip(bars, other_values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 100,
            f'{val:,}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add reduction percentage
ax3.text(0.5, 6500, '86.2%\nreduction',
         ha='center', fontsize=20, fontweight='bold', color='#dc2626',
         bbox=dict(boxstyle='round', facecolor='white', edgecolor='#dc2626', linewidth=2))

plt.tight_layout()
plt.savefig('output/categorization_improvement.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Saved comparison visualization to output/categorization_improvement.png")

# Print new categories added
print("\n" + "="*80)
print("NEW CATEGORIES ADDED:")
print("="*80)

new_cats = {
    "structure": "基础结构 - Basic structural elements, earth, plants",
    "magnitude": "规模量度 - Size, quantity, degree, scale",
    "transformation": "变化转换 - Change, becoming, doing/not-doing (火,無,為)",
    "perception": "感知观察 - Seeing, showing, manifesting, awareness",
    "communication": "沟通表达 - Speech, language, expression",
    "temporal": "时间 - Time, sun, moon, temporal markers",
    "direction": "方向定位 - Directional markers, orientation",
    "entity": "存在实体 - Living beings, creatures, entities",
    "connection": "连接关系 - Connecting elements, relationships",
    "material": "物质材料 - Physical materials, precious substances",
}

for i, (cat, desc) in enumerate(new_cats.items(), 1):
    count = improved_categories[cat]
    pct = 100 * count / improved_total
    print(f"{i:2d}. {cat:15s} ({count:5d}, {pct:4.1f}%) - {desc}")

print("\n" + "="*80)
print("TOP 5 CATEGORIES (by co-occurrence count):")
print("="*80)

sorted_cats = sorted(improved_categories.items(), key=lambda x: x[1], reverse=True)
for i, (cat, count) in enumerate(sorted_cats[:5], 1):
    pct = 100 * count / improved_total
    print(f"{i}. {cat:15s}: {count:5,} ({pct:4.1f}%)")

plt.close()
