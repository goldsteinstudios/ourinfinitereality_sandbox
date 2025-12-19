"""
Timeline builder for extracted voice messages.

Creates chronological views of the user's discovery path.
"""

from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

from .extractor import VoiceMessage


def build_timeline(
    messages: List[VoiceMessage],
    include_metadata: bool = True
) -> str:
    """
    Build a single markdown file with all messages in chronological order.

    Args:
        messages: List of VoiceMessage objects
        include_metadata: Whether to include frontmatter for each entry

    Returns:
        Markdown string containing the complete timeline
    """
    if not messages:
        return "# Voice Timeline\n\nNo messages extracted.\n"

    # Sort by timestamp
    sorted_messages = sorted(
        messages,
        key=lambda m: (m.timestamp is None, m.timestamp)
    )

    lines = [
        "# Voice Timeline",
        "",
        f"*{len(messages)} messages extracted*",
        "",
        "---",
        "",
    ]

    current_date = None

    for msg in sorted_messages:
        # Add date header when date changes
        date_str = msg.date_str
        if date_str != current_date:
            current_date = date_str
            lines.append(f"## {date_str}")
            lines.append("")

        # Add message
        if include_metadata:
            lines.append("```yaml")
            lines.append(f"time: {msg.datetime_str}")
            lines.append(f"source: {msg.platform}")
            lines.append(f"conversation: {msg.conversation_title or msg.conversation_id}")
            lines.append(f"length: {msg.char_count} chars")
            lines.append("```")
            lines.append("")

        lines.append(msg.content)
        lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def build_timeline_by_conversation(messages: List[VoiceMessage]) -> Dict[str, str]:
    """
    Build separate markdown timelines for each conversation.

    Args:
        messages: List of VoiceMessage objects

    Returns:
        Dictionary mapping conversation_id to markdown content
    """
    # Group by conversation
    by_conversation: Dict[str, List[VoiceMessage]] = defaultdict(list)

    for msg in messages:
        key = msg.conversation_id
        by_conversation[key].append(msg)

    timelines = {}

    for conv_id, conv_messages in by_conversation.items():
        # Sort messages within conversation
        conv_messages.sort(key=lambda m: (m.timestamp is None, m.timestamp))

        # Get conversation title from first message
        title = conv_messages[0].conversation_title or conv_id

        lines = [
            f"# {title}",
            "",
            f"*Conversation ID: {conv_id}*",
            f"*{len(conv_messages)} messages*",
            "",
            "---",
            "",
        ]

        for msg in conv_messages:
            lines.append(f"### {msg.datetime_str}")
            lines.append("")
            lines.append(msg.content)
            lines.append("")
            lines.append("---")
            lines.append("")

        timelines[conv_id] = '\n'.join(lines)

    return timelines


def build_daily_summaries(messages: List[VoiceMessage]) -> Dict[str, str]:
    """
    Build separate markdown files for each day.

    Args:
        messages: List of VoiceMessage objects

    Returns:
        Dictionary mapping date strings to markdown content
    """
    # Group by date
    by_date: Dict[str, List[VoiceMessage]] = defaultdict(list)

    for msg in messages:
        by_date[msg.date_str].append(msg)

    summaries = {}

    for date_str, day_messages in sorted(by_date.items()):
        # Sort messages within day
        day_messages.sort(key=lambda m: (m.timestamp is None, m.timestamp))

        total_chars = sum(m.char_count for m in day_messages)
        total_words = sum(m.word_count for m in day_messages)
        conversations = set(m.conversation_id for m in day_messages)

        lines = [
            f"# {date_str}",
            "",
            f"*{len(day_messages)} messages | {total_words} words | {len(conversations)} conversations*",
            "",
            "---",
            "",
        ]

        for msg in day_messages:
            time_str = msg.timestamp.strftime('%H:%M') if msg.timestamp else 'unknown'
            lines.append(f"### {time_str}")
            if msg.conversation_title:
                lines.append(f"*{msg.conversation_title}*")
            lines.append("")
            lines.append(msg.content)
            lines.append("")
            lines.append("---")
            lines.append("")

        summaries[date_str] = '\n'.join(lines)

    return summaries


def build_concept_timeline(
    messages: List[VoiceMessage],
    concepts: List[str]
) -> str:
    """
    Build a timeline showing when specific concepts first appeared and evolved.

    Args:
        messages: List of VoiceMessage objects
        concepts: List of concept terms to track

    Returns:
        Markdown string with concept evolution timeline
    """
    # Sort messages
    sorted_messages = sorted(
        messages,
        key=lambda m: (m.timestamp is None, m.timestamp)
    )

    # Track first mention and all mentions for each concept
    concept_data: Dict[str, Dict[str, Any]] = {}

    for concept in concepts:
        concept_lower = concept.lower()
        mentions = []

        for msg in sorted_messages:
            if concept_lower in msg.content.lower() or concept in msg.content:
                mentions.append(msg)

        if mentions:
            concept_data[concept] = {
                'first_mention': mentions[0],
                'total_mentions': len(mentions),
                'all_mentions': mentions,
            }

    # Build markdown
    lines = [
        "# Concept Evolution Timeline",
        "",
        f"*Tracking {len(concepts)} concepts across {len(messages)} messages*",
        "",
        "---",
        "",
    ]

    # Summary table
    lines.append("## First Mentions")
    lines.append("")
    lines.append("| Concept | First Mentioned | Total Mentions |")
    lines.append("|---------|-----------------|----------------|")

    for concept in concepts:
        if concept in concept_data:
            data = concept_data[concept]
            first = data['first_mention']
            lines.append(f"| {concept} | {first.date_str} | {data['total_mentions']} |")
        else:
            lines.append(f"| {concept} | *not found* | 0 |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed sections for each concept
    for concept in concepts:
        if concept not in concept_data:
            continue

        data = concept_data[concept]
        lines.append(f"## {concept}")
        lines.append("")
        lines.append(f"*First mentioned: {data['first_mention'].date_str}*")
        lines.append(f"*Total mentions: {data['total_mentions']}*")
        lines.append("")

        # Show first few mentions with context
        for i, msg in enumerate(data['all_mentions'][:5]):
            lines.append(f"### {i+1}. {msg.date_str}")
            lines.append("")

            # Extract snippet around concept
            snippet = _extract_snippet(msg.content, concept, context_chars=200)
            lines.append(f"> {snippet}")
            lines.append("")

        if data['total_mentions'] > 5:
            lines.append(f"*... and {data['total_mentions'] - 5} more mentions*")
            lines.append("")

        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def _extract_snippet(content: str, term: str, context_chars: int = 200) -> str:
    """
    Extract a snippet of text around the first occurrence of a term.
    """
    # Case-insensitive search
    lower_content = content.lower()
    lower_term = term.lower()

    idx = lower_content.find(lower_term)
    if idx == -1:
        # Try exact match
        idx = content.find(term)

    if idx == -1:
        return content[:context_chars * 2] + "..."

    start = max(0, idx - context_chars)
    end = min(len(content), idx + len(term) + context_chars)

    snippet = content[start:end]

    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    return snippet.replace('\n', ' ')
