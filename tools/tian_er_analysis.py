"""
天/而 Ambiguity Analysis for Guodian Laozi A

This module documents and analyzes the systematic visual similarity
between 天 (tiān, "heaven") and 而 (ér, "and/but") in Chu bamboo slip script.

Key finding: When 而 is written quickly, its two horizontal top strokes
can merge into one, making it visually identical to 天.

Distinguishing features (when clear):
- 天: Single horizontal top stroke, arms/legs radiating below
- 而: Double horizontal strokes at top (like =), lines radiating below

CHUBS acknowledges this with an explicit 天（而）folder for ambiguous cases.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class GlyphInstance:
    """A single glyph instance with provenance."""
    character: str
    slip: int
    position: int
    path: str
    classification: str  # 'clear', 'ambiguous', 'needs_review'
    notes: str = ""


class TianErAnalyzer:
    """Analyze 天/而 ambiguity in Guodian Laozi A."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.chubs_glyphs = self.project_root / "data" / "CHUBS_repo" / "glyphs"
        self.guodian_folder = self.project_root / "data" / "ddj" / "Guodian Strip Glyphs"

        # Manual classifications based on visual analysis
        # Format: (slip, position) -> ('clear_tian', 'clear_er', 'ambiguous', 'er_variant')
        self.visual_classifications = {
            # 天 folder instances - CLEAR
            (15, 9): ('clear_tian', '天: single top bar, clear arms/legs'),
            (18, 17): ('clear_tian', '天: single top bar'),
            (19, 9): ('clear_tian', '天: clear single bar'),
            (21, 6): ('clear_tian', '天: single top bar'),
            (22, 16): ('clear_tian', '天: clear single bar'),
            (24, 18): ('clear_tian', '天: very clear single bar'),

            # 而 folder instances - CLEAR (double bar visible)
            (12, 30): ('clear_er', '而: double top bar clearly visible, fan-like'),
            (13, 13): ('clear_er', '而: double bar, fan-like strokes'),
            (13, 20): ('clear_er', '而: double bar visible, fan-like'),
            (17, 17): ('clear_er', '而: double bar clear'),

            # 而 folder instances - VARIANT FORM (looping top)
            (17, 27): ('er_variant', '而: curved/looping top variant, distinctive'),

            # 而 folder instances - AMBIGUOUS (looks like 天)
            (17, 22): ('ambiguous', '而 classified but double bar barely visible'),
            (23, 24): ('ambiguous', '而 classified but looks like 天'),
            (28, 9): ('ambiguous', '而 classified but single top bar visible'),

            # Explicit ambiguous folder
            (19, 22): ('explicit_ambiguous', 'CHUBS marked as 天（而）'),
        }

    def get_all_instances(self) -> Dict[str, List[GlyphInstance]]:
        """Get all 天 and 而 instances from CHUBS Laozi A folders."""
        instances = {'天': [], '而': [], '天（而）': []}

        for char_folder in ['天', '而', '天（而）']:
            folder = self.chubs_glyphs / char_folder
            if not folder.exists():
                continue

            for img in folder.glob('*.png'):
                if '老子甲' not in img.name:
                    continue

                # Parse slip and position from filename
                import re
                match = re.search(r'老子甲_(\d+)_01A-\d+-(\d+)', img.name)
                if match:
                    slip = int(match.group(1))
                    pos = int(match.group(2))

                    # Get classification if we have one
                    classification = 'unreviewed'
                    notes = ''
                    if (slip, pos) in self.visual_classifications:
                        classification, notes = self.visual_classifications[(slip, pos)]

                    instances[char_folder].append(GlyphInstance(
                        character=char_folder,
                        slip=slip,
                        position=pos,
                        path=str(img),
                        classification=classification,
                        notes=notes
                    ))

        return instances

    def generate_report(self) -> str:
        """Generate analysis report."""
        instances = self.get_all_instances()

        report = []
        report.append("=" * 60)
        report.append("天/而 AMBIGUITY ANALYSIS - GUODIAN LAOZI A")
        report.append("=" * 60)
        report.append("")
        report.append("BACKGROUND:")
        report.append("- 天 (tiān): heaven, sky - single horizontal top stroke")
        report.append("- 而 (ér): and, but, yet - double horizontal top strokes")
        report.append("- In Chu script, 而's double bar often merges into single stroke")
        report.append("")

        report.append("CORPUS STATISTICS:")
        report.append(f"- 天 folder: {len(instances['天'])} Laozi A instances")
        report.append(f"- 而 folder: {len(instances['而'])} Laozi A instances")
        report.append(f"- 天（而）folder: {len(instances['天（而）'])} explicitly ambiguous")
        report.append("")

        report.append("VISUAL CLASSIFICATION RESULTS:")
        report.append("-" * 40)

        # Count by classification
        counts = {'clear_tian': 0, 'clear_er': 0, 'er_variant': 0,
                  'ambiguous': 0, 'explicit_ambiguous': 0, 'unreviewed': 0}

        for char, char_instances in instances.items():
            for inst in char_instances:
                counts[inst.classification] += 1

        report.append(f"Clear 天: {counts['clear_tian']}")
        report.append(f"Clear 而 (double bar): {counts['clear_er']}")
        report.append(f"而 variant (looping top): {counts['er_variant']}")
        report.append(f"Ambiguous (looks like opposite): {counts['ambiguous']}")
        report.append(f"CHUBS marked ambiguous: {counts['explicit_ambiguous']}")
        report.append(f"Unreviewed: {counts['unreviewed']}")
        report.append("")

        report.append("AMBIGUOUS INSTANCES (need verification):")
        report.append("-" * 40)
        for char, char_instances in instances.items():
            for inst in char_instances:
                if 'ambiguous' in inst.classification:
                    report.append(f"  Slip {inst.slip} pos {inst.position}: "
                                f"classified as {char}, {inst.notes}")

        report.append("")
        report.append("DISTINGUISHING FEATURES:")
        report.append("-" * 40)
        report.append("天 (clear cases):")
        report.append("  - Single horizontal stroke at top")
        report.append("  - Two curved 'arms' extending down/outward")
        report.append("  - Two 'legs' below, often straight")
        report.append("")
        report.append("而 (clear cases):")
        report.append("  - TWO horizontal strokes at top (like =)")
        report.append("  - Multiple strokes radiating downward")
        report.append("  - More 'fan-like' overall shape")
        report.append("")
        report.append("而 variant form:")
        report.append("  - Curved/looping element at top")
        report.append("  - Distinctive, less confusable with 天")
        report.append("  - May represent scribal variation")
        report.append("")
        report.append("而 (ambiguous cases):")
        report.append("  - Top strokes merged into single bar")
        report.append("  - Visually indistinguishable from 天")
        report.append("  - Must rely on textual context for identification")

        report.append("")
        report.append("IMPLICATIONS FOR TRANSLATION:")
        report.append("-" * 40)
        report.append("1. Some instances may be systematically misidentified")
        report.append("2. Context is crucial: 天下 (under heaven) vs 而 as conjunction")
        report.append("3. Consider alternative readings for ambiguous positions")
        report.append("4. DDJ phrases affected: 天下, 天地, 而不X, X而Y")

        return "\n".join(report)

    def get_context_dependent_readings(self) -> Dict[Tuple[int, int], Dict]:
        """
        Identify positions where context helps disambiguate.

        天 typically appears in:
        - 天下 (tiānxià, "all under heaven")
        - 天地 (tiāndì, "heaven and earth")
        - 天門 (tiānmén, "gates of heaven")

        而 typically appears as:
        - Conjunction between clauses: X而Y ("X and/but Y")
        - 而不X ("but not X")
        """
        # This would need chapter transcription data to implement fully
        # Placeholder for context analysis
        return {}

    def export_for_atlas(self) -> Dict:
        """Export data for the glyph atlas to show ambiguity warnings."""
        instances = self.get_all_instances()

        ambiguous_positions = []
        for char, char_instances in instances.items():
            for inst in char_instances:
                if 'ambiguous' in inst.classification:
                    ambiguous_positions.append({
                        'slip': inst.slip,
                        'position': inst.position,
                        'current_classification': char,
                        'notes': inst.notes,
                        'path': inst.path
                    })

        return {
            'analysis_type': '天而_ambiguity',
            'total_tian': len(instances['天']),
            'total_er': len(instances['而']),
            'ambiguous_count': len(ambiguous_positions),
            'ambiguous_instances': ambiguous_positions
        }


def main():
    analyzer = TianErAnalyzer()

    print(analyzer.generate_report())

    print("\n" + "=" * 60)
    print("EXPORTING FOR ATLAS...")
    print("=" * 60)

    export = analyzer.export_for_atlas()

    output_path = Path(__file__).parent.parent / "output" / "tian_er_analysis.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print(f"Exported to: {output_path}")


if __name__ == "__main__":
    main()
