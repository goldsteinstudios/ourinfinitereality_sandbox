#!/bin/bash

# Publish script: copies publishable content to public repo
# Usage: ./scripts/publish.sh "commit message"

set -e

# Configuration
PRIVATE_REPO="/Users/willgoldstein/claudecode/dao-de-jing-analyzer"
PUBLIC_REPO="/Users/willgoldstein/claudecode/ourinfinitereality"
COMMIT_MSG="${1:-Update published content}"

echo "Publishing to ourinfinitereality.com..."

# Ensure public repo exists
if [ ! -d "$PUBLIC_REPO" ]; then
    echo "Cloning public repo..."
    cd /Users/willgoldstein/claudecode
    git clone https://github.com/goldsteinstudios/ourinfinitereality.git
fi

cd "$PUBLIC_REPO"

# Clean existing content (except .git)
find . -maxdepth 1 ! -name '.git' ! -name '.' -exec rm -rf {} +

# Copy publishable content
echo "Copying content..."

# Site config
cp "$PRIVATE_REPO/mkdocs.yml" .

# Docs folder (landing page, about)
cp -r "$PRIVATE_REPO/docs" .
# Remove symlink, copy actual translations
rm -rf docs/translations

# Translations (the actual content)
mkdir -p docs/translations
cp -r "$PRIVATE_REPO/translations/chapters" docs/translations/
cp -r "$PRIVATE_REPO/translations/lexicon" docs/translations/
cp -r "$PRIVATE_REPO/translations/meta" docs/translations/
cp -r "$PRIVATE_REPO/translations/archaeology" docs/translations/ 2>/dev/null || true
cp -r "$PRIVATE_REPO/translations/appendices" docs/translations/ 2>/dev/null || true
cp "$PRIVATE_REPO/translations/README.md" docs/translations/
cp "$PRIVATE_REPO/translations/00_introduction.md" docs/translations/ 2>/dev/null || true

# GitHub Actions workflow - skip if can't push (add manually via GitHub web UI)
# mkdir -p .github/workflows
# cp "$PRIVATE_REPO/.github/workflows/deploy.yml" .github/workflows/

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
