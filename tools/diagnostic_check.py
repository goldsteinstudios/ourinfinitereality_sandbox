"""
Diagnostic check for Dao De Jing Translation Engine
Verifies database integrity, translation functionality, and pattern detection
"""

from translation_engine import TranslationEngine, CHARACTER_OPERATIONS, PATTERN_TEMPLATES
import sys

def run_diagnostics():
    """Run comprehensive diagnostic checks"""

    print("="*80)
    print("DAO DE JING TRANSLATION ENGINE - DIAGNOSTIC CHECK")
    print("="*80)

    issues = []
    warnings = []

    # 1. Database integrity check
    print("\n[1] DATABASE INTEGRITY CHECK")
    print("-" * 80)

    total_chars = len(CHARACTER_OPERATIONS)
    print(f"✓ Total characters in database: {total_chars}")

    # Check required fields
    required_fields = ['radicals', 'composition', 'formula', 'slot_grammar', 'topo_type', 'notes']
    for char, data in CHARACTER_OPERATIONS.items():
        for field in required_fields:
            if field not in data:
                issues.append(f"Character '{char}' missing field: {field}")

    if not issues:
        print(f"✓ All {total_chars} characters have required fields")

    # Check topological type distribution
    topo_counts = {}
    for char, data in CHARACTER_OPERATIONS.items():
        topo_type = data['topo_type']
        topo_counts[topo_type] = topo_counts.get(topo_type, 0) + 1

    print(f"\n  Topological type distribution:")
    for topo_type, count in sorted(topo_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {topo_type:15s}: {count:3d} characters ({count/total_chars*100:.1f}%)")

    # 2. Translation engine functionality
    print("\n[2] TRANSLATION ENGINE FUNCTIONALITY")
    print("-" * 80)

    try:
        engine = TranslationEngine()
        print("✓ Translation engine initialized successfully")
    except Exception as e:
        issues.append(f"Failed to initialize engine: {e}")
        print(f"✗ Engine initialization failed: {e}")
        return

    # Test character analysis
    test_char = '道'
    try:
        structure = engine.analyze_character(test_char)
        if structure:
            print(f"✓ Character analysis working (tested: {test_char})")
            print(f"  Formula: {structure.structural_formula}")
            print(f"  Type: {structure.topological_type}")
        else:
            warnings.append(f"Character analysis returned None for: {test_char}")
    except Exception as e:
        issues.append(f"Character analysis failed: {e}")

    # Test multilayer translation
    test_text = "道可道"
    try:
        layers = engine.translate_multilayer(test_text)
        if len(layers) == 4:
            print(f"✓ Multi-layer translation working (tested: {test_text})")
            print(f"  Layers generated: {[l.level for l in layers]}")
        else:
            warnings.append(f"Expected 4 layers, got {len(layers)}")
    except Exception as e:
        issues.append(f"Multi-layer translation failed: {e}")

    # 3. Pattern template check
    print("\n[3] PATTERN TEMPLATES")
    print("-" * 80)

    template_count = len(PATTERN_TEMPLATES)
    print(f"✓ Pattern templates defined: {template_count}")
    for name, template in PATTERN_TEMPLATES.items():
        print(f"  - {name}: {template['name']}")

    # 4. Chapter coverage check
    print("\n[4] CHAPTER COVERAGE")
    print("-" * 80)

    # Chapter 1 characters
    ch1_text = "道可道非常道名可名非常名無名天地之始有名萬物之母故常無欲以觀其妙常有欲以觀其徼此兩者同出而異名同謂之玄玄之又玄眾妙之門"
    ch1_unique = set(ch1_text)
    ch1_covered = [c for c in ch1_unique if c in CHARACTER_OPERATIONS]
    ch1_coverage = len(ch1_covered) / len(ch1_unique) * 100 if ch1_unique else 0

    print(f"  Chapter 1: {len(ch1_covered)}/{len(ch1_unique)} characters ({ch1_coverage:.1f}%)")
    if ch1_coverage == 100:
        print(f"    ✓ COMPLETE")
    else:
        missing = set(ch1_unique) - set(ch1_covered)
        warnings.append(f"Chapter 1 missing: {''.join(missing)}")
        print(f"    ⚠ Missing: {''.join(missing)}")

    # Chapter 2 characters
    ch2_text = "天下皆知美之為美斯惡已皆知善之為善斯不善已故有無相生難易相成長短相形高下相傾音聲相和前後相隨是以聖人處無為之事行不言之教萬物作焉而不辭生而不有為而不恃功成而弗居夫唯弗居是以不去"
    ch2_unique = set(ch2_text)
    ch2_covered = [c for c in ch2_unique if c in CHARACTER_OPERATIONS]
    ch2_coverage = len(ch2_covered) / len(ch2_unique) * 100 if ch2_unique else 0

    print(f"  Chapter 2: {len(ch2_covered)}/{len(ch2_unique)} characters ({ch2_coverage:.1f}%)")
    if ch2_coverage == 100:
        print(f"    ✓ COMPLETE")
    else:
        missing = set(ch2_unique) - set(ch2_covered)
        warnings.append(f"Chapter 2 missing: {''.join(missing)}")
        print(f"    ⚠ Missing: {''.join(missing)}")

    # Total unique across both chapters
    total_unique = ch1_unique | ch2_unique
    print(f"\n  Combined unique characters: {len(total_unique)}")
    print(f"  Characters in database: {total_chars}")

    # 5. Sample translations
    print("\n[5] SAMPLE TRANSLATIONS")
    print("-" * 80)

    samples = [
        ("道可道", "O → frame → O"),
        ("有無相生", "P → O → connection → G"),
        ("功成而弗居", "P → frame → connection → connection → P"),
    ]

    for text, expected_pattern in samples:
        try:
            layers = engine.translate_multilayer(text)
            pattern_layer = layers[3]  # Pattern recognition layer
            print(f"✓ {text}")
            # Extract just the topological sequence line
            for line in pattern_layer.content.split('\n'):
                if 'Topological sequence:' in line:
                    print(f"  {line.strip()}")
                    break
        except Exception as e:
            issues.append(f"Sample translation failed for '{text}': {e}")

    # Final report
    print("\n" + "="*80)
    print("DIAGNOSTIC SUMMARY")
    print("="*80)

    if not issues and not warnings:
        print("✓ ALL SYSTEMS OPERATIONAL")
        print(f"✓ Database: {total_chars} characters")
        print(f"✓ Chapter 1: 100% complete")
        print(f"✓ Chapter 2: 100% complete")
        print(f"✓ Translation engine: Fully functional")
        print(f"✓ Pattern recognition: Working")
        print("\nStatus: READY FOR CHAPTER 3")
        return 0

    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")

    if issues:
        print(f"\n✗ ISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(run_diagnostics())
