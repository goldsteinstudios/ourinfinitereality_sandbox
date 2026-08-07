# State of play — 2026-08-07

Canon **v9.52**. `research-archive` at `8bad9a6`, everything pushed, `checks.py` passing. Twenty
commits across 2026-08-06/07 from three instances working concurrently: this cloud session, a mobile
session on iPad/iPhone, and Claude Code on `wills-imac-local`.

**Read this before starting a stretch of work.** Fetch first — one audit this session ran against a
tip that was four commits stale by the time it finished.

---

## 1. What is now safe that wasn't

- **1,717 Guodian glyph PNGs** are tracked at `data/ddj/Guodian Strip Glyphs/` on `research-archive`, and the same 1,073-file subset sits at the identical path on `wip/claude-design-system`. Both branches agree on path and content; the merge is conflict-free. `.gitignore` now carries a per-child negation so new glyphs track without `-f`. **`wip/claude-design-system` still needs that same rule.**
- **The Guodian structured data** — `guodian_interactive.json` and three companions — backed up at `batches/backup-guodian-data-2026-08-07/`. That first file is what the 恆/常 survey runs on, and the survey states it was unreproducible from tracked inputs.
- **187 files recovered** from `claude/glyph-composer-v3-fQABj`, which had been unmerged since March and held the only copies. At `batches/recovery-pull-glyph-composer-2026-08-07/`.

## 2. Still able to vanish

1. **The Glyph Composer library** — browser `localStorage`, key `glyph-composer-library`. The tool has an export button. Everything composed lives there and nowhere else.
2. **`data/ddj/calligraphy/` and `guodian_strips_full/`** — same directory as the glyphs, never examined, not backed up.
3. **`~/Python Scripts/`** — `recursive_growth_simulator.py` (42 KB, in no branch) plus 23 MB of generated analysis PDFs. **`~/RSM_Database_v1.0/`** — referenced nowhere in the repo.
4. **The `.pages`/`.docx` manuscript layer** in iCloud — reachable now, still not converted or read.
5. **Chapters 28 and 36** of the DDJ have a single witness each, in `archive/ddj/ttc_chapter*.md` (July 2025). **Chapter 13** has no clean version anywhere — its only copy is in the contaminated lineage.

## 3. Open on the framework — ranked by leverage

| | Item | State |
|---|---|---|
| 1 | **Definition T (A8)** | The shared gate on all four of the math chain's chart-typed theorems, and through them on physics' two flagship correspondences (`1ₙ :: ℏ/2`, the spinor double cover). Necessary for any of them to move, sufficient for none. **Unattempted since v9.3 flagged it.** |
| 2 | **Quadraticity of the measure (A12)** | The metric gate. Until forced, "orthogonal" is a rendering fact and the dimension route's equidistance premise is measure-dependent. |
| 3 | **The native-magnitudes step (A1)** | The law gate. If the anchoring doesn't legitimate, the product form is one representative of an equivalence class and §4 onward is a rendering, not the spine. |
| 4 | **Dimension — "exactly three" (A5)** | Slot **empty**; both prior candidates withdrawn at v9.5. Worse than the "two rival derivations" it replaced. Physics inherits it as the (1,1)-vs-(1,3) strain. |
| 5 | **The cross-frame cluster** (A3 residue, A4, A9, A10) | The missing account of any relation between frames that isn't parent–child. The most *visible* hole for a reader. |

**Two confirmed defects, unruled, untouched by any instance:**

