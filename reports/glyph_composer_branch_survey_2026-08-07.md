# `claude/glyph-composer-v3-fQABj` — branch survey

**Tip:** `688f4ed`, 2026-03-15, *"Save WIP."* **Not merged.** 10 commits it has that `research-archive`
lacks; **241** that `research-archive` has and it lacks. It forked early and the canon line ran away
from it.

**875 files. 867 of them exist nowhere on `research-archive`.** This is not a feature branch. It is a
parallel corpus that was never brought across.

**Nothing edited, nothing ruled, nothing merged.**

| Directory | Unique files | What it is |
|---|---:|---|
| `research/` | 284 | working tree, `CURRENT/` + `ARCHIVE/` |
| `docsets/` | 199 | `docset_12.07.25/`, `docset_12.08.25/` |
| `translations/` | **187** | a structured translation project — see §2 |
| `docs/` | 67 | a full MkDocs site (`mkdocs.yml`, `landing.html`, essays, geometry, lore, living, pattern) |
| `python_analysis/` | 70 | radical co-occurrence, dictionary, translation engine, TTC parser, outputs |
| `src/` | 36 | the Vite/React app incl. `GlyphComposer.tsx` |
| `test_results/` | 8 | radical algebra test outputs |

---

## 1. Three live errands are answered by this branch

### 1a. The table-recovery errand — the originals are here, with tables intact

`reports/table_recovery_2026-08-06.md` gives the filter: a file whose first lines carry
`notebook:` / `source_id:` **is a NotebookLM export, already table-stripped**; the ones worth pulling
are those *without* that header. Round 1 uploaded twelve files from the iMac and scored mostly misses.

The originals were on this branch:

| Document | On this branch | Staged copy in the repo |
|---|---|---|
| `translations/meta/scythe_not_knife_2025-11-27.md` | no header, **13 table rows** | `expansion-scythe-not-knife.md` — header, **0 rows** |
| `translations/meta/loom_axiom_identity_2025-11-27.md` | no header, **35 rows** | `expansion-loom-axiom-identity.md` — header, **0 rows** |
| `translations/meta/forge_transformation_grammar_2025-12-07.md` | no header, **46 rows** | (v0.972 export staged) |
| `translations/meta/radical_technology_encoding_2025-11-27.md` | no header, **57 rows** | — |
| `translations/lexicon/06_technology_index.md` | no header, **87 rows**, 10,512 B | `expansion-technology-index.md` — header, **0 rows**, 7,010 B |

The technology index is the sharpest case. Round 1 recorded it as *"Still missing the two Universal
Failure Modes, the cross-substrate table, and the Reading Your Tools list."* The branch version
contains **Universal Failure** and **Reading Your Tools**; the cross-substrate table may be present
under different wording, unchecked.

Caveat that does not reduce the recovery: all five are **craft-cluster material, set aside whole at
D3**. Recovering the originals is not the same as reopening the cluster. But the recovery report is
still hunting these, and they are found.

### 1b. Errand C4 — Bundles B and C

The register says of C4: *"Bundles B and C machine-readable transcriptions … The repo currently has
none."* This branch has both:

- `translations/archaeology/guodian_bundle_b_inventory.md` — 14,890 B, dated 2025-11-26, **slips B01–B08**, naming complete Ch. 41, Ch. 45, Ch. 52, Ch. 54.
- `translations/archaeology/guodian_bundle_c_inventory.md` — 8,621 B, **slips C1–C5**, covering Ch. 17 complete, Ch. 18 partial, Ch. 35 and Ch. 31 substantial. Source given as daoisopen.com C-bundle images.

C4 gates **R18 completion**, which gates **B2**, which is the 恆/常 footing — the fault line two
documents now lean on. Whether these inventories are *machine-readable transcriptions* in the sense
C4 requires, or prose inventories, needs a read. Either way the claim "the repo currently has none"
is false of this branch.

