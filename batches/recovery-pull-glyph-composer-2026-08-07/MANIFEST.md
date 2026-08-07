# Recovery pull — `claude/glyph-composer-v3-fQABj`, `translations/` tree

**Pulled 2026-08-07** from branch tip `688f4ed` (2026-03-15, *"Save WIP"*). **187 files, 9.2 MB.**
Complete subtree, byte-identical to the branch. Survey: `reports/glyph_composer_branch_survey_2026-08-07.md`.

**Status: recovered, not promoted.** Nothing here is canon, nothing is staged for the editorial pass,
nothing is ruled. This directory is a Layer-3 recovery landing. Promotion out of it is a ruling.

**Why it was pulled:** the branch has been unmerged since March and held the only copies. Three open
errands are answered by material in this tree (§1). The branch remains intact; nothing was moved.

---

## 1. What answers an open errand

### `archaeology/guodian_bundle_b_inventory.md` · `guodian_bundle_c_inventory.md` → **errand C4**
C4 reads *"Bundles B and C machine-readable transcriptions … The repo currently has none."* Bundle B:
14.9 KB, 2025-11-26, slips **B01–B08**, naming complete Ch. 41, Ch. 45, Ch. 52, Ch. 54. Bundle C:
8.6 KB, slips **C1–C5**, Ch. 17 complete, Ch. 18 partial, Ch. 35 and Ch. 31 substantial; source given
as daoisopen.com C-bundle images.

**Owed before C4 can close:** a read confirming these are transcriptions in the sense C4 requires
rather than prose inventories. C4 gates **R18** → **B2** → the 恆/常 footing.

Also here and not previously in the repo: `guodian_bundle_a_inventory.md`,
`guodian_section_break_analysis.md`, `guodian_cross_reference_report.md`.

