# Recovery errands

Compiled 2026-08-02. Three classes: content lost to the NotebookLM exports (needs your local
originals), documents stranded on branches (needs a landing decision), and the visual-asset
inventory (find-and-list only; nothing built).

---

## 1. Stripped tables — pull from local originals

The NotebookLM exports dropped **every markdown table**: 0 tables across all 95 `v0.971` files
(and 1 of 53 in `v0.972`), while hand-written archive files keep theirs. The binary originals live
in the gitignored `research/archive/icloud_import/`, which is **not in this container** — recovery
must come from your local copy (or the tables re-derived).

Exactly which files and sections are needed:

| File (staged copy in `staging/editorial/`) | Missing sections |
|---|---|
| `expansion-packed-hanging.md` | "The Four Recursion Types Mapped" (heading, no content) · "Key Term Summary" (heading, no content) · the 常 and 可 "Translation Implications" lists ("Every instance of 常 should be re-examined:" / "Every instance of 可:" — both dangle) |
| `expansion-helix-structure.md` | "The Convergence" ("Same geometry. Different substrates." — table gone) · "RSM Mapping" ("The helix IS the recursion structure made spatial." — table gone) · "The Complete Picture" ("Different languages… One geometry." — table gone) · "The Stretched Zucchini" ("You can SEE the structure:" — content gone) |
| `expansion-technology-index.md` | "Universal Failure Modes" — "Every technology fails the same two ways:" **the two ways are missing** · "The Same Principle in Different Substrates" (cross-technology table gone) · "Reading Your Tools" ("Every handmade tool carries documentation on its surface:" — the list is gone) |
| `expansion-chapter76-v0972.md` | Lines 13–14: "Character-by-Character Decomposition" and "Key Structural Terms" are consecutive headings with zero content between them · the tabular parts of the four "Complete Teaching" blocks (prose survives; tables don't) |
| `expansion-chapter40-v0972.md`, `expansion-chapter05-v0972.md` | Same export family — spot-checks show the added observation-stances sections are prose-complete, but any tabular material in the original chapter analyses is gone; verify against local when pulling the others |

Also worth pulling while you're in the local archive: the whole `v0.96` export contains **ten
files that are only filenames** (`041`–`050`) — NotebookLM stub records for PNG charts it ingested
but extracted no text from (see §3a; the charts themselves are recoverable from branches).

## 2. Branch-stranded documents

Documents with no copy on `research-archive` until this staging pass. The staged copies under
`staging/editorial/` are now on `research-archive`; the **originals remain on their branches**, so
any *edits* should land here (or be pushed back to the branch deliberately) — do not edit the
branch copies in place and assume the archive sees it.

| Document | Branch + path | Status |
|---|---|---|
| The unpluggable hole | `sphere_model` · `research/unpluggable_hole_draft.md` | Staged → `expansion-unpluggable-hole.md` |
| The Laozi guided walk | `sphere_model` · `research/laozi_guided_walk_draft.md` | Staged → `expansion-laozi-guided-walk.md` |
| The Kai parable | `docset-pipeline` · `sets/nlm-parables/01_parable_kai_unmeasurable_field.md` | Staged → `parable-kai-unmeasurable-field.md` (three copies on branch; `sets/` + `processed/` identical, `staging/` differs) |
| The Sailor's Paradox | `docset-pipeline` · `sets/nlm-parables/02_the_sailors_paradox.md` | Staged → `parable-sailors-paradox.md` |

Related but out of the staged set (from the earlier survey, unchanged): the physics synthesis
quintet, `why_water.md`, and the geometry docs deleted by commit `98154a2` survive only on
`sphere_model`/`docset-pipeline` and in git history — a landing decision is pending for those too
if they're ever wanted.

## 3. Visuals — inventory (found, not built)

### 3a. Exists on OTHER branches — recoverable by `git show`, no rebuild needed
- **14 analysis charts** (radical heatmaps, category summaries, neighbor graphs, clustering
  dendrogram) referenced by `archive/rsm-versions/v0.96/038-key-findingsmd.md` — present at
  `python_analysis/output/{visualizations,statistical_analysis}/` on
  `claude/glyph-composer-v3-fQABj`, `sphere_model`, and `guodian-rsm-rebuild` (and under
  `tools/output/` on `claude/catch-up-UKmEu`). Plus `cross_reference_network.html`.
- **~74 Guodian slip photographs** (`guo_A01.jpg` … `guo_C05d.jpg`, bundles A/B/C) referenced by
  `v0.96/037-…` — present on `claude/catch-up-UKmEu` (`ddj/archaeology/source_images/`) and
  `claude/glyph-composer-v3-fQABj` (`translations/archaeology/source_images/`).
- **Curated assets** on `claude/catch-up-UKmEu` only: `assets/diagrams/` (3 PDFs incl.
  `Geometry_Underneath_Everything.pdf`), `assets/images/` (`Infographic .png`, `logo.svg`).

### 3b. Missing from every branch — needs your local machine (or is gone)
- **The seven NotebookLM source images** cited in `archive/notes/ai-sessions/Notebooklm briefing
  6.23.25.txt`: `IMG_2372.png`, `IMG_2506.png`, `IMG_2538.jpeg`, `IMG_8606.jpeg`, `IMG_8618.jpeg`,
  `IMG_8631.jpeg`, `IMG_8737.png` — the hand-drawn/photographed geometry the Gₙ/Bₙ/Pₙ/Zₙ notation
  was read off. **Highest-value absent assets in the corpus.** Not in `MANIFEST.csv`.
- **The Bridge document's figure**: `Attachments/30B68241-1024-4FB5-B73B-270FA3C2E8EE.png` —
  Obsidian-style attachment, never in git on any branch. Sits at the rhetorical hinge of the piece
  (after "The bridge works *because* the center remains empty"). The staged
  `expansion-bridge-thought-experiment.md` carries the broken link at line 62.
- **The five spec'd site diagrams** (`01_river_bridge.svg` … `05_derivation_chain.svg`) named in
  the v5/v5.5 website prompts — a diagram set that was never built (conceptually overlapping the
  seven diagram components that *were* later built under `src/components/diagrams/`).

### 3c. Off-repo, catalogued in `archive/MANIFEST.csv` — binaries not in the repo
From the inventoried but non-imported `Visuals/` (48 MB, 32 files) and `Glyph Explorer/` folders:
- `Rotating Hyperboloid Structure of Recursion.png` (812 KB) — the only *named* conceptual diagram
  in the manifest.
- `Silver Maple Crotch 6.23.25.usdz` (20.6 MB) — 3D LiDAR scan of a tree crotch; the physical
  referent for the orthogonality/branching argument.
- `graph.gcx` (8.7 MB, Apple Grapher) · `newplot.jpg` (Plotly export) · 24 undescribed screenshots
  (Nov 5 + Nov 12, 2025) · logos/previews.
- ⚠ `glyph explorer.pdf`, `glyph matrix.pdf`, `glyph_matrix_7pt_16384x16384.png` are recorded at
  **0 bytes in the manifest** — corrupt/empty at source; recovery may be impossible.
- Manifest totals: 2,046 image rows + 625 PDFs; 644 rows dispositioned `keep-glyph-new` (glyphs
  not among the 1,073 already on disk).

### 3d. On this branch (for orientation; nothing needed)
- `public/glyphs/guodian/` — 1,073 per-character glyph crops (4.3 MB).
- `src/components/diagrams/` — the 7 animated argument diagrams (`Divisibility`, `TwoExtremes`,
  `FirstCut`, `CutBringsWorld`, `CenterNeverMet`, `Circulation`, `Nesting`); `CutBringsWorld` and
  `Nesting` carry in-code "FIRST PASS — FOR WILL TO RULE" flags. Used only by `/pattern`.
- `public/icons/` + `src/icons/` — 7 object glyphs, byte-identical duplicate sets (only
  `src/icons` is consumed; `public/icons` is dead weight — known site issue, site is parked).
- `archive/scripts/Archimedes_polygons/` — 2 standalone React artifacts (polygon convergence
  animation; perimeter-ratio explorer). `archive/scripts/TaoTranslator/` — a complete Replit
  React/TS/Express "Translation Studio" app (77 files). `archive/notes/misc/RSM_paper.html.html` —
  standalone MathJax paper renderer.
- The **Glyph Composer** lives on branch `claude/glyph-composer-v3-fQABj`: a dedicated
  touch-oriented Vite/React entrypoint (`composer.html` → `GlyphComposer.tsx`), with a built copy
  committed under `docs/composer/` (was deployed via GitHub Pages), alongside ~19 further
  analysis/motion components. An older, composer-less version of the same app sits on
  `claude/catch-up-UKmEu` under `archive/react-app/`.
- No notebooks (`.ipynb`), no three.js/p5/d3/canvas work on any branch tree.

## 4. Provenance exposure (noted, not acted on)

- **Four** wholesale NotebookLM export directories, not two: `v0.96` (56 files), `v0.971` (95),
  `v0.972` (53), `v0.99` (16) — 220 files, every one carrying the `notebook:`/`source_id:` header.
- **Unstripped export headers travelled into working copies**: `batches/batch-3-register-split/`
  03 (scythe), 04 (loom), 05 (technology index) — and the same headers are present in the fresh
  `staging/editorial/` copies of every v0.97x-sourced file (left in place deliberately; this task
  records provenance, it doesn't clean it). The loom file asserts `Author: Will Goldstein` directly
  beneath a machine-export header — flagged for a provenance ruling.
- **Self-disclosed machine generation**: the Kai parable ("generated by NotebookLM," twice) and
  the Sailor's Paradox (same pipeline). Both staged with markers intact.
- **A transcribed NotebookLM podcast misfiled as an essay**: `archive/notes/misc/
  companion_posts_7.16.25.txt` (host patter: "Thank you for joining us on this deep dive…").
- **Verbatim Perplexity output with vendor logo**: `archive/notes/misc/Analyze this # RSM
  Framework_ Formal Mathematical.md`.
- **Raw chat residue** in 12 files, densest in `v0.99` (7 of 16 files; one document ends by asking
  the user a question). The canonical instance ("Oh Will. OH. WILL.") is
  `v0.96/002-111625-the-geometry-of-radical-equality-and-the-straw-dogs.md:11`.