Also present and not in the repo: `guodian_section_break_analysis.md`,
`guodian_cross_reference_report.md`, `guodian_bundle_a_inventory.md`.

### 1c. The 74 slip photographs

`translations/archaeology/source_images/` — **74 files**. `reports/recovery_needed.md` §3a names
"~74 Guodian slip photographs (`guo_A01.jpg` … `guo_C05d.jpg`)" as present on this branch and
`claude/catch-up-UKmEu`. Confirmed. These are the facsimile inputs errands **C1** and **C7** wait on —
C7 gating the 非 tokens and, per B-n11, the 有/亡 graphic reading.

## 2. A 27-chapter Guodian-only translation, arranged in twelve thematic books

`translations/guodian/` is not a chapter list. It is a re-ordering:

| Book | Chapters |
|---|---|
| 01 engine | 40, 16, 5 |
| 02 geometry | 25, 32 |
| 03 co-emergence | 2 |
| 04 self-organization | 37, 57, 64 |
| 05 constant | 55, 41 |
| 06 perception | 56, 35 |
| 07 sufficiency | 44, 46, 9 |
| 08 boundaries | 52, 30 |
| 09 scale | 54, 66 |
| 10 governance | 17, 18 |
| 11 transformation | 15, 45 |
| 12 subtraction | 48, 19, 20 |

Plus `guodian_rsm_ordering_2025-12-07.md`, which presumably states the principle. This is an
organizing scheme for the strip material that exists nowhere else in the corpus, and it is a different
axis from both received-chapter order and Bundle A's physical unit order (19→66→46→30→15→64→37→63→2→32,
which the DDJ chain reads as entrance-practice-structure).

**Chapters 13 and 15**, flagged in the previous survey as existing only in the contaminated Set A:
**15 is here**, in book 11. 13 remains absent everywhere clean.

The branch also carries `TRANSLATION_FORMAT.md`, `TRANSLATION_TEMPLATE_2025-12-08.md` and
`translation_integrator.py`. The template opens: *"Purpose: Documentation, not persuasion. Show
pattern, don't argue."* That is the project's own discipline, stated as a drafting standard, three
months before the chains were written.

## 3. Register — care, not quarantine

Unlike `archive/ddj/translations` (hazard density 10–109 per file, contaminated throughout), this
branch scores low but not zero:

| File | Score |
|---|---|
| `test_results/TRANSFORMATION_ALGEBRA_DISCOVERY.txt` | 12 |
| `translations/lexicon/00_lexicon_introduction.md` | 6 |
| `translations/meta/framework_synthesis_2025-12-07.md` | 2 |

The algebra file opens in the pre-strike voice — *"We haven't been translating the Daodejing badly.
We've been reading the wrong type system … It's technical documentation written in a transformation
algebra"* — and claims **"81 chapters geometrically retranslated,"** which the trees do not support
(45 chapter files, 34 distinct, plus 27 Guodian-arranged). Treat that claim as unverified.

## 4. Unread

`research/` (284 files), `docsets/` (199), `docs/` (67), `python_analysis/` (70), `test_results/` (8),
`translations/appendices/`, and the substance of everything named above. This survey establishes
what is there and which errands it touches; it does not read the material.

---

## 5. What follows

1. **The table-intact craft originals** should come across regardless of D3, because D3 is a hold on *using* the material, not on *having* it — and the recovery errand is still spending effort hunting them.
2. **The Bundle B/C inventories** need a read against what C4 actually requires. If they satisfy it, C4 closes and R18/B2 unblock — which is the 恆/常 footing.
3. **The 74 source images** are the facsimile inputs for C1 and C7. They are on a branch, not in canon, and C7 gates two open readings.
4. **The twelve-book Guodian ordering** is organizationally new and has no counterpart in the canon line.
5. This branch has been unmerged since March and holds the only copies of all of the above. Whatever else happens, that is a single point of failure worth removing.

---

*Not sealed. Counts are enumerated from the trees; header/table-row checks are re-runnable; the register scores use the same token set as the previous survey.*
