"""
Physics conversation extractor.

Extracts physics-related conversations from ChatGPT/Claude exports,
filtered to RSM/DDJ/Physics work from Dec 2024 - Aug 2025.

Usage:
    python -m python_analysis.voice.physics_extractor --output data/physics_extracts/
"""

import json
import re
from datetime import datetime, timezone
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict


# ============================================================================
# CONFIGURATION
# ============================================================================

# Title keywords that indicate RSM/DDJ/Physics work (case-insensitive)
TITLE_KEYWORDS = {
    # RSM/Framework
    'rsm', 'recursive', 'paradox', 'gradient', 'hollow', 'cambium',
    'structural model', 'recursion', 'scale invariance',

    # DDJ/Chinese
    'tao', 'dao', 'ddj', 'tte', 'ttc', '道', 'chinese', 'chapter',
    'translation', 'radical', 'guodian', 'lexicon',

    # Physics
    'physics', 'quantum', 'gravity', 'relativity', 'spacetime',
    'euler', 'field', 'energy', 'motion', 'thermodynamics',
}

# Physics topic classification
PHYSICS_TOPICS = {
    'gravity_relativity': {
        'name': 'Gravity & Relativity',
        'keywords': {
            'gravity', 'gravitational', 'spacetime', 'curvature', 'relativity',
            'einstein', 'geodesic', 'metric', 'tensor', 'lorentz', 'frame',
            'invariant', 'general relativity', 'special relativity', 'equivalence',
            'inertial', 'acceleration', 'free fall', 'curved space',
        }
    },
    'quantum_mechanics': {
        'name': 'Quantum Mechanics',
        'keywords': {
            'quantum', 'superposition', 'wave function', 'wavefunction',
            'measurement', 'collapse', 'entanglement', 'schrödinger', 'schrodinger',
            'heisenberg', 'uncertainty', 'orbital', 'electron', 'photon',
            'probability amplitude', 'eigenstate', 'eigenvalue', 'observable',
            'decoherence', 'interference', 'double slit', 'spin', 'qubit',
        }
    },
    'field_theory': {
        'name': 'Field Theory',
        'keywords': {
            'field', 'electromagnetic', 'maxwell', 'charge', 'magnetic',
            'electric', 'potential', 'flux', 'gauge', 'faraday', 'coulomb',
            'wave equation', 'propagation', 'radiation', 'vacuum',
        }
    },
    'black_holes': {
        'name': 'Black Holes',
        'keywords': {
            'black hole', 'event horizon', 'singularity', 'schwarzschild',
            'hawking', 'horizon', 'ergosphere', 'penrose', 'information paradox',
            'bekenstein', 'holographic', 'firewall', 'no-hair',
        }
    },
    'energy_conservation': {
        'name': 'Energy & Conservation',
        'keywords': {
            'kinetic', 'potential energy', 'conservation', 'momentum',
            'angular momentum', 'noether', 'symmetry', 'invariance', 'work',
            'mass-energy', 'e=mc', 'thermodynamics', 'entropy',
        }
    },
    'formalism': {
        'name': 'Mathematical Formalism',
        'keywords': {
            'lagrangian', 'hamiltonian', 'action', 'principle of least action',
            'euler-lagrange', 'canonical', 'phase space', 'poisson bracket',
            'inverse square', '1/r', '1/r²', 'differential equation',
            'variational', 'functional', 'path integral',
        }
    },
    'rsm_physics_bridges': {
        'name': 'RSM-Physics Bridges',
        'keywords': {
            'circulation', 'paradox center', 'g₁', 'p₁', 'o₁', 'p₀', 'o₀',
            'viewing angle', 'curvature cost', 'hollow center', 'recursive',
            'gradient field', 'perpendicular', 'orthogonal turn', 'cambium',
            'boundary condition', 'scale invariance', 'irrational constant',
            'rotation operator', 'hyperbola', 'xy=k', 'taijitu',
        }
    },
}

# Date range
DATE_START = datetime(2024, 12, 1)
DATE_END = datetime(2025, 8, 31)

