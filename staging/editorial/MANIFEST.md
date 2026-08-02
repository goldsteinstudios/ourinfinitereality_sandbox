# Editorial staging — MANIFEST

Staged 2026-08-02 from branch `research-archive` (plus two branches, noted per file).
Copies only; all originals left in place. Flat set for NotebookLM ingestion; `superseded/`
holds reference-only documents that must not be ingested as live doctrine.

Dates are content dates where known (the v0.971/v0.972 folders are NotebookLM exports made
2026-07-22 of Nov–Dec 2025 content; date given is the content date).

## The essay series (16)

| Staged file | Original | Branch | Date | Newer copy elsewhere? |
|---|---|---|---|---|
| `series-00-preface.md` … `series-15-what-pi-names.md` | `archive/notes/essay-series/00…15` | research-archive | 2026-07-18 | No — sole copies. Track v7.7 canon (RSM r13, math r7, physics r1+4, DDJ r6d); canon is now v9.3. |

(All sixteen staged under `series-NN-<title>.md`; original filenames use spaces, content unmodified.)

## Expansion documents (17)

| Staged file | Original | Branch | Date | Newer copy elsewhere? |
|---|---|---|---|---|
| `expansion-packed-hanging.md` | `archive/rsm-versions/v0.971/077-packed-hangingmd.md` | research-archive | 2025-12 | **No — v0.971 only** (dropped from v0.972). Tables stripped by export. |
| `expansion-laozi-guided-walk.md` | `research/laozi_guided_walk_draft.md` | **sphere_model** | undated (~Dec 2025–Mar 2026 era) | No copy on research-archive — **branch-stranded**. |
| `expansion-unpluggable-hole.md` | `research/unpluggable_hole_draft.md` | **sphere_model** | undated (same era) | No copy on research-archive — **branch-stranded**. |
| `expansion-bridge-thought-experiment.md` | `archive/alan/Bridge thought experiment (Claude 11.9.25).md` | research-archive | 2025-11-09 | A PDF render exists per archive manifest; this .md is the working copy. References a missing `Attachments/…png` image. |
| `expansion-motion-unification.md` | `archive/notes/physics/updated_motion_unification.md` | research-archive | 2025-08 | No. Sole copy of the escapement metaphor. |
| `expansion-helix-structure.md` | `archive/rsm-versions/v0.971/070-helix-structuremd.md` | research-archive | 2025-12 | **No — v0.971 only.** Tables stripped. |
| `expansion-loom-axiom-identity.md` | `archive/rsm-versions/v0.971/073-loom-axiom-identity-2025-11-27md.md` | research-archive | 2025-11-27 | v0.972 copy exists, prose byte-identical (export header differs only). |
| `expansion-scythe-not-knife.md` | `archive/rsm-versions/v0.971/088-scythe-not-knife-2025-11-27md.md` | research-archive | 2025-11-27 | v0.972 copy exists, prose byte-identical. |
| `expansion-forge-transformation-grammar-v0972.md` | `archive/rsm-versions/v0.972/046-forge-transformation-grammar-2025-12-07md.md` | research-archive | **2025-12-07 revision** | This IS the newer copy (v0.971 has the older 2025-11-27 draft; staged per instruction). |
| `expansion-hamon-chapter76.md` | `archive/rsm-versions/v0.971/069-hamon-chapter76-identity-2025-11-27md.md` | research-archive | 2025-11-27 | **No — v0.971 only.** |
| `expansion-chapter76-v0972.md` | `archive/rsm-versions/v0.972/040-chapter76-2025-11-26md.md` | research-archive | 2025-11-26 | v0.971 copy (044-) exists; header-only difference. Tables stripped (character decomposition, key terms, "Complete Teaching" blocks — see recovery report). |
| `expansion-chapter40-v0972.md` | `archive/rsm-versions/v0.972/030-chapter40-2025-11-26md.md` | research-archive | 2025-11-26 + 12-07 addition | This IS the newer copy — carries the observation-stances section v0.971's lacks. |
| `expansion-chapter05-v0972.md` | `archive/rsm-versions/v0.972/011-chapter05-2025-11-26md.md` | research-archive | 2025-11-26 + 12-07 addition | This IS the newer copy — observation-stances section. |
| `expansion-technology-index.md` | `archive/rsm-versions/v0.971/007-06-technology-indexmd.md` | research-archive | 2025-11-27 | v0.972 copy (006-) exists; header-only difference. Tables stripped. |
| `expansion-why-pi-starts-at-three.md` | `archive/rsm-versions/v5.5/essay_why_pi_starts_at_three.md` | research-archive | 2026-03 | No (six near-duplicates existed pre-dedup; this is the kept copy). |
| `expansion-cavp-longform.md` | `archive/notes/misc/cavp_longform.md` | research-archive | 2025-08-23 | No. Note: predates essay 12's retirement of "cost" vocabulary and uses it in places. |
| `expansion-three-contemplations.md` | `archive/rsm-versions/v5.5/three_contemplations.md` | research-archive | 2026-03-25 | No. |

