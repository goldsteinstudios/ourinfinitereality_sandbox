# RSM Framework Context

This repository contains the Recursive Structural Model (RSM) and its convergence with the Dao De Jing and physics. Read this file first to understand the framework before working on any RSM-related content.

## The :: Discipline

`::` denotes **imperfect structural correspondence** - two expressions from different registers point toward the same structural fact, neither captures it fully. 

- `::` forbids substitution, upgrade to identity, and congruence by default
- A `::` chain (A :: B :: C) claims all terms converge on one identified invariant
- The convergence of independent imperfect pointings marks one pattern pointed at from several registers — a shared referent, not evidence for a claim; the framework runs from a conditional and accumulates no confirmation

**In prose**: Use "to me, that looks just like..." rather than "X is Y"

## Foundational Conditional

> If reality has no terminal resolution in either direction, then neither a minimum scale nor a maximum extent obtains.

This is the load-bearing premise. Everything follows from it.

## The Chains (v9.52 — current working set; NOT sealed)

> **CANON UPDATE (2026-08-04, patch sets 1–5 + session drafting):** current canon is **v9.52**, and the
> **markdown layer is canonical**: `rsm/canonical/chains/v9.5/` (see its `README.md`, and
> the diff trail `reports/v9_4_patch_diff_report.md` → `v9_4_1…` → `v9_4_2…` → `v9_5_patch_diff_report.md`).
> The v9.3 PDFs are **deprecated as canon** (kept as history; not regenerated). The description
> below this block still describes **v9.3** and is retained as history — its "PDF-only"
> consequences no longer apply to current canon. Headline changes: §0 gains "Accuracy and
> precision"; "the two senses of smaller" → "Vantage"; §7 opens with the two transfers and
> derives O₍ₙ₊₁₎ = Pₙ; the disconnection re-justified directly; revolution re-typed
> available-not-forced (R3); anchoring-by-constitution resolved negative (R14); the math
> parturition-map theorem replaced by "The recursion (two transfers)"; the DDJ three-forms
> taxonomy retired (R5) with 有無相生/Ch. 40 rewrites flagged pending (R6).

v9.3 is a **spine + three renderings**. Only the structural chain is register-neutral; **no rendering
cites another rendering's theorems** — that is what makes their independence real. Every document
closes "Not sealed." Location: `rsm/canonical/chains/v9.3/`.

| Chain | Register | File |
|-------|----------|------|
| Structural (the spine) | logic only | `structural v9_3.pdf` |
| Just-Math | derivation | `just math v9_3.pdf` |
| Just-Physics | rendering (map + refusals ledger; predictions-only evidence) | `just physics v9_3.pdf` |
| Just-DDJ | correspondence (subject of translation) | `just ddj v9_3.pdf` |
| Change log | what was applied, and on whose authority | `v9_3 change log.pdf` |

**v9.3 is PDF-only — there is no markdown.** Consequences, all of them practical:
`site_vocab_lint.py --chains` **cannot read it** (it defaults to v9.2); `git diff` against v9.2 does
not work; quoting requires `pdftotext -layout`. v9.2 remains the newest *machine-readable* set, so a
lint run is a statement about v9.2, not about current canon.

**There is no editorial record**, though every v9.3 document closes by referring to one. v8 had one.

Read the **change log first** — it is the most useful document in the set and is structured as
`A.` rulings applied · `B.` **eleven machine inferences explicitly submitted for adversarial read** ·
`C.` what was not done. See "Working with AI" below; `B` is where the risk sits.

v9.3 supersedes **v9.2**, and through it **v9**, **v7.7**, **v7.5** (which called itself "sealed" but
carried the seating contradiction) and **v7.6-candidate** (audited; seating refused); all are kept in
place as history. The reconciliation trail is in `rsm/audit/`.

**Cross-reference convention (from v9.2):** references name their item and give the number in
parentheses — **the name is authoritative.** This exists because v9's numbering drifted (four
references to a nonexistent "item 10"). Cite by name. v9.3 gives fresh cause: the change log cites
"structural §8" for the involution, and **§8 no longer exists as a number.**

