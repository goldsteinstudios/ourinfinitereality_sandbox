"""
Markdown export functions for extracted voice messages.

Creates organized file structures for browsing and searching.
"""

from pathlib import Path
from typing import List, Optional
from collections import defaultdict
import re

from .extractor import VoiceMessage, filter_substantial
from .timeline import build_timeline, build_daily_summaries, build_timeline_by_conversation


def export_to_markdown(
    messages: List[VoiceMessage],
    output_dir: str,
    grouping: str = 'all'
) -> None:
    """
    Export messages to markdown files.

    Args:
        messages: List of VoiceMessage objects
        output_dir: Output directory path
        grouping: 'all', 'date', 'conversation', 'substantial', or 'full'
                  'full' creates all groupings
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if grouping == 'all' or grouping == 'full':
        # Single timeline file
        timeline = build_timeline(messages)
        (output_path / 'timeline.md').write_text(timeline, encoding='utf-8')
        print(f"  Written: timeline.md ({len(messages)} messages)")

    if grouping == 'date' or grouping == 'full':
        # By date
        date_dir = output_path / 'by_date'
        date_dir.mkdir(exist_ok=True)

        daily = build_daily_summaries(messages)
        for date_str, content in daily.items():
            filename = f"{date_str}.md"
            (date_dir / filename).write_text(content, encoding='utf-8')

        print(f"  Written: by_date/ ({len(daily)} files)")

    if grouping == 'conversation' or grouping == 'full':
        # By conversation
        conv_dir = output_path / 'by_conversation'
        conv_dir.mkdir(exist_ok=True)

        by_conv = build_timeline_by_conversation(messages)
        for conv_id, content in by_conv.items():
            # Sanitize filename
            safe_name = _sanitize_filename(conv_id)
            filename = f"{safe_name}.md"
            (conv_dir / filename).write_text(content, encoding='utf-8')

        print(f"  Written: by_conversation/ ({len(by_conv)} files)")

    if grouping == 'substantial' or grouping == 'full':
        # Substantial only
        substantial = filter_substantial(messages, min_chars=500)
        if substantial:
            sub_dir = output_path / 'substantial'
            sub_dir.mkdir(exist_ok=True)

            timeline = build_timeline(substantial)
            (sub_dir / 'substantial_timeline.md').write_text(timeline, encoding='utf-8')

            print(f"  Written: substantial/ ({len(substantial)} messages)")


def export_single_entry(
    message: VoiceMessage,
    output_dir: str
) -> str:
    """
    Export a single message as a standalone markdown file.

    Args:
        message: VoiceMessage object
        output_dir: Output directory path

    Returns:
        Path to the created file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create filename from date and hash
    filename = f"{message.date_str}_{message._hash}.md"
    filepath = output_path / filename

    content = _format_single_entry(message)
    filepath.write_text(content, encoding='utf-8')

    return str(filepath)


def _format_single_entry(message: VoiceMessage) -> str:
    """
    Format a single message as a complete markdown document.
    """
    lines = [
        "---",
        f"date: {message.datetime_str}",
        f"source: {message.platform}",
        f"conversation: {message.conversation_title or message.conversation_id}",
        f"length: {message.char_count} characters",
        f"words: {message.word_count}",
        "---",
        "",
        message.content,
        "",
        "---",
        "",
    ]

    return '\n'.join(lines)


def export_concepts_index(
    messages: List[VoiceMessage],
    concepts: List[str],
    output_file: str
) -> None:
    """
    Export an index of concept first mentions.

    Args:
        messages: List of VoiceMessage objects
        concepts: List of concept terms to track
        output_file: Output file path
    """
    from .search import find_first_mention

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    first_mentions = find_first_mention(messages, concepts)

    lines = [
        "# Concept Index",
        "",
        f"*Tracking first mentions of {len(concepts)} concepts*",
        "",
        "---",
        "",
        "## First Mentions",
        "",
        "| Concept | Date | Conversation | Snippet |",
        "|---------|------|--------------|---------|",
    ]

    for term, data in sorted(first_mentions.items(), key=lambda x: x[1]['date'] if x[1] else 'z'):
        if data:
            date = data['date']
            conv = data['conversation'][:30] + '...' if len(data['conversation']) > 30 else data['conversation']
            snippet = data['snippet'][:50] + '...' if len(data['snippet']) > 50 else data['snippet']
            snippet = snippet.replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {term} | {date} | {conv} | {snippet} |")
        else:
            lines.append(f"| {term} | *not found* | - | - |")

    lines.extend([
        "",
        "---",
        "",
        "## Detailed First Mentions",
        "",
    ])

    for term, data in sorted(first_mentions.items(), key=lambda x: x[1]['date'] if x[1] else 'z'):
        if data:
            lines.extend([
                f"### {term}",
                "",
                f"**First mentioned:** {data['date']}",
                f"**Conversation:** {data['conversation']}",
                "",
                f"> {data['snippet']}",
                "",
                "---",
                "",
            ])

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Written: {output_file}")


def _sanitize_filename(name: str, max_length: int = 50) -> str:
    """
    Sanitize a string for use as a filename.
    """
    # Remove or replace problematic characters
    safe = re.sub(r'[<>:"/\\|?*]', '_', name)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_')

    # Truncate if too long
    if len(safe) > max_length:
        safe = safe[:max_length].rstrip('_')

    return safe or 'unnamed'
