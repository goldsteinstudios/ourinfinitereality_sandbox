#!/bin/bash

# Update Docset Script
# Regenerates the RSM docset from audited source files and publishes
# Usage: ./scripts/update_docset.sh [commit message]

set -e

REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
DOCSET_DIR="$REPO/docset"
PUBLIC_DOCSET="$REPO/public/docset"
TODAY=$(date +%Y-%m-%d)
COMMIT_MSG="${1:-Update RSM docset}"

echo "=== Updating RSM Docset ==="
echo ""

# Step 1: Create dated folder
echo "1. Creating dated folder: $TODAY"
mkdir -p "$DOCSET_DIR/$TODAY"

# Step 2: Copy audited source files with numbered prefixes
echo "2. Copying audited source files..."

cp "$REPO/rsm/canonical/rsm_v0979.md" "$DOCSET_DIR/$TODAY/01_rsm_v0979.md"
cp "$REPO/rsm/takes/operators.md" "$DOCSET_DIR/$TODAY/02_operators.md"
cp "$REPO/rsm/canonical/notation_guide.md" "$DOCSET_DIR/$TODAY/03_notation_guide.md"
cp "$REPO/rsm/canonical/recursive_structural_model.md" "$DOCSET_DIR/$TODAY/04_recursive_structural_model.md"
cp "$REPO/ddj/canonical/chapters/chapter01.md" "$DOCSET_DIR/$TODAY/05_ddj_chapter01.md"
cp "$REPO/ddj/canonical/chapters/chapter11.md" "$DOCSET_DIR/$TODAY/06_ddj_chapter11.md"
cp "$REPO/ddj/canonical/chapters/chapter40.md" "$DOCSET_DIR/$TODAY/07_ddj_chapter40.md"
cp "$REPO/ddj/canonical/chapters/chapter42.md" "$DOCSET_DIR/$TODAY/08_ddj_chapter42.md"
cp "$REPO/consolidated/essays/euler_tao_identity.md" "$DOCSET_DIR/$TODAY/09_euler_tao_identity.md"

# Step 3: Create index
echo "3. Creating index..."
cat > "$DOCSET_DIR/$TODAY/00_index.md" << EOF
# RSM v0.979 Document Set — $TODAY

Documents audited and aligned with RSM v0.979 operator grammar.

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | rsm_v0979.md | Complete formal treatment (43 theorems, master identity) |
| 02 | operators.md | DDJ operator grammar (名=i, 利₁=-1, 反=+1, 相生=e) |
| 03 | notation_guide.md | Six constants, φ derivation, conventions |
| 04 | recursive_structural_model.md | Accessible introduction |
| 05 | ddj_chapter01.md | Coordinate system (名=i, 玄=0, 有=1) |
| 06 | ddj_chapter11.md | Scythe principle (利₁/利₂/用 distinction) |
| 07 | ddj_chapter40.md | Oscillation engine (反=+1) |
| 08 | ddj_chapter42.md | Generative sequence (道生一 = P₀→O₁) |
| 09 | euler_tao_identity.md | Both canonical identities |

## Canonical Identities

**Euler:** e^(iπ) + 1 = 0
**Master:** e^(2iπ/5) − φ·e^(iπ/5) + 1 = 0

---
*Co-authored by Will Goldstein and Claude*
EOF

# Step 4: Concatenate into single markdown file
echo "4. Creating combined markdown file..."
cat "$DOCSET_DIR/$TODAY/00_index.md" > "$DOCSET_DIR/rsm_v0979_complete.md"
echo -e "\n\n---\n\n" >> "$DOCSET_DIR/rsm_v0979_complete.md"

for f in 01_rsm_v0979.md 02_operators.md 03_notation_guide.md 04_recursive_structural_model.md 05_ddj_chapter01.md 06_ddj_chapter11.md 07_ddj_chapter40.md 08_ddj_chapter42.md 09_euler_tao_identity.md; do
    echo -e "# ═══════════════════════════════════════════════════════════════\n# FILE: $f\n# ═══════════════════════════════════════════════════════════════\n" >> "$DOCSET_DIR/rsm_v0979_complete.md"
    cat "$DOCSET_DIR/$TODAY/$f" >> "$DOCSET_DIR/rsm_v0979_complete.md"
    echo -e "\n\n---\n\n" >> "$DOCSET_DIR/rsm_v0979_complete.md"
done

# Step 5: Create HTML version for NotebookLM
echo "5. Creating HTML version..."
cat > "$DOCSET_DIR/rsm_v0979_complete.html" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>RSM v0.979 Complete</title>
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

cat "$DOCSET_DIR/rsm_v0979_complete.md" >> "$DOCSET_DIR/rsm_v0979_complete.html"

cat >> "$DOCSET_DIR/rsm_v0979_complete.html" << 'HTMLEOF'
</pre>
</body>
</html>
HTMLEOF

# Step 6: Copy to public folder
echo "6. Copying to public folder..."
rm -rf "$PUBLIC_DOCSET"
cp -r "$DOCSET_DIR" "$PUBLIC_DOCSET"

# Step 7: Show stats
LINES=$(wc -l < "$DOCSET_DIR/rsm_v0979_complete.md" | tr -d ' ')
SIZE=$(ls -lh "$DOCSET_DIR/rsm_v0979_complete.md" | awk '{print $5}')
echo ""
echo "=== Docset Ready ==="
echo "Combined file: $LINES lines, $SIZE"
echo "Dated folder: $TODAY"
echo ""

# Step 8: Commit and publish
read -p "Commit and publish? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "7. Committing to sandbox..."
    cd "$REPO"
    git add docset/ public/docset/
    git commit -m "$COMMIT_MSG

---
Co-authored by Will Goldstein and Claude" || echo "No changes to commit"
    git push

    echo "8. Publishing to live site..."
    "$REPO/scripts/publish.sh" "$COMMIT_MSG"

    echo ""
    echo "=== Published ==="
    echo "NotebookLM URL: https://ourinfinitereality.com/docset/rsm_v0979_complete.html"
else
    echo "Skipped publish. Run manually:"
    echo "  git add docset/ public/docset/ && git commit && git push"
    echo "  ./scripts/publish.sh"
fi
