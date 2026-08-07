# Archive Inventory

What was consolidated, where it came from, and where it went.
Generated 2026-08-01 on branch `research-archive`.

The machine-readable companion is [`MANIFEST.csv`](MANIFEST.csv) — one row per file
across **both** iCloud imports, recording `path, size, mtime, md5, tree, strand,
disposition, git_target, binary_target`. It describes the **pre-consolidation** state
plus the planned destination of every file, so the whole reorganization is reproducible
and auditable. Every delete and every move was driven from it.

---

## The two imports

This consolidation merged two overlapping iCloud dumps.

| Import | Location | Files | Size | Date |
|---|---|---:|---:|---|
| **Complete Archive** | `archive/Complete Archive/` | 3,195 | 308 MB | Jul 2026 |
| **Prior import** | `research/archive/icloud_import/archive_oir_icloud_folder_12.19.25/` | 1,049 | 9.8 GB | Dec 19 2025 |

**652 files were byte-identical across the two** (md5-verified). The prior import's
`Podcasts/` folder — 115 files, 9.0 GB of audio/video — is the only copy of that material
and was excluded from every sweep.

Material spans **Oct 2022 → Jul 2026**.

---

## Source composition (Complete Archive)

1,759 PNG · 539 MD · 395 PDF · 108 JPG · 57 TSX · 42 RTFD · 41 TXT · 21 DOCX · 19 CSV ·
10 `.pages` · 5 `.numbers` · 6 `.nb` (Mathematica) · 4 `.ggb` (GeoGebra) · 2 USDZ · 2 GCX.

### 1. `DDJ Translations/` — 75 MB, 1,968 files
- **`Guodian Laozi-老子/`** — 1,717 glyph PNGs, Bundle A/B/C, per-slip folders.
  1,073 were byte-identical to `data/ddj/Guodian Strip Glyphs/`; **644 were new** and were
  merged into that corpus.
- `Guodian Laozi from daoisopen.com/` — 92 files, A/B/C bundle JPEGs + `unsorted from web/`.
- `Guodian laozi high re full strips/` — 15 high-res strip photos.
- `Guodian glyph analyses/` — the Feb 2026 papers: `jue_the_severing`, `zhi_the_knowing`,
  `qi_the_winnowing`, `guodian_primitives_2.23.26`.
- `ddj_characters_pinyin.full.csv/` — **a directory despite the name.** 13 structured files:
  bundle inventories, cross-reference report, section-break analysis, `guodian.yaml`,
  `ttc_data.csv`, `ttc_visualizer.py`.
- ~120 loose files: `dao_ch1..ch16_translation.md`, chapter analyses, four generations of
  lexicon, the `guo.lao.jia_dictionary` in five formats, `cooccurrence_matrix_2025-11-13.csv`.

### 2. `RSM Version History/` — 140 MB, 923 files
The version ladder. Only 12 files anywhere in the archive already existed in git.

| Folder | Files | Notes |
|---|---:|---|
| `RSM v0.9/` | 220 | Four NotebookLM docset exports: v0.96, v0.971, v0.972, v0.99. v0.971/v0.972 are per-chapter DDJ lexicon exports; **v0.99 holds the reconciled just-math / just-ddj / just-physics / parallax chains.** |
| `RSM v2/` | 0 | Empty. |
| `v3`, `v4`, `v6` | 5 | PDF-only. No source text survives. |
| `RSM v5/` | 100 | Heaviest duplication in the archive — one file existed 9×. |
| `RSM v7/` | 145 | v7.0–v7.7. v7.6 = the `7 6c` candidates; **v7.7 = the deepest revision tree** (chain r2…r12, math r1…r7, ddj r1…r6) plus `adversarial_pass_r1`, `divergence_ledger_r1`, `provenance_map_math_r2`. |
| **`RSM v8/`** | 12 | **Cleanest folder in the archive** — all `.md`, zero duplicates, complete set. See finding E. |
| `RSM v9/` | 29 | v9.1 (PDF), v9.2 (md+pdf, already in git), v9.3 (PDF-only), v9.4 (see finding C). |
| `AL-AN/` | 32 | Distinct sub-project — framework, ring memory, phase tracker, engine card, perpendicular protocol, governance rules. |
| `Unversioned/` | 380 | The dumping ground — seven strands, split out on move (see below). |

### 3. `Scripts etc/` — 45 MB, 249 files
- `Archimedes_polygons/` — contained `Polygon-circles/`, a byte-for-byte copy of its own parent.
- `Glyph Explorer/` — the 16384×16384 glyph matrix.
- `TaoTranslator/` — a complete Replit Node/Vite/Drizzle app. See finding G.

### 4. `Visuals/` — 48 MB, 32 files
24 undescribed Nov 2025 screenshots, a 20 MB USDZ tree scan, an 8.3 MB Grapher file,
the logo, and one third-party book PDF (see finding G).

---

## Strand split applied to `Unversioned/`

The 380-file dump was sorted into these strands, recorded per-file in `MANIFEST.csv`:

