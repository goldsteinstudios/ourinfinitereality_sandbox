"""
Core voice extraction logic.

Orchestrates parsing and provides the main extraction interface.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib

from .parsers.claude import parse_claude_export
from .parsers.chatgpt import parse_chatgpt_export


@dataclass
class VoiceMessage:
    """
    A single extracted message from the user's voice.
    """
    content: str
    timestamp: Optional[datetime]
    conversation_id: str
    conversation_title: str
    platform: str
    char_count: int
    word_count: int
    _hash: str = field(default='', repr=False)

    def __post_init__(self):
        # Generate hash for deduplication
        if not self._hash:
            self._hash = hashlib.md5(
                f"{self.content}{self.timestamp}".encode('utf-8')
            ).hexdigest()[:12]

    @property
    def date_str(self) -> str:
        """Return date as string for grouping."""
        if self.timestamp:
            return self.timestamp.strftime('%Y-%m-%d')
        return 'undated'

    @property
    def datetime_str(self) -> str:
        """Return full datetime as string."""
        if self.timestamp:
            return self.timestamp.isoformat()
        return 'undated'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'content': self.content,
            'timestamp': self.datetime_str,
            'conversation_id': self.conversation_id,
            'conversation_title': self.conversation_title,
            'platform': self.platform,
            'char_count': self.char_count,
            'word_count': self.word_count,
        }


def extract_voice(
    export_file: str,
    platform: str = 'claude'
) -> List[VoiceMessage]:
    """
    Extract user messages from an AI conversation export.

    Args:
        export_file: Path to the export JSON file
        platform: 'claude' or 'chatgpt'

    Returns:
        List of VoiceMessage objects
    """
    path = Path(export_file)

    if not path.exists():
        raise FileNotFoundError(f"Export file not found: {export_file}")

    # Select parser based on platform
    if platform.lower() == 'claude':
        raw_messages = parse_claude_export(str(path))
    elif platform.lower() in ('chatgpt', 'openai'):
        raw_messages = parse_chatgpt_export(str(path))
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    # Convert to VoiceMessage objects
    messages = []
    for msg in raw_messages:
        messages.append(VoiceMessage(
            content=msg['content'],
            timestamp=msg.get('timestamp'),
            conversation_id=msg.get('conversation_id', 'unknown'),
            conversation_title=msg.get('conversation_title', ''),
            platform=msg.get('platform', platform),
            char_count=msg.get('char_count', len(msg['content'])),
            word_count=msg.get('word_count', len(msg['content'].split())),
        ))

    # Sort by timestamp
    messages.sort(key=lambda m: (m.timestamp is None, m.timestamp))

    # Deduplicate
    messages = deduplicate(messages)

    return messages


def extract_from_directory(
    directory: str,
    platform: str = 'claude'
) -> List[VoiceMessage]:
    """
    Extract user messages from all export files in a directory.

    Args:
        directory: Path to directory containing export files
        platform: 'claude' or 'chatgpt'

    Returns:
        List of VoiceMessage objects from all files
    """
    path = Path(directory)

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    all_messages = []

    for json_file in path.glob('*.json'):
        try:
            messages = extract_voice(str(json_file), platform)
            all_messages.extend(messages)
        except Exception as e:
            print(f"Warning: Failed to parse {json_file}: {e}")

    # Sort and deduplicate combined results
    all_messages.sort(key=lambda m: (m.timestamp is None, m.timestamp))
    all_messages = deduplicate(all_messages)

    return all_messages


def deduplicate(messages: List[VoiceMessage]) -> List[VoiceMessage]:
    """
    Remove duplicate messages based on content and timestamp.
    """
    seen_hashes = set()
    unique = []

    for msg in messages:
        if msg._hash not in seen_hashes:
            seen_hashes.add(msg._hash)
            unique.append(msg)

    return unique


def filter_substantial(
    messages: List[VoiceMessage],
    min_chars: int = 500
) -> List[VoiceMessage]:
    """
    Filter to only substantial messages (above character threshold).

    Args:
        messages: List of VoiceMessage objects
        min_chars: Minimum character count to include

    Returns:
        Filtered list containing only substantial entries
    """
    return [m for m in messages if m.char_count >= min_chars]


def filter_by_date_range(
    messages: List[VoiceMessage],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[VoiceMessage]:
    """
    Filter messages to a date range.

    Args:
        messages: List of VoiceMessage objects
        start_date: Include messages on or after this date
        end_date: Include messages on or before this date

    Returns:
        Filtered list
    """
    filtered = messages

    if start_date:
        filtered = [m for m in filtered if m.timestamp and m.timestamp >= start_date]

    if end_date:
        filtered = [m for m in filtered if m.timestamp and m.timestamp <= end_date]

    return filtered


def get_statistics(messages: List[VoiceMessage]) -> Dict[str, Any]:
    """
    Get statistics about extracted messages.
    """
    if not messages:
        return {
            'total_messages': 0,
            'total_characters': 0,
            'total_words': 0,
            'date_range': None,
            'conversations': 0,
            'platforms': [],
        }

    dated = [m for m in messages if m.timestamp]
    conversations = set(m.conversation_id for m in messages)
    platforms = set(m.platform for m in messages)

    return {
        'total_messages': len(messages),
        'total_characters': sum(m.char_count for m in messages),
        'total_words': sum(m.word_count for m in messages),
        'date_range': {
            'earliest': min(m.timestamp for m in dated).isoformat() if dated else None,
            'latest': max(m.timestamp for m in dated).isoformat() if dated else None,
        },
        'conversations': len(conversations),
        'platforms': list(platforms),
        'substantial_count': len([m for m in messages if m.char_count >= 500]),
        'undated_count': len(messages) - len(dated),
    }
