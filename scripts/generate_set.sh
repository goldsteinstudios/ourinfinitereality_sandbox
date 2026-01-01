#!/bin/bash

# Generate Combined File for a Single Set
# Usage: ./scripts/generate_set.sh <set-name>
# Example: ./scripts/generate_set.sh rsm-core

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
SETS_DIR="$REPO/sets"
DOCSET_DIR="$REPO/docset"

# Require set name
if [ -z "$1" ]; then
    echo "Usage: $0 <set-name>"
    echo ""
    echo "Available sets:"
    ls -1 "$SETS_DIR" | sed 's/^/  /'
    exit 1
fi

SET_NAME="$1"
SET_DIR="$SETS_DIR/$SET_NAME"
OUTPUT_FILE="$DOCSET_DIR/set_${SET_NAME}.md"

# Validate set exists
if [ ! -d "$SET_DIR" ]; then
    echo "Error: Set not found: $SET_DIR"
    echo ""
    echo "Available sets:"
    ls -1 "$SETS_DIR" | sed 's/^/  /'
    exit 1
fi

# Validate _set.yaml exists
if [ ! -f "$SET_DIR/_set.yaml" ]; then
    echo "Error: _set.yaml not found in $SET_DIR"
    exit 1
fi

echo "=== Generating Combined File for $SET_NAME ==="
echo ""

# Get set metadata
SET_DISPLAY=$(grep "set_name:" "$SET_DIR/_set.yaml" | sed 's/set_name: "//' | sed 's/"$//')
VERSION=$(grep "version:" "$SET_DIR/_set.yaml" | sed 's/version: "//' | sed 's/"$//')
TODAY=$(date +%Y-%m-%d)

# Create output file header
cat > "$OUTPUT_FILE" << EOF
# $SET_DISPLAY — Combined Document
## Version $VERSION | Generated $TODAY

---

EOF

# Append each markdown file (sorted, excluding _set.yaml)
FILE_COUNT=0
for f in "$SET_DIR"/*.md; do
    if [ -f "$f" ]; then
        BASENAME=$(basename "$f")
        echo "  Adding: $BASENAME"

        echo -e "\n# ═══════════════════════════════════════════════════════════════" >> "$OUTPUT_FILE"
        echo -e "# FILE: $BASENAME" >> "$OUTPUT_FILE"
        echo -e "# ═══════════════════════════════════════════════════════════════\n" >> "$OUTPUT_FILE"

        cat "$f" >> "$OUTPUT_FILE"
        echo -e "\n\n---\n\n" >> "$OUTPUT_FILE"

        FILE_COUNT=$((FILE_COUNT + 1))
    fi
done

# Show stats
LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')

echo ""
echo "=== Generated ==="
echo "Set: $SET_NAME"
echo "Files: $FILE_COUNT"
echo "Output: $OUTPUT_FILE"
echo "Lines: $LINES"
echo "Size: $SIZE"
