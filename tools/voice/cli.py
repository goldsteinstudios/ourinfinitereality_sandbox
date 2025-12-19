#!/usr/bin/env python3
"""
Voice Extractor CLI

Extract user prompts from AI conversation exports.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .extractor import (
    extract_voice,
    extract_from_directory,
    filter_substantial,
    get_statistics,
    VoiceMessage,
)
from .timeline import build_timeline, build_concept_timeline
from .search import find_first_mention, search_voice, count_mentions
from .export import export_to_markdown, export_concepts_index


def main():
    parser = argparse.ArgumentParser(
        description='Extract user voice from AI conversation exports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from Claude export
  python -m voice extract --input export.json --platform claude --output ./extracted/

  # Build timeline
  python -m voice timeline --input export.json --output timeline.md

  # Find first mentions of concepts
  python -m voice first-mentions --input export.json --terms "cambium,hollow center,常"

  # Search across all extracted voice
  python -m voice search --input export.json --query "tree"

  # Export substantial entries only
  python -m voice export --input export.json --min-chars 500 --output ./substantial/
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract voice from export file')
    extract_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    extract_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform (default: claude)')
    extract_parser.add_argument('--output', '-o', required=True, help='Output directory')
    extract_parser.add_argument('--grouping', '-g', default='full', choices=['all', 'date', 'conversation', 'substantial', 'full'], help='Grouping method (default: full)')

    # Timeline command
    timeline_parser = subparsers.add_parser('timeline', help='Build timeline from export')
    timeline_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    timeline_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')
    timeline_parser.add_argument('--output', '-o', required=True, help='Output markdown file')

    # First mentions command
    mentions_parser = subparsers.add_parser('first-mentions', help='Find first mentions of terms')
    mentions_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    mentions_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')
    mentions_parser.add_argument('--terms', '-t', required=True, help='Comma-separated list of terms to find')
    mentions_parser.add_argument('--output', '-o', help='Output file (optional, prints to stdout if not specified)')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search across all messages')
    search_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    search_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')
    search_parser.add_argument('--query', '-q', required=True, help='Search query')
    search_parser.add_argument('--limit', '-l', type=int, default=20, help='Max results (default: 20)')
    search_parser.add_argument('--regex', '-r', action='store_true', help='Treat query as regex')

    # Export command (alias for extract with specific options)
    export_parser = subparsers.add_parser('export', help='Export to markdown with filters')
    export_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    export_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')
    export_parser.add_argument('--output', '-o', required=True, help='Output directory')
    export_parser.add_argument('--min-chars', type=int, default=0, help='Minimum character count')
    export_parser.add_argument('--grouping', '-g', default='all', choices=['all', 'date', 'conversation', 'substantial', 'full'], help='Grouping method')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics about export')
    stats_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    stats_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')

    # Concepts command
    concepts_parser = subparsers.add_parser('concepts', help='Build concept evolution timeline')
    concepts_parser.add_argument('--input', '-i', required=True, help='Input JSON file or directory')
    concepts_parser.add_argument('--platform', '-p', default='claude', choices=['claude', 'chatgpt'], help='Platform')
    concepts_parser.add_argument('--terms', '-t', required=True, help='Comma-separated list of concepts')
    concepts_parser.add_argument('--output', '-o', required=True, help='Output markdown file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'extract':
            cmd_extract(args)
        elif args.command == 'timeline':
            cmd_timeline(args)
        elif args.command == 'first-mentions':
            cmd_first_mentions(args)
        elif args.command == 'search':
            cmd_search(args)
        elif args.command == 'export':
            cmd_export(args)
        elif args.command == 'stats':
            cmd_stats(args)
        elif args.command == 'concepts':
            cmd_concepts(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _load_messages(input_path: str, platform: str) -> List[VoiceMessage]:
    """Load messages from file or directory."""
    path = Path(input_path)

    if path.is_dir():
        messages = extract_from_directory(str(path), platform)
    else:
        messages = extract_voice(str(path), platform)

    return messages


def cmd_extract(args):
    """Handle extract command."""
    print(f"Extracting voice from {args.input}...")

    messages = _load_messages(args.input, args.platform)

    print(f"Found {len(messages)} messages")

    export_to_markdown(messages, args.output, args.grouping)

    print(f"\nExport complete: {args.output}")


def cmd_timeline(args):
    """Handle timeline command."""
    print(f"Building timeline from {args.input}...")

    messages = _load_messages(args.input, args.platform)

    print(f"Found {len(messages)} messages")

    timeline = build_timeline(messages)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(timeline, encoding='utf-8')

    print(f"Timeline written to {args.output}")


def cmd_first_mentions(args):
    """Handle first-mentions command."""
    messages = _load_messages(args.input, args.platform)

    terms = [t.strip() for t in args.terms.split(',')]

    print(f"Searching for first mentions of {len(terms)} terms in {len(messages)} messages...\n")

    results = find_first_mention(messages, terms)

    output_lines = []
    for term, data in results.items():
        if data:
            output_lines.append(f"## {term}")
            output_lines.append(f"**First mentioned:** {data['date']}")
            output_lines.append(f"**Conversation:** {data['conversation']}")
            output_lines.append(f"\n> {data['snippet']}\n")
        else:
            output_lines.append(f"## {term}")
            output_lines.append("*Not found*\n")

    output = '\n'.join(output_lines)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Results written to {args.output}")
    else:
        print(output)


def cmd_search(args):
    """Handle search command."""
    messages = _load_messages(args.input, args.platform)

    print(f"Searching for '{args.query}' in {len(messages)} messages...\n")

    results = search_voice(messages, args.query, regex=args.regex, limit=args.limit)

    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} matches:\n")

    for i, result in enumerate(results, 1):
        msg = result.message
        print(f"### {i}. {msg.date_str}")
        print(f"*{msg.conversation_title or msg.conversation_id}* ({result.match_count} matches)")
        print(f"\n> {result.snippet}\n")
        print("---\n")


def cmd_export(args):
    """Handle export command."""
    print(f"Exporting from {args.input}...")

    messages = _load_messages(args.input, args.platform)

    if args.min_chars > 0:
        messages = filter_substantial(messages, args.min_chars)
        print(f"Filtered to {len(messages)} substantial messages (>= {args.min_chars} chars)")
    else:
        print(f"Found {len(messages)} messages")

    export_to_markdown(messages, args.output, args.grouping)

    print(f"\nExport complete: {args.output}")


def cmd_stats(args):
    """Handle stats command."""
    messages = _load_messages(args.input, args.platform)

    stats = get_statistics(messages)

    print("\n=== Voice Extraction Statistics ===\n")
    print(f"Total messages:     {stats['total_messages']:,}")
    print(f"Total characters:   {stats['total_characters']:,}")
    print(f"Total words:        {stats['total_words']:,}")
    print(f"Conversations:      {stats['conversations']}")
    print(f"Platforms:          {', '.join(stats['platforms'])}")
    print(f"Substantial (500+): {stats['substantial_count']}")
    print(f"Undated:            {stats['undated_count']}")

    if stats['date_range']['earliest']:
        print(f"\nDate range:")
        print(f"  Earliest: {stats['date_range']['earliest']}")
        print(f"  Latest:   {stats['date_range']['latest']}")


def cmd_concepts(args):
    """Handle concepts command."""
    messages = _load_messages(args.input, args.platform)

    terms = [t.strip() for t in args.terms.split(',')]

    print(f"Building concept timeline for {len(terms)} terms in {len(messages)} messages...")

    timeline = build_concept_timeline(messages, terms)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(timeline, encoding='utf-8')

    print(f"Concept timeline written to {args.output}")


if __name__ == '__main__':
    main()
