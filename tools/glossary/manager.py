"""
GlossaryManager: Central manager for the Living Glossary.

Single source of truth for character translations with:
- Full version history tracking
- Dual-hypothesis support (standard vs. agricultural)
- CHUBS validation integration
- Font data linking
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any, Union
import copy


class GlossaryManager:
    """
    Central manager for the Living Glossary.
    Single source of truth for character translations.
    """

    def __init__(self, glossary_dir: Optional[Path] = None):
        """
        Initialize the GlossaryManager.

        Args:
            glossary_dir: Path to glossary directory. Defaults to data/glossary/
        """
        if glossary_dir is None:
            # Default to project's data/glossary directory
            self.glossary_dir = Path(__file__).parent.parent.parent / "data" / "glossary"
        else:
            self.glossary_dir = Path(glossary_dir)

        self.entries_dir = self.glossary_dir / "entries"
        self.schema_path = self.glossary_dir / "schema.json"
        self.history_path = self.glossary_dir / "history.jsonl"

        self._schema = None
        self._cache: Dict[str, Dict] = {}

        # Ensure directories exist
        self.entries_dir.mkdir(parents=True, exist_ok=True)

    @property
    def schema(self) -> dict:
        """Lazy-load and cache schema."""
        if self._schema is None:
            if self.schema_path.exists():
                with open(self.schema_path, encoding='utf-8') as f:
                    self._schema = json.load(f)
            else:
                self._schema = {}
        return self._schema

    # === CRUD Operations ===

    def get(self, character: str) -> Optional[Dict]:
        """
        Get entry for a character.

        Args:
            character: The Chinese character to look up

        Returns:
            Entry dict or None if not found
        """
        if character in self._cache:
            return copy.deepcopy(self._cache[character])

        path = self._entry_path(character)
        if not path.exists():
            return None

        with open(path, encoding='utf-8') as f:
            entry = json.load(f)

        self._cache[character] = entry
        return copy.deepcopy(entry)

    def exists(self, character: str) -> bool:
        """Check if an entry exists for a character."""
        return self._entry_path(character).exists()

    def create(self, entry: Dict, author: str = "system") -> Dict:
        """
        Create new glossary entry.

        Args:
            entry: Entry data (must include 'character' field)
            author: Who is creating the entry

        Returns:
            The created entry

        Raises:
            ValueError: If entry already exists or character field missing
        """
        if "character" not in entry:
            raise ValueError("Entry must include 'character' field")

        character = entry["character"]

        if self.exists(character):
            raise ValueError(f"Entry already exists for {character}")

        # Add timestamps
        now = datetime.utcnow().isoformat() + "Z"
        entry["created"] = now
        entry["modified"] = now

        # Ensure history array exists
        if "history" not in entry:
            entry["history"] = []

        # Add creation event to history
        entry["history"].append({
            "date": now,
            "field": "created",
            "from": None,
            "to": "initial_entry",
            "rationale": "Entry created",
            "author": author
        })

        # Ensure unicode field
        if "unicode" not in entry:
            entry["unicode"] = f"U+{ord(character):04X}"

        # Save
        self._save_entry(entry)
        self._log_history({
            "action": "create",
            "character": character,
            "date": now,
            "author": author
        })

        self._cache[character] = entry
        return copy.deepcopy(entry)

    def update(self, character: str, updates: Dict[str, Any],
               rationale: str, author: str = "system",
               evidence: Optional[List[str]] = None) -> Dict:
        """
        Update entry with full history tracking.

        Args:
            character: Character to update
            updates: Dict of {field_path: new_value} (dot notation supported)
            rationale: Why this update is being made
            author: Who is making the update
            evidence: Optional list of evidence supporting the update

        Returns:
            The updated entry

        Raises:
            ValueError: If entry doesn't exist
        """
        entry = self.get(character)
        if not entry:
            raise ValueError(f"No entry for {character}")

        now = datetime.utcnow().isoformat() + "Z"

        for field_path, new_value in updates.items():
            # Get old value
            old_value = self._get_nested(entry, field_path)

            # Record in history
            history_entry = {
                "date": now,
                "field": field_path,
                "from": self._serialize_value(old_value),
                "to": self._serialize_value(new_value),
                "rationale": rationale,
                "author": author
            }
            if evidence:
                history_entry["evidence"] = evidence

            entry["history"].append(history_entry)

            # Apply update
            self._set_nested(entry, field_path, new_value)

        entry["modified"] = now

        # Save
        self._save_entry(entry)
        self._invalidate_cache(character)

        return self.get(character)

    def update_confidence(self, character: str,
                          confidence: str,
                          score: float,
                          evidence: List[str],
                          author: str = "system") -> Dict:
        """
        Update confidence level with evidence.

        Args:
            character: Character to update
            confidence: One of 'tested', 'provisional', 'speculative'
            score: Numerical score 0-1
            evidence: List of evidence supporting the confidence level
            author: Who is making the update

        Returns:
            The updated entry
        """
        return self.update(
            character,
            {
                "confidence": confidence,
                "confidence_score": score
            },
            rationale=f"Confidence updated based on: {', '.join(evidence)}",
            author=author,
            evidence=evidence
        )

    def link_font_data(self, character: str,
                       vector_path: str,
                       source_images: List[Dict],
                       extracted_features: Optional[Dict],
                       tracing_metadata: Dict) -> Dict:
        """
        Link font tracing data to glossary entry.

        Args:
            character: Character to update
            vector_path: Path to SVG vector file
            source_images: List of source image metadata
            extracted_features: Extracted geometric features
            tracing_metadata: Tracing session metadata

        Returns:
            The updated entry
        """
        updates = {
            "font_data.traced": True,
            "font_data.vector_path": vector_path,
            "font_data.source_images": source_images,
            "font_data.tracing_metadata": tracing_metadata
        }

        if extracted_features:
            updates["font_data.extracted_features"] = extracted_features

        return self.update(
            character,
            updates,
            rationale="Font glyph traced and features extracted",
            author=tracing_metadata.get("traced_by", "system")
        )

    def link_chubs_validation(self, character: str,
                              validation_data: Dict) -> Dict:
        """
        Link CHUBS validation data.

        Args:
            character: Character to update
            validation_data: CHUBS validation results

        Returns:
            The updated entry
        """
        return self.update(
            character,
            {"chubs_validation": validation_data},
            rationale="CHUBS POS validation updated",
            author="chubs_validator"
        )

    def delete(self, character: str, author: str = "system") -> bool:
        """
        Delete an entry.

        Args:
            character: Character to delete
            author: Who is deleting

        Returns:
            True if deleted, False if not found
        """
        path = self._entry_path(character)
        if not path.exists():
            return False

        # Log deletion
        now = datetime.utcnow().isoformat() + "Z"
        self._log_history({
            "action": "delete",
            "character": character,
            "date": now,
            "author": author
        })

        path.unlink()
        self._invalidate_cache(character)
        return True

    # === Query Operations ===

    def all_characters(self) -> List[str]:
        """List all characters with entries."""
        characters = []
        for path in self.entries_dir.glob("U+*.json"):
            # Extract character from filename (U+XXXX_char.json)
            parts = path.stem.split('_', 1)
            if len(parts) >= 2:
                characters.append(parts[1])
        return sorted(characters)

    def count(self) -> int:
        """Count total entries."""
        return len(list(self.entries_dir.glob("U+*.json")))

    def by_confidence(self, level: str) -> List[Dict]:
        """
        Get all entries with given confidence level.

        Args:
            level: One of 'tested', 'provisional', 'speculative'

        Returns:
            List of matching entries
        """
        results = []
        for char in self.all_characters():
            entry = self.get(char)
            if entry and entry.get("confidence") == level:
                results.append(entry)
        return results

    def by_radical(self, radical: str) -> List[Dict]:
        """
        Get all entries containing a radical.

        Args:
            radical: The radical to search for

        Returns:
            List of matching entries
        """
        results = []
        for char in self.all_characters():
            entry = self.get(char)
            if not entry:
                continue

            decomp = entry.get("radical_decomposition", {})

            # Check standard components
            standard = decomp.get("standard", {}).get("components", [])
            if any(c.get("component") == radical for c in standard):
                results.append(entry)
                continue

            # Check agricultural components
            agricultural = decomp.get("agricultural", {}).get("components", [])
            if any(c.get("component") == radical for c in agricultural):
                results.append(entry)

        return results

    def untraced_characters(self) -> List[Dict]:
        """Get entries without font data."""
        results = []
        for char in self.all_characters():
            entry = self.get(char)
            if entry and not entry.get("font_data", {}).get("traced"):
                results.append(entry)
        return results

    def needs_validation(self, days_old: int = 30) -> List[Dict]:
        """
        Get entries that need CHUBS validation refresh.

        Args:
            days_old: Consider stale if validated more than this many days ago

        Returns:
            List of entries needing validation
        """
        cutoff = datetime.utcnow()
        results = []

        for char in self.all_characters():
            entry = self.get(char)
            if not entry:
                continue

            chubs = entry.get("chubs_validation")
            if not chubs:
                results.append(entry)
                continue

            last = chubs.get("last_validated", "")
            if not last:
                results.append(entry)
                continue

            try:
                last_date = datetime.fromisoformat(last.replace("Z", "+00:00"))
                if (cutoff - last_date.replace(tzinfo=None)).days > days_old:
                    results.append(entry)
            except (ValueError, TypeError):
                results.append(entry)

        return results

    def tier_1_characters(self) -> List[Dict]:
        """Get Tier 1 hypothesis-bearing characters."""
        tier_1 = ["道", "德", "自", "反", "弱", "者"]
        return [self.get(c) for c in tier_1 if self.exists(c)]

    def by_semantic_field(self, field: str) -> List[Dict]:
        """Get entries by semantic field."""
        results = []
        for char in self.all_characters():
            entry = self.get(char)
            if entry and entry.get("semantic_field") == field:
                results.append(entry)
        return results

    # === Export Operations ===

    def export_combined(self) -> Dict[str, Dict]:
        """Export all entries as single dict."""
        return {c: self.get(c) for c in self.all_characters()}

    def export_for_translations(self) -> Dict[str, Dict]:
        """
        Export format compatible with existing validated_characters.json.

        Returns:
            Dict in legacy format for backwards compatibility
        """
        result = {}
        for char in self.all_characters():
            entry = self.get(char)
            if entry:
                result[char] = {
                    "traditional": entry.get("current_translation", {}).get("traditional", ""),
                    "geometric": entry.get("current_translation", {}).get("structural", ""),
                    "structure": self._format_structure(entry),
                    "validation": entry.get("confidence", ""),
                    "radical_family": self._format_radical_family(entry)
                }
        return result

    def save_combined(self, output_path: Optional[Path] = None) -> Path:
        """
        Save combined glossary to file.

        Args:
            output_path: Where to save. Defaults to data/glossary/glossary.json

        Returns:
            Path to saved file
        """
        if output_path is None:
            output_path = self.glossary_dir / "glossary.json"

        combined = self.export_combined()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)

        return output_path

    # === History Operations ===

    def get_history(self, character: str) -> List[Dict]:
        """Get version history for a character."""
        entry = self.get(character)
        if not entry:
            return []
        return entry.get("history", [])

    def get_field_history(self, character: str, field: str) -> List[Dict]:
        """Get history for a specific field."""
        history = self.get_history(character)
        return [h for h in history if h.get("field") == field]

    # === Private Helpers ===

    def _entry_path(self, character: str) -> Path:
        """Get file path for character entry."""
        codepoint = f"U+{ord(character):04X}"
        return self.entries_dir / f"{codepoint}_{character}.json"

    def _save_entry(self, entry: Dict):
        """Save entry to disk."""
        path = self._entry_path(entry["character"])
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

    def _invalidate_cache(self, character: str):
        """Remove from cache."""
        self._cache.pop(character, None)

    def _log_history(self, event: Dict):
        """Append to global history log."""
        with open(self.history_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _get_nested(self, obj: Dict, path: str) -> Any:
        """Get nested value by dot-separated path."""
        keys = path.split('.')
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                return None
        return obj

    def _set_nested(self, obj: Dict, path: str, value: Any):
        """Set nested value by dot-separated path."""
        keys = path.split('.')
        for key in keys[:-1]:
            obj = obj.setdefault(key, {})
        obj[keys[-1]] = value

    def _serialize_value(self, value: Any) -> Optional[str]:
        """Serialize value for history storage."""
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return str(value)
        return json.dumps(value, ensure_ascii=False)

    def _format_structure(self, entry: Dict) -> str:
        """Format radical decomposition as string."""
        decomp = entry.get("radical_decomposition", {})
        preferred = decomp.get("preferred", "standard")
        source = decomp.get(preferred or "standard", {})
        components = source.get("components", [])

        if not components:
            return ""

        parts = []
        for c in components:
            comp = c.get("component", "")
            meaning = c.get("meaning", "")
            if meaning:
                parts.append(f"{comp}({meaning})")
            else:
                parts.append(comp)

        return " + ".join(parts)

    def _format_radical_family(self, entry: Dict) -> str:
        """Format primary radical family."""
        decomp = entry.get("radical_decomposition", {})
        standard = decomp.get("standard", {})
        components = standard.get("components", [])

        if components:
            return components[0].get("component", "")
        return ""
