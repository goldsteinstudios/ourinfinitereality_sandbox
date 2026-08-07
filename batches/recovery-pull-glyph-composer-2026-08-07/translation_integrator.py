#!/usr/bin/env python3
"""
Translation Integration System
Bidirectionally sync draft translations with test validation corpus
"""

import re
import os
from pathlib import Path
from collections import defaultdict
import json

# Load validated character corrections from test results
VALIDATED_CHARACTERS = {
    '常': {
        'traditional': 'eternal, constant',
        'geometric': 'implicit, concealed, that which has no interface',
        'structure': '巾(cloth) + 尚(elevated) = covered/hidden',
        'validation': 'TEST1',
        'radical_family': 'cloth/covering'
    },
    '欲': {
        'traditional': 'desire, craving (moral weakness)',
        'geometric': 'directed orientation, tendency toward',
        'structure': '谷(valley) + 欠(opening) = flow toward gap',
        'validation': 'TEST1',
        'radical_family': 'mouth/opening'
    },
    '利': {
        'traditional': 'benefit, advantage',
        'geometric': 'constraint, path-cutting through field',
        'structure': '禾(grain) + 刀(knife) = paths cut through distributed resource',
        'validation': 'TEST6, TEST7',
        'radical_family': 'grain (禾)'
    },
    '仁': {
        'traditional': 'benevolence, humaneness',
        'geometric': 'relational accommodation between two entities',
        'structure': '人(person) + 二(two) = two-body configuration',
        'validation': 'TEST1',
        'radical_family': 'person'
    },
    '反': {
        'traditional': 'return, oppose',
        'geometric': 'reversal, oscillation, unitary conjugation',
        'structure': '又(hand) + 厂(cliff) = turning back at boundary',
        'validation': 'TEST1, TEST2',
        'radical_family': 'hand/motion'
    },
    '弱': {
        'traditional': 'weak, feeble',
        'geometric': 'flexible, indefinite, superposition state',
        'structure': '弓+弓 (double bow) = flexible tension',
        'validation': 'TEST1, TEST2',
        'radical_family': 'bow/flexibility'
    },
    '德': {
        'traditional': 'virtue, moral character',
        'geometric': 'straight path in internal-state motion',
        'structure': '彳(step) + 直(straight) + 心(internal) = aligned dynamics',
        'validation': 'TEST9',
        'radical_family': 'heart (心) + motion (彳)'
    },
    '慈': {
        'traditional': 'compassion, kindness',
        'geometric': 'expansive internal state (multiplication operator)',
        'structure': '心(heart) + 茲(multiply) = generative pressure',
        'validation': 'TEST9',
        'radical_family': 'heart (心)'
    },
    '愛': {
        'traditional': 'love, affection',
        'geometric': 'attractive bonding force between states',
        'structure': '心(heart) + 友(friend) = bonded configuration',
        'validation': 'TEST9',
        'radical_family': 'heart (心)'
    },
    '惡': {
        'traditional': 'evil, wickedness',
        'geometric': 'degraded state mode, inferior configuration',
        'structure': '心(heart) + 亞(inferior) = sub-optimal point',
        'validation': 'TEST9',
        'radical_family': 'heart (心)'
    },
    '治': {
        'traditional': 'govern, rule',
        'geometric': 'channeling flow through constructed platform',
        'structure': '氵(water) + 台(platform) = directing fluid',
        'validation': 'TEST8',
        'radical_family': 'water (氵)',
        'note': '13 occurrences - most frequent! Governance IS flow management'
    },
    '清': {
        'traditional': 'pure, clear',
        'geometric': 'transparent medium, light unimpeded through fluid',
        'structure': '氵(water) + 青(blue/pure) = clarity',
        'validation': 'TEST8',
        'radical_family': 'water (氵)'
    },
    '和': {
        'traditional': 'harmony, peace',
        'geometric': 'distribution through opening, flow equilibrium',
        'structure': '禾(grain) + 口(mouth/opening) = distributed flow',
        'validation': 'TEST7',
        'radical_family': 'grain (禾)'
    },
    '名': {
        'traditional': 'name, reputation',
        'geometric': 'explicit, manifest, that which has interface',
        'structure': '夕(evening) + 口(mouth) = called into presence',
        'validation': 'TEST1',
        'radical_family': 'mouth/calling'
    },
    '非': {
        'traditional': 'not, wrong',
        'geometric': 'complementary pair, dual aspects',
        'structure': 'Two mirrored elements showing duality',
        'validation': 'TEST1',
        'radical_family': 'symmetry'
    },
    '玄': {
        'traditional': 'mysterious, profound',
        'geometric': 'dark/subtle entry point, inaccessible boundary',
        'structure': 'Threading/subtle connection',
        'validation': 'TEST1',
        'radical_family': 'thread'
    },
}

