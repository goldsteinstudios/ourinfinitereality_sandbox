# Catalog of RSM Supporting Material — August 2026 sweep

A full survey of the repository and all GitHub branches for **metaphors, worked examples, thought
experiments, parables, analyses, and essays** drafted to support the RSM. Four parallel searches:
the consolidated iCloud `archive/`, the `docs`/`drafts`/`research`/`data` directories, the site
(`src/`), and a diff of every other branch against `research-archive`.

Compiled 2026-08-01, on branch `research-archive`. File paths are relative to the repo root unless
a branch is named. **Not a ruling on anything** — an inventory, with version-era hazards flagged.

---

## Headline findings

1. **The entire rhetorical layer of the project lives in `archive/` and nowhere else.** No metaphor,
   parable, or essay from the archive appears in the canon chains, the audit trail, or (with a few
   exceptions) the site. The tracked non-archive corpus is chains + audit + ~7 site essays + 7
   object pages — a different set entirely.
2. **Two branches hold unique material `research-archive` does not:** `sphere_model` (the geometric
   exposition, incl. three never-merged long drafts) and `docset-pipeline` (the NotebookLM parable/
   dialogue/theorem corpus). `guodian-rsm-rebuild` / `claude/glyph-composer-v3` add a smaller layer
   of DDJ analytical notes. All other branches (`main`, `rsm/v9-canon`, etc.) are strict subsets.