## Status Tags — REMOVED IN v9.3

**v9.3 deleted the entire epistemic tag apparatus.** Across the four chains: 38 tag instances in v9.2,
**zero** in v9.3. Gone: `[derived]`, `[candidate]`, `[open]`, `[rendering]`, `[verified]`. Also struck:
the physics entry tags, the break-condition entrance rule, the banned sentence class, the evidential
posture, and the forbidden flows.

**Retained:** `::`, the strike list as a list, the implicit/explicit register distinction (§0), plain
prose for what is unsettled — and, in the DDJ chain, **`[G]` / `[R]`** (Guodian-attested vs
received-text/Mawangdui). The manuscript stratum tags survived; the epistemic ones did not.

This removal is **change-log section B item 7 — a machine inference, not a ruling of Will's, and
reversible.** Weigh it accordingly. The cost is concrete and compounding: when `[unaudited]` was
retired in v9.2 the note here was that it had been *the only tag recording who owed what*. v9.3
removes the rest of that machinery. **Epistemic standing must now be read out of prose, per claim,
with nothing marking it** — and the change log's section B is a one-time list, not a per-claim marker.
Prior CLAUDE.md guidance to "check status tags" no longer has anything to check.

## The two tests — REMOVED IN v9.3

v9.2's structural §8 was "The two tests." v9.3 replaces it with an **unnumbered** section, *"Words that
assert what the framework denies"* — described in the chain as **"a standing list, not a procedure."**

- **The grammar test survives as that list**: agentive verbs for structural facts; transfer-language
  for non-events; removal narratives for constitutive exclusions; staging conjunctions for simultaneous
  constitution; reified infinities; occupancy language for the loci; address-language for constitution;
  "negative" for a conjugate; **any noun that turns a paradox into a place**.
- **The chart test survives only as §6's "Rendering guard"**: *a drawing shows a smooth curve through
  an unproblematic point; the implicit facts have no rendering; the drawing's verdict never overwrites
  the logic's.* It is no longer a named test applied before entry.

The change log struck both as "invented tests" (section B item 7, machine inference). **Keep applying
them anyway** — they are how perpendicularity, straightness-as-driver, ambient space for the sphere,
and the sign on a mode were each caught. Their removal is exactly the kind of judgment `B` exists to
have audited.

## §0 — The two registers (new in v9.3)

v9.3 opens the spine with a division that is **decidable before any result arrives**:

- **Implicit** — what follows from P1, P2 and the frame Definition with **no measurement, no units, no
  drawing**. X and Y are not names; they are the slots two conjugate modes occupy.
- **Explicit** — anything requiring a rendering to state: coordinates, a metric, a sign convention, a
  quantity, an instance. **Physics, biology, and any named pair (有/無, up/down) live here.**

"The implicit register fixes the structure; it fixes no parameters. Two systems can instantiate one
structure and differ in every number. It follows that **no quantity is ever owed by this chain, and no
quantity ever confirms it.**"

The chain states this is not a defence built after the fact: *a claim is implicit only if it can be
derived without a chart; anything else is explicit whether it succeeds or fails.*

This is the single most load-bearing addition in v9.3 and it heads every chain. It also absorbs part of
what the removed tag system used to carry — but only the implicit/explicit axis, not epistemic standing.

## Premises (v9.3)

**P1 — the Conditional** (definitional: vast + divisible) · **P2 — the Bridge** (what obtains is
distinguishable) · **Definition (frame)**: a frame is the coinherence of one distinction — two
conjugate modes, their reciprocal relation, their balance, and their origin, arriving together or not
at all; **one constitutive pair per frame** · **Corollary**: every distinction constitutes a frame, so
distinction beneath a frame's unit is *another frame*, not a smaller item within this one.

That is the whole premise set (unchanged from v9). Everything else is what P1 and P2 jointly require;
where a further assumption operates, v9.3 names it in the open items.

