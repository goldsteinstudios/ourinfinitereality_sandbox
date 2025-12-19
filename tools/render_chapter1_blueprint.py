"""
Render Chapter 1 as an engineering blueprint
Shows the complete structural mechanics in a beautiful format
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib
import numpy as np
from pathlib import Path

# Configure fonts
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

from translation_engine import TranslationEngine, CHARACTER_OPERATIONS

# Chapter 1 full text
CHAPTER_1_TEXT = """道可道，非常道；
名可名，非常名。
無名天地之始；
有名萬物之母。
故常無欲，以觀其妙；
常有欲，以觀其徼。
此兩者，同出而異名，
同謂之玄。
玄之又玄，
眾妙之門。"""

def render_blueprint_page(text, output_path):
    """Create a technical blueprint-style visualization of a passage"""

    engine = TranslationEngine()

    # Split into lines
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    # Create figure with blueprint aesthetic
    fig = plt.figure(figsize=(16, 20))
    fig.patch.set_facecolor('#0a1628')  # Dark blue blueprint background

    # Title
    fig.text(0.5, 0.97, 'TAO TE CHING - CHAPTER 1',
             ha='center', fontsize=24, fontweight='bold',
             color='#00d4ff', family='monospace')
    fig.text(0.5, 0.95, 'STRUCTURAL ENGINEERING BLUEPRINT',
             ha='center', fontsize=14,
             color='#00aacc', family='monospace', style='italic')

    # Process each line
    y_position = 0.90

    for line_num, line in enumerate(lines, 1):
        # Remove punctuation for analysis
        clean_line = line.replace('，', '').replace('；', '').replace('。', '')

        # Section header
        fig.text(0.05, y_position, f'LINE {line_num}',
                ha='left', fontsize=10, fontweight='bold',
                color='#ffaa00', family='monospace')

        # Chinese text
        fig.text(0.05, y_position - 0.02, f'原文: {line}',
                ha='left', fontsize=12,
                color='#ffffff', family='Arial Unicode MS')

        y_position -= 0.04

        # Character breakdown
        char_breakdown = []
        for char in clean_line:
            if char in CHARACTER_OPERATIONS:
                data = CHARACTER_OPERATIONS[char]
                rads = "+".join([r['radical'] for r in data['radicals']])
                char_breakdown.append(f"{char}[{rads}]")
            else:
                char_breakdown.append(char)

        breakdown_text = " ".join(char_breakdown)
        fig.text(0.05, y_position, f'分解: {breakdown_text}',
                ha='left', fontsize=10,
                color='#00ff88', family='Arial Unicode MS')

        y_position -= 0.03

        # Structural formulas
        formulas = []
        topo_types = []
        for char in clean_line:
            if char in CHARACTER_OPERATIONS:
                data = CHARACTER_OPERATIONS[char]
                formulas.append(f"{char}={data['formula']}")
                topo_types.append(data['topo_type'])
            else:
                formulas.append(char)
                topo_types.append('?')

        # Show first few formulas (if line is long)
        formula_display = "  ".join(formulas[:8])
        if len(formulas) > 8:
            formula_display += "  ..."

        fig.text(0.05, y_position, f'公式: {formula_display}',
                ha='left', fontsize=8,
                color='#cccccc', family='monospace')

        y_position -= 0.025

        # Topological sequence
        topo_seq = " → ".join(topo_types)
        fig.text(0.05, y_position, f'拓扑: {topo_seq}',
                ha='left', fontsize=8,
                color='#ff66ff', family='monospace')

        y_position -= 0.025

        # Pattern detection
        patterns_found = []
        if 'O' in topo_types and 'G' in topo_types and 'P' in topo_types:
            patterns_found.append("O→G→P cycle")
        if '無' in clean_line and '為' in clean_line:
            patterns_found.append("Transformation pair (無/為)")
        if 'frame' in topo_types and topo_types.count('frame') >= 2:
            patterns_found.append("Frame recursion")

        if patterns_found:
            pattern_text = ", ".join(patterns_found)
            fig.text(0.05, y_position, f'模式: {pattern_text}',
                    ha='left', fontsize=8,
                    color='#ffff00', family='monospace', fontweight='bold')
            y_position -= 0.025

        # Separator
        y_position -= 0.015

        if y_position < 0.15:
            break  # Page full

    # Legend at bottom
    legend_y = 0.08
    fig.text(0.05, legend_y, 'LEGEND / 图例',
            ha='left', fontsize=10, fontweight='bold',
            color='#00d4ff', family='monospace')

    legend_items = [
        ('O', 'Origin/Source - 起源/源泉', '#ff6666'),
        ('G', 'Gradient/Flow - 梯度/流动', '#66ff66'),
        ('P', 'Perimeter/Bound - 边界/界限', '#6666ff'),
        ('frame', 'Frame/Constraint - 框架/约束', '#ffaa66'),
        ('connection', 'Connection - 连接', '#ff66ff'),
    ]

    legend_y -= 0.02
    for code, desc, color in legend_items:
        fig.text(0.05, legend_y, f'{code:12s}',
                ha='left', fontsize=8, color=color, family='monospace', fontweight='bold')
        fig.text(0.15, legend_y, desc,
                ha='left', fontsize=8, color='#cccccc', family='monospace')
        legend_y -= 0.015

    # Notes
    notes_y = legend_y - 0.02
    fig.text(0.05, notes_y, 'NOTE: This is a TOPOLOGICAL GRAMMAR, not semantic translation.',
            ha='left', fontsize=7, color='#888888', family='monospace', style='italic')
    notes_y -= 0.012
    fig.text(0.05, notes_y, 'Each character encodes operations, not just meanings. Radicals specify transformations.',
            ha='left', fontsize=7, color='#888888', family='monospace', style='italic')

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0a1628')
    print(f"✓ Blueprint saved to {output_path}")
    plt.close()


def create_comparative_table(output_path):
    """Create a comparison table showing traditional vs. structural translation"""

    engine = TranslationEngine()

    comparisons = [
        {
            'chinese': '道可道',
            'traditional': 'The Tao that can be told',
            'structural': 'Process(continuous) CAN-BE-PINNED Process(continuous)',
            'insight': 'Trying to pin/name the continuous process creates another process, not THE process'
        },
        {
            'chinese': '非常道',
            'traditional': 'Is not the eternal Tao',
            'structural': 'NOT Constant(frame_independent) Process(continuous)',
            'insight': 'A pinned/framed process is NOT the frame-independent pattern'
        },
        {
            'chinese': '無為',
            'traditional': 'Non-action / Not doing',
            'structural': 'Transform(mode=absence) ⟷ Transform(mode=action)',
            'insight': 'Not "doing nothing" - choosing absence-mode transformation over action-mode'
        },
        {
            'chinese': '有名萬物之母',
            'traditional': 'The named is the mother of ten thousand things',
            'structural': 'Exist(manifest) → Named(framed) → Generates(myriad) → Things(distinct) → Source',
            'insight': 'P→frame→G→P→O cycle: bounded existence generates multiplicity back to source'
        },
    ]

    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#0a1628')
    ax.set_facecolor('#0a1628')

    # Title
    ax.text(0.5, 0.95, 'TRANSLATION COMPARISON: Traditional vs. Structural',
           ha='center', va='top', fontsize=18, fontweight='bold',
           color='#00d4ff', transform=ax.transAxes)

    y_pos = 0.88
    for comp in comparisons:
        # Chinese
        ax.text(0.05, y_pos, comp['chinese'],
               ha='left', va='top', fontsize=14,
               color='#ffffff', family='Arial Unicode MS',
               transform=ax.transAxes, fontweight='bold')

        y_pos -= 0.04

        # Traditional
        ax.text(0.05, y_pos, f"Traditional: {comp['traditional']}",
               ha='left', va='top', fontsize=10,
               color='#ffaa88', transform=ax.transAxes)

        y_pos -= 0.03

        # Structural
        ax.text(0.05, y_pos, f"Structural: {comp['structural']}",
               ha='left', va='top', fontsize=10,
               color='#88ffaa', family='monospace', transform=ax.transAxes)

        y_pos -= 0.03

        # Insight
        ax.text(0.05, y_pos, f"→ {comp['insight']}",
               ha='left', va='top', fontsize=9,
               color='#ffff88', transform=ax.transAxes, style='italic')

        y_pos -= 0.06

        # Separator
        ax.plot([0.05, 0.95], [y_pos + 0.01, y_pos + 0.01],
               color='#004466', linewidth=1, transform=ax.transAxes)

        y_pos -= 0.02

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0a1628')
    print(f"✓ Comparison table saved to {output_path}")
    plt.close()


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("Rendering Chapter 1 Engineering Blueprint...")
    render_blueprint_page(
        CHAPTER_1_TEXT,
        str(output_dir / "chapter1_engineering_blueprint.png")
    )

    print("\nCreating comparative translation table...")
    create_comparative_table(
        str(output_dir / "translation_comparison.png")
    )

    print("\n" + "="*80)
    print("TRANSLATION ENGINE - KEY INSIGHTS")
    print("="*80)

    insights = [
        ("道可道", "Any process you can pin to a frame is not the governing process"),
        ("非常道", "Framed processes are not frame-independent patterns"),
        ("無名 vs 有名", "Nameless=origin, Named=mother of manifestations"),
        ("無 vs 為", "Two modes of transformation: absence vs. action (both active!)"),
        ("玄之又玄", "Mystery recursing into mystery = pre-distinction origin"),
        ("眾妙之門", "Gateway of all subtleties = generative aperture"),
    ]

    for chinese, insight in insights:
        print(f"\n{chinese}:")
        print(f"  → {insight}")

    print("\n" + "="*80)
    print("Next: Expand character database to cover all Chapter 1 characters")
    print("Then: Build pattern recognition for recursive structures")
    print("="*80)
