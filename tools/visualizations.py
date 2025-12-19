"""
Visualization tools for radical co-occurrence analysis
Creates heat maps, network graphs, and other visualizations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Optional
import matplotlib.patches as mpatches

from ttc_parser import parse_ttc_csv
from radical_cooccurrence import RadicalCoOccurrenceMatrix
from radical_dictionary import RADICAL_CATEGORIES, get_radical_category

# Configure matplotlib to use Chinese fonts
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'Heiti SC', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # Fix minus sign display


def create_heatmap(
    matrix: RadicalCoOccurrenceMatrix,
    output_path: str,
    title: str = "Radical Co-occurrence Heat Map",
    figsize: tuple = (20, 18),
    normalize: bool = True,
    min_count: int = 0
):
    """
    Create a heat map of radical co-occurrences.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        output_path: Path to save the figure
        title: Title for the plot
        figsize: Figure size (width, height)
        normalize: Whether to normalize values
        min_count: Minimum co-occurrence count to display
    """
    # Get the matrix data
    if normalize:
        data = matrix.get_normalized_matrix()
        cmap = "YlOrRd"
        vmax = 1.0
    else:
        data = matrix.matrix
        cmap = "YlOrRd"
        vmax = None

    # Filter by minimum count
    if min_count > 0:
        data = data.copy()
        data[data < min_count] = 0

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create heatmap
    sns.heatmap(
        data,
        cmap=cmap,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8, "label": "Normalized Frequency" if normalize else "Count"},
        ax=ax,
        vmax=vmax,
        fmt=".0f" if not normalize else ".2f"
    )

    # Styling
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Radical", fontsize=12)
    ax.set_ylabel("Radical", fontsize=12)

    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved heat map to {output_path}")
    plt.close()


def create_category_heatmap(
    matrix: RadicalCoOccurrenceMatrix,
    output_path: str,
    title: str = "Radical Category Co-occurrence"
):
    """
    Create a heat map showing co-occurrences by radical category.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        output_path: Path to save the figure
        title: Title for the plot
    """
    # Get category-level matrix
    cat_matrix = matrix.get_category_cooccurrence()

    # Normalize by row totals for better visualization
    row_sums = cat_matrix.sum(axis=1)
    normalized = cat_matrix.div(row_sums, axis=0).fillna(0)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Create heatmap
    sns.heatmap(
        normalized,
        annot=cat_matrix.values,  # Show raw counts as annotations
        fmt='d',
        cmap='Blues',
        square=True,
        linewidths=1,
        cbar_kws={"label": "Proportion"},
        ax=ax
    )

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Co-occurring Category", fontsize=11)
    ax.set_ylabel("Category", fontsize=11)

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved category heat map to {output_path}")
    plt.close()


def create_top_pairs_bar_chart(
    matrix: RadicalCoOccurrenceMatrix,
    output_path: str,
    n: int = 30,
    title: str = "Top Radical Co-occurrence Pairs"
):
    """
    Create a bar chart of top co-occurring radical pairs.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        output_path: Path to save the figure
        n: Number of top pairs to show
        title: Title for the plot
    """
    # Get top pairs
    pairs = matrix.get_top_pairs(n)

    # Prepare data
    labels = [f"{r1} + {r2}" for r1, r2, _ in pairs]
    counts = [count for _, _, count in pairs]

    # Color by category similarity
    colors = []
    for r1, r2, _ in pairs:
        cat1 = get_radical_category(r1)
        cat2 = get_radical_category(r2)
        if cat1 == cat2 and cat1 != 'other':
            # Same category - use category color
            colors.append(RADICAL_CATEGORIES[cat1]['color'])
        else:
            colors.append('#6b7280')  # Gray for different categories

    # Create figure
    fig, ax = plt.subplots(figsize=(12, max(8, n * 0.3)))

    # Create horizontal bar chart
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, counts, color=colors, edgecolor='black', linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Co-occurrence Count', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.invert_yaxis()  # Highest at top

    # Add count labels
    for i, count in enumerate(counts):
        ax.text(count + max(counts) * 0.01, i, str(count),
                va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved bar chart to {output_path}")
    plt.close()


def create_focused_heatmap(
    matrix: RadicalCoOccurrenceMatrix,
    radicals: List[str],
    output_path: str,
    title: str = "Focused Radical Co-occurrence"
):
    """
    Create a heat map focusing on specific radicals of interest.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        radicals: List of radicals to focus on
        output_path: Path to save the figure
        title: Title for the plot
    """
    # Filter matrix to only include specified radicals
    available_radicals = [r for r in radicals if r in matrix.unique_radicals]

    if not available_radicals:
        print(f"None of the specified radicals found in matrix")
        return

    # Extract submatrix
    submatrix = matrix.matrix.loc[available_radicals, available_radicals]

    # Create figure
    fig, ax = plt.subplots(figsize=(len(available_radicals) * 0.8,
                                   len(available_radicals) * 0.8))

    # Create heatmap
    sns.heatmap(
        submatrix,
        annot=True,
        fmt='d',
        cmap='Reds',
        square=True,
        linewidths=1,
        cbar_kws={"label": "Co-occurrence Count"},
        ax=ax
    )

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Radical", fontsize=11)
    ax.set_ylabel("Radical", fontsize=11)

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved focused heat map to {output_path}")
    plt.close()


def create_radical_neighbors_plot(
    matrix: RadicalCoOccurrenceMatrix,
    radical: str,
    output_path: str,
    n: int = 15
):
    """
    Create a bar chart showing top co-occurring radicals for a specific radical.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        radical: The radical to analyze
        output_path: Path to save the figure
        n: Number of neighbors to show
    """
    if radical not in matrix.unique_radicals:
        print(f"Radical {radical} not found in matrix")
        return

    # Get neighbors
    neighbors = matrix.get_radical_neighbors(radical, n)

    if not neighbors:
        print(f"No neighbors found for radical {radical}")
        return

    # Prepare data
    rads, counts = zip(*neighbors)

    # Color by category
    colors = [RADICAL_CATEGORIES.get(get_radical_category(r), {}).get('color', '#6b7280')
              for r in rads]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, max(6, n * 0.4)))

    y_pos = np.arange(len(rads))
    ax.barh(y_pos, counts, color=colors, edgecolor='black', linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(rads, fontsize=10)
    ax.set_xlabel('Co-occurrence Count', fontsize=11)
    ax.set_title(f'Top Co-occurring Radicals with {radical}',
                fontsize=14, fontweight='bold', pad=15)
    ax.invert_yaxis()

    # Add count labels
    for i, count in enumerate(counts):
        ax.text(count + max(counts) * 0.01, i, str(count),
                va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved neighbors plot to {output_path}")
    plt.close()


def create_category_summary_plot(
    matrix: RadicalCoOccurrenceMatrix,
    output_path: str
):
    """
    Create a comprehensive summary visualization of category patterns.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        output_path: Path to save the figure
    """
    cat_matrix = matrix.get_category_cooccurrence()

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # 1. Full category heatmap (normalized)
    ax1 = axes[0, 0]
    row_sums = cat_matrix.sum(axis=1)
    normalized = cat_matrix.div(row_sums, axis=0).fillna(0)
    sns.heatmap(normalized, annot=True, fmt='.2f', cmap='Blues',
                square=True, linewidths=1, ax=ax1, cbar_kws={"label": "Proportion"})
    ax1.set_title('Category Co-occurrence (Normalized)', fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('')

    # 2. Raw counts heatmap
    ax2 = axes[0, 1]
    sns.heatmap(cat_matrix, annot=True, fmt='d', cmap='Oranges',
                square=True, linewidths=1, ax=ax2, cbar_kws={"label": "Count"})
    ax2.set_title('Category Co-occurrence (Raw Counts)', fontweight='bold')
    ax2.set_xlabel('')
    ax2.set_ylabel('')

    # 3. Self-co-occurrence (diagonal values)
    ax3 = axes[1, 0]
    categories = list(cat_matrix.index)
    self_counts = [cat_matrix.loc[cat, cat] for cat in categories]
    colors_cat = [RADICAL_CATEGORIES.get(cat, {}).get('color', '#6b7280')
                  for cat in categories]

    ax3.bar(categories, self_counts, color=colors_cat, edgecolor='black', linewidth=1)
    ax3.set_title('Within-Category Co-occurrence', fontweight='bold')
    ax3.set_xlabel('Category')
    ax3.set_ylabel('Count')
    ax3.tick_params(axis='x', rotation=45)

    # 4. Cross-category strength (off-diagonal sums)
    ax4 = axes[1, 1]
    cross_counts = []
    for cat in categories:
        total = cat_matrix.loc[cat].sum()
        self_count = cat_matrix.loc[cat, cat]
        cross_counts.append(total - self_count)

    ax4.bar(categories, cross_counts, color=colors_cat, edgecolor='black', linewidth=1)
    ax4.set_title('Cross-Category Co-occurrence', fontweight='bold')
    ax4.set_xlabel('Category')
    ax4.set_ylabel('Count')
    ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved category summary to {output_path}")
    plt.close()


if __name__ == "__main__":
    # Load data and build matrix
    csv_path = Path(__file__).parent.parent / "public" / "Just Characters-Table 1.csv"
    print("Loading Dao De Jing data...")
    characters = parse_ttc_csv(str(csv_path))

    print("Building co-occurrence matrix...")
    matrix = RadicalCoOccurrenceMatrix(characters, window_size=5)

    # Create output directory
    output_dir = Path(__file__).parent / "output" / "visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nGenerating visualizations...")

    # 1. Full heat map (normalized)
    create_heatmap(
        matrix,
        str(output_dir / "full_heatmap_normalized.png"),
        title="Radical Co-occurrence Heat Map (Normalized)",
        normalize=True
    )

    # 2. Full heat map (raw counts, filtered)
    create_heatmap(
        matrix,
        str(output_dir / "full_heatmap_filtered.png"),
        title="Radical Co-occurrence Heat Map (Count ≥ 10)",
        normalize=False,
        min_count=10
    )

    # 3. Category-level heat map
    create_category_heatmap(
        matrix,
        str(output_dir / "category_heatmap.png")
    )

    # 4. Top pairs bar chart
    create_top_pairs_bar_chart(
        matrix,
        str(output_dir / "top_pairs_bar.png"),
        n=30
    )

    # 5. Category summary
    create_category_summary_plot(
        matrix,
        str(output_dir / "category_summary.png")
    )

    # 6. Focused heat maps for specific radical categories
    # Motion radicals
    motion_radicals = ["辶", "走", "足", "行"]
    create_focused_heatmap(
        matrix,
        motion_radicals,
        str(output_dir / "motion_radicals_focused.png"),
        title="Motion Radical Co-occurrence"
    )

    # Fluid radicals
    fluid_radicals = ["水", "氵", "冫", "雨"]
    create_focused_heatmap(
        matrix,
        fluid_radicals,
        str(output_dir / "fluid_radicals_focused.png"),
        title="Fluid Radical Co-occurrence"
    )

    # Constraint radicals
    constraint_radicals = ["尸", "厂", "广", "宀"]
    create_focused_heatmap(
        matrix,
        constraint_radicals,
        str(output_dir / "constraint_radicals_focused.png"),
        title="Constraint Radical Co-occurrence"
    )

    # Thread and cloth radicals
    thread_cloth = ["糸", "纟", "巾", "衣", "布"]
    create_focused_heatmap(
        matrix,
        thread_cloth,
        str(output_dir / "thread_cloth_focused.png"),
        title="Thread/Cloth Radical Co-occurrence"
    )

    # 7. Individual radical neighbor plots
    for radical in ["辶", "水", "心", "扌", "口"]:
        if radical in matrix.unique_radicals:
            create_radical_neighbors_plot(
                matrix,
                radical,
                str(output_dir / f"neighbors_{radical}.png"),
                n=15
            )

    print(f"\nAll visualizations saved to {output_dir}/")