**The ground runs through P2 alone.** §2: P₀ cannot obtain, nor can indistinction on its own — it is one
side of the master pair, and by P2 what is not distinguishable does not obtain. **P1 is the Conditional
and asserts no existence.** The change log's review pass is explicit that P1 does no work at this step;
a conditional is not refuted by its antecedent failing.

**What changed from v9.2 — the register split, and the guards removed:**

1. **§0 added** (above). §5 renamed "The two centers, **and the line between them**."
2. **Pₙ re-typed: "met at resolution" → does not obtain.** v9.2 said *"Met at resolution; no exactness
   anywhere; no origin here."* v9.3 §5: *"Pₙ does not obtain, for the reason B does not. What frame n has
   instead is a **resolution limit**: at frame n's resolution the two amounts are not distinguishable
   near Pₙ. That is a fact about the frame's **discrimination**, not about a locus being reached."*
   Change-log section A records "met at resolution" as struck — **a ruling of Will's, not an inference.**
3. **Bₙ is the whole line** `Xₙ = Yₙ`, reaching from Oₙ outward through the gradient's paradoxical
   center; **no point of B obtains** along its entire length. Pₙ is the crossing, not a segment endpoint.
4. **"The joint" struck** as a surplus noun (10 mentions → 1): Pₙ is a paradox, not a place. "The
   reciprocity joint" is now **the reciprocity requirement**.
5. **The tag apparatus and the two tests removed** — see the two sections above. Both are section-B
   machine inferences.
6. **The DDJ etymology guard removed** — and note the whiplash: v9.2 *added* it; v9.3 deletes it on the
   grounds that *"it banned the project's own method — radical-level analysis is the project's primary
   instrument, and a rule against reading structure off graphs bans the method."* The 萬 case is re-scoped
   as narrower than the rule made it. The 始/母 entry stands as written. Section B item 10.

**New results in v9.3:**
- **Disconnection** — since no point of B obtains, the X-dominant and Y-dominant regions have **no path
  between them**; they are *related* (each is the other under σ_B) but **not connected**. Holds in the
  modes' own magnitudes, with no sign convention. The change log calls this *"the largest single recovery
  in the set, and the line to attack first"* (section B item 2) — **it is an inference, not a ruling.**
- **Revolution, forced** — the relation between the two regions *must* be carried by revolution of Gₙ
  about Bₙ, not merely can be. Will ruled that rotation gives the recursion; **the necessity argument is
  the machine's** (section B item 3).
- **The parturition map** — `w = z²`, 2-to-1, the two preimages differing by ν: *one branch compared from
  the child's side*, an indexed comparison across a frame boundary.
- **The Amplitude Floor** `a ≥ √1ₙ` names the mode-expressible domain (carried from v9.2).
- **The Archimedean demonstration** — π bounded from both sides, occupied by neither; each polygon a
  frame, exact at its own resolution; the non-terminating expansion as deferred exactness.

**Open item counts are unchanged from v9.2: structural 4, math 8.** No open item closed in v9.3.

**What changed from v9 → v9.2 — the involution fork closed, and the bill paid:**

v9 carried it as structural open item 6 / math open item 9: is the mode-swap `σ_B` or the sign-flip `ν`
structural? **v9.2 rules `σ_B` structural, `ν` chart** (structural §8, three grounds: grammar, chart,
motion). The DDJ side contributes *resistance* — across every 非 token, **no token negates between
conjugate opposites**.

The ruling's cost was **collected, not pocketed** — v9 said in advance that if the sign is chart, the
binding-dependent results become rendering, and v9.2 re-tags every one: T2 and the two returns →
`[verified as computation; [rendering] as claim]`; both i² routes and the ν-centroid → `[rendering]`;
the complementarity floor `[derived]` → `[rendering]`; T1 keeps its topology but drops the binding
reading; physics **retires** charge conjugation; and the `1ₙ :: ℏ/2` flagship downgrades *itself*.
Open items: **structural 6 → 4, math 9 → 8.**

