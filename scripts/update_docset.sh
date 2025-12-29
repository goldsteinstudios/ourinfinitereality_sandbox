#!/bin/bash

# Update Docset Script
# Regenerates the RSM docset with versioning and archiving
# Usage: ./scripts/update_docset.sh <version> [commit message]
# Example: ./scripts/update_docset.sh v0.981 "Add 玄牝 analysis"

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
DOCSET_DIR="$REPO/docset"
PUBLIC_DOCSET="$REPO/public/docset"
CURRENT_DIR="$DOCSET_DIR/current"
ARCHIVE_DIR="$DOCSET_DIR/archive"

# Require version parameter
if [ -z "$1" ]; then
    echo "Usage: $0 <version> [commit message]"
    echo "Example: $0 v0.981 \"Update with deep review refinements\""
    exit 1
fi

VERSION="$1"
RSM_FILE="$REPO/rsm/canonical/rsm_${VERSION}.md"
COMMIT_MSG="${2:-Update docset to RSM $VERSION}"
TODAY=$(date +%Y-%m-%d)

# Validate RSM file exists
if [ ! -f "$RSM_FILE" ]; then
    echo "Error: RSM file not found: $RSM_FILE"
    echo "Available versions:"
    ls "$REPO/rsm/canonical/" | grep "rsm_v" | sed 's/rsm_/  /; s/.md//'
    exit 1
fi

echo "=== Updating RSM Docset to $VERSION ==="
echo ""