# Minimum keywords for topic classification
MIN_TOPIC_KEYWORDS = 2


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Message:
    """A single message (user or assistant)."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime]


@dataclass
class Conversation:
    """A full conversation with metadata."""
    id: str
    title: str
    platform: str
    created: Optional[datetime]
    messages: List[Message]

    @property
    def date_str(self) -> str:
        if self.created:
            return self.created.strftime('%Y-%m-%d')
        return 'undated'


@dataclass
class TopicExtract:
    """Extracted conversation for a topic."""
    conversation: Conversation
    matched_keywords: Set[str]
    all_topics: Set[str]
    primary_topic: str


@dataclass
class TopicCollection:
    """All extracts for a physics topic."""
    topic_id: str
    topic_name: str
    extracts: List[TopicExtract] = field(default_factory=list)

    @property
    def unique_conversations(self) -> int:
        return len(set(e.conversation.id for e in self.extracts))

    @property
    def total_messages(self) -> int:
        seen = set()
        count = 0
        for e in self.extracts:
            if e.conversation.id not in seen:
                seen.add(e.conversation.id)
                count += len(e.conversation.messages)
        return count


# ============================================================================
# PARSERS
# ============================================================================

def parse_chatgpt_conversations(file_path: str) -> List[Conversation]:
    """Parse ChatGPT export, extracting both user and assistant messages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conversations = []

    for conv in data:
        conv_id = conv.get('conversation_id') or conv.get('id', 'unknown')
        title = conv.get('title', '')
        created = None

        ts = conv.get('create_time')
        if ts:
            try:
                created = datetime.fromtimestamp(ts)
            except:
                pass

        # Extract messages from mapping
        mapping = conv.get('mapping', {})
        messages = []

        msg_list = []
        for node_id, node in mapping.items():
            if not isinstance(node, dict):
                continue
            msg = node.get('message')
            if msg and isinstance(msg, dict):
                msg['_create_time'] = msg.get('create_time', 0)
                msg_list.append(msg)

        # Sort by time
        msg_list.sort(key=lambda m: m.get('_create_time', 0) or 0)

        for msg in msg_list:
            author = msg.get('author', {})
            role = author.get('role', '') if isinstance(author, dict) else ''

            if role not in ('user', 'assistant'):
                continue

            # Extract content
            content = msg.get('content', {})
            if isinstance(content, dict):
                parts = content.get('parts', [])
                text = '\n'.join(p for p in parts if isinstance(p, str))
            elif isinstance(content, str):
                text = content
            else:
                continue

            if not text.strip():
                continue

            msg_ts = None
            if msg.get('create_time'):
                try:
                    msg_ts = datetime.fromtimestamp(msg['create_time'])
                except:
                    pass

            messages.append(Message(
                role=role,
                content=text.strip(),
                timestamp=msg_ts
            ))

        if messages:
            conversations.append(Conversation(
                id=conv_id,
                title=title,
                platform='chatgpt',
                created=created,
                messages=messages
            ))

    return conversations


