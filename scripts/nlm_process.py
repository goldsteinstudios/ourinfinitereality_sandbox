#!/usr/bin/env python3
"""
NotebookLM Document Processor
Normalizes unicode, injects frontmatter, validates structure.

Usage:
    python scripts/nlm_process.py
    python scripts/nlm_process.py --file path/to/doc.md
    python scripts/nlm_process.py --dry-run
"""

import unicodedata
import re
import json
import argparse
from pathlib import Path
from datetime import date

# ============= CONFIGURATION =============
REPO = Path("/Users/willgoldstein/claudecode/ourinfinitereality_sandbox")
STAGING_DIR = REPO / "notebooklm_staging"
PROCESSED_DIR = REPO / "notebooklm_processed"

# Files to exclude from processing
EXCLUDE_FILES = {
    "the_hamon_tools_as_textbooks.md",
    ".DS_Store",
}

# Unicode normalization form (NFC for Chinese characters)
UNICODE_FORM = "NFC"

# ============= DOCUMENT TYPE DETECTION =============

# Patterns for detecting document types
TYPE_PATTERNS = {
    'core': [
        r'white\s*paper',
        r'formal\s+treatment',
        r'falsifiable\s+framework',
        r'universe\s+as\s+.*verb',
    ],
    'reference': [
        r'glossary',
        r'guide',
        r'vocabulary',
        r'lexicon',
    ],
    'dialogue': [
        r'dialogue',
        r'conversation',
        r'\*\*\w+:\*\*',  # Speaker markers like **Physicist:**
        r'\*\*\w+\s*\([^)]+\):\*\*',  # **Name (role):**
    ],
    'parable': [
        r'parable',
        r'teaching\s+story',
        r'allegory',
        r'sailor',
        r'sisyphus',
        r'kai\s+and',
    ],
}


def detect_document_type(content: str, filename: str) -> str:
    """
    Heuristic categorization based on content patterns.
    Returns: 'core', 'reference', 'dialogue', 'parable', or 'essay'
    """
    text = content.lower()
    fname = filename.lower()

    # Check filename patterns first
    for doc_type, patterns in TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, fname, re.IGNORECASE):
                return doc_type

    # Check content patterns
    for doc_type, patterns in TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return doc_type

    # Default to essay
    return 'essay'


# ============= UNICODE NORMALIZATION =============

def normalize_unicode(text: str) -> str:
    """
    Normalize unicode to NFC form.
    Critical for Chinese characters in DDJ references.
    Also decodes any escaped unicode sequences.
    """
    # First, decode escaped unicode (e.g., \u7121 -> 無)
    def decode_escape(match):
        try:
            return chr(int(match.group(1), 16))
        except ValueError:
            return match.group(0)

    text = re.sub(r'\\u([0-9a-fA-F]{4})', decode_escape, text)

    # Apply NFC normalization
    return unicodedata.normalize(UNICODE_FORM, text)


# ============= TAG EXTRACTION =============

def extract_tags(content: str) -> list:
    """Extract relevant tags from document content."""
    tags = set()

    # RSM core concepts
    if re.search(r'V₀|V_0|absolute\s+void', content, re.IGNORECASE):
        tags.add('V₀')
    if re.search(r'O₁|O_1|generative\s+center', content, re.IGNORECASE):
        tags.add('O₁')
    if re.search(r'無\s*\(|無\s*=|無\s*is', content):
        tags.add('無')
    if re.search(r'有\s*\(|有\s*=|有\s*is', content):
        tags.add('有')
    if re.search(r'道\s*\(|道\s*=|道\s*is|Dao\s+De\s+Jing', content, re.IGNORECASE):
        tags.add('道')
    if re.search(r'無為|wu\s*wei', content, re.IGNORECASE):
        tags.add('無為')
    if re.search(r'Euler', content, re.IGNORECASE):
        tags.add('Euler-identity')
    if re.search(r'recursiv', content, re.IGNORECASE):
        tags.add('recursion')
    if re.search(r'persist', content, re.IGNORECASE):
        tags.add('persistence')

    return sorted(list(tags))


# ============= FRONTMATTER =============

def has_frontmatter(content: str) -> bool:
    """Check if document already has YAML frontmatter."""
    return content.strip().startswith('---')


