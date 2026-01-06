#!/bin/bash

# NotebookLM Publication Pipeline
# Generates docsets from NLM sets and optionally publishes
#
# Usage: ./scripts/nlm_publish.sh [commit_message]

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
SCRIPT_DIR="$REPO/scripts"
COMMIT_MSG="${1:-Add NotebookLM generated content}"

echo "=== NotebookLM Publication Pipeline ==="
echo ""

# Step 1: Generate combined files for all sets (including new nlm-* sets)
echo "Step 1: Generating combined set files..."
"$SCRIPT_DIR/generate_all_sets.sh"
echo ""

# Step 2: Validate NLM docsets were generated
echo "Step 2: Validating NLM docsets..."
NLM_DOCSETS=$(ls "$REPO/docset"/set_nlm-*.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$NLM_DOCSETS" -eq 0 ]; then
    echo "  WARNING: No NLM docsets generated"
else
    echo "  Found $NLM_DOCSETS NLM docsets:"
    for f in "$REPO/docset"/set_nlm-*.md; do
        if [ -f "$f" ]; then
            LINES=$(wc -l < "$f" | tr -d ' ')
            SIZE=$(ls -lh "$f" | awk '{print $5}')
            echo "    $(basename "$f"): $LINES lines, $SIZE"
        fi
    done
fi
echo ""

# Step 3: Show summary of new content
echo "Step 3: NLM Sets Summary..."
for set_dir in "$REPO/sets"/nlm-*/; do
    if [ -d "$set_dir" ]; then
        SET_NAME=$(basename "$set_dir")
        FILE_COUNT=$(find "$set_dir" -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')
        echo "  $SET_NAME: $FILE_COUNT files"
    fi
done
echo ""

# Step 4: Ask about publication
echo "Step 4: Publication..."
echo ""
echo "Generated docsets are ready for NotebookLM loading:"
echo "  $REPO/docset/set_nlm-*.md"
echo ""

read -p "Publish to ourinfinitereality.com? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Publishing..."
    "$SCRIPT_DIR/publish.sh" "$COMMIT_MSG"
else
    echo "Skipping publication."
    echo "Run './scripts/publish.sh' manually when ready."
fi

echo ""
echo "=== Pipeline Complete ==="