Two things to watch:
- **Open item 5 was dissolved, not closed.** "Priority and uniqueness of the first distinction" is gone;
  §2 now says *"at least one is what the impossibility gives. Nothing here counts the roots, and nothing
  here excludes more than one."* That withdraws the claim rather than answering it — the one drop not
  paid for by an argument. It did propagate consistently ("each obtained tree is rooted").
- **The involution's third ground is chart-stated.** *Motion* appeals to a swept rendering and to
  orientation, yet is presented as coequal with grammar and chart. Using a rendering fact as one of
  three *independent* grounds is the move the chart test exists to catch. Unmarked in the chain.

Also: the **Amplitude Floor** promoted to the name of the mode-expressible domain (`a ≥ √1ₙ`; the circle
as a complete object is `[rendering]`) · **"occupiable" finally gone** from §1, which had contradicted §5
since v9 · **"the two senses of smaller"** replaces "where the two infinities live" — **fineness**
(in-frame) vs **descent** (across-frame), so two relations stop sharing a word · **"generation has no
address"** (§6) · **"what a child shares with its parent"** (§7) · DDJ **etymology guard** (the 萬
scorpion-pictogram argument is *declined*, not used).

**What changed from v7.7 → v9 — three re-typings (still worth knowing):**
- **L1 became the Corollary.** v7.7's open item 1 — "no unframed distinction," *the single head of the
  audit*, carrying four loads — is now a corollary of the frame Definition and appears in no open-items
  list. The load did not vanish; it moved into a definition. Definitions are where audits don't look.
- **The measure is no longer derived.** v7.7 struck Postulate Q by forcing `Q_i` in four steps. v9
  re-typed the measure as **definitional-by-register** and stated the non-quadratic candidate in the
  open; v9.2 keeps it `[open]` and adds that the register the measure is defined on is *itself*
  `[rendering]` as a complete object — **the measure is doubly downstream of the skeleton.** So
  **"orthogonal" is a rendering fact** — the skeleton says *independent*.
- **P₀ re-typed.** Not "absolute indistinguishability" (v7.7) but the **master pair
  (distinction/indistinction) at equality and cancellation** — explicitly *not* indistinction, which is
  only one side. Faces: `|0|` collapse-via-emptiness, `|1|` collapse-via-fullness.

Earlier dissolutions still stand as history: Postulate F, Postulate R, Frame-Universality, Postulate Q,
Lemma L2. The reconciliation trail is in `rsm/audit/`.

## The two centers, and the line between them (v9.3)

Naming: **Oₙ** = the co-vanishing locus · **Bₙ** = the balance line · **Pₙ** = the balance paradox ·
**P₀** = the total paradox :: 玄牝. `Pₙ` and `P₀` are **one species at two scopes**; the difference is
what survives the collapse — at Pₙ the frame obtains elsewhere, at P₀ there is no elsewhere.

- **O = the co-vanishing locus.** Where both modes would reach operational absence together; nothing on
  the curve approaches it. The curve bends *around* O — "no through, only around" describes the curve,
  it is not an added rule.
- **B = the balance line** — the *whole* locus `Xₙ = Yₙ`, from Oₙ outward through the paradoxical center.
  **No point of B obtains**: at any point of B the two modes stand in no proportion, so nothing
  distinguishes them, and by P2 the condition does not obtain. **B is a limit locus along its whole
  length** — approached, never occupied.
- **P = the balance paradox**, where the gradient meets B. The center the curve *has*, as against O which
  it bends around and never reaches; its one point fixed by the mode-swap. **Pₙ does not obtain**, for the
  reason B does not. What frame n has instead is a **resolution limit**: at frame n's resolution the two
  amounts are not distinguishable near Pₙ — a fact about the frame's **discrimination**, not about a locus
  being reached. Beneath the floor the difference is there and the frame cannot state it.

**v9.3 changed this typing.** v9.2 said balance-at-resolution *obtains*; v9.3 says it does not, and
substitutes indiscriminability. Do not carry "met at resolution" forward — it was struck by ruling.
Occupancy language does not type these loci at all (`Cₙ`/`Sₙ±` was retired for calling `Gₙ ∩ Bₙ`
"occupiable" — the seating error).

