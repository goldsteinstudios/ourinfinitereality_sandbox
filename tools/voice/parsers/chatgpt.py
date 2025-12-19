"""
ChatGPT conversation export parser.

Handles exports from Settings → Data Controls → Export.
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


def parse_chatgpt_export(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a ChatGPT JSON export file and extract user messages.

    Args:
        file_path: Path to the ChatGPT export JSON file (conversations.json)

    Returns:
        List of message dictionaries with standardized fields
    """
    path = Path(file_path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = []

    # ChatGPT exports are typically a list of conversations
    if isinstance(data, list):
        for conversation in data:
            messages.extend(_parse_conversation(conversation))
    elif isinstance(data, dict):
        # Single conversation or wrapped
        if 'conversations' in data:
            for conversation in data['conversations']:
                messages.extend(_parse_conversation(conversation))
        else:
            messages.extend(_parse_conversation(data))

    return messages


def _parse_conversation(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse a single ChatGPT conversation object and extract user messages.
    """
    messages = []

    # Get conversation metadata
    conv_id = conversation.get('id') or conversation.get('conversation_id', 'unknown')
    conv_title = conversation.get('title', '')
    conv_created = conversation.get('create_time')

    # ChatGPT uses a 'mapping' structure for messages
    mapping = conversation.get('mapping', {})

    if not mapping:
        return messages

    # Flatten and sort the mapping
    message_list = []
    for node_id, node in mapping.items():
        if not isinstance(node, dict):
            continue

        msg = node.get('message')
        if msg and isinstance(msg, dict):
            msg['_node_id'] = node_id
            msg['_parent'] = node.get('parent')
            message_list.append(msg)

    # Sort by create_time
    message_list.sort(key=lambda m: m.get('create_time', 0) or 0)

    for msg in message_list:
        # Check if this is a user message
        author = msg.get('author', {})
        if not isinstance(author, dict):
            continue

        role = author.get('role', '')
        if role.lower() != 'user':
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
            'platform': 'chatgpt',
            'char_count': len(content),
            'word_count': len(content.split()),
        })

    return messages


def _extract_content(msg: Dict[str, Any]) -> str:
    """
    Extract the text content from a ChatGPT message object.
    """
    content = msg.get('content', {})

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, dict):
        parts = content.get('parts', [])
        if parts:
            # Join all text parts
            text_parts = []
            for part in parts:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict):
                    # Handle structured content (images, etc.)
                    text_parts.append(part.get('text', ''))
            return '\n'.join(text_parts).strip()

    return ''


def _extract_timestamp(msg: Dict[str, Any], fallback: Optional[float] = None) -> Optional[datetime]:
    """
    Extract and parse timestamp from a ChatGPT message.
    """
    ts = msg.get('create_time') or msg.get('update_time') or fallback

    if ts is None:
        return None

    # ChatGPT uses Unix timestamps (float)
    if isinstance(ts, (int, float)):
        try:
            return datetime.fromtimestamp(ts)
        except (ValueError, OSError):
            return None

    return None
