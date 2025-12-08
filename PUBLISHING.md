# Publishing Workflow

## Overview

This project uses a two-repo setup:

- **Private repo:** `dao-de-jing-analyzer` — working space with scripts, drafts, experiments
- **Public repo:** `ourinfinitereality` — published content only, powers the website

The website at **ourinfinitereality.com** auto-builds from the public repo via GitHub Pages.

---

## Daily Workflow

Work normally in the private repo. Edit translations, add chapters, revise framework docs. Nothing is public until you explicitly publish.

---

## Publishing

When ready to make changes public:

```bash
./scripts/publish.sh "Description of what changed"
```

This script:
1. Copies publishable content from private → public repo
2. Commits with your message
3. Pushes to GitHub
4. Site rebuilds automatically (~2 minutes)

### Example

```bash
./scripts/publish.sh "Add Chapter 42 translation, update lexicon"
```

---

## What Gets Published

The publish script copies:

- `docs/` — landing page, about page, CNAME
- `translations/chapters/` — chapter translations
- `translations/lexicon/` — vocabulary files
- `translations/meta/` — framework documents
- `translations/archaeology/` — Guodian materials
- `translations/appendices/` — appendices (if exists)
- `mkdocs.yml` — site configuration/navigation

### What Stays Private

- `scripts/` — automation scripts
- `research/` — working notes, experiments
- `docsets/` — notebook exports
- `translations/guodian/` — RSM rebuild (separate branch)
- Git history of private repo
- Any file not in the above "published" list

---

## Updating Navigation

The site navigation is defined in `mkdocs.yml` under `nav:`.

When adding a new chapter:
1. Add the file to `translations/chapters/`
2. Add an entry to `mkdocs.yml` nav section
3. Run publish script

---

## Checking the Site

- **Live site:** https://ourinfinitereality.com
- **Build status:** https://github.com/goldsteinstudios/ourinfinitereality/actions
- **Public repo:** https://github.com/goldsteinstudios/ourinfinitereality

---

## If Something Breaks

### Site won't build
Check GitHub Actions for error message. Usually a missing file referenced in `mkdocs.yml`.

### DNS issues
Check GoDaddy DNS settings. Should have:
- 4 A records pointing to `185.199.108-111.153`
- CNAME `www` → `goldsteinstudios.github.io`

### Workflow file issues
The GitHub Actions workflow can only be edited via GitHub web interface (token limitation). File is at `.github/workflows/deploy.yml` in the public repo.

---

## File Locations

| What | Where |
|------|-------|
| Private repo | `/Users/willgoldstein/claudecode/dao-de-jing-analyzer` |
| Public repo | `/Users/willgoldstein/claudecode/ourinfinitereality` |
| Publish script | `scripts/publish.sh` |
| Site config | `mkdocs.yml` |
| Landing page | `docs/index.md` |
| About page | `docs/about.md` |

---

## Quick Reference

```bash
# Publish changes
./scripts/publish.sh "commit message"

# Check site status
open https://github.com/goldsteinstudios/ourinfinitereality/actions

# View live site
open https://ourinfinitereality.com
```