**Three discipline notes that still bite:**
- **The modes are magnitudes, not signed quantities.** The conjugate of a mode is another mode, not its
  negative; a mode is *incoherent* without its contrasting mode, and a sign is an **indexed comparison**
  whose implication varies with the reference chosen. **v9.2 settled this** (it was math open item 9):
  the **mode-swap `σ_B` is structural, the sign-flip `ν` is explicit** — v9.3 restates it in §0 terms,
  "sign therefore belongs to the explicit register throughout," and gives the motion argument: a
  half-turn about B sends X→Y, whereas componentwise negation reverses orientation and is no rotation at
  all. So both i² routes, the ν-centroid, the minimal traversal and the complementarity floor are
  rendering results, and the audit scripts — which compute in a signed chart — yield `[PASS]`es that are
  rendering facts **outright**, not pending a ruling. That is a *stronger* caveat than v9's. The one debt
  left open: the measured 2π phase of spin-½ (neutron interferometry) is owed an account. v9.3 physics §6
  now records **two candidate accounts** — the parturition map's two preimages, and orientation-space
  double-connectedness recovered from the earlier corpus — noting they *rhyme rather than compete*, and
  enters them **as shapes an account would take, not as claims.**
- Two things are written `1ₙ` and are **different quantities**: the conserved product `Q_j = XₙYₙ`, and
  `Q_i` = the squared distance from `Oₙ`. Two slices of one law; they agree only at the seats.
- Cross-frame **magnitude comparison is undefined**. "Sub-1ₙ" is unit-relative typing, not size — the
  child is not smaller; it is the approach that does not finish.

Run `python3 rsm/audit/checks.py` and `python3 rsm/audit/cross_model_checks.py`.

## Open Items (v9.3)

Cite these **by name**, not by number — the convention exists because v9's numbering drifted, and v9.3
has already produced a dangling "§8" reference.

**Structural chain (4) — unchanged in count and content from v9.2:**
1. **The open closures** — the **reciprocity requirement's** native-magnitudes step ("the joint" was
   struck in v9.3); anchoring-by-constitution; the ground's self-sufficiency candidate.
2. **Cross-frame unit relation** `1ₙ ↔ 1₍ₙ₊₁₎` — whether any *quantitative* relation accompanies the
   constitutive share of §7. An explicit-register question. Not needed for size comparison, which is not
   defined.
3. **Dimension count** — revolution about B requires a direction the plane lacks (§6); how many the
   structure requires is unsettled. **v9.3 gives "at least three" a route**: with no orientation
   privileged, the arcs over the center sweep a sphere, and a sphere needs three dimensions while
   requiring no fourth. **"Exactly three" remains open** — that nothing *requires* a fourth is not yet
   that nothing *can use* one. Two rival derivations, unadjudicated.
4. **Branching beyond the balance** — candidate, unruled: it cannot, since the frame has one constitutive
   pair and any conjugate equality reduces to the same balance. The step needing adversarial read is
   whether *derivative pairings* qualify.

**Math chain (8):** the open closures · cross-frame unit relation · dimension three · cross-frame
expression · **Definition T (traversal)** — v9.3 flags it as needing restatement in the
mode-expressible domain, where the disconnection now lives; **not attempted** (change log C) · the
tree-question · branching beyond Pₙ · quantitative complementarity.

