"""
ExemplarSelector: Select best exemplar images for font tracing.

Chooses the highest quality glyph images from CHUBS dataset,
with preference for Guodian Laozi manuscripts.
"""

import json
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

from .image_processor import GlyphImageProcessor


class ExemplarSelector:
    """
    Select best exemplar images for a character from CHUBS dataset.

    Selection criteria:
    1. Guodian Laozi manuscripts (if available)
    2. Image quality score
    3. Source diversity (different manuscripts)
    """

    # Source preferences (higher = more preferred)
    SOURCE_PREFERENCES = {
        "郭店簡_01A-老子甲": 10,  # Guodian Laozi A
        "郭店簡_01B-老子乙": 10,  # Guodian Laozi B
        "郭店簡_01C-老子丙": 10,  # Guodian Laozi C
        "郭店簡": 8,              # Other Guodian
        "上博簡": 6,              # Shanghai Museum
        "清華簡": 5,              # Tsinghua
        "包山簡": 4,              # Baoshan
        "曾侯乙簡": 3,            # Zenghouyi
        "望山簡": 2,              # Wangshan
    }

    def __init__(self, processor: Optional[GlyphImageProcessor] = None):
        """
        Initialize the selector.

        Args:
            processor: GlyphImageProcessor instance
        """
        self.processor = processor or GlyphImageProcessor()
        self.project_root = Path(__file__).parent.parent.parent
        self.selected_dir = self.project_root / "fonts" / "sources" / "selected"
        self.glyph_mappings_path = self.project_root / "data" / "CHUBS_repo" / "twelve_book_glyph_mappings.json"

        self._glyph_mappings = None

    @property
    def glyph_mappings(self) -> Dict:
        """Lazy-load glyph mappings."""
        if self._glyph_mappings is None:
            if self.glyph_mappings_path.exists():
                with open(self.glyph_mappings_path, encoding='utf-8') as f:
                    self._glyph_mappings = json.load(f)
            else:
                self._glyph_mappings = {}
        return self._glyph_mappings

    def get_source_from_path(self, image_path: Path) -> Optional[str]:
        """
        Extract source manuscript from image path.

        CHUBS paths look like: .../glyphs/道/郭店簡_01A-老子甲_001.png

        Args:
            image_path: Path to image

        Returns:
            Source identifier or None
        """
        name = image_path.stem
        # Try to extract source from filename
        for source in self.SOURCE_PREFERENCES.keys():
            if source in name or source in str(image_path):
                return source
        return None

    def get_source_preference(self, source: Optional[str]) -> int:
        """
        Get preference score for a source.

        Args:
            source: Source identifier

        Returns:
            Preference score (higher = better)
        """
        if source is None:
            return 0

        for key, score in self.SOURCE_PREFERENCES.items():
            if key in source:
                return score
        return 1  # Default for unknown sources

    def score_image(self, image_path: Path) -> Dict[str, Any]:
        """
        Calculate comprehensive score for an image.

        Args:
            image_path: Path to image

        Returns:
            Dict with scores and metadata
        """
        # Quality score from processor
        quality_score = self.processor.get_image_quality_score(image_path)

        # Source preference
        source = self.get_source_from_path(image_path)
        source_score = self.get_source_preference(source)

        # Combined score (source preference weighted higher for Tier 1)
        combined_score = 0.4 * quality_score + 0.6 * (source_score / 10)

        return {
            "path": str(image_path),
            "quality_score": quality_score,
            "source": source,
            "source_score": source_score,
            "combined_score": combined_score
        }

    def select_exemplars(
        self,
        character: str,
        count: int = 3,
        prefer_guodian_laozi: bool = True,
        ensure_diversity: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Select best exemplar images for a character.

        Args:
            character: The Chinese character
            count: Number of exemplars to select
            prefer_guodian_laozi: Prioritize Guodian Laozi manuscripts
            ensure_diversity: Try to select from different sources

        Returns:
            List of selected exemplar metadata dicts
        """
        images = self.processor.list_glyph_images(character)
        if not images:
            return []

        # Score all images
        scored = [self.score_image(img) for img in images]

        # If preferring Guodian Laozi, boost those scores
        if prefer_guodian_laozi:
            for s in scored:
                if s["source"] and "老子" in s["source"]:
                    s["combined_score"] *= 1.5

        # Sort by combined score
        scored.sort(key=lambda x: x["combined_score"], reverse=True)

        # Select with diversity if requested
        if ensure_diversity and len(scored) > count:
            selected = []
            used_sources = set()

            for s in scored:
                if len(selected) >= count:
                    break

                # For diversity, skip if we've used this source already
                # (unless we don't have enough diversity)
                if ensure_diversity and s["source"] in used_sources:
                    if len(scored) - len(selected) > count - len(selected):
                        continue

                selected.append(s)
                if s["source"]:
                    used_sources.add(s["source"])

            return selected
        else:
            return scored[:count]

    def prepare_for_tracing(
        self,
        character: str,
        count: int = 3,
        copy_files: bool = True
    ) -> Dict[str, Any]:
        """
        Prepare a character for tracing by selecting and organizing exemplars.

        Args:
            character: The Chinese character
            count: Number of exemplars
            copy_files: Whether to copy files to selected/ directory

        Returns:
            Preparation result with exemplar info
        """
        unicode_code = f"U+{ord(character):04X}"
        output_dir = self.selected_dir / f"{unicode_code}_{character}"

        # Select exemplars
        exemplars = self.select_exemplars(character, count=count)

        if not exemplars:
            return {
                "character": character,
                "unicode": unicode_code,
                "success": False,
                "error": "No glyph images found",
                "exemplars": []
            }

        # Copy files if requested
        if copy_files:
            output_dir.mkdir(parents=True, exist_ok=True)

            for i, ex in enumerate(exemplars):
                src = Path(ex["path"])
                dst = output_dir / f"exemplar_{i+1:02d}{src.suffix}"
                try:
                    shutil.copy2(src, dst)
                    ex["copied_to"] = str(dst)
                except Exception as e:
                    ex["copy_error"] = str(e)

            # Save selection metadata
            metadata = {
                "character": character,
                "unicode": unicode_code,
                "selection_date": datetime.utcnow().isoformat() + "Z",
                "exemplar_count": len(exemplars),
                "exemplars": exemplars,
                "guodian_laozi": any(ex.get("source") and "老子" in ex["source"] for ex in exemplars)
            }

            metadata_path = output_dir / "selection_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

        return {
            "character": character,
            "unicode": unicode_code,
            "success": True,
            "output_dir": str(output_dir) if copy_files else None,
            "exemplars": exemplars,
            "guodian_laozi": any(ex.get("source") and "老子" in ex["source"] for ex in exemplars)
        }

    def prepare_tier_1(self) -> Dict[str, Any]:
        """
        Prepare all Tier 1 characters for tracing.

        Returns:
            Summary of preparation results
        """
        tier_1 = ["道", "德", "自", "反", "弱", "者"]
        results = {}

        for char in tier_1:
            result = self.prepare_for_tracing(char, count=5, copy_files=True)
            results[char] = {
                "success": result["success"],
                "exemplar_count": len(result.get("exemplars", [])),
                "guodian_laozi": result.get("guodian_laozi", False),
                "output_dir": result.get("output_dir")
            }
            if result["success"]:
                print(f"  {char}: {len(result['exemplars'])} exemplars selected")
            else:
                print(f"  {char}: FAILED - {result.get('error')}")

        return {
            "tier": 1,
            "total": len(tier_1),
            "successful": sum(1 for r in results.values() if r["success"]),
            "characters": results
        }

    def get_selection_status(self, character: str) -> Dict[str, Any]:
        """
        Check if exemplars have been selected for a character.

        Args:
            character: The Chinese character

        Returns:
            Status dict
        """
        unicode_code = f"U+{ord(character):04X}"
        char_dir = self.selected_dir / f"{unicode_code}_{character}"
        metadata_path = char_dir / "selection_metadata.json"

        if not metadata_path.exists():
            return {
                "character": character,
                "selected": False,
                "exemplar_count": 0
            }

        with open(metadata_path, encoding='utf-8') as f:
            metadata = json.load(f)

        return {
            "character": character,
            "selected": True,
            "selection_date": metadata.get("selection_date"),
            "exemplar_count": metadata.get("exemplar_count", 0),
            "guodian_laozi": metadata.get("guodian_laozi", False)
        }


def main():
    """Test the selector."""
    selector = ExemplarSelector()

    # Test single character
    print("Testing exemplar selection for 道...")
    result = selector.prepare_for_tracing("道", count=3, copy_files=False)

    print(f"Success: {result['success']}")
    print(f"Exemplars found: {len(result.get('exemplars', []))}")

    for ex in result.get('exemplars', []):
        print(f"  - {ex['source']}: quality={ex['quality_score']:.2f}, combined={ex['combined_score']:.2f}")

    # Check Tier 1 status
    print("\nTier 1 character availability:")
    for char in ["道", "德", "自", "反", "弱", "者"]:
        images = selector.processor.list_glyph_images(char)
        mapping = selector.glyph_mappings.get(char, {})
        guodian = mapping.get("guodian_laozi", False)
        print(f"  {char}: {len(images)} images, Guodian Laozi: {'✓' if guodian else '✗'}")


if __name__ == "__main__":
    main()
