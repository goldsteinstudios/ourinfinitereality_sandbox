"""
Search and discovery functions for extracted voice messages.

Find first mentions, search across all messages, and track concept evolution.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .extractor import VoiceMessage


@dataclass
class SearchResult:
    """A single search result with context."""
    message: VoiceMessage
    snippet: str
    match_count: int
    match_positions: List[int]


def find_first_mention(
    messages: List[VoiceMessage],
    search_terms: List[str]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Find the first occurrence of each search term.

    Args:
        messages: List of VoiceMessage objects (should be sorted by timestamp)
        search_terms: List of terms to search for

    Returns:
        Dictionary mapping terms to first occurrence data:
        {
            'term': {
                'date': '2023-04-12',
                'conversation': 'conversation title',
                'conversation_id': 'uuid',
                'snippet': '...context around match...',
                'message': VoiceMessage object
            }
        }
    """
    # Sort messages by timestamp
    sorted_messages = sorted(
        messages,
        key=lambda m: (m.timestamp is None, m.timestamp)
    )

    results = {}

    for term in search_terms:
        results[term] = None

        for msg in sorted_messages:
            if _contains_term(msg.content, term):
                snippet = _extract_snippet(msg.content, term, context_chars=150)
                results[term] = {
                    'date': msg.date_str,
                    'conversation': msg.conversation_title or msg.conversation_id,
                    'conversation_id': msg.conversation_id,
                    'snippet': snippet,
                    'message': msg,
                }
                break  # Found first mention, move to next term

    return results


def search_voice(
    messages: List[VoiceMessage],
    query: str,
    case_sensitive: bool = False,
    regex: bool = False,
    limit: Optional[int] = None
) -> List[SearchResult]:
    """
    Search across all messages for a query.

    Args:
        messages: List of VoiceMessage objects
        query: Search string or regex pattern
        case_sensitive: Whether to match case
        regex: Whether to treat query as regex
        limit: Maximum number of results to return

    Returns:
        List of SearchResult objects
    """
    results = []

    # Compile pattern
    if regex:
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            pattern = re.compile(query, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    else:
        if case_sensitive:
            pattern = re.compile(re.escape(query))
        else:
            pattern = re.compile(re.escape(query), re.IGNORECASE)

    # Sort by timestamp for consistent ordering
    sorted_messages = sorted(
        messages,
        key=lambda m: (m.timestamp is None, m.timestamp)
    )

    for msg in sorted_messages:
        matches = list(pattern.finditer(msg.content))

        if matches:
            # Get positions
            positions = [m.start() for m in matches]

            # Extract snippet around first match
            snippet = _extract_snippet(msg.content, query, context_chars=150)

            results.append(SearchResult(
                message=msg,
                snippet=snippet,
                match_count=len(matches),
                match_positions=positions,
            ))

            if limit and len(results) >= limit:
                break

    return results


def search_by_date_range(
    messages: List[VoiceMessage],
    query: str,
    start_date: str,
    end_date: str
) -> List[SearchResult]:
    """
    Search within a specific date range.

    Args:
        messages: List of VoiceMessage objects
        query: Search string
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        List of SearchResult objects
    """
    # Filter by date range
    filtered = [
        m for m in messages
        if m.date_str >= start_date and m.date_str <= end_date
    ]

    return search_voice(filtered, query)


def count_mentions(
    messages: List[VoiceMessage],
    terms: List[str]
) -> Dict[str, int]:
    """
    Count total mentions of each term across all messages.

    Args:
        messages: List of VoiceMessage objects
        terms: List of terms to count

    Returns:
        Dictionary mapping terms to mention counts
    """
    counts = {term: 0 for term in terms}

    for msg in messages:
        content_lower = msg.content.lower()
        for term in terms:
            # Count all occurrences
            term_lower = term.lower()
            counts[term] += content_lower.count(term_lower)

            # Also try exact match for Chinese characters
            if term != term_lower:
                counts[term] += msg.content.count(term)

    return counts


def get_mentions_over_time(
    messages: List[VoiceMessage],
    term: str
) -> Dict[str, int]:
    """
    Track how mentions of a term change over time.

    Args:
        messages: List of VoiceMessage objects
        term: Term to track

    Returns:
        Dictionary mapping date strings to mention counts
    """
    # Sort by timestamp
    sorted_messages = sorted(
        messages,
        key=lambda m: (m.timestamp is None, m.timestamp)
    )

    by_date: Dict[str, int] = {}

    for msg in sorted_messages:
        if _contains_term(msg.content, term):
            date = msg.date_str
            by_date[date] = by_date.get(date, 0) + 1

    return by_date


def find_related_messages(
    messages: List[VoiceMessage],
    reference_message: VoiceMessage,
    min_shared_words: int = 5
) -> List[VoiceMessage]:
    """
    Find messages that share significant content with a reference message.

    Args:
        messages: List of VoiceMessage objects
        reference_message: The message to find related messages for
        min_shared_words: Minimum number of shared significant words

    Returns:
        List of related VoiceMessage objects
    """
    # Extract significant words from reference (skip common words)
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'to', 'of',
        'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'between', 'under',
        'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
        'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why',
        'how', 'all', 'each', 'every', 'any', 'some', 'no', 'none', 'more',
        'most', 'other', 'such', 'like', 'about', 'if', 'then', 'because',
    }

    ref_words = set(
        word.lower() for word in re.findall(r'\b\w+\b', reference_message.content)
        if len(word) > 3 and word.lower() not in stop_words
    )

    related = []

    for msg in messages:
        if msg._hash == reference_message._hash:
            continue

        msg_words = set(
            word.lower() for word in re.findall(r'\b\w+\b', msg.content)
            if len(word) > 3 and word.lower() not in stop_words
        )

        shared = ref_words & msg_words

        if len(shared) >= min_shared_words:
            related.append(msg)

    return related


def _contains_term(content: str, term: str) -> bool:
    """
    Check if content contains a term (case-insensitive for ASCII).
    """
    # For Chinese/unicode characters, do exact match
    if term in content:
        return True

    # For ASCII, do case-insensitive
    return term.lower() in content.lower()


def _extract_snippet(content: str, term: str, context_chars: int = 150) -> str:
    """
    Extract a snippet of text around the first occurrence of a term.
    """
    # Find term (case-insensitive for ASCII)
    idx = content.find(term)
    if idx == -1:
        idx = content.lower().find(term.lower())

    if idx == -1:
        # Term not found, return beginning of content
        return content[:context_chars * 2] + "..." if len(content) > context_chars * 2 else content

    # Extract context around match
    start = max(0, idx - context_chars)
    end = min(len(content), idx + len(term) + context_chars)

    snippet = content[start:end]

    # Clean up
    snippet = snippet.replace('\n', ' ')
    snippet = re.sub(r'\s+', ' ', snippet)

    # Add ellipsis
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    return snippet.strip()