## Parables (4)

| Staged file | Original | Branch | Date | Newer copy elsewhere? |
|---|---|---|---|---|
| `parable-true-punishment-sisyphus.md` | `archive/notes/misc/true_punishment.md` | research-archive | 2026-01-05 | Argued companion exists: `v0.971/089-sisyphus-breathmd.md` (different document, not staged). |
| `parable-sailor-and-waves.md` | `archive/notes/misc/sailor_and_waves.md` | research-archive | 2026-01-05 | `docset-pipeline` carries a frontmatter-wrapped copy of the same story. Dev transcript: `archive/notes/misc/sailor_waves_chat.txt`. |
| `parable-sailors-paradox.md` | `sets/nlm-parables/02_the_sailors_paradox.md` | **docset-pipeline** | 2026-01-05 | **Different story** from sailor-and-waves (kept deliberately, per instruction). Also at `batches/batch-4-narrative/02b_…` on research-archive. |
| `parable-kai-unmeasurable-field.md` | `sets/nlm-parables/01_parable_kai_unmeasurable_field.md` | **docset-pipeline** | 2026-01-05 | Three copies on that branch; `sets/nlm-parables/` and `notebooklm_processed/` byte-identical (staged from the former); `notebooklm_staging/` differs. Also at `batches/batch-4-narrative/03_…`. Machine-generated ("teaching story generated by NotebookLM", `version: 0.993`). |

## superseded/ (4) — reference only, do NOT ingest as live doctrine

| Staged file | Original | Date | Why superseded |
|---|---|---|---|
| `superseded/tree-essay-updated.md` | `archive/notes/misc/tree_essay_updated.md` | 2025-07-26 | Types the pith as **P₁ (paradox center)** — the reading the botany refused; canon (essay 10 / chains) types the pith's analog as the *unmet* center, cambium as the gradient. Retired notation (Z₁). (The `batches/batch-5…/07_tree_essay_updated.md` copy is the same file.) |
| `superseded/seven-dialogues.md` | `archive/notes/misc/seven_dialogues.md` | 2026-01-05 | Runs on **V₀** (retired vocabulary; current object is P₀, which is *not* the void) and V₀→O₁ transition framing. Wanted for reference per instruction. |
| `superseded/consolidated-biology-section.md` | `archive/notes/misc/consolidated_biology_section.md` | 2025-08 | Line 150 types **pith as Pₙ** (`Pₙ (pith center) → Gₙ (cambium)…`); also Zₙ notation. Caught by the pith sweep. |
| `superseded/arboreal-form-v099.md` | `archive/rsm-versions/v0.99/008-the-recursive-geometry-of-arboreal-form.md` | 2025-11/12 | States "**The pith is Pₙ**" outright; the compact slide-copy version of the same superseded typing. |

## Not staged, noted for completeness

- `archive/rsm-versions/v0.971/089-sisyphus-breathmd.md` — the argued Sisyphus essay; not on the
  requested list. Flag if wanted.
- The batches/ copies of many of these files (built 2026-08-02 for the project-folder handoff) are
  earlier extractions of the same originals; staging here is fresh from the sources.
