#!/usr/bin/env python3
"""
Glossary CLI - Command-line interface for the Living Glossary.

Usage:
    ./glossary_cli.py get <character>
    ./glossary_cli.py list [--confidence <level>] [--untraced]
    ./glossary_cli.py update <character> --field <path> --value <value> --rationale <text>
    ./glossary_cli.py add <character> --pinyin <pinyin> --primary <translation>
    ./glossary_cli.py validate <character>
    ./glossary_cli.py validate --all
    ./glossary_cli.py export [--format json|markdown]
    ./glossary_cli.py history <character>
    ./glossary_cli.py stats
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from python_analysis.glossary.manager import GlossaryManager
from python_analysis.glossary.integration import GlossaryIntegrator


def cmd_get(args, gm: GlossaryManager):
    """Get and display an entry."""
    entry = gm.get(args.character)
    if not entry:
        print(f"No entry found for: {args.character}")
        return 1

    if args.json:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    else:
        print_entry_summary(entry)
    return 0


def cmd_list(args, gm: GlossaryManager):
    """List entries with optional filters."""
    if args.confidence:
        entries = gm.by_confidence(args.confidence)
    elif args.untraced:
        entries = gm.untraced_characters()
    elif args.tier1:
        entries = gm.tier_1_characters()
    else:
        entries = [gm.get(c) for c in gm.all_characters()]

    entries = [e for e in entries if e]  # Filter None

    print(f"Found {len(entries)} entries:\n")
    for entry in entries:
        char = entry['character']
        confidence = entry.get('confidence', '?')
        primary = entry.get('current_translation', {}).get('primary', '')
        traced = '✓' if entry.get('font_data', {}).get('traced') else ' '
        print(f"  {char}  [{confidence:12}] [traced:{traced}] {primary}")

    return 0


def cmd_update(args, gm: GlossaryManager):
    """Update a field in an entry."""
    if not gm.exists(args.character):
        print(f"No entry found for: {args.character}")
        return 1

    # Parse value as JSON if it looks like JSON
    value = args.value
    if value.startswith('[') or value.startswith('{'):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass  # Keep as string

    try:
        entry = gm.update(
            args.character,
            {args.field: value},
            rationale=args.rationale,
            author=args.author or "cli"
        )
        print(f"Updated {args.character}.{args.field}")
        print(f"  New value: {value}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_add(args, gm: GlossaryManager):
    """Add a new entry."""
    if gm.exists(args.character):
        print(f"Entry already exists for: {args.character}")
        return 1

    entry = {
        "character": args.character,
        "unicode": f"U+{ord(args.character):04X}",
        "pinyin": args.pinyin or "",
        "current_translation": {
            "primary": args.primary or "",
            "structural": args.structural or "",
            "traditional": args.traditional or "",
            "notes": ""
        },
        "confidence": "speculative",
        "confidence_score": 0.3,
        "radical_decomposition": {
            "standard": {"components": []},
            "agricultural": {"components": []},
            "preferred": None,
            "preference_rationale": None
        },
        "character_evolution": {
            "oracle_bone": {"attested": None, "image_refs": [], "analysis": None},
            "bronze": {"attested": None, "image_refs": [], "analysis": None},
            "chu": {"attested": None, "image_refs": [], "analysis": None},
            "seal": {"attested": None, "image_refs": [], "analysis": None}
        },
        "agricultural_hypothesis": {
            "claim": None,
            "predictions": [],
            "falsification_threshold": None
        },
        "counter_evidence": [],
        "chubs_validation": None,
        "guodian_attestation": None,
        "font_data": {
            "traced": False,
            "vector_path": None,
            "source_images": [],
            "extracted_features": None,
            "tracing_metadata": None
        },
        "semantic_field": None,
        "pictographic_analysis": None,
        "exemplar_provenance": None,
        "cross_references": {
            "related_characters": [],
            "ddj_chapters": [],
            "lexicon_category": None,
            "rsm_mapping": None
        },
        "history": []
    }

    try:
        gm.create(entry, author=args.author or "cli")
        print(f"Created entry for: {args.character}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_history(args, gm: GlossaryManager):
    """Show history for a character."""
    history = gm.get_history(args.character)
    if not history:
        print(f"No history found for: {args.character}")
        return 1

    print(f"History for {args.character} ({len(history)} entries):\n")
    for h in history:
        date = h.get('date', '')[:10]
        field = h.get('field', '')
        author = h.get('author', '')
        rationale = h.get('rationale', '')
        print(f"  {date} | {field:30} | {author:15} | {rationale[:50]}")

    return 0


def cmd_export(args, gm: GlossaryManager):
    """Export the glossary."""
    if args.format == 'json':
        combined = gm.export_combined()
        print(json.dumps(combined, ensure_ascii=False, indent=2))
    elif args.format == 'markdown':
        export_markdown(gm)
    elif args.format == 'legacy':
        legacy = gm.export_for_translations()
        print(json.dumps(legacy, ensure_ascii=False, indent=2))
    return 0


def cmd_stats(args, gm: GlossaryManager):
    """Show glossary statistics."""
    total = gm.count()
    tested = len(gm.by_confidence('tested'))
    provisional = len(gm.by_confidence('provisional'))
    speculative = len(gm.by_confidence('speculative'))
    untraced = len(gm.untraced_characters())
    tier1 = len(gm.tier_1_characters())

    print("Glossary Statistics:")
    print(f"  Total entries:     {total}")
    print(f"  Confidence levels:")
    print(f"    - tested:        {tested}")
    print(f"    - provisional:   {provisional}")
    print(f"    - speculative:   {speculative}")
    print(f"  Font status:")
    print(f"    - untraced:      {untraced}")
    print(f"    - traced:        {total - untraced}")
    print(f"  Tier 1 characters: {tier1}/6")

    return 0


def cmd_validate(args, gm: GlossaryManager):
    """Validate entries against CHUBS corpus."""
    integrator = GlossaryIntegrator(gm)

    if args.all:
        # Batch validate all entries
        print("Running CHUBS batch validation...")
        results = integrator.batch_validate_all(author=args.author or "cli")

        print(f"\nValidation complete:")
        print(f"  Validated: {results['validated']}")
        print(f"  Skipped: {results['skipped']}")
        print(f"\nVerdicts:")
        for verdict, count in sorted(results['verdicts'].items()):
            print(f"  {verdict}: {count}")

        # Show Guodian Laozi count
        guodian_count = sum(1 for d in results['details'].values() if d.get('guodian_laozi'))
        print(f"\nGuodian Laozi: {guodian_count} characters")

        # Save combined glossary
        gm.save_combined()
        print("\nCombined glossary saved.")

    elif args.character:
        # Validate single character
        if not gm.exists(args.character):
            print(f"No entry found for: {args.character}")
            return 1

        result = integrator.link_chubs_to_entry(args.character, author=args.author or "cli")
        if result:
            chubs = result.get('chubs_validation', {})
            print(f"Validation for {args.character}:")
            print(f"  Verdict: {chubs.get('verdict', '?')}")
            print(f"  Glyph count: {chubs.get('glyph_count', 0)}")
            print(f"  Guodian Laozi: {'Yes' if chubs.get('guodian_laozi') else 'No'}")
            print(f"  POS instances: {chubs.get('total_pos_instances', 0)}")
            if chubs.get('dominant_pos'):
                print(f"  Dominant POS: {chubs.get('dominant_pos_english')} ({chubs.get('pos_percentages', {}).get(chubs.get('dominant_pos'), 0):.1f}%)")

            if chubs.get('pos_distribution'):
                print(f"  POS distribution:")
                for pos, count in sorted(chubs['pos_distribution'].items(), key=lambda x: -x[1]):
                    pct = chubs['pos_percentages'].get(pos, 0)
                    eng = integrator.POS_TRANSLATIONS.get(pos, pos)
                    print(f"    {pos} ({eng}): {count} ({pct:.1f}%)")
        else:
            print(f"Validation failed for: {args.character}")
            return 1

    elif args.report:
        # Generate validation report
        report = integrator.export_validation_report()
        print(report)

    else:
        print("Specify --all, a character, or --report")
        return 1

    return 0


def print_entry_summary(entry: dict):
    """Print a formatted summary of an entry."""
    char = entry['character']
    unicode = entry.get('unicode', '')
    pinyin = entry.get('pinyin', '')
    confidence = entry.get('confidence', '?')
    score = entry.get('confidence_score', 0)

    trans = entry.get('current_translation', {})
    primary = trans.get('primary', '')
    structural = trans.get('structural', '')
    traditional = trans.get('traditional', '')

    print(f"═══════════════════════════════════════")
    print(f"  {char}  ({unicode})  [{pinyin}]")
    print(f"═══════════════════════════════════════")
    print(f"  Confidence: {confidence} ({score:.2f})")
    print(f"  Primary:    {primary}")
    print(f"  Structural: {structural}")
    print(f"  Traditional: {traditional}")

    # Radical decomposition
    decomp = entry.get('radical_decomposition', {})
    preferred = decomp.get('preferred', 'standard')
    if preferred and preferred in decomp:
        components = decomp[preferred].get('components', [])
        if components:
            comp_str = ' + '.join(f"{c['component']}({c.get('meaning', '')})" for c in components)
            print(f"  Decomposition ({preferred}): {comp_str}")

    # CHUBS validation
    chubs = entry.get('chubs_validation')
    if chubs:
        verdict = chubs.get('verdict', '?')
        glyph_count = chubs.get('glyph_count', 0)
        guodian = '✓' if chubs.get('guodian_laozi') else ' '
        print(f"  CHUBS: {verdict} ({glyph_count} glyphs) [Guodian Laozi: {guodian}]")

    # Font data
    font = entry.get('font_data', {})
    if font.get('traced'):
        print(f"  Font: Traced ({font.get('vector_path', '')})")
    else:
        print(f"  Font: Not traced")

    # History summary
    history = entry.get('history', [])
    print(f"  History: {len(history)} entries")

    print()


def export_markdown(gm: GlossaryManager):
    """Export as markdown."""
    print("# Living Glossary\n")
    print(f"*Generated: {datetime.now().isoformat()}*\n")

    for char in sorted(gm.all_characters()):
        entry = gm.get(char)
        if not entry:
            continue

        trans = entry.get('current_translation', {})
        print(f"## {char} ({entry.get('unicode', '')})")
        print(f"**Primary:** {trans.get('primary', '')}")
        print(f"**Structural:** {trans.get('structural', '')}")
        print(f"**Traditional:** {trans.get('traditional', '')}")
        print(f"**Confidence:** {entry.get('confidence', '')} ({entry.get('confidence_score', 0):.2f})")
        print()


def main():
    parser = argparse.ArgumentParser(description='Living Glossary CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # get command
    get_parser = subparsers.add_parser('get', help='Get entry for a character')
    get_parser.add_argument('character', help='The character to look up')
    get_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # list command
    list_parser = subparsers.add_parser('list', help='List entries')
    list_parser.add_argument('--confidence', choices=['tested', 'provisional', 'speculative'],
                            help='Filter by confidence level')
    list_parser.add_argument('--untraced', action='store_true', help='Show only untraced characters')
    list_parser.add_argument('--tier1', action='store_true', help='Show only Tier 1 characters')

    # update command
    update_parser = subparsers.add_parser('update', help='Update a field')
    update_parser.add_argument('character', help='The character to update')
    update_parser.add_argument('--field', required=True, help='Field path (dot notation)')
    update_parser.add_argument('--value', required=True, help='New value')
    update_parser.add_argument('--rationale', required=True, help='Reason for update')
    update_parser.add_argument('--author', help='Who is making the update')

    # add command
    add_parser = subparsers.add_parser('add', help='Add a new entry')
    add_parser.add_argument('character', help='The character to add')
    add_parser.add_argument('--pinyin', help='Pinyin with tone')
    add_parser.add_argument('--primary', help='Primary translation')
    add_parser.add_argument('--structural', help='Structural interpretation')
    add_parser.add_argument('--traditional', help='Traditional translation')
    add_parser.add_argument('--author', help='Who is creating the entry')

    # history command
    history_parser = subparsers.add_parser('history', help='Show history for a character')
    history_parser.add_argument('character', help='The character')

    # export command
    export_parser = subparsers.add_parser('export', help='Export the glossary')
    export_parser.add_argument('--format', choices=['json', 'markdown', 'legacy'],
                              default='json', help='Export format')

    # stats command
    subparsers.add_parser('stats', help='Show glossary statistics')

    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate against CHUBS corpus')
    validate_parser.add_argument('character', nargs='?', help='Character to validate (optional)')
    validate_parser.add_argument('--all', action='store_true', help='Validate all entries')
    validate_parser.add_argument('--report', action='store_true', help='Generate validation report')
    validate_parser.add_argument('--author', help='Who is running the validation')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize manager
    gm = GlossaryManager()

    # Dispatch to command handler
    commands = {
        'get': cmd_get,
        'list': cmd_list,
        'update': cmd_update,
        'add': cmd_add,
        'history': cmd_history,
        'export': cmd_export,
        'stats': cmd_stats,
        'validate': cmd_validate,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args, gm)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
