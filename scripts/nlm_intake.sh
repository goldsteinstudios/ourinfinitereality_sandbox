#!/bin/bash

# NotebookLM Document Intake
# Validates staging directory and creates inventory
#
# Usage: ./scripts/nlm_intake.sh [staging_dir]

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
STAGING_DIR="${1:-$REPO/notebooklm_staging}"

echo "=== NotebookLM Document Intake ==="
echo ""
echo "Staging directory: $STAGING_DIR"
echo ""

# Validate staging directory exists
if [ ! -d "$STAGING_DIR" ]; then
    echo "ERROR: Staging directory not found"
    exit 1
fi

# Count markdown files (excluding .DS_Store and nested directories)
FILE_COUNT=$(find "$STAGING_DIR" -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "ERROR: No markdown files found in staging directory"
    exit 1
fi

echo "Found $FILE_COUNT markdown files:"
echo ""

# List files with sizes
TOTAL_SIZE=0
for f in "$STAGING_DIR"/*.md; do
    if [ -f "$f" ]; then
        BASENAME=$(basename "$f")
        SIZE=$(ls -lh "$f" | awk '{print $5}')
        WORDS=$(wc -w < "$f" | tr -d ' ')
        echo "  $BASENAME ($SIZE, $WORDS words)"
    fi
done

echo ""

# Check for files that already exist in sets/
echo "Checking for duplicates in existing sets..."
DUPLICATES=0
for f in "$STAGING_DIR"/*.md; do
    if [ -f "$f" ]; then
        BASENAME=$(basename "$f")
        # Check if file exists in any set
        EXISTING=$(find "$REPO/sets" -name "*$BASENAME" 2>/dev/null | head -1)
        if [ -n "$EXISTING" ]; then
            echo "  DUPLICATE: $BASENAME -> $EXISTING"
            DUPLICATES=$((DUPLICATES + 1))
        fi
    fi
done

if [ "$DUPLICATES" -eq 0 ]; then
    echo "  No duplicates found"
fi

echo ""

# Check for excluded files
EXCLUDED="the_hamon_tools_as_textbooks.md"
if [ -f "$STAGING_DIR/$EXCLUDED" ]; then
    echo "Note: $EXCLUDED will be excluded from processing"
    echo ""
fi

# Summary
echo "=== Intake Summary ==="
echo "Files ready for processing: $FILE_COUNT"
echo ""
echo "Next steps:"
echo "  1. python scripts/nlm_process.py --dry-run  # Preview processing"
echo "  2. python scripts/nlm_process.py            # Process documents"
echo "  3. python scripts/nlm_organize.py           # Organize into sets"
