"""
GlossaryIntegrator: CHUBS validation and cross-system integration.

Validates glossary entries against the CHUBS (Chu Bamboo Slip) corpus,
integrates glyph data, and propagates updates to translation files.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from collections import Counter

from .manager import GlossaryManager


class GlossaryIntegrator:
    """
    Integrates Living Glossary with CHUBS corpus and other data sources.
    """

    # POS tag translations (Chinese → English)
    POS_TRANSLATIONS = {
        "名词": "noun",
        "动词": "verb",
        "形容词": "adjective",
        "副词": "adverb",
        "介词": "preposition",
        "连词": "conjunction",
        "助词": "particle",
        "数词": "numeral",
        "量词": "classifier",
        "代词": "pronoun",
        "方位词": "localizer",
        "叹词": "interjection",
    }

    def __init__(self, glossary_manager: Optional[GlossaryManager] = None):
        """
        Initialize the integrator.

        Args:
            glossary_manager: GlossaryManager instance. Creates one if not provided.
        """
        self.gm = glossary_manager or GlossaryManager()

        # Paths to data sources
        self.project_root = Path(__file__).parent.parent.parent
        self.chubs_dir = self.project_root / "data" / "CHUBS_repo"
        self.pos_dir = self.chubs_dir / "pos-tagging-data"
        self.glyph_mappings_path = self.chubs_dir / "twelve_book_glyph_mappings.json"

        # Caches
        self._pos_data = None
        self._glyph_mappings = None
        self._pos_distributions = None

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

    @property
    def pos_data(self) -> Dict[str, List[Dict]]:
        """Lazy-load all POS data from train/dev/test."""
        if self._pos_data is None:
            self._pos_data = {"train": [], "dev": [], "test": []}
            for split in ["train", "dev", "test"]:
                path = self.pos_dir / f"{split}_examples.json"
                if path.exists():
                    with open(path, encoding='utf-8') as f:
                        self._pos_data[split] = json.load(f)
        return self._pos_data

    def get_pos_distribution(self, character: str) -> Dict[str, int]:
        """
        Get POS distribution for a character across the CHUBS corpus.

        Args:
            character: The character to analyze

        Returns:
            Dict mapping POS tags to counts
        """
        if self._pos_distributions is None:
            self._build_pos_distributions()

        return self._pos_distributions.get(character, {})

    def _build_pos_distributions(self):
        """Build POS distribution cache for all characters."""
        self._pos_distributions = {}

        for split, examples in self.pos_data.items():
            for example in examples:
                inputs = example.get("input", [])
                labels = example.get("label", [])

                for char, label in zip(inputs, labels):
                    if label == "O" or not char.strip():
                        continue

                    # Extract POS from BIO tag (e.g., "B-名词" → "名词")
                    if "-" in label:
                        pos = label.split("-", 1)[1]
                    else:
                        pos = label

                    if char not in self._pos_distributions:
                        self._pos_distributions[char] = Counter()
                    self._pos_distributions[char][pos] += 1

        # Convert Counters to dicts
        self._pos_distributions = {
            char: dict(counter)
            for char, counter in self._pos_distributions.items()
        }

    def validate_with_chubs(self, character: str) -> Dict:
        """
        Validate a character's interpretation against CHUBS corpus.

        Args:
            character: The character to validate

        Returns:
            Validation result dict with verdict, counts, and distribution
        """
        # Get glyph data
        glyph_data = self.glyph_mappings.get(character, {})
        glyph_count = glyph_data.get("glyph_count", 0)
        guodian_laozi = glyph_data.get("guodian_laozi", False)
        paths = glyph_data.get("paths", [])
        sources = glyph_data.get("sources", {})

        # Get POS distribution
        pos_dist = self.get_pos_distribution(character)
        total_pos = sum(pos_dist.values()) if pos_dist else 0

        # Calculate percentage distribution
        pos_percentages = {}
        if total_pos > 0:
            pos_percentages = {
                pos: round(count / total_pos * 100, 1)
                for pos, count in pos_dist.items()
            }

        # Determine dominant POS
        dominant_pos = None
        dominant_pct = 0
        if pos_dist:
            dominant_pos = max(pos_dist, key=pos_dist.get)
            dominant_pct = pos_percentages.get(dominant_pos, 0)

        # Determine verdict based on attestation
        if glyph_count == 0 and total_pos == 0:
            verdict = "NOT_ATTESTED"
        elif glyph_count > 0 and total_pos == 0:
            verdict = "GLYPHS_ONLY"  # Has images but no POS tags
        elif dominant_pct >= 50:
            verdict = "CONFIRMED"
        elif dominant_pct >= 20:
            verdict = "PLAUSIBLE"
        else:
            verdict = "MINORITY_USAGE"

        return {
            "verdict": verdict,
            "glyph_count": glyph_count,
            "guodian_laozi": guodian_laozi,
            "glyph_paths": paths,
            "sources": sources,
            "pos_distribution": pos_dist,
            "pos_percentages": pos_percentages,
            "dominant_pos": dominant_pos,
            "dominant_pos_english": self.POS_TRANSLATIONS.get(dominant_pos, dominant_pos),
            "total_pos_instances": total_pos,
            "last_validated": datetime.utcnow().isoformat() + "Z"
        }

    def link_chubs_to_entry(self, character: str, author: str = "chubs_integrator") -> Optional[Dict]:
        """
        Validate character with CHUBS and update glossary entry.

        Args:
            character: The character to validate
            author: Who is running the validation

        Returns:
            Updated entry or None if character not in glossary
        """
        if not self.gm.exists(character):
            return None

        validation = self.validate_with_chubs(character)

        return self.gm.update(
            character,
            {"chubs_validation": validation},
            rationale=f"CHUBS validation: {validation['verdict']} ({validation['glyph_count']} glyphs, {validation['total_pos_instances']} POS instances)",
            author=author
        )

    def batch_validate_all(self, author: str = "chubs_integrator") -> Dict[str, Any]:
        """
        Validate all glossary entries against CHUBS.

        Args:
            author: Who is running the validation

        Returns:
            Summary of validation results
        """
        results = {
            "validated": 0,
            "skipped": 0,
            "verdicts": Counter(),
            "details": {}
        }

        for character in self.gm.all_characters():
            try:
                updated = self.link_chubs_to_entry(character, author)
                if updated:
                    validation = updated.get("chubs_validation", {})
                    verdict = validation.get("verdict", "UNKNOWN")
                    results["verdicts"][verdict] += 1
                    results["validated"] += 1
                    results["details"][character] = {
                        "verdict": verdict,
                        "glyph_count": validation.get("glyph_count", 0),
                        "guodian_laozi": validation.get("guodian_laozi", False)
                    }
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["details"][character] = {"error": str(e)}
                results["skipped"] += 1

        # Convert Counter to dict for JSON serialization
        results["verdicts"] = dict(results["verdicts"])

        return results

    def get_guodian_laozi_characters(self) -> List[str]:
        """
        Get all characters attested in Guodian Laozi manuscripts.

        Returns:
            List of characters found in Guodian Laozi
        """
        guodian = []
        for char, data in self.glyph_mappings.items():
            if data.get("guodian_laozi", False):
                guodian.append(char)
        return sorted(guodian)

    def get_unvalidated_entries(self) -> List[Dict]:
        """
        Get glossary entries without CHUBS validation.

        Returns:
            List of entries needing validation
        """
        unvalidated = []
        for char in self.gm.all_characters():
            entry = self.gm.get(char)
            if entry and not entry.get("chubs_validation"):
                unvalidated.append(entry)
        return unvalidated

    def enrich_from_glyph_mappings(self, character: str) -> Optional[Dict]:
        """
        Enrich entry with glyph mapping data (sources, paths).

        Args:
            character: Character to enrich

        Returns:
            Updated entry or None
        """
        if not self.gm.exists(character):
            return None

        glyph_data = self.glyph_mappings.get(character, {})
        if not glyph_data:
            return None

        # Extract Guodian attestation info from sources
        sources = glyph_data.get("sources", {})
        guodian_sources = {
            k: v for k, v in sources.items()
            if k.startswith("郭店簡")
        }

        updates = {}

        # Update guodian_attestation if relevant
        if guodian_sources:
            guodian_attestation = {
                "attested": True,
                "sources": guodian_sources,
                "total_instances": sum(guodian_sources.values()),
                "in_laozi": glyph_data.get("guodian_laozi", False)
            }
            updates["guodian_attestation"] = guodian_attestation

        if updates:
            return self.gm.update(
                character,
                updates,
                rationale="Enriched from CHUBS glyph mappings",
                author="chubs_integrator"
            )

        return None

    def export_validation_report(self) -> str:
        """
        Generate markdown report of CHUBS validation status.

        Returns:
            Markdown formatted report
        """
        lines = [
            "# CHUBS Validation Report",
            f"\n*Generated: {datetime.utcnow().isoformat()}*\n",
            "## Summary\n"
        ]

        # Count by verdict
        verdicts = Counter()
        guodian_count = 0

        for char in self.gm.all_characters():
            entry = self.gm.get(char)
            if entry:
                chubs = entry.get("chubs_validation", {})
                verdict = chubs.get("verdict", "NOT_VALIDATED")
                verdicts[verdict] += 1
                if chubs.get("guodian_laozi"):
                    guodian_count += 1

        for verdict, count in sorted(verdicts.items()):
            lines.append(f"- **{verdict}**: {count}")

        lines.append(f"\n- **Guodian Laozi**: {guodian_count} characters\n")

        # Detail by character
        lines.append("## Details\n")
        lines.append("| Character | Verdict | Glyphs | Guodian Laozi | Dominant POS |")
        lines.append("|-----------|---------|--------|---------------|--------------|")

        for char in sorted(self.gm.all_characters()):
            entry = self.gm.get(char)
            if not entry:
                continue

            chubs = entry.get("chubs_validation", {})
            verdict = chubs.get("verdict", "—")
            glyph_count = chubs.get("glyph_count", 0)
            guodian = "✓" if chubs.get("guodian_laozi") else ""
            dom_pos = chubs.get("dominant_pos_english", "—")

            lines.append(f"| {char} | {verdict} | {glyph_count} | {guodian} | {dom_pos} |")

        return "\n".join(lines)


def main():
    """Run batch validation."""
    integrator = GlossaryIntegrator()
    print("Running CHUBS batch validation...")
    results = integrator.batch_validate_all()

    print(f"\nValidation complete:")
    print(f"  Validated: {results['validated']}")
    print(f"  Skipped: {results['skipped']}")
    print(f"\nVerdicts:")
    for verdict, count in sorted(results['verdicts'].items()):
        print(f"  {verdict}: {count}")

    # Save combined glossary
    integrator.gm.save_combined()
    print("\nCombined glossary saved.")


if __name__ == "__main__":
    main()
