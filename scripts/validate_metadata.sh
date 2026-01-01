#!/bin/bash

# Validate YAML Front Matter Across All Sets
# Usage: ./scripts/validate_metadata.sh

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
SETS_DIR="$REPO/sets"

echo "=== Validating YAML Front Matter ==="
echo ""

ERRORS=0
FILES_CHECKED=0
SETS_CHECKED=0

for SET_DIR in "$SETS_DIR"/*/; do
    SET_NAME=$(basename "$SET_DIR")
    SETS_CHECKED=$((SETS_CHECKED + 1))

    echo "Checking set: $SET_NAME"

    # Check _set.yaml exists
    if [ ! -f "$SET_DIR/_set.yaml" ]; then
        echo "  ERROR: Missing _set.yaml"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ✓ _set.yaml present"
    fi

    # Check each .md file for YAML front matter
    for f in "$SET_DIR"*.md; do
        if [ -f "$f" ]; then
            FILES_CHECKED=$((FILES_CHECKED + 1))
            BASENAME=$(basename "$f")

            # Check for YAML front matter (starts with ---)
            if ! head -1 "$f" | grep -q "^---$"; then
                echo "  ERROR: $BASENAME missing YAML front matter"
                ERRORS=$((ERRORS + 1))
            else
                # Check for required fields
                if ! grep -q "^title:" "$f"; then
                    echo "  WARNING: $BASENAME missing 'title' field"
                fi
                if ! grep -q "^version:" "$f"; then
                    echo "  WARNING: $BASENAME missing 'version' field"
                fi
                if ! grep -q "^set:" "$f"; then
                    echo "  WARNING: $BASENAME missing 'set' field"
                fi
            fi
        fi
    done

    echo ""
done

echo "=== Validation Complete ==="
echo "Sets checked: $SETS_CHECKED"
echo "Files checked: $FILES_CHECKED"
echo "Errors: $ERRORS"

if [ $ERRORS -gt 0 ]; then
    exit 1
else
    echo "All files valid!"
    exit 0
fi
