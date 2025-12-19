"""
Transcription Generator: Create draft transcriptions for all Guodian Laozi chapters.

Uses CHUBS reverse-mapping data to:
1. Generate slip-by-slip character sequences
2. Group by chapter
3. Apply phonetic loan mappings
4. Flag uncertain positions for manual review
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime

from chubs_reverse_mapper import ChubsReverseMapper
from corrections_manager import CorrectionsManager


class TranscriptionGenerator:
    """Generate draft transcriptions from CHUBS glyph index."""

    # Phonetic loans: guodian_char → received_char
    PHONETIC_LOANS = {
        # Confirmed loans from Guodian scholarship
        "返": "反",      # fǎn - return/reversal
        "溺": "弱",      # ruò - weak/yielding
        "僮": "動",      # dòng - movement
        "甬": "用",      # yòng - use/function
        "又": "有",      # yǒu - existence
        "亡": "無",      # wú - non-existence
        "勿": "物",      # wù - things
        "恆": "常",      # cháng - constant (Han taboo)
        "潰": "逝",      # shì - overflow/depart

        # Graphic variants (same character, different form)
        "亓": "其",      # qí - its/that
        "㠯": "以",      # yǐ - by/with
        "智": "知",      # zhī - know (variant)
        "唬": "乎",      # hū - question particle
        "肰": "然",      # rán - thus/so
        "舊": "久",      # jiǔ - long time
        "浧": "盈",      # yíng - full
        "埶": "勢",      # shì - force/power

        # Less common loans
        "女": "如",      # rú - like/as
        "谷": "欲",      # yù - desire (context-dependent)
        "奴": "若",      # ruò - like/if
        "才": "在",      # zài - at/in
        "城": "成",      # chéng - become
        "拃": "作",      # zuò - make/do
        "浴": "谷",      # gǔ - valley
    }

    # Slip-to-chapter mapping (from guodian_glyph_mapper.py)
    SLIP_CHAPTERS = {
        1: [(19, 1, 30)],
        2: [(46, 1, 31)],
        3: [(66, 1, 31)],
        4: [(66, 1, 31)],
        5: [(66, 1, 31)],
        6: [(46, 1, 25), (30, 26, 31)],
        7: [(30, 1, 31)],
        8: [(15, 1, 31)],
        9: [(15, 1, 31)],
        10: [(15, 1, 31)],
        11: [(64, 1, 31)],
        12: [(63, 1, 31)],
        13: [(37, 1, 31)],
        14: [(37, 1, 34)],
        15: [(2, 1, 33)],
        16: [(2, 1, 31)],
        17: [(2, 1, 31)],
        18: [(32, 1, 25)],
        19: [(32, 1, 29)],
        20: [(32, 1, 31)],
        21: [(25, 1, 31)],
        22: [(25, 1, 31)],
        23: [(25, 1, 31), (5, 20, 31)],
        24: [(16, 1, 31)],
        25: [(64, 1, 31)],
        26: [(64, 1, 16)],
        27: [(56, 1, 31)],
        28: [(56, 1, 31)],
        29: [(56, 1, 10), (57, 11, 31)],
        30: [(57, 1, 31)],
        31: [(57, 1, 31)],
        32: [(57, 1, 22)],
        33: [(55, 1, 31)],
        34: [(55, 1, 31)],
        35: [(55, 1, 20), (44, 21, 31)],
        36: [(44, 1, 31)],
        37: [(40, 1, 29)],
        38: [(9, 1, 25)],
        39: [(9, 1, 20)],
    }

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.mapper = ChubsReverseMapper()
        self.glyph_index = self.mapper.build_glyph_index()
        self.corrections = CorrectionsManager()

    def get_received_char(self, guodian_char: str) -> str:
        """Map Guodian character to received text equivalent."""
        return self.PHONETIC_LOANS.get(guodian_char, guodian_char)

    def get_chapter_slips(self, chapter_num: int) -> List[int]:
        """Get list of slips containing a chapter."""
        slips = []
        for slip, mappings in self.SLIP_CHAPTERS.items():
            for ch, start, end in mappings:
                if ch == chapter_num:
                    slips.append(slip)
        return sorted(set(slips))

    def get_all_chapters(self) -> List[int]:
        """Get list of all chapters in Guodian Laozi A."""
        chapters = set()
        for slip, mappings in self.SLIP_CHAPTERS.items():
            for ch, start, end in mappings:
                chapters.add(ch)
        return sorted(chapters)

    def generate_slip_transcription(self, slip_num: int) -> Dict:
        """
        Generate transcription for a single slip.

        Returns:
            {
                "slip": 37,
                "positions": [
                    {
                        "position": 5,
                        "guodian_char": "返",
                        "received_char": "反",
                        "is_loan": True,
                        "is_undefined": False,
                        "confidence": "high",
                        "needs_review": False,
                        "path": "..."
                    },
                    ...
                ],
                "guodian_text": "返也者道...",
                "received_text": "反者道之...",
                "review_needed": [...]
            }
        """
        slip_glyphs = self.mapper.get_slip_transcription(slip_num)

        positions = []
        guodian_chars = []
        received_chars = []
        review_needed = []

        for glyph in slip_glyphs:
            position = glyph["position"]

            # Check for manual correction first
            correction = self.corrections.get_correction(slip_num, position)
            if correction:
                guodian_char = correction["guodian"]
                received_char = correction.get("received")
                is_corrected = True
            else:
                guodian_char = glyph["guodian_char"]
                received_char = self.get_received_char(guodian_char)
                is_corrected = False

            is_loan = guodian_char != received_char if received_char else False
            is_undefined = glyph["is_undefined"] and not is_corrected
            needs_review = (is_undefined or glyph.get("ambiguous", False)) and not is_corrected

            # Particles (也) have no received equivalent in many cases
            is_particle = guodian_char == "也"

            pos_entry = {
                "position": position,
                "guodian_char": guodian_char,
                "received_char": received_char if not is_particle else None,
                "is_loan": is_loan,
                "is_particle": is_particle,
                "is_undefined": is_undefined,
                "is_corrected": is_corrected,
                "confidence": "manual" if is_corrected else glyph["confidence"],
                "needs_review": needs_review,
                "folder": glyph["folder"],
                "path": glyph.get("path", "")
            }

            positions.append(pos_entry)
            guodian_chars.append(guodian_char)

            if is_particle:
                # Don't include particles in received text
                pass
            else:
                received_chars.append(received_char)

            if needs_review:
                review_needed.append({
                    "position": glyph["position"],
                    "guodian_char": guodian_char,
                    "reason": "undefined" if is_undefined else "ambiguous"
                })

        return {
            "slip": slip_num,
            "positions": positions,
            "guodian_text": "".join(guodian_chars),
            "received_text": "".join(received_chars),
            "review_needed": review_needed,
            "total_glyphs": len(positions),
            "undefined_count": sum(1 for p in positions if p["is_undefined"]),
            "loan_count": sum(1 for p in positions if p["is_loan"] and not p["is_undefined"]),
            "corrected_count": sum(1 for p in positions if p.get("is_corrected", False))
        }

    def generate_chapter_transcription(self, chapter_num: int) -> Dict:
        """
        Generate transcription for a chapter (may span multiple slips).

        Returns:
            {
                "chapter": 40,
                "slips": [37],
                "guodian_text": "返也者道僮也...",
                "received_text": "反者道之動弱...",
                "positions": {
                    5: ("返", "反"),  # (guodian_char, received_char)
                    ...
                },
                "verification_status": "auto_generated",
                "review_needed": [...],
                "stats": {...}
            }
        """
        slips = self.get_chapter_slips(chapter_num)

        all_positions = {}
        guodian_text = []
        received_text = []
        review_needed = []
        total_glyphs = 0
        undefined_count = 0
        loan_count = 0
        corrected_count = 0

        for slip_num in slips:
            slip_data = self.generate_slip_transcription(slip_num)

            # Add positions with slip prefix to avoid collision
            for pos in slip_data["positions"]:
                key = (slip_num, pos["position"])
                all_positions[key] = (pos["guodian_char"], pos["received_char"])

            guodian_text.append(slip_data["guodian_text"])
            received_text.append(slip_data["received_text"])
            review_needed.extend([
                {"slip": slip_num, **r} for r in slip_data["review_needed"]
            ])
            total_glyphs += slip_data["total_glyphs"]
            undefined_count += slip_data["undefined_count"]
            loan_count += slip_data["loan_count"]
            corrected_count += slip_data.get("corrected_count", 0)

        return {
            "chapter": chapter_num,
            "slips": slips,
            "guodian_text": "".join(guodian_text),
            "received_text": "".join(received_text),
            "positions": all_positions,
            "verification_status": "auto_generated",
            "generated_date": datetime.now().isoformat(),
            "review_needed": review_needed,
            "stats": {
                "total_glyphs": total_glyphs,
                "undefined_count": undefined_count,
                "loan_count": loan_count,
                "corrected_count": corrected_count,
                "review_count": len(review_needed),
                "auto_confidence": (total_glyphs - len(review_needed)) / total_glyphs if total_glyphs > 0 else 0
            }
        }

    def generate_all_transcriptions(self) -> Dict:
        """Generate transcriptions for all chapters."""
        chapters = self.get_all_chapters()
        transcriptions = {}

        for chapter in chapters:
            transcriptions[chapter] = self.generate_chapter_transcription(chapter)

        return transcriptions

    def export_transcriptions(self, output_path: Optional[Path] = None) -> Path:
        """Export all transcriptions to JSON file."""
        if output_path is None:
            output_path = self.project_root / "data" / "ddj" / "draft_transcriptions.json"

        transcriptions = self.generate_all_transcriptions()

        # Convert tuple keys to strings for JSON
        for chapter, data in transcriptions.items():
            data["positions"] = {
                f"{k[0]}_{k[1]}": v for k, v in data["positions"].items()
            }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcriptions, f, ensure_ascii=False, indent=2)

        return output_path

    def generate_summary_report(self) -> str:
        """Generate summary report of transcription coverage."""
        transcriptions = self.generate_all_transcriptions()

        report = []
        report.append("=" * 60)
        report.append("GUODIAN LAOZI TRANSCRIPTION SUMMARY")
        report.append("=" * 60)
        report.append("")

        total_glyphs = 0
        total_undefined = 0
        total_loans = 0
        total_review = 0

        report.append(f"{'Chapter':>8} {'Slips':<15} {'Glyphs':>6} {'Loans':>6} {'Undef':>6} {'Review':>6} {'Conf':>6}")
        report.append("-" * 60)

        for chapter in sorted(transcriptions.keys()):
            data = transcriptions[chapter]
            stats = data["stats"]
            slips_str = ",".join(str(s) for s in data["slips"])

            conf = f"{stats['auto_confidence']:.0%}"
            report.append(
                f"{chapter:>8} {slips_str:<15} {stats['total_glyphs']:>6} "
                f"{stats['loan_count']:>6} {stats['undefined_count']:>6} "
                f"{stats['review_count']:>6} {conf:>6}"
            )

            total_glyphs += stats["total_glyphs"]
            total_undefined += stats["undefined_count"]
            total_loans += stats["loan_count"]
            total_review += stats["review_count"]

        report.append("-" * 60)
        report.append(
            f"{'TOTAL':>8} {'':<15} {total_glyphs:>6} "
            f"{total_loans:>6} {total_undefined:>6} "
            f"{total_review:>6} {(total_glyphs - total_review) / total_glyphs:.0%}"
        )

        report.append("")
        report.append(f"Chapters: {len(transcriptions)}")
        report.append(f"Total glyphs: {total_glyphs}")
        report.append(f"Phonetic loans: {total_loans}")
        report.append(f"Undefined (need review): {total_undefined}")
        report.append(f"Overall confidence: {(total_glyphs - total_review) / total_glyphs:.1%}")

        return "\n".join(report)


def main():
    """Generate and export all transcriptions."""
    generator = TranscriptionGenerator()

    print(generator.generate_summary_report())

    print("\n" + "=" * 60)
    output = generator.export_transcriptions()
    print(f"Exported transcriptions to: {output}")

    # Show sample chapter
    print("\n" + "-" * 40)
    print("SAMPLE: CHAPTER 40 (Reference)")
    print("-" * 40)
    ch40 = generator.generate_chapter_transcription(40)
    print(f"Slips: {ch40['slips']}")
    print(f"Guodian: {ch40['guodian_text']}")
    print(f"Received: {ch40['received_text']}")
    print(f"Loans: {ch40['stats']['loan_count']}")
    print(f"Undefined: {ch40['stats']['undefined_count']}")


if __name__ == "__main__":
    main()
