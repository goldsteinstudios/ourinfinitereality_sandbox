#!/bin/bash

# Creates a single concatenated docset for AI context
# Output: docset_YYYY-MM-DD.md in project root

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
DATE=$(date +%Y-%m-%d)
OUTPUT="$REPO/docset_$DATE.md"

echo "Creating docset..."

cat > "$OUTPUT" << 'HEADER'
# Our Infinite Reality - Complete Docset

This document contains the complete structural translation corpus for AI context.

---

HEADER

# Framework docs first (provides context)
echo "Adding framework docs..."
echo -e "\n\n# PART 1: FRAMEWORK\n" >> "$OUTPUT"

for f in "$REPO/translations/meta/recursive_structural_model.md" \
         "$REPO/translations/meta/framework_synthesis_2025-12-07.md" \
         "$REPO/translations/meta/chapter25_rosetta_stone_2025-12-07.md"; do
    if [ -f "$f" ]; then
        echo -e "\n---\n" >> "$OUTPUT"
        cat "$f" >> "$OUTPUT"
    fi
done

# Lexicon
echo "Adding lexicon..."
echo -e "\n\n# PART 2: LEXICON\n" >> "$OUTPUT"

for f in "$REPO/translations/lexicon/"*.md; do
    if [ -f "$f" ]; then
        echo -e "\n---\n" >> "$OUTPUT"
        cat "$f" >> "$OUTPUT"
    fi
done

# All chapters in order
echo "Adding chapters..."
echo -e "\n\n# PART 3: CHAPTER TRANSLATIONS\n" >> "$OUTPUT"

for f in $(ls "$REPO/translations/chapters/"*.md | sort); do
    if [ -f "$f" ]; then
        echo -e "\n---\n" >> "$OUTPUT"
        cat "$f" >> "$OUTPUT"
    fi
done

# Additional meta docs
echo "Adding additional framework docs..."
echo -e "\n\n# PART 4: ADDITIONAL FRAMEWORK\n" >> "$OUTPUT"

for f in "$REPO/translations/meta/"*.md; do
    # Skip ones we already added
    case "$f" in
        *recursive_structural_model*|*framework_synthesis*|*rosetta_stone*|*recently_updated*)
            continue
            ;;
    esac
    if [ -f "$f" ]; then
        echo -e "\n---\n" >> "$OUTPUT"
        cat "$f" >> "$OUTPUT"
    fi
done

# Word count
WC=$(wc -w < "$OUTPUT")
LINES=$(wc -l < "$OUTPUT")

echo ""
echo "✓ Docset created: $OUTPUT"
echo "  $LINES lines, $WC words"
