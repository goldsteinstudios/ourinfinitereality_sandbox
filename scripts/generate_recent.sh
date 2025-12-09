#!/bin/bash

# Generate Recently Updated page sorted by modification date
# Run this before publishing to keep the page current

OUTPUT="translations/meta/recently_updated.md"

cat > "$OUTPUT" << 'HEADER'
# Recently Updated

*Documents sorted by last modification date*

---

HEADER

# Get all markdown files with their modification times and format as table
echo "| Document | Last Updated |" >> "$OUTPUT"
echo "|----------|--------------|" >> "$OUTPUT"

# Find all .md files, get mod time, sort by most recent
find translations -name "*.md" -type f ! -name "recently_updated.md" -exec stat -f "%m|%N" {} \; | \
sort -rn | \
while IFS='|' read -r timestamp filepath; do
    # Convert timestamp to readable date
    date_str=$(date -r "$timestamp" "+%Y-%m-%d")

    # Get filename without path for display
    filename=$(basename "$filepath")

    # Create relative path for link (from docs/translations perspective)
    # Remove 'translations/' prefix since we're already in that context
    linkpath="${filepath#translations/}"

    # Extract title from first # heading if possible, otherwise use filename
    title=$(grep -m1 "^# " "$filepath" 2>/dev/null | sed 's/^# //')
    if [ -z "$title" ]; then
        title="$filename"
    fi

    # Truncate long titles
    if [ ${#title} -gt 50 ]; then
        title="${title:0:47}..."
    fi

    echo "| [$title]($linkpath) | $date_str |" >> "$OUTPUT"
done

cat >> "$OUTPUT" << 'FOOTER'

---

*This page is automatically generated from file modification dates.*
FOOTER

echo "Generated $OUTPUT"