- **Audit 1.1** — `just_math_v9_5.md` line 60 still says the relation between the two mode-dominant regions "is carried by revolution." Structural §6 and physics §1 both assign that to **descent**. R3's demotion reached two chains of three, and missed the one whose entry is named "Revolution."
- **Audit 1.3 / E4** — the **Corollary** (v7.7's L1, once "the single head of the audit," carrying four loads) has no entry in `reports/open_items.md`. Load-bearing in structural §4's floor argument.

**Two structural questions nobody has answered**, both upstream of how the book frames itself:

- The independence claim isn't true of the physics chain. Its entries split cleanly into those standing on the spine (time, circulation, excluded cores, RG, irreversibility, Bekenstein) and those standing on the math chain's chart (ℏ/2, c, E=mc², Wick, spin-½) — and the second list is the impressive half.
- Physics runs on **one live prediction of four**. Prediction 1 is a genuine kill-condition; 2 is unseparated from standard predictions; 3 and 4 are unbuilt.

## 4. Open on filing and the register

- **`rsm/audit/register_update_2026-08-06.md` is still unmerged** into `reports/open_items.md`. It carries A-n13 **CORRECTED**, A-n14, A-n15, B-n8 through B-n12 (B-n12 retired), C-n3, and D5. The register now has one strand merged and one pending from the same two days — the next regeneration should take both.
- **E2, needs a ruling.** `just_ddj_v9_5.md` line 27 names **恆** as the register marker. Line 11 still reads *"可 and 常 are the explicit and implicit registers. 常 is what holds frame-independently"* — a **gloss, not a quotation**, contradicting line 27 in the same file. The quotation-vs-gloss HOLD doesn't cover it. Same sentence sits in `CLAUDE.md` 313–315.
- **E3, a contradiction between two of our own records.** C7 names only the 非 tokens. B-n11 asserts C7 also gates the 有/亡 grasping-hand reading. False of C7 as written — either C7 widens or B-n11 corrects.
- **E1** — the ±1 face/value fix is applied in the Euler paper only. `series-02` and `series-08` are owed; essay 8's version is the exhibit's clearest statement anywhere.
- **C4** — Bundle B and C inventories are now recovered. A read is owed on whether they are transcriptions in the sense C4 requires. C4 gates R18 → B2 → the 恆/常 footing.
- **`site_vocab_lint.py` has no ban for "generative crossing."** `CLAUDE.md` says it enforces the 2026-07-29 correction. It doesn't. **12 occurrences across 8 files in `src/`**, including the homepage and the rosetta-stone page. Adding a ban is a change to a guard, so it wants a ruling.
- **D2 closed as lost.** The 2026-08-04 in-session Euler patch is unrecoverable — this clone postdates it and no reflog, stash or dangling object holds it.

## 5. The DDJ translations

**36 chapters across five lineages.** Two independent reads this session, filed at
`reports/ddj_translations_read_2026-08-07.md` (site set, in full),
`reports/ddj_translation_sets_survey_2026-08-07.md` (four generations, hazard-scored), and
`reports/ddj_retranslation_corpus_read_2026-08-07.md` (five lineages — this one caught the July 2025
`ttc_chapter*` stratum the other two missed).

- **24 translated chapters are unpublished**, recovered from the branch: 3, 4, 5, 6, 7, 9, 10, 12, 14, 16, 21, 34, 37, 38, 39, 41, 46, 48, 51, 52, 56, 65, 78, 81.
- **`archive/ddj/translations/` (16 chapters) is pre-strike register**, not merely stale — P₀ carrying a time derivative and a Hamiltonian, retired X₁/Y₁/Z₁, consciousness as mechanism, "lost technology." Hazard density 10–109 per file, every file contaminated. **M9 says an archived error is a seeded error. It sits unmarked. Quarantine-typing it is a ruling.**
- **Two glosses in the site set contradict standing rulings at strong confidence:** ch. 40 reads 弱 where the chain types the slot as **溺, attested-uninterpreted, no `::` assignable**; ch. 25 glosses 王 as "the conscious agent," an underived slot, importing the one thing physics excludes.
- **Don't trust `_clean_` in a filename.** `chapter40_clean_2025-12-08` dropped the Guodian attestation table and reverted co-emergence to linear emergence — the staged hierarchy the preregistered test scored against. Three other `_clean_` files unchecked.
- **Recoveries pointing upstream:** ch. 1 states 妙/徼 as a *procedure* (fix centre vary boundary / fix boundary vary centre, geometrically orthogonal) — the parallax method operationalized, and absent from the chain. And every site file carries per-element confidence with levels and reasons: the epistemic apparatus v9.3 deleted, alive and finer-grained than what was purged.

## 6. The book and the voice

- **The voice profile and the collated notes were built on 4,579 words.** `podcast_outline_convo.txt` holds **27,812 words** of Will's own prose — 791 turns, zero em-dashes, 6.1× the corpus. Both artifacts should be re-run on the larger set.
- **The em-dash test holds**: 0.00 per 1,000 words across everything verbatim; the machine layer runs 15.9–27.4. Any page above ~5 has no sentence of his on it.
- **His sustained register is spoken.** Every passage over 100 words in the corpus is dictated. Typed, he tops out near 95 and compresses to aphorism.
- **The conviction census** — proposed, agreed in principle, never started. Ladder for ranking, conversations to restore the nuance formalization strips.
- **Ch. 1 of the book outline is `[DISCOVERY NARRATIVE — Will only]`** — the lathe story. The machine declined to write it. Natural first dictation.
- **Fiction set aside whole (D5).** The trilogy, the generation ship, the Vonnegut story. The myth work and ancient-people work stay: transmission thesis, mounds vs pyramids, agriculture and hubris, the teaching parables. Six borderline items unruled at `reports/fiction_sort_2026-08-07.md` §3.

## 7. The failure mode this session named

Three instances of one shape, now logged: a guard applied to the edit rather than the page (Entry 006);
`site_vocab_lint` watching the downstream copy rather than the source (its own header); and a search
anchored on the path the claim itself assumed (Entry 007). **All three run clean, exit zero, and look
like diligence.** When checking a claim, the check must not inherit the claim's coordinates.

Also standing: the CHECKABLE tag is the handoff. Route what an instance *distributes, recovers, files
and tags* straight through; route what it *generates or repairs* back through the soundness lane.

---

*Not sealed. Facts verified against the tree at `8bad9a6`.*