# Radical families from test validations
RADICAL_FAMILIES = {
    '禾': {
        'substrate': 'discrete resource domain',
        'operations': 10,
        'test': 'TEST7',
        'examples': ['利', '和', '私', '稱', '穀', '稷', '秀', '秋', '季', '委']
    },
    '氵': {
        'substrate': 'continuous fluid domain',
        'operations': 20,
        'test': 'TEST8',
        'examples': ['治', '清', '深', '海', '江', '沖', '淵', '渙', '渾', '湛']
    },
    '心': {
        'substrate': 'internal state space',
        'operations': 16,
        'test': 'TEST9',
        'examples': ['德', '慈', '愛', '惡', '恐', '忘', '思']
    }
}


class TranslationIntegrator:
    def __init__(self, translations_dir='translations/chapters'):
        self.translations_dir = Path(translations_dir)
        self.translations = {}
        self.coverage_map = defaultdict(list)

    def parse_translation(self, chapter_file):
        """Parse a chapter translation file"""
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract chapter number
        chapter_num = re.search(r'Chapter (\d+)', content)
        chapter_num = int(chapter_num.group(1)) if chapter_num else None

        # Find all Chinese characters in the translation
        chinese_chars = set(re.findall(r'[\u4e00-\u9fff]', content))

        # Identify which validated characters are used
        used_validations = {}
        for char in chinese_chars:
            if char in VALIDATED_CHARACTERS:
                used_validations[char] = VALIDATED_CHARACTERS[char]

        # Identify radical families present
        radical_usage = defaultdict(list)
        for char in chinese_chars:
            for radical, data in RADICAL_FAMILIES.items():
                if char in data['examples']:
                    radical_usage[radical].append(char)

        return {
            'chapter': chapter_num,
            'file': chapter_file,
            'chinese_chars': chinese_chars,
            'validated_chars_used': used_validations,
            'radical_families': dict(radical_usage),
            'content': content
        }

    def extract_new_insights(self, translation_data):
        """Identify patterns in translation not yet in corpus"""
        new_insights = []

        content = translation_data['content']

        # Look for geometric interpretations mentioned
        geometric_patterns = re.findall(
            r'(?:geometric|operation|transformation|substrate):\s*([^\n]+)',
            content,
            re.IGNORECASE
        )

        # Look for character structures mentioned
        structures = re.findall(
            r'(\S+)\s*=\s*(\S+)\s*\+\s*(\S+)',
            content
        )

        for pattern in geometric_patterns:
            new_insights.append({
                'type': 'geometric_pattern',
                'description': pattern.strip()
            })

        for struct in structures:
            char, comp1, comp2 = struct
            if char not in VALIDATED_CHARACTERS:
                new_insights.append({
                    'type': 'new_structure',
                    'character': char,
                    'components': f"{comp1} + {comp2}"
                })

        return new_insights

    def generate_coverage_report(self):
        """Generate report showing which validations appear in which chapters"""
        report = []
        report.append("=" * 70)
        report.append("TRANSLATION-CORPUS INTEGRATION REPORT")
        report.append("=" * 70)
        report.append("")

        # Coverage by character
        report.append("VALIDATED CHARACTER USAGE ACROSS CHAPTERS:")
        report.append("-" * 70)

        char_coverage = defaultdict(list)
        for trans_data in self.translations.values():
            ch = trans_data['chapter']
            for char in trans_data['validated_chars_used'].keys():
                char_coverage[char].append(ch)

        for char in sorted(VALIDATED_CHARACTERS.keys()):
            data = VALIDATED_CHARACTERS[char]
            chapters = sorted(char_coverage.get(char, []))
            status = f"✓ {len(chapters)} chapters" if chapters else "✗ not used yet"

            report.append(f"\n{char} ({data['validation']}): {status}")
            report.append(f"  Traditional: {data['traditional']}")
            report.append(f"  Geometric: {data['geometric']}")
            if chapters:
                report.append(f"  Appears in chapters: {', '.join(map(str, chapters))}")

        # Radical family coverage
        report.append("\n" + "=" * 70)
        report.append("RADICAL FAMILY USAGE:")
        report.append("-" * 70)

        for radical, data in RADICAL_FAMILIES.items():
            report.append(f"\n{radical} - {data['substrate']}")
            report.append(f"  Validation: {data['test']} ({data['operations']} operations)")

            # Count usage across translations
            total_usage = 0
            for trans_data in self.translations.values():
                if radical in trans_data['radical_families']:
                    total_usage += len(trans_data['radical_families'][radical])

            report.append(f"  Usage: {total_usage} character instances across translations")

        return "\n".join(report)

    def suggest_updates(self, chapter_file):
        """Suggest updates to a translation based on corpus"""
        trans_data = self.parse_translation(chapter_file)
        suggestions = []

        suggestions.append(f"SUGGESTED UPDATES FOR CHAPTER {trans_data['chapter']}")
        suggestions.append("=" * 70)
        suggestions.append("")

        # Characters that appear but might not use geometric reading
        for char in trans_data['chinese_chars']:
            if char in VALIDATED_CHARACTERS:
                data = VALIDATED_CHARACTERS[char]
                suggestions.append(f"✓ {char} - Ensure using geometric reading:")
                suggestions.append(f"  '{data['geometric']}' (NOT '{data['traditional']}')")
                suggestions.append(f"  Validated by: {data['validation']}")
                suggestions.append("")

        # Radical patterns that could be highlighted
        for radical, chars in trans_data['radical_families'].items():
            family_data = RADICAL_FAMILIES[radical]
            suggestions.append(f"Pattern: {radical} ({family_data['substrate']})")
            suggestions.append(f"  Found: {', '.join(chars)}")
            suggestions.append(f"  Consider highlighting as {family_data['operations']}-operation family")
            suggestions.append("")

        return "\n".join(suggestions)


def main():
    """Interactive integration workflow"""
    integrator = TranslationIntegrator()

    print("Translation Integration System")
    print("=" * 70)
    print()
    print("This tool helps integrate your draft translations with")
    print("the validated test corpus (Tests 1-9).")
    print()
    print("Options:")
    print("  1. Parse existing translations")
    print("  2. Generate coverage report")
    print("  3. Get update suggestions for specific chapter")
    print("  4. Export validated character reference")
    print()

    # Export validated characters for easy reference
    os.makedirs('analysis', exist_ok=True)
    with open('analysis/validated_characters.json', 'w', encoding='utf-8') as f:
        json.dump(VALIDATED_CHARACTERS, f, indent=2, ensure_ascii=False)

    print("✓ Exported validated_characters.json")
    print()
    print("Ready to process translations. Place chapter files in:")
    print("  translations/chapters/chapterXX.md")


if __name__ == '__main__':
    main()
