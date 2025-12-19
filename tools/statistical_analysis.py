"""
Statistical analysis of radical co-occurrence patterns
Includes clustering, significance testing, and pattern detection
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Tuple, Dict

from ttc_parser import parse_ttc_csv
from radical_cooccurrence import RadicalCoOccurrenceMatrix
from radical_dictionary import get_radical_category, RADICAL_CATEGORIES

# Configure matplotlib to use Chinese fonts
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'Heiti SC', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # Fix minus sign display


def calculate_expected_cooccurrence(
    matrix: RadicalCoOccurrenceMatrix,
    radical1: str,
    radical2: str
) -> float:
    """
    Calculate expected co-occurrence under random distribution.

    Uses the formula: E(X,Y) = (count(X) * count(Y)) / total_pairs

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        radical1: First radical
        radical2: Second radical

    Returns:
        Expected co-occurrence count under random distribution
    """
    # Count total occurrences of each radical in the matrix
    total_cooccurrences = matrix.matrix.sum().sum() / 2  # Divide by 2 because matrix is symmetric

    if total_cooccurrences == 0:
        return 0.0

    # Count occurrences for each radical (sum of its row/column)
    count1 = matrix.matrix.loc[radical1].sum()
    count2 = matrix.matrix.loc[radical2].sum()

    # Expected value under independence
    expected = (count1 * count2) / (2 * total_cooccurrences)

    return expected


def calculate_significance(
    matrix: RadicalCoOccurrenceMatrix,
    min_observed: int = 5
) -> pd.DataFrame:
    """
    Calculate statistical significance for all radical pairs using chi-square test.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        min_observed: Minimum observed count to consider

    Returns:
        DataFrame with observed, expected, and significance metrics
    """
    results = []

    for i, rad1 in enumerate(matrix.unique_radicals):
        for j in range(i + 1, len(matrix.unique_radicals)):
            rad2 = matrix.unique_radicals[j]

            observed = matrix.matrix.loc[rad1, rad2]

            if observed < min_observed:
                continue

            expected = calculate_expected_cooccurrence(matrix, rad1, rad2)

            # Calculate chi-square statistic
            if expected > 0:
                chi_sq = ((observed - expected) ** 2) / expected
                enrichment = observed / expected
            else:
                chi_sq = 0
                enrichment = 0

            # Categorize
            cat1 = get_radical_category(rad1)
            cat2 = get_radical_category(rad2)
            same_category = (cat1 == cat2 and cat1 != 'other')

            results.append({
                'radical1': rad1,
                'radical2': rad2,
                'category1': cat1,
                'category2': cat2,
                'same_category': same_category,
                'observed': int(observed),
                'expected': expected,
                'enrichment': enrichment,
                'chi_square': chi_sq,
                'significant': chi_sq > 3.84  # p < 0.05 threshold
            })

    df = pd.DataFrame(results)
    df = df.sort_values('chi_square', ascending=False)

    return df


def analyze_category_clustering(matrix: RadicalCoOccurrenceMatrix) -> Dict:
    """
    Analyze whether radicals cluster with others in the same category.

    Args:
        matrix: RadicalCoOccurrenceMatrix object

    Returns:
        Dictionary with clustering analysis results
    """
    # Get category matrix
    cat_matrix = matrix.get_category_cooccurrence()

    results = {}

    for category in cat_matrix.index:
        if category == 'other':
            continue

        # Within-category co-occurrence
        within = cat_matrix.loc[category, category]

        # Cross-category co-occurrence
        total = cat_matrix.loc[category].sum()
        cross = total - within

        # Proportion within category
        if total > 0:
            within_proportion = within / total
        else:
            within_proportion = 0

        results[category] = {
            'within_category': int(within),
            'cross_category': int(cross),
            'total': int(total),
            'within_proportion': within_proportion
        }

    return results


def find_radical_sequences(
    characters: List,
    sequence: List[str],
    window_size: int = 10
) -> List[Dict]:
    """
    Find sequences of radicals in the text (e.g., water -> constraint -> emergence).

    Args:
        characters: List of Character objects
        sequence: List of radical categories in order
        window_size: Maximum distance between radicals in sequence

    Returns:
        List of found sequences with details
    """
    from ttc_parser import Character
    from radical_dictionary import get_radicals

    found_sequences = []

    # Extract all radical occurrences with their categories
    radical_occurrences = []
    for char_obj in characters:
        radicals = get_radicals(char_obj.char)
        for radical in radicals:
            category = get_radical_category(radical)
            radical_occurrences.append({
                'radical': radical,
                'category': category,
                'char': char_obj.char,
                'position': char_obj.global_position,
                'chapter': char_obj.chapter
            })

    # Search for sequences
    for i, occ1 in enumerate(radical_occurrences):
        if occ1['category'] != sequence[0]:
            continue

        # Try to find the rest of the sequence
        seq_match = [occ1]
        last_pos = occ1['position']

        for target_category in sequence[1:]:
            found = False
            # Look ahead for next category
            for j in range(i + 1, len(radical_occurrences)):
                occ2 = radical_occurrences[j]

                # Stop if too far
                if occ2['position'] - last_pos > window_size:
                    break

                if occ2['category'] == target_category:
                    seq_match.append(occ2)
                    last_pos = occ2['position']
                    found = True
                    break

            if not found:
                break

        # If we matched the full sequence, record it
        if len(seq_match) == len(sequence):
            found_sequences.append({
                'sequence': [s['radical'] for s in seq_match],
                'characters': [s['char'] for s in seq_match],
                'positions': [s['position'] for s in seq_match],
                'chapter': seq_match[0]['chapter']
            })

    return found_sequences


def create_hierarchical_clustering(
    matrix: RadicalCoOccurrenceMatrix,
    output_path: str,
    method: str = 'average'
):
    """
    Create hierarchical clustering dendogram of radicals based on co-occurrence.

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        output_path: Path to save the figure
        method: Linkage method ('single', 'complete', 'average', 'ward')
    """
    # Use normalized matrix for clustering
    data = matrix.get_normalized_matrix()

    # Calculate distance matrix (1 - correlation)
    distances = pdist(data.values, metric='correlation')

    # Perform hierarchical clustering
    linkage = hierarchy.linkage(distances, method=method)

    # Create dendrogram
    fig, ax = plt.subplots(figsize=(15, 10))

    dendro = hierarchy.dendrogram(
        linkage,
        labels=data.index.tolist(),
        ax=ax,
        leaf_font_size=10,
        leaf_rotation=90
    )

    ax.set_title('Hierarchical Clustering of Radicals by Co-occurrence',
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Radical', fontsize=11)
    ax.set_ylabel('Distance (1 - Correlation)', fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved clustering dendrogram to {output_path}")
    plt.close()


def analyze_avoidance_pairs(
    matrix: RadicalCoOccurrenceMatrix,
    significance_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Find radical pairs that actively avoid each other (observed << expected).

    Args:
        matrix: RadicalCoOccurrenceMatrix object
        significance_df: DataFrame from calculate_significance()

    Returns:
        DataFrame of avoidance pairs
    """
    # Find pairs where observed is much less than expected
    avoidance = significance_df[
        (significance_df['expected'] > 5) &
        (significance_df['enrichment'] < 0.5)
    ].copy()

    avoidance['avoidance_ratio'] = avoidance['expected'] / (avoidance['observed'] + 1)
    avoidance = avoidance.sort_values('avoidance_ratio', ascending=False)

    return avoidance[['radical1', 'radical2', 'category1', 'category2',
                     'observed', 'expected', 'avoidance_ratio']]


