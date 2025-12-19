#!/bin/bash

# Publish script: builds Astro site and deploys to public repo
# Usage: ./scripts/publish.sh "commit message"

set -e

# Configuration
PRIVATE_REPO="/Users/willgoldstein/claudecode/ourinfinitereality_sandbox"
PUBLIC_REPO="/Users/willgoldstein/claudecode/ourinfinitereality"
COMMIT_MSG="${1:-Update published content}"

echo "Publishing to ourinfinitereality.com..."

# Build Astro site
echo "Building Astro site..."
cd "$PRIVATE_REPO"
npm run build

# Ensure public repo exists
if [ ! -d "$PUBLIC_REPO" ]; then
    echo "Cloning public repo..."
    cd /Users/willgoldstein/claudecode
    git clone https://github.com/goldsteinstudios/ourinfinitereality.git
fi

cd "$PUBLIC_REPO"

# Clean existing content (except .git, .github, and CNAME)
find . -maxdepth 1 ! -name '.git' ! -name '.github' ! -name 'CNAME' ! -name '.' -exec rm -rf {} +

# Copy built site from dist/
echo "Copying built site..."
cp -r "$PRIVATE_REPO/dist/"* .

# GitHub Pages needs .nojekyll to serve _astro folder
touch .nojekyll

# Commit and push
echo "Committing..."
git add -A
git commit -m "$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)" || echo "No changes to commit"

echo "Pushing..."
git push origin main

echo ""
echo "✓ Published to https://ourinfinitereality.com"
echo "  (Site should be live within minutes)"