def extract_title(content: str, filename: str) -> tuple:
    """Extract title and subtitle from H1/H2 headings."""
    # Remove frontmatter if present
    text = content
    if has_frontmatter(content):
        match = re.search(r'^---\n.*?\n---\n', content, re.DOTALL)
        if match:
            text = content[match.end():]

    # Find H1
    title_match = re.search(r'^#\s+(.+?)(?:\n|$)', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else None

    # Find H2 (subtitle)
    subtitle_match = re.search(r'^##\s+(.+?)(?:\n|$)', text, re.MULTILINE)
    subtitle = subtitle_match.group(1).strip() if subtitle_match else None

    # Fallback to filename
    if not title:
        title = filename.replace('.md', '').replace('_', ' ').title()

    return title, subtitle


def generate_frontmatter(filename: str, content: str, doc_type: str) -> str:
    """Generate YAML frontmatter block."""
    title, subtitle = extract_title(content, filename)
    tags = extract_tags(content)

    lines = [
        '---',
        f'title: "{title}"',
    ]

    if subtitle:
        lines.append(f'subtitle: "{subtitle}"')

    lines.extend([
        'source: notebooklm',
        'version: "0.993"',
        f'doc_type: {doc_type}',
        f'generated_date: "2026-01-05"',
        f'processed_date: "{date.today()}"',
        'status: draft',
    ])

    if tags:
        lines.append('tags:')
        for tag in tags:
            lines.append(f'  - "{tag}"')

    lines.append('---')

    return '\n'.join(lines)


def inject_frontmatter(content: str, frontmatter: str) -> str:
    """Add YAML frontmatter block to document."""
    # Remove existing frontmatter if present
    if has_frontmatter(content):
        match = re.search(r'^---\n.*?\n---\n', content, re.DOTALL)
        if match:
            content = content[match.end():]

    return frontmatter + '\n\n' + content.lstrip()


# ============= VALIDATION =============

def validate_document(content: str) -> list:
    """
    Validate processed document structure.
    Returns list of warnings (empty = valid).
    """
    warnings = []

    # Check for frontmatter
    if not has_frontmatter(content):
        warnings.append("Missing frontmatter")

    # Check for at least one heading
    if not re.search(r'^#', content, re.MULTILINE):
        warnings.append("No headings found")

    # Check for broken Chinese character encoding
    if '\ufffd' in content:
        warnings.append("Contains replacement characters (encoding issue)")

    # Check for unescaped unicode
    if '\\u' in content:
        warnings.append("Contains unescaped unicode sequences")

    # Check minimum content length
    if len(content) < 500:
        warnings.append("Document unusually short (<500 chars)")

    # Count Chinese characters
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    if len(chinese_chars) < 3:
        warnings.append(f"Few Chinese characters ({len(chinese_chars)}) - unusual for RSM docs")

    return warnings


# ============= PROCESSING =============

def process_file(filepath: Path) -> tuple:
    """
    Process a single file through the pipeline.
    Returns (processed_content, doc_type, warnings)
    """
    content = filepath.read_text(encoding='utf-8')

    # Step 1: Unicode normalization
    content = normalize_unicode(content)

    # Step 2: Detect document type
    doc_type = detect_document_type(content, filepath.name)

    # Step 3: Generate and inject frontmatter
    frontmatter = generate_frontmatter(filepath.name, content, doc_type)
    content = inject_frontmatter(content, frontmatter)

    # Step 4: Validate
    warnings = validate_document(content)

    return content, doc_type, warnings


def process_all(dry_run: bool = False):
    """Process all files in staging directory."""
    if not STAGING_DIR.exists():
        print(f"ERROR: Staging directory not found: {STAGING_DIR}")
        return

    # Create output directory
    if not dry_run:
        PROCESSED_DIR.mkdir(exist_ok=True)

    # Get all markdown files
    files = [f for f in STAGING_DIR.glob('*.md') if f.name not in EXCLUDE_FILES]

    print(f"=== NotebookLM Document Processor ===")
    print(f"Staging: {STAGING_DIR}")
    print(f"Output:  {PROCESSED_DIR}")
    print(f"Files:   {len(files)}")
    print(f"Mode:    {'DRY RUN' if dry_run else 'PROCESSING'}")
    print()

    results = []

    for filepath in sorted(files):
        print(f"Processing: {filepath.name}")

        try:
            content, doc_type, warnings = process_file(filepath)

            # Count stats
            word_count = len(content.split())
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))

            result = {
                'filename': filepath.name,
                'doc_type': doc_type,
                'word_count': word_count,
                'chinese_chars': chinese_chars,
                'warnings': warnings,
                'status': 'PASS' if not warnings else 'WARN',
            }
            results.append(result)

            # Print result
            status_icon = '✓' if not warnings else '⚠'
            print(f"  {status_icon} {doc_type} | {word_count} words | {chinese_chars} 漢字")
            for w in warnings:
                print(f"    - {w}")

            # Write output
            if not dry_run:
                output_path = PROCESSED_DIR / filepath.name
                output_path.write_text(content, encoding='utf-8')

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append({
                'filename': filepath.name,
                'status': 'ERROR',
                'error': str(e),
            })

    # Summary
    print()
    print("=== Summary ===")
    by_type = {}
    for r in results:
        t = r.get('doc_type', 'error')
        by_type[t] = by_type.get(t, 0) + 1

    for doc_type, count in sorted(by_type.items()):
        print(f"  {doc_type}: {count}")

    passed = sum(1 for r in results if r.get('status') == 'PASS')
    warned = sum(1 for r in results if r.get('status') == 'WARN')
    errored = sum(1 for r in results if r.get('status') == 'ERROR')

    print()
    print(f"  PASS: {passed} | WARN: {warned} | ERROR: {errored}")

    if not dry_run:
        # Save report
        report_path = PROCESSED_DIR / '_processing_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nReport saved: {report_path}")


# ============= MAIN =============

def main():
    parser = argparse.ArgumentParser(description='Process NotebookLM documents')
    parser.add_argument('--file', type=Path, help='Process a single file')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = parser.parse_args()

    if args.file:
        if not args.file.exists():
            print(f"ERROR: File not found: {args.file}")
            return
        content, doc_type, warnings = process_file(args.file)
        print(f"Type: {doc_type}")
        print(f"Warnings: {warnings if warnings else 'None'}")
        print()
        print(content[:500] + '...' if len(content) > 500 else content)
    else:
        process_all(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