def parse_claude_conversations(file_path: str) -> List[Conversation]:
    """Parse Claude export, extracting both human and assistant messages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conversations = []

    for conv in data:
        conv_id = conv.get('uuid') or conv.get('id', 'unknown')
        title = conv.get('name', '')
        created = None

        created_str = conv.get('created_at')
        if created_str:
            try:
                created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                created = created.replace(tzinfo=None)  # Make naive for comparison
            except:
                pass

        # Extract messages
        chat_messages = conv.get('chat_messages', [])
        messages = []

        for msg in chat_messages:
            sender = msg.get('sender', '')

            # Map Claude roles
            if sender == 'human':
                role = 'user'
            elif sender == 'assistant':
                role = 'assistant'
            else:
                continue

            # Extract content
            content = msg.get('text', '')
            if isinstance(content, list):
                content = '\n'.join(str(p) for p in content)

            if not content.strip():
                continue

            msg_ts = None
            ts_str = msg.get('created_at')
            if ts_str:
                try:
                    msg_ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    msg_ts = msg_ts.replace(tzinfo=None)
                except:
                    pass

            messages.append(Message(
                role=role,
                content=str(content).strip(),
                timestamp=msg_ts
            ))

        if messages:
            conversations.append(Conversation(
                id=conv_id,
                title=title,
                platform='claude',
                created=created,
                messages=messages
            ))

    return conversations


# ============================================================================
# FILTERING
# ============================================================================

def title_matches(title: str) -> bool:
    """Check if title indicates RSM/DDJ/Physics work."""
    title_lower = title.lower()
    return any(kw in title_lower for kw in TITLE_KEYWORDS)


def in_date_range(dt: Optional[datetime]) -> bool:
    """Check if datetime is in target range."""
    if not dt:
        return False
    return DATE_START <= dt <= DATE_END


def classify_conversation(conv: Conversation) -> Dict[str, Set[str]]:
    """Classify conversation by physics topics based on content."""
    # Combine all message content
    all_content = ' '.join(m.content for m in conv.messages).lower()

    results = {}

    for topic_id, config in PHYSICS_TOPICS.items():
        matches = set()
        for kw in config['keywords']:
            if ' ' in kw:
                if kw in all_content:
                    matches.add(kw)
            else:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, all_content):
                    matches.add(kw)

        if len(matches) >= MIN_TOPIC_KEYWORDS:
            results[topic_id] = matches

    return results


# ============================================================================
# EXTRACTION
# ============================================================================

def extract_physics_conversations(
    chatgpt_file: str,
    claude_file: str,
) -> Dict[str, TopicCollection]:
    """Extract and classify physics conversations."""

    # Initialize collections
    collections = {
        topic_id: TopicCollection(topic_id=topic_id, topic_name=config['name'])
        for topic_id, config in PHYSICS_TOPICS.items()
    }

    all_conversations = []

    # Load ChatGPT
    print(f"Loading ChatGPT conversations...")
    try:
        chatgpt_convs = parse_chatgpt_conversations(chatgpt_file)
        print(f"  Loaded {len(chatgpt_convs)} conversations")
        all_conversations.extend(chatgpt_convs)
    except Exception as e:
        print(f"  Error: {e}")

    # Load Claude
    print(f"Loading Claude conversations...")
    try:
        claude_convs = parse_claude_conversations(claude_file)
        print(f"  Loaded {len(claude_convs)} conversations")
        all_conversations.extend(claude_convs)
    except Exception as e:
        print(f"  Error: {e}")

    print(f"\nTotal conversations: {len(all_conversations)}")

    # Filter and classify
    print(f"\nFiltering by date ({DATE_START.date()} to {DATE_END.date()}) and title keywords...")

    filtered = []
    for conv in all_conversations:
        if in_date_range(conv.created) and title_matches(conv.title):
            filtered.append(conv)

    print(f"  {len(filtered)} conversations match filters")

    # Classify by topic
    print(f"\nClassifying by physics topic...")

    classified_count = 0
    for conv in filtered:
        topics = classify_conversation(conv)

        if not topics:
            continue

        classified_count += 1

        # Get primary topic
        primary = max(topics.keys(), key=lambda t: len(topics[t]))
        all_keywords = set()
        for kws in topics.values():
            all_keywords.update(kws)

        extract = TopicExtract(
            conversation=conv,
            matched_keywords=all_keywords,
            all_topics=set(topics.keys()),
            primary_topic=primary
        )

        # Add to primary topic
        collections[primary].extracts.append(extract)

        # Also add to other relevant topics (as cross-reference)
        for topic_id in topics.keys():
            if topic_id != primary:
                collections[topic_id].extracts.append(extract)

    print(f"  {classified_count} conversations classified into topics")

    # Sort by date
    for collection in collections.values():
        collection.extracts.sort(key=lambda e: e.conversation.date_str)

    return collections


# ============================================================================
# OUTPUT
# ============================================================================

def format_topic_markdown(collection: TopicCollection) -> str:
    """Format topic collection as markdown with full conversation context."""
    lines = [
        f"# {collection.topic_name} Extracts",
        "",
        f"*{collection.unique_conversations} conversations, {collection.total_messages} messages*",
        "",
        "---",
        "",
    ]

    seen_ids = set()

    for extract in collection.extracts:
        conv = extract.conversation

        # Skip duplicates (same conv in multiple topics)
        if conv.id in seen_ids:
            continue
        seen_ids.add(conv.id)

        lines.extend([
            f"## {conv.title or conv.id[:12]}",
            "",
            f"**Date:** {conv.date_str}",
            f"**Platform:** {conv.platform}",
            f"**Keywords:** {', '.join(sorted(extract.matched_keywords)[:15])}",
            f"**Topics:** {', '.join(PHYSICS_TOPICS[t]['name'] for t in extract.all_topics)}",
            "",
        ])

        # Include all messages (with truncation for very long ones)
        for i, msg in enumerate(conv.messages):
            role_label = "**User:**" if msg.role == 'user' else "**Assistant:**"

            content = msg.content
            if len(content) > 3000:
                content = content[:3000] + "\n\n*[truncated...]*"

            lines.extend([
                role_label,
                "",
                content,
                "",
            ])

            # Limit total messages per conversation
            if i >= 30:
                remaining = len(conv.messages) - i - 1
                if remaining > 0:
                    lines.append(f"*[{remaining} more messages...]*\n")
                break

        lines.append("---\n")

    return '\n'.join(lines)


def format_timeline(collections: Dict[str, TopicCollection]) -> str:
    """Generate chronological timeline of all conversations."""
    lines = [
        "# Physics Discussion Timeline",
        "",
        f"*RSM/DDJ/Physics conversations from {DATE_START.date()} to {DATE_END.date()}*",
        "",
        "---",
        "",
    ]

    # Gather unique conversations
    all_extracts = []
    seen_ids = set()

    for collection in collections.values():
        for extract in collection.extracts:
            if extract.conversation.id not in seen_ids:
                seen_ids.add(extract.conversation.id)
                all_extracts.append(extract)

    # Sort by date
    all_extracts.sort(key=lambda e: e.conversation.date_str)

    # Group by month
    by_month: Dict[str, List[TopicExtract]] = defaultdict(list)
    for extract in all_extracts:
        month = extract.conversation.date_str[:7]
        by_month[month].append(extract)

    for month in sorted(by_month.keys()):
        extracts = by_month[month]
        lines.extend([
            f"## {month}",
            "",
            f"*{len(extracts)} conversations*",
            "",
        ])

        for extract in extracts:
            conv = extract.conversation
            topics = ', '.join(PHYSICS_TOPICS[t]['name'] for t in extract.all_topics)
            lines.append(f"- **{conv.date_str}** [{conv.platform}] {conv.title} — {topics}")

        lines.append("")

    # Summary
    lines.extend([
        "---",
        "",
        "## Summary by Topic",
        "",
        "| Topic | Conversations | Messages |",
        "|-------|---------------|----------|",
    ])

    for topic_id, collection in collections.items():
        lines.append(f"| {collection.topic_name} | {collection.unique_conversations} | {collection.total_messages} |")

    lines.extend([
        "",
        f"**Total unique conversations:** {len(all_extracts)}",
    ])

    return '\n'.join(lines)


# ============================================================================
# MAIN
# ============================================================================

def run_extraction(output_dir: str):
    """Run the full extraction pipeline."""

    # Paths
    chatgpt_file = "research/work/ARCHIVE/exported_chat_dumps_12.5.25/chatgpt/6466764e0e63e66144efd8de3e824c2cd931fab16df171cbbd478b93be656db3-2025-12-05-23-22-02-c9076f945456469184866691d4dca8a5/conversations.json"
    claude_file = "research/work/ARCHIVE/exported_chat_dumps_12.5.25/claude/data-2025-12-05-23-17-50-batch-0000/conversations.json"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract
    collections = extract_physics_conversations(chatgpt_file, claude_file)

    # Write output files
    print(f"\nWriting output to {output_dir}/...")

    file_mapping = {
        'gravity_relativity': '01_gravity_relativity.md',
        'quantum_mechanics': '02_quantum_mechanics.md',
        'field_theory': '03_field_theory.md',
        'black_holes': '04_black_holes.md',
        'energy_conservation': '05_energy_conservation.md',
        'formalism': '06_formalism.md',
        'rsm_physics_bridges': '07_rsm_physics_bridges.md',
    }

    for topic_id, filename in file_mapping.items():
        collection = collections[topic_id]
        content = format_topic_markdown(collection)

        filepath = output_path / filename
        filepath.write_text(content, encoding='utf-8')

        print(f"  {filename}: {collection.unique_conversations} conversations")

    # Timeline
    timeline = format_timeline(collections)
    (output_path / '00_physics_timeline.md').write_text(timeline, encoding='utf-8')
    print(f"  00_physics_timeline.md")

    print("\nDone!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='data/physics_extracts')
    args = parser.parse_args()

    run_extraction(args.output)