| Strand | Files | What it is |
|---|---:|---|
| `misc` | 134 | Unclassified — standalone essays, one-off notes. Re-sort as needed. |
| `book-drafts` | 78 | ~12 generations of one manuscript, Mar–Jul 2025, in `.pdf`/`.pages`/`.docx`. |
| `physics` | 31 | Physics Sections I–IV, classical/quantum/field-theory/statistical, Lagrangian. |
| `axioms` | 30 | `Axiom 1`…`Axiom 9`, `Pre-Axioms`, the 7.8.25 and 7.27.25 framework versions. |
| `ai-sessions` | 25 | NotebookLM dumps, ChatGPT/Gemini/Perplexity exports, podcast outline. |
| `notation` | 23 | The P₀/O₁/G₀/G₁/B₀/B₁/X₀/Y₀/Y₁/Z₀ symbol family, notation guides, glossaries. |
| `fragments` | 21 | `.rtfd` story/prompt fragments **named by their opening sentence.** |
| `essay-series` | 16 | `00 series preface` → `15 what pi names`. Coherent and complete. |
| `chains-superseded` | 10 | Reconciled chains, orthogonality closure, formal formulation paper. |

`.rtfd` files are macOS **package directories**, not files. They are moved as atomic units.

---

## Findings

**A. Duplication (all md5-verified).** 138 redundant copies inside Complete Archive
(the iCloud `foo 2.md` / `foo copy.pdf` pattern), 652 across the two imports, 1,073 glyphs
already on disk, 10 files in the self-nested Archimedes copy, 58 `.DS_Store`, 142 nested
`.git` objects. **1,873 deletions, every one proven to have a surviving byte-identical copy;
0 unique contents lost.**

**B. Only 12 of 3,195 files already existed in git** — the v7.6c / v7.7 / v9.2 chains.
This was genuinely new material, not a re-import.

**C. `RSM v9.4` is probably not version 9.4. — UNRESOLVED, needs a ruling.**
Everything in it is stamped `9.4.25`: `Phase_{1..5}_updates_9.4.25`,
`Rsm Master Bibliography_9.4.25`, `Rsm Modules 1-4_9.4.25`, `Rsm Field Framework_9.4.25`.
That reads as **Sept 4 2025**, which would place it *before* v9.1/v9.2/v9.3, not after.
`RSM v9.2` has the same smell (`RSM_9.2.25.txt`) but also holds genuine `just math v9_2.md`
chains matching the repo, so v9.2 is real. **A mislabelled folder here poisons canon ordering.**
Preserved under its original name pending a decision.

**D. Archive `v9.3` is PDF-only** — `just {ddj,math,physics} v9_3.pdf` plus a change log.
The authoritative markdown set is held separately.

**E. `RSM v8/` is a complete, clean generation that never entered `rsm/canonical/`.**
The repo goes v7.7 → v9 with nothing between. Not promoted here — that is a canon ruling.

**F. The Guodian glyph corpus has no git backup.** — **CORRECTED 2026-08-07; RESOLVED the same day.**

> **The original finding was wrong on one factual point.** It read: *"`data/` is gitignored on every
> branch, and `git ls-tree` confirms zero branches track a single glyph PNG. The archive copy was the
> only redundancy; after dedup, `data/ddj/Guodian Strip Glyphs/` (1,717 files) is the sole copy."*
>
> **`wip/claude-design-system` tracked 1,073 of them** at `ddj/archaeology/Guodian Strip Glyphs/` —
> a different path, which is why a `data/`-anchored search missed them. Verified blob-for-blob:
> byte-identical to the working-tree copies, a clean subset with nothing present there and absent
> here. **The genuinely unbacked count was 644, not 1,717.**
>
> Everything else in the finding held: 1,717 files, 3.1 MB, `data/` gitignored at `.gitignore:19`.
>
> **Resolved** 2026-08-07 by `1eaee9f`, which force-added all 1,717 to `research-archive` at
> `data/ddj/Guodian Strip Glyphs/`. Correction and fix both from the Claude Code instance on
> `wills-imac-local`; the cloud session had repeated the finding without independently verifying it.
> See divergence ledger Entry 007.
>
> **Open, and not a mechanical call:** the corpus now sits at two paths on two branches —
> `data/ddj/` on `research-archive` and `ddj/archaeology/` on `wip/claude-design-system`. Which is
> canonical wants deciding before the split sets.

**G. Three hazards, all handled.**
- `TaoTranslator/` carried its own `.git` (branches `main`, `replit-agent`; 7 commits, all
  2025-07-19, all by wgoldstein, describing initial build + two bugfix rounds). A nested repo
  breaks `git add`, so the `.git` directory was stripped and only the working tree kept.
  Nothing unique was in history that isn't in the tree.
- ⚠️ `Lao Tzu Te-Tao Ching … (Henricks) … (Z-Library).pdf` is a **third-party copyrighted
  book.** It is kept out of git entirely and **must never reach the public repo.**
- ~267 MB of binaries were routed out of git (see below).

---

## Where things went

```
archive/                       ← text, tracked in git (599 files, 13.2 MB)
  INVENTORY.md                   this file
  MANIFEST.csv                   the full record
  rsm-versions/                  text-form version ladder, by version
  alan/                          the AL-AN sub-project
  ddj/  guodian-structured/ lexicons/ translations/
  notes/<strand>/                Unversioned, split by the strands above
  scripts/                       archimedes.jsx, ttc_visualizer.py, TaoTranslator (no .git)
  visuals/

research/archive/icloud_import/           ← gitignored, existing convention
  archive_oir_icloud_folder_12.19.25/        prior import, deduped, Podcasts/ untouched
  complete_archive_2026.08/                  565 binaries, 267 MB, mirroring source shape

data/ddj/Guodian Strip Glyphs/            ← gitignored; 644 new glyphs merged in
```

**Binaries are deliberately out of git.** PDFs, images, scans, Office/iWork documents and
the Replit app live on disk under the already-established gitignored
`research/archive/icloud_import/` convention. Git holds only text.
