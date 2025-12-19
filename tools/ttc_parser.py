"""
Parser for Dao De Jing CSV file - extracts characters with position information
"""

import csv
from typing import List, Dict, Tuple
from pathlib import Path


class Character:
    """Represents a character with its position in the text."""
    def __init__(self, char: str, pinyin: str, chapter: int, position: int):
        self.char = char
        self.pinyin = pinyin
        self.chapter = chapter
        self.position = position  # Position within chapter
        self.global_position = 0  # Will be set during parsing

    def __repr__(self):
        return f"Character({self.char}, ch{self.chapter}:{self.position})"


def parse_ttc_csv(csv_path: str) -> List[Character]:
    """
    Parse the TTC CSV file and extract all characters with their positions.

    Args:
        csv_path: Path to the CSV file

    Returns:
        List of Character objects ordered by appearance in the text
    """
    characters = []
    global_position = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row

        for row_idx, row in enumerate(reader, start=1):
            if not row or len(row) < 3:
                continue

            # First column is chapter number
            try:
                chapter = int(row[0])
            except (ValueError, IndexError):
                continue

            # Process character columns (odd indices: char, even indices: pinyin)
            position = 1
            for i in range(1, len(row), 2):
                if i >= len(row) or i + 1 >= len(row):
                    break

                char = row[i].strip()
                pinyin = row[i + 1].strip() if i + 1 < len(row) else ""

                # Skip empty cells and multi-character entries (like "天下")
                # We want individual characters only
                if char and len(char) == 1 and char != '':
                    character = Character(char, pinyin, chapter, position)
                    character.global_position = global_position
                    characters.append(character)
                    global_position += 1
                    position += 1
                # Handle multi-character entries by splitting them
                elif char and len(char) > 1 and ' ' not in char:
                    # Split compound entries like "天下" into individual chars
                    for single_char in char:
                        character = Character(single_char, pinyin, chapter, position)
                        character.global_position = global_position
                        characters.append(character)
                        global_position += 1
                        position += 1

    return characters


def get_unique_characters(characters: List[Character]) -> Dict[str, int]:
    """
    Get frequency count of unique characters.

    Args:
        characters: List of Character objects

    Returns:
        Dictionary mapping character to frequency count
    """
    freq = {}
    for char in characters:
        freq[char.char] = freq.get(char.char, 0) + 1
    return freq


def get_character_positions(characters: List[Character], target_char: str) -> List[Tuple[int, int]]:
    """
    Get all positions where a character appears.

    Args:
        characters: List of Character objects
        target_char: Character to search for

    Returns:
        List of (chapter, position) tuples
    """
    positions = []
    for char in characters:
        if char.char == target_char:
            positions.append((char.chapter, char.position))
    return positions


def get_context_window(characters: List[Character], global_pos: int, window_size: int = 5) -> List[Character]:
    """
    Get characters within a window around a position.

    Args:
        characters: List of Character objects
        global_pos: Global position to center on
        window_size: Number of characters before and after

    Returns:
        List of characters in the window
    """
    start = max(0, global_pos - window_size)
    end = min(len(characters), global_pos + window_size + 1)
    return characters[start:end]


if __name__ == "__main__":
    # Test the parser
    csv_path = Path(__file__).parent.parent / "public" / "Just Characters-Table 1.csv"

    if csv_path.exists():
        print(f"Parsing {csv_path}...")
        characters = parse_ttc_csv(str(csv_path))

        print(f"\nTotal characters parsed: {len(characters)}")

        # Get unique character frequencies
        freq = get_unique_characters(characters)
        print(f"Unique characters: {len(freq)}")

        # Show top 20 most frequent characters
        print("\nTop 20 most frequent characters:")
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20]
        for char, count in sorted_freq:
            print(f"  {char}: {count}")

        # Show some context for a character
        print("\n Example context for 道:")
        dao_positions = [c.global_position for c in characters if c.char == "道"][:3]
        for pos in dao_positions:
            context = get_context_window(characters, pos, window_size=5)
            context_str = "".join([c.char for c in context])
            print(f"  Position {pos}: {context_str}")
    else:
        print(f"CSV file not found at {csv_path}")
