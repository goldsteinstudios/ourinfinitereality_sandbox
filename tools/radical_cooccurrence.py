"""
Radical co-occurrence matrix calculator for Dao De Jing
Analyzes how radicals co-occur within proximity windows
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Set
from collections import defaultdict, Counter
from pathlib import Path

from ttc_parser import parse_ttc_csv, Character, get_context_window
from radical_dictionary import get_radicals, get_all_radicals, RADICAL_CATEGORIES


class RadicalOccurrence:
    """Represents a radical occurring at a specific position."""
    def __init__(self, radical: str, char: str, global_position: int, chapter: int, position: int):
        self.radical = radical
        self.char = char  # The character containing this radical
        self.global_position = global_position
        self.chapter = chapter
        self.position = position


class RadicalCoOccurrenceMatrix:
    """
    Calculate and store radical co-occurrence patterns.
    """

    def __init__(self, characters: List[Character], window_size: int = 5):
        """
        Initialize the co-occurrence matrix.

        Args:
            characters: List of Character objects from TTC
            window_size: Characters within ±window_size are considered co-occurring
        """
        self.characters = characters
        self.window_size = window_size
        self.radical_occurrences = self._extract_radical_occurrences()
        self.unique_radicals = sorted(list(set([r.radical for r in self.radical_occurrences])))

        # Build the co-occurrence matrix
        self.matrix, self.pair_details = self._build_cooccurrence_matrix()

    def _extract_radical_occurrences(self) -> List[RadicalOccurrence]:
        """Extract all radical occurrences from the character list."""
        occurrences = []

        for char_obj in self.characters:
            radicals = get_radicals(char_obj.char)

            for radical in radicals:
                occurrence = RadicalOccurrence(
                    radical=radical,
                    char=char_obj.char,
                    global_position=char_obj.global_position,
                    chapter=char_obj.chapter,
                    position=char_obj.position
                )
                occurrences.append(occurrence)

        return occurrences

    def _build_cooccurrence_matrix(self) -> Tuple[pd.DataFrame, Dict]:
        """
        Build the co-occurrence matrix.

        Returns:
            Tuple of (DataFrame matrix, dictionary of pair details)
        """
        # Initialize counts
        pair_counts = defaultdict(int)
        pair_details = defaultdict(list)  # Store specific instances

        # For each radical occurrence, look within the window
        for i, occ1 in enumerate(self.radical_occurrences):
            # Look ahead within window
            for j in range(i + 1, len(self.radical_occurrences)):
                occ2 = self.radical_occurrences[j]

                # Calculate distance
                distance = abs(occ2.global_position - occ1.global_position)

                # Stop if beyond window
                if distance > self.window_size:
                    break

                # Don't count same character with itself
                if occ1.global_position == occ2.global_position:
                    continue

                # Record co-occurrence (use sorted tuple for symmetry)
                radical_pair = tuple(sorted([occ1.radical, occ2.radical]))
                pair_counts[radical_pair] += 1

                # Store details
                pair_details[radical_pair].append({
                    'char1': occ1.char,
                    'char2': occ2.char,
                    'position1': occ1.global_position,
                    'position2': occ2.global_position,
                    'distance': distance,
                    'chapter': occ1.chapter,
                })

        # Build DataFrame matrix
        n = len(self.unique_radicals)
        matrix_data = np.zeros((n, n), dtype=int)

        for (rad1, rad2), count in pair_counts.items():
            idx1 = self.unique_radicals.index(rad1)
            idx2 = self.unique_radicals.index(rad2)
            matrix_data[idx1, idx2] = count
            matrix_data[idx2, idx1] = count  # Symmetric matrix

        df = pd.DataFrame(
            matrix_data,
            index=self.unique_radicals,
            columns=self.unique_radicals
        )

        return df, dict(pair_details)

    def get_normalized_matrix(self) -> pd.DataFrame:
        """
        Get normalized co-occurrence matrix (frequencies instead of raw counts).

        Returns:
            DataFrame with normalized values (0-1)
        """
        # Normalize by the maximum value
        max_val = self.matrix.max().max()
        if max_val == 0:
            return self.matrix

        return self.matrix / max_val

    def get_top_pairs(self, n: int = 20) -> List[Tuple[str, str, int]]:
        """
        Get top N most frequently co-occurring radical pairs.

        Args:
            n: Number of top pairs to return

        Returns:
            List of (radical1, radical2, count) tuples
        """
        pairs = []

        for i, rad1 in enumerate(self.unique_radicals):
            for j in range(i + 1, len(self.unique_radicals)):
                rad2 = self.unique_radicals[j]
                count = self.matrix.loc[rad1, rad2]
                if count > 0:
                    pairs.append((rad1, rad2, int(count)))

        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs[:n]

    def get_radical_neighbors(self, radical: str, n: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top N radicals that most frequently co-occur with a given radical.

        Args:
            radical: The radical to analyze
            n: Number of neighbors to return

        Returns:
            List of (co-occurring_radical, count) tuples
        """
        if radical not in self.unique_radicals:
            return []

        row = self.matrix.loc[radical]
        neighbors = [(rad, int(count)) for rad, count in row.items()
                    if count > 0 and rad != radical]
        neighbors.sort(key=lambda x: x[1], reverse=True)
        return neighbors[:n]

    def export_to_csv(self, output_path: str):
        """Export the raw co-occurrence matrix to CSV."""
        self.matrix.to_csv(output_path)
        print(f"Exported co-occurrence matrix to {output_path}")

    def export_normalized_to_csv(self, output_path: str):
        """Export the normalized matrix to CSV."""
        normalized = self.get_normalized_matrix()
        normalized.to_csv(output_path)
        print(f"Exported normalized matrix to {output_path}")

    def export_top_pairs_to_csv(self, output_path: str, n: int = 100):
        """Export top N pairs with details to CSV."""
        pairs = self.get_top_pairs(n)

        rows = []
        for rad1, rad2, count in pairs:
            # Get category for each radical
            cat1 = None
            cat2 = None
            for category, info in RADICAL_CATEGORIES.items():
                if rad1 in info["radicals"]:
                    cat1 = category
                if rad2 in info["radicals"]:
                    cat2 = category

            # Get example character pairs
            pair_key = tuple(sorted([rad1, rad2]))
            examples = self.pair_details.get(pair_key, [])[:5]
            example_chars = ", ".join([f"{e['char1']}-{e['char2']}" for e in examples])

            rows.append({
                'radical1': rad1,
                'radical2': rad2,
                'category1': cat1 or 'other',
                'category2': cat2 or 'other',
                'count': count,
                'example_pairs': example_chars
            })

        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        print(f"Exported top {n} pairs to {output_path}")

    def get_category_cooccurrence(self) -> pd.DataFrame:
        """
        Aggregate co-occurrences by radical category.

        Returns:
            DataFrame showing how radical categories co-occur
        """
        # Map radicals to categories
        radical_to_category = {}
        for category, info in RADICAL_CATEGORIES.items():
            for radical in info["radicals"]:
                radical_to_category[radical] = category

        # Aggregate by category
        categories = list(RADICAL_CATEGORIES.keys()) + ['other']
        category_matrix = defaultdict(lambda: defaultdict(int))

        for i, rad1 in enumerate(self.unique_radicals):
            cat1 = radical_to_category.get(rad1, 'other')
            for j, rad2 in enumerate(self.unique_radicals):
                cat2 = radical_to_category.get(rad2, 'other')
                count = self.matrix.iloc[i, j]
                category_matrix[cat1][cat2] += count

        # Convert to DataFrame
        df = pd.DataFrame(category_matrix).fillna(0).astype(int)
        df = df.reindex(index=categories, columns=categories, fill_value=0)

        return df


