"""
Claude conversation export parser.

Handles multiple Claude export formats:
- Older format: messages array with "role" field
- Newer format: chat_messages with "sender" field
- Project exports: may have different structure
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


def parse_claude_export(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a Claude JSON export file and extract human messages.

    Args:
        file_path: Path to the Claude export JSON file

    Returns:
        List of message dictionaries with standardized fields
    """
    path = Path(file_path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = []

    # Handle different export formats
    if isinstance(data, list):
        # List of conversations
        for conversation in data:
            messages.extend(_parse_conversation(conversation))
    elif isinstance(data, dict):
        if 'conversations' in data:
            # Wrapped in conversations key
            for conversation in data['conversations']:
                messages.extend(_parse_conversation(conversation))
        elif 'chat_messages' in data or 'messages' in data:
            # Single conversation
            messages.extend(_parse_conversation(data))
        else:
            # Try to find messages in any nested structure
            messages.extend(_parse_conversation(data))

    return messages


def _parse_conversation(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse a single conversation object and extract human messages.
    """
    messages = []

    # Get conversation metadata
    conv_id = conversation.get('uuid') or conversation.get('id') or conversation.get('conversation_id', 'unknown')
    conv_title = conversation.get('name') or conversation.get('title') or conversation.get('conversation_name', '')
    conv_created = conversation.get('created_at') or conversation.get('create_time')

    # Find the messages array - try multiple possible locations
    message_list = (
        conversation.get('chat_messages') or
        conversation.get('messages') or
        conversation.get('mapping') or
        []
    )

    # Handle mapping format (nested dict with message objects)
    if isinstance(message_list, dict):
        message_list = _flatten_mapping(message_list)

    for msg in message_list:
        if not isinstance(msg, dict):
            continue

        # Check if this is a human message
        is_human = _is_human_message(msg)

        if not is_human:
            continue

        # Extract content
        content = _extract_content(msg)

        if not content or not content.strip():
            continue

        # Extract timestamp
        timestamp = _extract_timestamp(msg, conv_created)

        messages.append({
            'content': content,
            'timestamp': timestamp,
            'conversation_id': conv_id,
            'conversation_title': conv_title,
            'platform': 'claude',
            'char_count': len(content),
            'word_count': len(content.split()),
        })

    return messages


def _is_human_message(msg: Dict[str, Any]) -> bool:
    """
    Determine if a message is from the human user.
    """
    # Check various field names used across formats
    role = msg.get('role') or msg.get('sender') or ''

    if isinstance(role, str):
        return role.lower() in ('human', 'user')

    # Check for author object (ChatGPT-like format)
    author = msg.get('author', {})
    if isinstance(author, dict):
        return author.get('role', '').lower() in ('human', 'user')

    return False


def _extract_content(msg: Dict[str, Any]) -> str:
    """
    Extract the text content from a message object.
    """
    # Direct content field
    content = msg.get('content') or msg.get('text') or ''

    # Handle content as list (some formats have parts)
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                parts.append(part.get('text', ''))
        content = '\n'.join(parts)

    # Handle nested content object
    if isinstance(content, dict):
        content = content.get('text') or content.get('parts', [''])[0] or ''

    return str(content).strip()


def _extract_timestamp(msg: Dict[str, Any], fallback: Optional[str] = None) -> Optional[datetime]:
    """
    Extract and parse timestamp from a message.
    """
    # Try various timestamp field names
    ts = (
        msg.get('created_at') or
        msg.get('timestamp') or
        msg.get('create_time') or
        msg.get('updated_at') or
        fallback
    )

    if ts is None:
        return None

    # Handle numeric timestamps (Unix epoch)
    if isinstance(ts, (int, float)):
        try:
            return datetime.fromtimestamp(ts)
        except (ValueError, OSError):
            # Try milliseconds
            try:
                return datetime.fromtimestamp(ts / 1000)
            except (ValueError, OSError):
                return None

    # Handle string timestamps
    if isinstance(ts, str):
        # Try various formats
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
        ]
        for fmt in formats:
            try:
                return datetime.strptime(ts, fmt)
            except ValueError:
                continue

    return None


def _flatten_mapping(mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Flatten a mapping-style message structure (used in some exports).
    """
    messages = []

    for key, value in mapping.items():
        if isinstance(value, dict):
            msg = value.get('message')
            if msg and isinstance(msg, dict):
                messages.append(msg)

    # Sort by create_time if available
    messages.sort(key=lambda m: m.get('create_time', 0) or 0)

    return messages
