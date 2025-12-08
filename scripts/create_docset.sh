#!/bin/bash

# Create docset for Our Infinite Reality notebook import
# Usage: ./scripts/create_docset.sh [date]
# Example: ./scripts/create_docset.sh 12.08.25

DATE=${1:-$(date +"%m.%d.%y")}
DOCSET_DIR="docsets/docset_${DATE}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_ROOT"

# Create docset directory
mkdir -p "$DOCSET_DIR"

echo "Creating docset for $DATE..."

# Copy all .md files from these directories:
# - translations/ (chapters, meta, lexicon, analysis, appendices, archaeology, guodian)
# - research/work/CURRENT/ (framework, physics, biology, ttc_mappings, essays)

# Translations
find translations -name "*.md" -type f | while read file; do
    cp "$file" "$DOCSET_DIR/"
done

# Research CURRENT (not ARCHIVE)
find research/work/CURRENT -name "*.md" -type f 2>/dev/null | while read file; do
    cp "$file" "$DOCSET_DIR/"
done

# Exclude patterns (remove if accidentally copied):
# - Chat dumps, transcripts
# - Anything with "dump" or "transcript" in name
# - Anything in ARCHIVE folders
cd "$DOCSET_DIR"
rm -f *dump* *transcript* *chat* 2>/dev/null

# Count files
COUNT=$(ls -1 *.md 2>/dev/null | wc -l | tr -d ' ')

echo "Created $DOCSET_DIR with $COUNT markdown files"
echo ""
echo "Contents:"
ls -1 *.md | head -20
if [ "$COUNT" -gt 20 ]; then
    echo "... and $((COUNT - 20)) more files"
fi