def analyze_specific_character(characters: List[Character], target_char: str, window_size: int = 5):
    """
    Analyze radicals that co-occur with a specific character.

    Args:
        characters: List of Character objects
        target_char: Character to analyze
        window_size: Window size for co-occurrence

    Returns:
        Dictionary with analysis results
    """
    # Find all occurrences of the target character
    target_positions = [c.global_position for c in characters if c.char == target_char]

    if not target_positions:
        return {"error": f"Character {target_char} not found"}

    # Get radicals in the target character
    target_radicals = get_radicals(target_char)

    # Find co-occurring radicals
    cooccurring_radicals = Counter()
    cooccurring_chars = defaultdict(list)

    for pos in target_positions:
        # Get context window
        start = max(0, pos - window_size)
        end = min(len(characters), pos + window_size + 1)

        for i in range(start, end):
            if i == pos:  # Skip the target character itself
                continue

            char_obj = characters[i]
            radicals = get_radicals(char_obj.char)

            for radical in radicals:
                cooccurring_radicals[radical] += 1
                cooccurring_chars[radical].append(char_obj.char)

    # Prepare results
    results = {
        "character": target_char,
        "character_radicals": target_radicals,
        "frequency": len(target_positions),
        "top_cooccurring_radicals": cooccurring_radicals.most_common(10),
        "radical_examples": {
            rad: list(set(chars))[:5]
            for rad, chars in cooccurring_chars.items()
        }
    }

    return results


