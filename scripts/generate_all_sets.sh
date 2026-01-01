#!/bin/bash

# Generate Combined Files for All Sets
# Usage: ./scripts/generate_all_sets.sh

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
SETS_DIR="$REPO/sets"
DOCSET_DIR="$REPO/docset"
SCRIPT_DIR="$REPO/scripts"

echo "=== Generating Combined Files for All Sets ==="
echo ""

# Ensure docset directory exists
mkdir -p "$DOCSET_DIR"

# Generate each set
SETS_GENERATED=0
TOTAL_LINES=0
for SET_DIR in "$SETS_DIR"/*/; do
    SET_NAME=$(basename "$SET_DIR")

    if [ -f "$SET_DIR/_set.yaml" ]; then
        echo "--- Generating: $SET_NAME ---"
        "$SCRIPT_DIR/generate_set.sh" "$SET_NAME"

        # Count lines
        OUTPUT_FILE="$DOCSET_DIR/set_${SET_NAME}.md"
        if [ -f "$OUTPUT_FILE" ]; then
            LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
            TOTAL_LINES=$((TOTAL_LINES + LINES))
        fi

        SETS_GENERATED=$((SETS_GENERATED + 1))
        echo ""
    fi
done

echo ""
echo "=== All Sets Generated ==="
echo "Sets: $SETS_GENERATED"
echo "Total lines: $TOTAL_LINES"
echo ""
echo "Output files:"
ls -lh "$DOCSET_DIR"/set_*.md 2>/dev/null || echo "  (none generated)"