# Step 1: Archive current version (if exists)
if [ -d "$CURRENT_DIR" ] && [ -f "$CURRENT_DIR/VERSION" ]; then
    OLD_VERSION=$(cat "$CURRENT_DIR/VERSION")
    echo "1. Archiving current ($OLD_VERSION) to archive/$OLD_VERSION/"
    mkdir -p "$ARCHIVE_DIR/$OLD_VERSION"
    cp -r "$CURRENT_DIR"/* "$ARCHIVE_DIR/$OLD_VERSION/"
    # Also archive the combined files
    if [ -f "$DOCSET_DIR/rsm_complete.md" ]; then
        cp "$DOCSET_DIR/rsm_complete.md" "$ARCHIVE_DIR/$OLD_VERSION/"
        cp "$DOCSET_DIR/rsm_complete.html" "$ARCHIVE_DIR/$OLD_VERSION/"
    fi
else
    echo "1. No current version to archive (fresh start)"
fi

# Step 2: Create/clear current folder
echo "2. Setting up current/ folder..."
rm -rf "$CURRENT_DIR"
mkdir -p "$CURRENT_DIR"

# Step 3: Copy audited source files
echo "3. Copying audited source files..."
cp "$RSM_FILE" "$CURRENT_DIR/01_rsm.md"
cp "$REPO/rsm/takes/operators.md" "$CURRENT_DIR/02_operators.md"
cp "$REPO/rsm/canonical/notation_guide.md" "$CURRENT_DIR/03_notation_guide.md"
cp "$REPO/rsm/canonical/recursive_structural_model.md" "$CURRENT_DIR/04_recursive_structural_model.md"
cp "$REPO/ddj/canonical/chapters/chapter01.md" "$CURRENT_DIR/05_ddj_chapter01.md"
cp "$REPO/ddj/canonical/chapters/chapter05.md" "$CURRENT_DIR/06_ddj_chapter05.md"
cp "$REPO/ddj/canonical/chapters/chapter11.md" "$CURRENT_DIR/07_ddj_chapter11.md"
cp "$REPO/ddj/canonical/chapters/chapter16.md" "$CURRENT_DIR/08_ddj_chapter16.md"
cp "$REPO/ddj/canonical/chapters/chapter40.md" "$CURRENT_DIR/09_ddj_chapter40.md"
cp "$REPO/ddj/canonical/chapters/chapter42.md" "$CURRENT_DIR/10_ddj_chapter42.md"
cp "$REPO/ddj/canonical/chapters/chapter51.md" "$CURRENT_DIR/11_ddj_chapter51.md"
cp "$REPO/ddj/canonical/chapters/chapter81.md" "$CURRENT_DIR/12_ddj_chapter81.md"
cp "$REPO/consolidated/essays/euler_tao_identity.md" "$CURRENT_DIR/13_euler_tao_identity.md"
cp "$REPO/src/content/essays/between-e-and-phi.md" "$CURRENT_DIR/14_between_e_and_phi.md"

# Step 4: Write version file
echo "$VERSION" > "$CURRENT_DIR/VERSION"

# Step 5: Create index
echo "4. Creating index..."
cat > "$CURRENT_DIR/00_index.md" << EOF
# RSM $VERSION Document Set — $TODAY

Documents audited and aligned with RSM $VERSION operator grammar.

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | rsm.md | Complete formal treatment ($VERSION) |
| 02 | operators.md | DDJ operator grammar (名=i, 利₁=-1, 反=+1, 相生=e) |
| 03 | notation_guide.md | Six constants, φ derivation, conventions |
| 04 | recursive_structural_model.md | Accessible introduction |
| 05 | ddj_chapter01.md | Coordinate system (名=i, 玄=0, 有=1) |
| 06 | ddj_chapter05.md | Bellows principle (橐籥, 虛/不屈/守中) |
| 07 | ddj_chapter11.md | Scythe principle (利₁/利₂/用 distinction) |
| 08 | ddj_chapter16.md | Return to root (復 operator, 常 cascade) |
| 09 | ddj_chapter40.md | Oscillation engine (反=+1) |
| 10 | ddj_chapter42.md | Generative sequence (道生一 = P₀→O₁) |
| 11 | ddj_chapter51.md | 道生/德畜 formula (玄德) |
| 12 | ddj_chapter81.md | Closure validation (三 paradoxes) |
| 13 | euler_tao_identity.md | Both canonical identities |
| 14 | between_e_and_phi.md | e/φ architecture, 非 grammar, 玄牝=φ |

## Canonical Identities

**Euler:** e^(iπ) + 1 = 0
**Master:** e^(2iπ/5) − φ·e^(iπ/5) + 1 = 0

---
*Co-authored by Will Goldstein and Claude*
EOF

# Step 6: Create combined markdown file
echo "5. Creating combined markdown file..."
cat "$CURRENT_DIR/00_index.md" > "$DOCSET_DIR/rsm_complete.md"
echo -e "\n\n---\n\n" >> "$DOCSET_DIR/rsm_complete.md"

for f in 01_rsm.md 02_operators.md 03_notation_guide.md 04_recursive_structural_model.md 05_ddj_chapter01.md 06_ddj_chapter05.md 07_ddj_chapter11.md 08_ddj_chapter16.md 09_ddj_chapter40.md 10_ddj_chapter42.md 11_ddj_chapter51.md 12_ddj_chapter81.md 13_euler_tao_identity.md 14_between_e_and_phi.md; do
    echo -e "# ═══════════════════════════════════════════════════════════════\n# FILE: $f\n# ═══════════════════════════════════════════════════════════════\n" >> "$DOCSET_DIR/rsm_complete.md"
    cat "$CURRENT_DIR/$f" >> "$DOCSET_DIR/rsm_complete.md"
    echo -e "\n\n---\n\n" >> "$DOCSET_DIR/rsm_complete.md"
done

# Step 7: Create HTML version
echo "6. Creating HTML version..."
cat > "$DOCSET_DIR/rsm_complete.html" << HTMLEOF
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>RSM $VERSION Complete</title>
<style>
body { font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
pre, code { background: #f4f4f4; padding: 2px 6px; }
pre { padding: 12px; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
h1, h2, h3 { margin-top: 1.5em; }
</style>
</head>
<body>
<pre style="white-space: pre-wrap; font-family: inherit; background: none;">
HTMLEOF

cat "$DOCSET_DIR/rsm_complete.md" >> "$DOCSET_DIR/rsm_complete.html"

cat >> "$DOCSET_DIR/rsm_complete.html" << 'HTMLEOF'
</pre>
</body>
</html>
HTMLEOF

# Step 8: Copy to public folder
echo "7. Copying to public folder..."
rm -rf "$PUBLIC_DOCSET"
cp -r "$DOCSET_DIR" "$PUBLIC_DOCSET"

# Step 9: Show stats
LINES=$(wc -l < "$DOCSET_DIR/rsm_complete.md" | tr -d ' ')
SIZE=$(ls -lh "$DOCSET_DIR/rsm_complete.md" | awk '{print $5}')
echo ""
echo "=== Docset Ready ==="
echo "Version: $VERSION"
echo "Combined file: $LINES lines, $SIZE"
echo ""

# List archived versions
if [ -d "$ARCHIVE_DIR" ] && [ "$(ls -A $ARCHIVE_DIR 2>/dev/null)" ]; then
    echo "Archived versions:"
    ls -1 "$ARCHIVE_DIR" | sed 's/^/  /'
    echo ""
fi

# Step 10: Commit and publish
read -p "Commit and publish? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "8. Committing to sandbox..."
    cd "$REPO"
    git add docset/ public/docset/
    git commit -m "$COMMIT_MSG

---
Co-authored by Will Goldstein and Claude" || echo "No changes to commit"
    git push

    echo "9. Publishing to live site..."
    "$REPO/scripts/publish.sh" "$COMMIT_MSG"

    echo ""
    echo "=== Published ==="
    echo "NotebookLM URL: https://ourinfinitereality.com/docset/rsm_complete.html"
else
    echo "Skipped publish. Run manually:"
    echo "  git add docset/ public/docset/ && git commit && git push"
    echo "  ./scripts/publish.sh"
fi