if __name__ == "__main__":
    # Load the TTC data
    csv_path = Path(__file__).parent.parent / "public" / "Just Characters-Table 1.csv"
    print("Loading Dao De Jing data...")
    characters = parse_ttc_csv(str(csv_path))
    print(f"Loaded {len(characters)} characters")

    # Build co-occurrence matrix
    print("\nBuilding radical co-occurrence matrix (window=5)...")
    matrix = RadicalCoOccurrenceMatrix(characters, window_size=5)
    print(f"Matrix dimensions: {len(matrix.unique_radicals)} x {len(matrix.unique_radicals)}")
    print(f"Unique radicals found in text: {len(matrix.unique_radicals)}")

    # Show top co-occurring pairs
    print("\nTop 20 co-occurring radical pairs:")
    top_pairs = matrix.get_top_pairs(20)
    for rad1, rad2, count in top_pairs:
        print(f"  {rad1} + {rad2}: {count}")

    # Show category-level co-occurrence
    print("\nCategory-level co-occurrence:")
    cat_matrix = matrix.get_category_cooccurrence()
    print(cat_matrix)

    # Analyze specific characters
    print("\n" + "="*60)
    print("Analysis of 無 (wu - nothing/without):")
    wu_analysis = analyze_specific_character(characters, "無", window_size=5)
    print(f"  Character radicals: {wu_analysis['character_radicals']}")
    print(f"  Frequency in text: {wu_analysis['frequency']}")
    print(f"  Top co-occurring radicals:")
    for radical, count in wu_analysis['top_cooccurring_radicals']:
        print(f"    {radical}: {count}")

    print("\n" + "="*60)
    print("Analysis of 為 (wei - do/act):")
    wei_analysis = analyze_specific_character(characters, "為", window_size=5)
    print(f"  Character radicals: {wei_analysis['character_radicals']}")
    print(f"  Frequency in text: {wei_analysis['frequency']}")
    print(f"  Top co-occurring radicals:")
    for radical, count in wei_analysis['top_cooccurring_radicals']:
        print(f"    {radical}: {count}")

    # Export matrices
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    matrix.export_to_csv(str(output_dir / "radical_cooccurrence_matrix.csv"))
    matrix.export_normalized_to_csv(str(output_dir / "radical_cooccurrence_normalized.csv"))
    matrix.export_top_pairs_to_csv(str(output_dir / "top_radical_pairs.csv"), n=100)

    print(f"\nExported analysis results to {output_dir}/")