3. **A large expository corpus was deleted from history** by commit `98154a2` ("Slim main to Astro
   site build + deploy files only", 2026-03-15): the physics synthesis quintet, `why_water.md`, the
   geometry docs, and the whole `docs/framework|pattern|physics` tree. Absent from every current
   tree but recoverable from git history (and much of it still present on `sphere_model` /
   `docset-pipeline`).
4. **The site is pinned to v7.7** (last retype 2026-07-14; canon is now v9.3) with itemized lags
   (§6 below).
5. **Version hazard throughout:** the archive's version numbers run in two incompatible schemes —
   the `v9.x` files are **Sept 2025** (early), `v5→v7→v8` are **Mar–Jul 2026** (late), and
   `v0.9x` are NotebookLM notebook labels, not RSM versions. Date by mtime, not by number.

---

## 1. Metaphors

### The ancient-technology cluster ⭐ (Nov 2025; `archive/rsm-versions/v0.971/`, dup in v0.972)
Twelve tight, thesis-driven pieces arguing pre-literate crafts *are* the axiom system. All
archive-only, one voice, signed, dated 2025-11-27:

| File (in `archive/rsm-versions/v0.971/`) | Metaphor | Concept |
|---|---|---|
| `073-loom-axiom-identity-…` | **The loom** — "the loom IS the axiom system, running in thread and wood"; 經/緯 as orthogonality | i, π, ⊥, e from one premise |
| `057-forge-transformation-grammar-…` | **The forge** — transformation algebra in fire and iron | f(substrate, operator) → result |
| `069-hamon-chapter76-identity-…` | **The hamon** — "Chapter 76 written in steel" | 剛/柔 as a placed gradient |
| `094-wuwei-clay-principle-…` | **Clay on the blade** — "you can't force the hamon; you create the conditions" | 無為 operationally |
| `088-scythe-not-knife-…` | **Scythe vs. knife** — 利 as the π-operation (arc), not linear cut | load-bearing; propagates to Ch. 11 site copy |
| `056-focusing-operation-…` | **Bronze ladle** — 勺 as concave focusing | field → point |
| `071/072-hydraulic-…` | **River channel / water management** — 治 = 氵+台; governance *is* channeling | the river/tributary family's home |
| `070-helix-structuremd` | **Rain chain** — water spiralling "around the absence of a downspout" | best orbit-around-excluded-center image |
| `077-packed-hangingmd` | **Paper honeycomb decoration** — the 3D form was always present, folded | 常↔可 register |
| `081-radical-technology-encoding-…` | Thesis paper: "radicals are compressed engineering manuals" | the cluster's argument |
| `007-06-technology-indexmd` | The cluster's index — "each craft has its entry point into the same geometry" | finding aid |

### Other strong single metaphors
- **The grain field** ⭐ — `docs/essays/line_one.md` ("The Path and the Field"): path and field
  co-emerge; the grain growing back is the engine, not the failure. The best sustained metaphor in
  the tracked tree. (Pre-v7.7 vocabulary — needs a pass.)
- **The spring coil** — `drafts/frontpage_section2_spine_r1.md` step 5 (from
  `_grammar-of-existence.md`): "the coils crowd infinitely closer and the collapse never finishes."
- **"Keep it on your left and keep going"** — same file, step 6; the circulation image, harvested
  from a retired argument's conclusion while discarding its circular route.
- **The unpluggable hole** ⭐ — `research/unpluggable_hole_draft.md` on **branch `sphere_model`**
  (never on research-archive): the wheel-center you can't stand on → the narrowing hose → four
  graded impossibilities (physical/intellectual/epistemological/ontological, yet logically
  necessary) → the hollow tree → "The impossibility is the engine."
- **The bellows/vortex/gyroscope/escapement set** — `archive/notes/physics/updated_motion_unification.md`
  is the *only* file carrying the full circulation-metaphor set including the clock escapement.
- **The tree, ruled** — `drafts/site_v7.7_redraft_r2.md` B2.4 + `src/content/objects/tree.mdx`:
  pith :: Oₙ · cambium :: Gₙ · rays :: Bₙ · branch node :: Pₙ, with the pith-toroid retraction
  displayed ("losing the toroid improved the fit"). Deep version:
  `archive/notes/misc/tree_essay_updated.md` (needs style pass).
- **Emptiness list** — essay `05 on emptiness`: "The hollow of the bowl. The eye of the vortex.
  The silence between the notes."

## 2. Thought experiments

| Where | What |
|---|---|
| `archive/alan/Bridge thought experiment (Claude 11.9.25).md` ⭐ | **The stone arch bridge** — "standing on a structure held up by something that isn't there"; obstacle → arc → excluded center. The most developed standalone thought experiment (21 KB). |
| `archive/rsm-versions/v5.5/three_contemplations.md` ⭐ | **The Bundle / The Wind / (third)** — written *for the landing page*, never used. Highest reuse-per-word in the archive. |
| `archive/rsm-versions/v0.96/054…040…053…` | **The Block vs. the Body** — push a block across a room vs. walk it yourself; the body generates a dimension to escape Zeno. Three overlapping drafts. |
| `archive/rsm-versions/v0.96/011/012…` | **Zeno / coffee mug**; the "Forever Halves" onboarding question ladder. |
| `archive/notes/misc/universe_as_verb.md` | "Try to imagine the universe ending — where's the edge?"; "try to imagine absolute nothing" (designed to fail). |
| `archive/notes/misc/time_rsm_exploration.md`, `time_orbital_narrative.md` | "Try to catch the present moment" — subdivide `now` until it has no duration. |
| `src/pages/pattern.astro` (long version) | The spring compressed toward its core; the "no *there* to pass through" elimination that leaves circling as sole survivor. |
| `src/content/essays/topology-of-being-alive.md` | **The torus/gut-lumen** — "the tube from mouth to anus has never been inside you." |
| Branch `sphere_model`: `research/laozi_guided_walk_draft.md` ⭐ | **The guided walk** — a 60-minute suburb→woods→suburb walk in four quadrants (妙/徼 × 常/可), 21 stations each mapped to a DDJ chapter; the register distinction taught kinesthetically. |

## 3. Parables, dialogues, counter-myths

- `archive/notes/misc/sailor_and_waves.md` ⭐ — **"The Sailor and the Waves"**, finished narrative
  fiction. Long version with the effort-cost divergence arc: branch `docset-pipeline`,
  `sets/nlm-parables/02_the_sailors_paradox.md`.
- `archive/notes/misc/true_punishment.md` ⭐ — **"The True Punishment of Sisyphus"** — the curse was
  never the boulder; it was the *promise* that the summit means release. Publishable as-is.
  Companion essay: `v0.971/089-sisyphus-breathmd.md` (反者道之動).
- `archive/notes/misc/seven_dialogues.md` ⭐ — **Laozi and Einstein**, seven dialogues, each pinned
  to a transition with Chinese text + matching physics. Einstein as sage, Laozi as master.
- Branch `docset-pipeline`: `sets/nlm-parables/01_parable_kai_unmeasurable_field.md` ⭐ — **Kai and
  the unmeasurable field** (knife vs. scythe; "the center does not need to be located; it needs to
  be referenced"); `sets/nlm-dialogues/03_dialogue_sailor_to_sisyphus.md` ⭐ — cross-parable
  dialogue ("You, friend, are trying to knife the mountain"), with a Bellows-Cycle vs.
  Sisyphus-Cycle table; `01_dialogue_physicist_sage.md`.
- `archive/notes/ai-sessions/conversations_with_laozi_8.11.25.txt` — the 142 KB raw quarry.

## 4. Essay series and long-form essays

### "Around the Center" ⭐ — `archive/notes/essay-series/00–15` (Jul 2026, tracks v7.7)
The only complete, epistemically disciplined series: every essay names its invariant plainly, then
points from each register without merging; claims carry `[derived]/[candidate]/[observation]/[P2]`.
Standouts: **10 on the tree** (nesting is a tree, not a ladder), **12 on energy** (a public
*refusal* essay — retires the misalignment-cost through-line), **14 on dimensionality** (ends
without concluding on purpose), **15 what pi names** (everything held at `[observation]` by
ruling). Related book chapter: `archive/notes/misc/around the center ch5.md` ("The Center Becomes
a Door" — the seed as compressed tree-logic).

### The Aug 2025 longform cluster — `archive/notes/misc/`
- `cavp_longform.md` ⭐ — the only narrative exposition of **CAVP** (accuracy belongs to structure,
  precision to description).
- `energy_longform_narrative.md` — "The Currency of Existence" (superseded in doctrine by essay 12;
  read as history).
- `consciousness_straw_dogs_essay.md` — 49 KB, the meta/self-reflexive essay ("The Great Detour").
- `recursive_orientations_essay.md`, `scale_invariance_rsm.md`, `time_orbital_narrative.md`,
  `unity-paradox-paper.md`, `paradox_essay_updated.md`.

### Tracked-tree essays
- `docs/essays/line_one.md` ⭐ (grain field; pre-v7.7) and `chapter_one_translation.md`
  (operator table; **superseded** — 玄 :: O₁ is inverted by later canon).
- `drafts/frontpage_section2_spine_r1.md` ⭐ — the nine-step plain-language derivation with
  `[RULE]`/`[DE-TENSED]`/`[TRAP AVOIDED]` flags; the best current exposition of the argument.
- `drafts/frontpage_storyboard_r1.md` — the scroll-as-camera ten-shot storyboard ("the camera move
  *is* the argument").
- Site essays (`src/content/essays/`): `the-gap.md` (seven angles on one gap; **lags canon**),
  `standing-wave-pattern.md` (CAVP; disciplined "What This Isn't"),
  `topology-of-being-alive.md` (banner applied to one paragraph only), plus two **unpublished**
  reservoirs: `_grammar-of-existence.md` and `_between-e-and-phi.md` (crystal vs. tree; the
  archaeology section — tell, henge, pyramid, landfill).
- `archive/rsm-versions/v5.5/essay_why_pi_starts_at_three.md` ⭐ — self-contained, publishable,
  needs no framework knowledge.
- Euler set-piece at three maturities; most finished: `archive/essays/euler-tao-identity.md`
  (site-ready frontmatter, not on the site). Also `archive/essays/ddj-chapter01.md`,
  `ddj-chapter11.md` (the wheel/pot/room with the scythe-corrected 利).
- Branch `sphere_model` (never merged): `research/integrated_geometry_paper_draft.md` (DDJ ↔
  Sanskrit ↔ complementarity on one hyperbolic geometry); **deleted-from-history** physics quintet
  under `docs/framework/`: time_recursion, black_hole, quantum_measurement, energy_conservation
  ("energy is rotation… reality cannot occupy its own center, so it turns"), formalism (wu wei as
  stationary action), plus `docs/essays/why_water.md` (water has no agenda) and the **Paradox
  Sphere Π₀** construction (`docs/framework/geometry.md`).
- Branch `docset-pipeline`: `sets/nlm-essays/01_the_loom_and_the_forge.md`,
  `02_wu_wei_gardeners_principle.md`, the theorem set `sets/theorems/t01–t07` (incl.
  `t07_ex_nihilo_impossibility.md`, 451 lines), and `sets/meta/` (epistemic tiers, dependency
  graph, falsification criteria).

## 5. Analyses, formalizations, teaching material

- `research/archive/external_analysis/chatgpt_double_colon_formalization.md` ⭐ — Galois-connection
  **witnessed-correspondence semantics for `::`**; chaining licit only under a shared witness.
  **Loose thread:** answers the "chained ::" dispute adjudicated in `site_v7.7_redraft_r2.md`,
  but the two were never connected.
- `research/archive/conversation_summaries/rsm_deep_critique_march_2026.md` ⭐ — the four-round
  adversarial dialogue; origin of the **e-to-φ continuum** and its proposed biological test
  (perturbation resilience near φ-ratios across unrelated systems). v5-era; contains the retired
  measurement-crisis argument.
- `archive/notes/misc/9.26.25_research_review.md` — the honest null result ("RSM as described does
  not exist in current academic literature").
- The Sept 2025 **monograph triplet** (`9.26.25_rsm_technical_monograph_*.md`) — one monograph in
  three voices; A/B/C material for voice decisions.
- `archive/notes/physics/` — the four-section physics series + `time_relativity_essay.md`
  ("The Dance of Dragons") + `RSM_vs_Relativity.md`.
- Substack/podcast: `substackpost_1_8.25.25.md` (the 4025-archaeologists cold open),
  `SUBSTACK_POSTS_READERS_GUIDES_9.16.25.txt` ⭐ (scaffolded on-ramp, posts 2–9),
  `archive/notes/book-drafts/draft episodes_7.16.25.txt` ⭐ (full podcast scripts; Episode 2 is
  misfiled as `notes/misc/Untitled 2.txt`).
- `archive/alan/` — the AL-AN sub-project: `ALAN_Communication_Guide.md` ⭐ (audience-targeted
  scripts, "plant seeds"), `Commentary Series…md` (53 KB systematic DDJ↔RSM Q&A),
  `one-distinction.md` ⭐ ("agreement is cheap under single authorship" — the most intellectually
  honest document in the archive) and `one-distinction-heart.md` (the pure-exposition cut),
  `ALAN_Perpendicular_Protocol.md` (checkable tree-branching prediction),
  `ALAN_Phase_Implementation_v3.py` (the only executable expression of the framework).
- Branch `guodian-rsm-rebuild` / `glyph-composer`: `wei_wu_wei_vs_wu_wei` analysis, Ch. 25
  convergent-geometries note, hydraulic 治 etymology, and the **12-book structural reordering of
  the Guodian corpus** (the ordering itself is an RSM argument).
- Data: `data/rsm/v7.5/through_lines.yaml` (11 cross-domain through-lines — densest worked-example
  index), `correspondences.yaml`, `status.yaml`; `data/ddj/guodian_interactive.json` carries a
  ~2%-complete glyph-exposition seam (the "scythe arcing through grain = π-operation" reading) that
  `tools/dedupe_guodian_slips.py` documents as **unreproducible** (source CSVs gitignored).

## 6. The site layer (`src/`) — and where it lags

Interactive demos: `/zoom` (the premise experienced, not told — strongest piece; **unlinked**),
`/pattern` (eight beats, seven animated argument diagrams; **unlinked**), `/guodian` (the `[G]` tag
made inspectable — the only evidential piece), seven animated object glyphs. Object catalog
(7 `.mdx`), ten DDJ chapter commentaries, three published + two unpublished essays, and the
discipline pages (`rosetta-stone` — the canonical `::` exposition; `confidence`, `claims`,
`methodology` with the worked negative example).

**Lags (site is at v7.7; canon v9.3):** three incompatible live glosses of 玄;
`chapter-01.md` self-contradiction (table vs. body vs. frontmatter); essays running the superseded
empty-center typing; retired O₁ notation and occupancy framing in `claims.astro`/`faq.astro`;
two parallel confidence vocabularies (schema enum vs. tag system) and zero `[G]/[R]` tags in
chapter files; Kleiber's-Law still live in FAQ against `claims.astro`'s own retraction;
`chapter-42.md` frontmatter contradicts its retyped body; two diagrams marked "FOR WILL TO RULE"
shipping on `/pattern`; `public/icons/` dead duplicates. No escapement or river metaphor anywhere
in `src/`.

## 7. Gaps, hazards, loose threads

- **Three essays are indexed but textless** (`archive/rsm-versions/v9.2/RSM_Core_Essay_Library_Index.md`):
  "The Complete Geometric Framework: Why the Wheel, Bellows, and Vessel"; "The Secret Language of
  Reality" (irrational numbers); "The Curvature of Precision" (orbital shells). Probably PDF-only
  in the gitignored `research/archive/icloud_import/` — check before assuming lost.
- **Doctrinal drift traps:** energy-as-cost (retired by essay 12); voice guide v1 (killed by v2);
  `chapter_one_translation.md`'s 玄 :: O₁; the v5 measurement-crisis argument; `docset-pipeline`'s
  older copies of two site essays (don't back-port).
- **Misfiled:** `Untitled 2.txt` (podcast Ep. 2), `Untitled.txt` (Lexicon v4.0), `Untitled copy.txt`
  (Ch. 1 translation); `ttc_chapter28…md.md` doubled extension.
- **Dedup:** v0.971 vs v0.972 overlap heavily (v0.972 is the trimmed successor).
- **The `::` transitivity loose thread** (§5 above) — formalization and ruling never connected.
- **Recovery targets in git history** (deleted by `98154a2`, still on `sphere_model`/
  `docset-pipeline`): physics quintet, `why_water.md`, geometry docs, NotebookLM sets.

## 8. Shortlist — strongest pieces, least work to use

1. `archive/rsm-versions/v5.5/three_contemplations.md` — written for the landing page; still unused.
2. `archive/rsm-versions/v7.6/our infinite reality introduction.md` — the "stay-at-home dad and
   woodworker" opening; strongest cold open in the corpus.
3. `archive/notes/essay-series/00–15` — the complete disciplined series (esp. 12, 14, 15).
4. `archive/alan/Bridge thought experiment…md` — best standalone thought experiment.
5. `archive/notes/misc/sailor_and_waves.md` + `true_punishment.md` — publishable fiction as-is.
6. The Nov-2025 technology cluster — twelve metaphors, one voice, archive-only.
7. `archive/essays/euler-tao-identity.md` + `ddj-chapter11.md` — already carry site frontmatter.
8. `archive/alan/one-distinction-heart.md` — the framework at its most compressed and readable.
9. Branch `sphere_model`: `research/unpluggable_hole_draft.md` — best metaphor document overall.
10. Branch `docset-pipeline`: the Kai parable + sailor→Sisyphus dialogue.