if __name__ == "__main__":
    # Load data
    csv_path = Path(__file__).parent.parent / "public" / "Just Characters-Table 1.csv"
    print("Loading Dao De Jing data...")
    characters = parse_ttc_csv(str(csv_path))

    print("Building co-occurrence matrix...")
    matrix = RadicalCoOccurrenceMatrix(characters, window_size=5)

    output_dir = Path(__file__).parent / "output" / "statistical_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # === STATISTICAL SIGNIFICANCE ===
    print("\n" + "="*70)
    print("STATISTICAL SIGNIFICANCE ANALYSIS")
    print("="*70)

    sig_df = calculate_significance(matrix, min_observed=5)

    print(f"\nTotal significant pairs (p < 0.05): {sig_df['significant'].sum()}")
    print(f"\nTop 10 most enriched pairs:")
    print(sig_df[['radical1', 'radical2', 'category1', 'category2',
                  'observed', 'expected', 'enrichment']].head(10).to_string())

    # Export
    sig_df.to_csv(str(output_dir / "significance_analysis.csv"), index=False)
    print(f"\nExported significance analysis to {output_dir}/significance_analysis.csv")

    # === CATEGORY CLUSTERING ===
    print("\n" + "="*70)
    print("CATEGORY CLUSTERING ANALYSIS")
    print("="*70)

    clustering = analyze_category_clustering(matrix)

    print("\nDo radicals cluster with same-category radicals?")
    for category, stats in clustering.items():
        print(f"\n{category.upper()}:")
        print(f"  Within-category: {stats['within_category']}")
        print(f"  Cross-category: {stats['cross_category']}")
        print(f"  Proportion within: {stats['within_proportion']:.2%}")

    # === AVOIDANCE PAIRS ===
    print("\n" + "="*70)
    print("RADICAL AVOIDANCE ANALYSIS")
    print("="*70)

    avoidance_df = analyze_avoidance_pairs(matrix, sig_df)

    print(f"\nTop 10 pairs that avoid each other:")
    print(avoidance_df.head(10).to_string())

    avoidance_df.to_csv(str(output_dir / "avoidance_pairs.csv"), index=False)

    # === HIERARCHICAL CLUSTERING ===
    print("\nGenerating hierarchical clustering...")
    create_hierarchical_clustering(
        matrix,
        str(output_dir / "radical_clustering_dendrogram.png")
    )

    # === SPECIFIC RESEARCH QUESTIONS ===
    print("\n" + "="*70)
    print("ANSWERING SPECIFIC RESEARCH QUESTIONS")
    print("="*70)

    # Q1: Do motion radicals cluster together?
    print("\nQ1: Do motion radicals (辶) cluster with other motion radicals?")
    motion_radicals = [r for r in ["辶", "走", "足", "行"] if r in matrix.unique_radicals]
    if "辶" in matrix.unique_radicals:
        neighbors = matrix.get_radical_neighbors("辶", n=20)
        motion_neighbors = [(r, c) for r, c in neighbors
                          if get_radical_category(r) == "motion"]
        print(f"  Top co-occurring motion radicals with 辶:")
        for rad, count in motion_neighbors:
            print(f"    {rad}: {count}")

        if not motion_neighbors:
            print("    No other motion radicals found in top 20 neighbors")

    # Q2: Do constraint radicals appear before emergence/release?
    print("\nQ2: Finding constraint → release sequences...")
    constraint_release_seqs = find_radical_sequences(
        characters,
        ["constraint", "motion"],  # Constraint followed by motion
        window_size=5
    )
    print(f"  Found {len(constraint_release_seqs)} constraint→motion sequences")
    print(f"  Examples (first 5):")
    for seq in constraint_release_seqs[:5]:
        chars_str = "".join(seq['characters'])
        print(f"    Chapter {seq['chapter']}: {chars_str}")

    # Q3: Do thread and cloth radicals cluster together?
    print("\nQ3: Do thread (糸) and cloth (巾) radicals cluster together?")
    thread_cloth_pairs = []
    for rad1 in ["糸", "纟"]:
        if rad1 in matrix.unique_radicals:
            for rad2 in ["巾", "衣", "布"]:
                if rad2 in matrix.unique_radicals:
                    count = matrix.matrix.loc[rad1, rad2]
                    if count > 0:
                        thread_cloth_pairs.append((rad1, rad2, int(count)))

    if thread_cloth_pairs:
        print(f"  Thread/Cloth radical pairs:")
        for r1, r2, count in thread_cloth_pairs:
            print(f"    {r1} + {r2}: {count}")
    else:
        print("  No thread/cloth pairs found in co-occurrence matrix")

    # Q4: What radicals appear most with 無 and 為?
    print("\nQ4: What radicals appear most frequently with 無 (wu) and 為 (wei)?")

    from radical_cooccurrence import analyze_specific_character

    wu_analysis = analyze_specific_character(characters, "無", window_size=5)
    print(f"\n  無 (nothing/without):")
    print(f"    Radicals in 無: {wu_analysis['character_radicals']}")
    print(f"    Top 10 co-occurring radicals:")
    for radical, count in wu_analysis['top_cooccurring_radicals'][:10]:
        category = get_radical_category(radical)
        print(f"      {radical} ({category}): {count}")

    wei_analysis = analyze_specific_character(characters, "為", window_size=5)
    print(f"\n  為 (do/act/make):")
    print(f"    Radicals in 為: {wei_analysis['character_radicals']}")
    print(f"    Top 10 co-occurring radicals:")
    for radical, count in wei_analysis['top_cooccurring_radicals'][:10]:
        category = get_radical_category(radical)
        print(f"      {radical} ({category}): {count}")

    # === SUMMARY STATISTICS ===
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)

    # Overall patterns
    top_pairs = matrix.get_top_pairs(10)
    print("\nTop 10 most frequent radical co-occurrences:")
    for r1, r2, count in top_pairs:
        cat1 = get_radical_category(r1)
        cat2 = get_radical_category(r2)
        same = "✓" if cat1 == cat2 and cat1 != "other" else ""
        print(f"  {r1} ({cat1}) + {r2} ({cat2}): {count} {same}")

    # Category statistics
    cat_matrix = matrix.get_category_cooccurrence()
    print("\nCategory co-occurrence matrix:")
    print(cat_matrix.to_string())

    print(f"\n\nAll analysis results saved to {output_dir}/")