**Nothing closed in v9.3.** Change log section C names four things explicitly not done: the Ch. 40
Mawangdui facsimiles (blocking the *dating* only — **Will's errand**), branching beyond Pₙ, dimension
three, and Definition T.

**Closed in v9.2:** the involution (structural 6 / math 9) — ruled. **Dissolved in v9.2:** priority and
uniqueness of the first distinction (structural 5) — the claim was withdrawn, not answered. v9.3 §2
carries the withdrawal forward verbatim: *"at least one is what the impossibility gives. Nothing here
counts the roots, and nothing here excludes more than one."*

**DDJ checksums (6):** 反/復 · 恆/常 · 生/成 · 亡/無 · 溺 · the Mawangdui facsimiles (the one outstanding
errand behind a scored result; it blocks only the *dating* of the Ch. 40 emendation).

**Physics open exposures:** the s-orbital strain · the two arrows · the Bekenstein sort · the Planck floor
(the closest thing to a falsifier-shaped exposure) · the spin-½ 2π phase, owed an account.

## DDJ Correspondences

The DDJ chain is the source of record — it carries the correspondences with `[G]`/`[R]` stratum tags,
the checksum doctrine, and the open checksum items. See `rsm/canonical/chains/v9.3/just ddj v9_3.pdf`
(v9.2's markdown remains the grep-able copy). **`[G]`/`[R]` survived v9.3's tag purge** — the
manuscript stratum tags are still in force even though the epistemic tags are gone.
Anchors: `玄 :: Pₙ`, `玄牝 :: P₀`, `有 × 無 = 1ₙ`, `弗居 ::` the origin-denial (the strongest `[G]`
match), `非 ::` the divergence of two registers around a shared invariant.

**New in v9.3 — the opening as a register declaration.** 可 and 恆 *are* §0's explicit and implicit
registers: 恆 is what holds frame-independently and parameter-free; 可 is anything framed, indexed,
instantiated. 道可道非常道 declares this and nothing else — "here is how the logic works even if you
don't apply it to anything real." That licenses the chains' notation: 有 and 無 are **names** (可名, an
indexed instance); X and Y are the **slots** the two modes occupy. Ch. 1 is `[R]` — absent from the
strips — and the chain marks as a **candidate** the reading that it was prepended as a scope note once
readers had begun taking the 可 for the 常.

**玄 is paradox; 牝 is generative; 玄牝 is the generative paradox.** The compound is **compositional** —
that is what makes the `P₀` assignment motivated rather than brute — so **"generative" must not be folded
into 玄**, or 玄牝 reads as generative-generative and the argument dissolves. Site copy that glossed `Pₙ`
as "the generative crossing" was corrected 2026-07-29 to **the paradoxical center**, and
`site_vocab_lint.py` now enforces it. `Pₙ` *is* generative structurally (parturition-生); the ruling is
about which character carries the sense.

**The three generative forms, never conflated:** entailment-生 (the ground, `P₀ : O₁`) ≠ parturition-生
(`Pₙ → Pₙ, O₍ₙ₊₁₎`) ≠ 相生 (mutual constitution within the frame).

The DDJ is typed as **subject of translation, generatively upstream of the framework** — the author
built the framework through the text, so agreement between them carries **no public evidential
weight**. What the text *can* supply is **resistance**: manuscript readings that refuse a
correspondence, and preregistered tests scored against the strips.

**The instrument's traffic rules** (v9.2, still in force): text→math at the *notation* layer and
math→commentary at the *reading* layer are legitimate. Text→math at the *premise* layer and math→text at
the *attestation* layer are **forbidden** — no character enters a derivation; no structure overrides the
strips. v9.3 states the same rule as "one discipline throughout."

**The etymology guard — added in v9.2, REMOVED in v9.3.** The guard barred inferring a pre-attested
sense from a graph's picture. v9.3 deletes it on the grounds that **it banned the project's own method**:
radical-level analysis is the primary instrument, and a rule against reading structure off graphs bans
that. The 萬 case is re-scoped as narrower than the rule made it — *the graph belongs to a different word
than the number.* The 始/母 entry stands as written (with the separate philological note that 母 is a
modified 女 graph rather than 女-plus-determinative). **Section B item 10 — a machine inference.** What
the guard was protecting against has not gone away: there is still no witness for a reconstructed stage.

## Reference Locations

- **Layer separation policy**: `rsm/layer_separation_policy.md` — standing governance. Three
  layers: canonical chains (assertions + live standing only), editorial/staging (corrected text
  stands clean), tracking (`rsm/audit/`, `reports/` — all change-history). The test: does a
  caveat describe the claim's *standing* (content) or its *history* (tracking)? Applies to every
  filing pass; a filing agent may move history out of content unprompted but may never rule,
  promote, or resolve.

- **Current chains**: `rsm/canonical/chains/v9.5/` — **markdown, canonical** (has a
  `README.md`). The v9.3 set (`rsm/canonical/chains/v9.3/`, PDF + `transcription_2026-08/`
  markdown) is superseded and kept as history; read its change log for the v9.3 rulings.
- **Older machine-readable chains**: `rsm/canonical/chains/v9.2/` (markdown + PDF; has a `README.md`).
  Use for grep, diff and lint; remember it is **one version behind canon** on the register split, the Pₙ
  typing, the tag system and the two tests.
- **Audit / reconciliation trail**: `rsm/audit/` — `divergence_ledger_r1.md` (the active AI-error
  filter), `math_chain_walkthrough_ledger_r1.md` (Will's rulings, through supplement r7),
  `checks.py` (re-runnable geometry), `cross_model_checks.py` + `cross_model_findings_r1.md`
  (v7.5's own theorems checked; v7.7 r4's appendix re-verified from scratch),
  `v9_comparison_r1.md` (v9 against the prior audit; the transcription fidelity record), plus the
  resolved v7.5→v7.7 reconciliation notes.
  **Note:** `cross_model_checks.py`'s cross-reference block is deliberately still pinned to **v9** — it
  is a *finding* about v9's numbering drift, and repointing it would delete the finding.
- **Superseded chains**: `rsm/canonical/chains/v9/`, `v7.7/`, `v7.6-candidate/`, `v7.5/` (kept as history)
- **Earlier development chains**: `rsm/canonical/chains/v7.3-development/`
- **Structured data**: `data/rsm/v7.5/` · **Research archive**: `research/archive/`
- **Consolidated iCloud archive**: `archive/` (text, tracked) + `archive/INVENTORY.md` and
  `archive/MANIFEST.csv`. Binaries live in the gitignored `research/archive/icloud_import/`.
  Unresolved there: **`RSM v9.4` is stamped `9.4.25` throughout and probably means Sept 4 2025**, which
  would place it *before* v9.1–v9.3 rather than after. Do not treat it as a later version.

## Working with RSM Content

1. **v9.52 is the current working set** (markdown canonical at `rsm/canonical/chains/v9.5/`) —
   supersedes v9.3/v9.2/v9/v7.7/v7.6c/v7.5. It is **not sealed**; the open closures are open
   item 1 in both chains. Don't treat it as finished.
2. **Sort every claim by register first** (§0): implicit if it can be derived with no measurement, no
   units and no drawing; explicit otherwise, **whether it succeeds or fails.** Physics, biology and any
   named pair are explicit. No quantity is owed by the chains, and no quantity confirms them.
3. **There are no status tags any more.** v9.3 removed them; standing must be read out of prose. Do not
   invent tags, and do not assume an untagged claim is `[derived]` — the tags' absence is a *loss of
   information*, not a promotion. `[G]`/`[R]` still apply in the DDJ chain: don't treat `[R]` as `[G]`.
   When standing is unclear, the change log's sections A (Will's rulings) and B (machine inferences) are
   the best available discriminator.
4. **Keep applying the chart test and the grammar test** even though v9.3 struck them as named tests.
   Perpendicularity and the sign on a mode already failed the chart test. **Cite open items by name, not
   number** — "§8" is now a dangling reference.
5. **Use `::` discipline** — never equate across registers; the structural chain is the spine, the
   renderings do not cite each other. **Physics entries still carry "Where it would fail" throughout,
   even though v9.3 removed the break-condition *entrance rule*** — keep writing them.
6. **The conditional is load-bearing** — everything traces to P1 (infinite: vast + divisible) — **but
   note where it does no work:** the ground (§2) runs through **P2 alone**, because P1 asserts no
   existence.

## Working with AI on this framework

The characteristic failure mode is **find a matching set, declare an identity** — false closure,
especially where an open item wants closing. The `signature_forcing` seating error and the Gemini
image-9 error are both instances. Guards:

- **Read the v9.3 change log's section B first.** It lists **eleven machine inferences the drafting
  model explicitly submitted for adversarial read** — including the disconnection theorem (which it
  names as "the line to attack first"), revolution-as-forced, the ring derived rather than postulated,
  the P₀/Pₙ differentiator rewrite, the removal of the tag apparatus and both tests, and the removal of
  the DDJ etymology guard. **None of these are Will's rulings.** Section A is. Section C is what was not
  done. Until B is audited, treat its contents as `[candidate]` in the old vocabulary — the vocabulary
  v9.3 no longer provides.
- **Verify geometry against `rsm/audit/checks.py` and `rsm/audit/cross_model_checks.py`** — both exit
  non-zero on a false claim. Both compute in a **signed chart**, and the sign-flip was settled as
  explicit in v9.2 (restated in v9.3's §0 terms): a `[PASS]` there is a rendering fact **outright**, not
  one pending adjudication. The caveat got stronger, not weaker — nothing in those scripts can be
  promoted later by a ruling that has already been made.
- **`site_vocab_lint.py --chains` cannot read v9.3, and cannot be repointed at it.** The script globs
  `.md`; v9.3 is PDF-only. Its `CURRENT_CHAINS` is **`v9`** in the committed script (`v9.2` in the
  pending audit-branch changes) — either way a run reports on a **superseded** set, and its authority
  strings still cite `structural_v9.md`. It is lexicon-only and explicitly not a ruling. **And do not
  mistake a clean run for clean text:** it ran clean on `src/` while the site glossed 玄 as "the
  generative crossing" in eight places and `chapter-01.md` contradicted itself within one file. A lexicon
  guard catches only what someone thought to write down. Note its "occupancy vocabulary" rule now lags
  canon in a second way: v9.3 struck "met at resolution," so the *authority* it cites has moved.
- **Quote v9.3 via `pdftotext -layout`, never from memory.** There is no markdown, so ordinary
  grep/diff workflows silently fall back to v9.2 and you will cite superseded text — the Pₙ typing and
  the tag system both changed.
- **Divergences between AI instances are the data; convergences are priced near zero** (shared corpora).
  Log rejected proposals in `rsm/audit/divergence_ledger_r1.md` per its standing protocol.
- **The unflagged false closure is the harder case** (ledger Entry 003). The seating error flagged
  itself `[commitment]` and was caught; v7.5's Lemma 4.4 carried no flag, read as rigorous, and was
  arithmetically false. **Careful hedging on one axis reads as rigor on all axes.**
- **Watch for silent replacement.** When a revision drops a prior draft's load-bearing lemma without
  refuting it, check the prior lemma before pricing the swap as a retreat. This has now happened twice
  (v7.5→v7.7 on the conservation cost; v7.7→v9 on the measure derivation). **v9→v9.2 is the
  counter-example worth studying:** v9 stated in advance what closing the involution fork would cost, and
  v9.2 paid it in full — six re-tags, a retired physics entry, a self-downgraded flagship. Read a version
  bump by checking whether the prior draft's *stated* contingencies actually fired.
- **A dropped open item is not the same as a closed one.** v9.2 closed the involution by *argument* and
  dissolved "priority and uniqueness of the first distinction" by *withdrawing the claim*. Both leave the
  list shorter. Only one is an answer. **v9.3 closed nothing** — its list is the same length as v9.2's.
- **Watch for guards removed rather than claims added.** v9.3's most consequential edits are *deletions*:
  the tag apparatus, both tests, the break-condition entrance rule, the DDJ etymology guard — one of
  which (etymology) v9.2 had *added* one version earlier. Each was argued, and the etymology argument in
  particular is a good one. But a version that removes four guards and closes no open items has made the
  framework easier to write in and harder to audit, and **every one of those removals is a machine
  inference in section B, not a ruling.** Removing a check is a claim that the check was wrong; price it
  like any other claim.
- **Arithmetic → scripts; ontology, referents, and readings → Will.** Do not ask Will to rule a
  computation, and do not record a preference as a derivation.
