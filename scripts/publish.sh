#!/bin/bash

# Publish script: copies publishable content to public repo
# Usage: ./scripts/publish.sh "commit message"

set -e

# Configuration
PRIVATE_REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
PUBLIC_REPO="/Users/willgoldstein/claudecode/ourinfinitereality"
COMMIT_MSG="${1:-Update published content}"

echo "Publishing to ourinfinitereality.com..."

# Generate recently updated page before publishing
echo "Generating recently updated page..."
"$PRIVATE_REPO/scripts/generate_recent.sh"

# Ensure public repo exists
if [ ! -d "$PUBLIC_REPO" ]; then
    echo "Cloning public repo..."
    cd /Users/willgoldstein/claudecode
    git clone https://github.com/goldsteinstudios/ourinfinitereality.git
fi

cd "$PUBLIC_REPO"

# Clean existing content (except .git and .github)
find . -maxdepth 1 ! -name '.git' ! -name '.github' ! -name '.' -exec rm -rf {} +

# Copy publishable content
echo "Copying content..."

# Site config
cp "$PRIVATE_REPO/mkdocs.yml" .

# Docs folder (landing page, about)
cp -r "$PRIVATE_REPO/docs" .
# Remove symlink, copy actual translations
rm -rf docs/translations

# Translations from new structure (ddj/canonical/)
mkdir -p docs/translations
cp -r "$PRIVATE_REPO/ddj/canonical/chapters" docs/translations/
cp -r "$PRIVATE_REPO/ddj/canonical/lexicon" docs/translations/
cp -r "$PRIVATE_REPO/ddj/canonical/meta" docs/translations/
cp -r "$PRIVATE_REPO/ddj/archaeology" docs/translations/ 2>/dev/null || true
cp "$PRIVATE_REPO/ddj/canonical/README.md" docs/translations/ 2>/dev/null || true
cp "$PRIVATE_REPO/ddj/canonical/00_introduction.md" docs/translations/ 2>/dev/null || true

# Copy overrides directory for MkDocs custom_dir
cp -r "$PRIVATE_REPO/overrides" . 2>/dev/null || mkdir -p overrides

# Commit and push
echo "Committing..."
git add -A
git commit -m "$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)" || echo "No changes to commit"

echo "Pushing..."
git push origin main

echo ""
echo "✓ Published to https://ourinfinitereality.com"
echo "  (Site will rebuild in ~2 minutes)"