### `archaeology/source_images/` → **errands C1 and C7**
**74 slip photographs**: `A_bundle` 41, `B_bundle` 19, `C_bundle` 14. These are the facsimile inputs
C1 (the batched slip images, including slip 34's ○ — *"the highest-value single graph in the survey"*)
and C7 (the 非 tokens, and per **B-n11** the 有/亡 grasping-hand reading) have been waiting on.

**Owed:** whether these resolve at sufficient resolution for the graph-level calls. Not assessed.

### `meta/` and `lexicon/06_technology_index.md` → **the table-recovery errand**
`reports/table_recovery_2026-08-06.md` gives the filter: files carrying a `notebook:` / `source_id:`
header are already table-stripped NotebookLM exports; the ones worth pulling lack it. These lack it:

| File | Table rows | Repo's staged copy |
|---|---:|---|
| `lexicon/06_technology_index.md` | **87** (10.5 KB) | 0 rows, 7.0 KB, has header |
| `meta/radical_technology_encoding_2025-11-27.md` | **57** | not in repo |
| `meta/forge_transformation_grammar_2025-12-07.md` | **46** | v0.972 export staged |
| `meta/loom_axiom_identity_2025-11-27.md` | **35** | 0 rows, has header |
| `meta/scythe_not_knife_2025-11-27.md` | **13** | 0 rows, has header |

Round 1 recorded the technology index as still missing *"the two Universal Failure Modes … and the
Reading Your Tools list."* The version here contains both. The cross-substrate table may be present
under other wording; unchecked.

---

## 2. Register flags — read before using anything here

**⚠ D3 — craft cluster, set aside whole 2026-08-03.** These are the recovered *originals* of material
Will set aside. **Recovering a document is not reopening the hold.** Do not draft from these:

`meta/scythe_not_knife_2025-11-27.md` · `meta/loom_axiom_identity_2025-11-27.md` ·
`meta/forge_transformation_grammar_{2025-11-27,2025-12-07}.md` ·
`meta/radical_technology_encoding_2025-11-27.md` · `meta/loom_and_forge_revised.docx` ·
`lexicon/06_technology_index.md`

Standing inputs for whenever D3 opens: `reports/technology_index_anachronism_check.md`, R22/R23.

**✓ Not part of D3.** The pot/wheel material is **Will's own ruled work** (B-n1), expressly excluded
from the set-aside. `chapters/chapter11_wheel_reread_2025-11-26.md` is unread and relevant.

**⚠ Pre-strike vocabulary present, low density.** `lexicon/00_lexicon_introduction.md` and
`lexicon/01_substrate_families.md` carry "substrate," which is retired. Density is far below
`archive/ddj/translations` (which scores 10–109 per file and is contaminated throughout), but it is
not zero. Read, don't lift.

**⚠ An unverified claim travels with this tree.** `test_results/TRANSFORMATION_ALGEBRA_DISCOVERY.txt`
on the branch — **not pulled** — asserts *"81 chapters geometrically retranslated."* The trees do not
support it: 45 chapter files covering 34 distinct chapters, plus 27 Guodian-arranged. If that number
appears anywhere downstream, it came from there.

---

## 3. What is in the tree

| Path | Files | Notes |
|---|---:|---|
| `chapters/` | 45 | 34 distinct chapters, 2025-11-26 → 2025-12-08. **24 are unpublished** — 3, 4, 5, 6, 7, 9, 10, 12, 14, 16, 21, 34, 37, 38, 39, 41, 46, 48, 51, 52, 56, 65, 78, 81. Variants: `chapter11_direct`, `chapter11_wheel_reread`, `chapter11_scythe_corrected`, `chapter22_pi_operation`, `chapter25_sphere_proof`, `chapter01` at three dates. **The four `_clean_2025-12-08` files are suspect** — the chapter-40 one dropped the Guodian attestation table and reverted co-emergence to linear emergence, which the preregistered test scored against. Only that one was checked. |
| `guodian/` | 28 | A **27-chapter Guodian-only translation in twelve thematic books** (engine · geometry · co-emergence · self-organization · constant · perception · sufficiency · boundaries · scale · governance · transformation · subtraction), plus `guodian_rsm_ordering_2025-12-07.md`. A third organizing axis, distinct from received-chapter order and from Bundle A's physical unit order. **Chapter 15 is here, clean** — previously only in the contaminated set. Chapter 13 remains absent everywhere clean. |
| `archaeology/` | 79 | 5 inventories/reports + 74 slip photographs |
| `meta/` | 19 | craft cluster (D3, above) plus `chapter25_rosetta_stone` ×2, `framework_synthesis` ×2, `hydraulic_origin_of_governance`, `governance_hydraulic_etymology`, `wei_wu_wei_vs_wu_wei_2025-12-08`, `dao_x_compounds`, `focusing_operation`, `radical_families_grain_blade` ×2, `corpus_status_2025-11-27` |
| `lexicon/` | 8 | substrate/operator families, structural positions ×2, concept and pinyin indexes, technology index (D3) |
| `analysis/` | 2 | `chapter01_integration.md`, `validated_characters.json` |
| `appendices/` | 1 | |
| root | 5 | `00_introduction.md`, `README.md`, `TRANSLATION_FORMAT.md`, `TRANSLATION_TEMPLATE_2025-12-08.md`, `translation_integrator.py` |

`TRANSLATION_TEMPLATE_2025-12-08.md` opens: *"Purpose: Documentation, not persuasion. Show pattern,
don't argue."* Dated three months before the chains were drafted.

---

## 4. What was NOT pulled, and why

Still only on the branch:

- `research/` (284 files) · `output/` — **`.gitignore` blocks both**; they cannot be tracked here without changing it.
- `docsets/` (199) — generated NotebookLM exports; `docset_*.md` is also gitignored.
- `docs/` (67) — a full MkDocs site build.
- `python_analysis/` (70) — radical co-occurrence, dictionary, translation engine, TTC parser, outputs. **Not gitignored; pullable. Unread, so not pulled.**
- `test_results/` (8) — pre-strike register; see §2.
- `src/`, `composer.html`, config — the Glyph Composer app. Inventoried separately at `reports/glyph_system_inventory_2026-08-06.md`; left in place deliberately.
- `guodian_bundle_a_data.csv`, `cooccurrence_matrix_2025-11-13.csv` at branch root — **pullable, not pulled.** Flag: the Bundle A CSV may bear on the dataset-reproducibility gap `reports/heng_chang_distribution_survey.md` records (*"this dataset's source CSVs are gitignored and off-disk — the dataset is currently unreproducible from tracked inputs"*). Worth a look.

---

*Not sealed. Byte-identical to `688f4ed:translations/`; the branch is untouched.*
