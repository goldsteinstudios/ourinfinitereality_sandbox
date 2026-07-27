# v9 against the prior audit

**Date:** 2026-07-27 · **Status:** audit record, not a chain. Nothing here enters canon.
**Re-runnable:** `python3 rsm/audit/cross_model_checks.py` (111 checks, Part C is v9) ·
`python3 rsm/audit/site_vocab_lint.py --chains`

v9 arrived as four PDFs dated 2026-07-25, after the v7.5/v7.7 audit
(`cross_model_findings_r1.md`) was already written. This document does three things: records how
that audit's findings fare against v9, reports what is new, and records the transcription's fidelity
so the `.md` in `rsm/canonical/chains/v9/` can be disbelieved and re-checked.

**Headline:** v9 resolves four of the five prior findings — one of them by going *further* than v7.7
did. The fifth transfers to v9 unchanged. Four new items turned up, all concrete; one of them shows
a rule the framework has stated since v7.7 has never actually been enforced in the chains.

---

## 1. The prior audit's five findings, against v9

| Finding | Fate in v9 |
|---|---|
| §1 — v7.5's Lemma 4.4 (the conservation-cost argument) is arithmetically false | **Not carried.** The apparatus is gone entirely. |
| §2 — v7.5's Thm 6.1 silently restricts to quadratic forms | **Stated in the open.** v9 names the non-quadratic candidate. |
| §3 — the all-directions lemma's stated reason is borderline | **Moot.** v9 dropped the four-step derivation. |
| §4 — appendix chart hygiene (items 5 vs 23 both write `z`) | **Appendix gone**; a sharper related issue replaces it (§3 below). |
| **§5 — the physics "excised point"** | **Still live, verbatim.** |

**On §1 and §3 — v9 went further than the audit asked.** The prior audit showed Lemma 4.4 was false
and that v7.7's Definition T was therefore a *forced* repair, not a retreat. v9 does not merely keep
Definition T; it re-types the measure itself as **definitional-by-register**, tags it `[unaudited]`,
and states the Finsler obstruction plainly: *"a non-quadratic candidate satisfying the coarse
constraints exists and fails only the parallelogram condition."* The consequence is drawn out loud —
*"'orthogonal' is a rendering fact: the skeleton says independent, and perpendicularity enters with
the measure, downstream."* The founding observation (slope product −1 at the seat) is demoted in the
same breath to *"corroborating, never load-bearing."*

That is the strongest epistemic move in the version. It also means finding §3 evaporates: there is no
longer a step-4 argument to restate, because there is no longer a four-step argument.

**On §5 — the one that transfers.** v9's physics Refusals still read:

> the manifold-excision reading (the singularity as excised point: unmet origin, not early event) is
> its strongest general-relativistic face.

The correction is unchanged from the prior audit and was source-checked then: **standard GR has no
point to excise.** The singularity is not part of the manifold, is diagnosed by *geodesic
incompleteness*, boundary-attachment constructions (b-boundary and kin) are known to be pathological,
and in FLRW it is approached everywhere in space at once rather than at a location. Proposed
replacement, preserving the reading:

> the singularity is not a point of the manifold at all — an unmet limit diagnosed by geodesic
> incompleteness, not an excised location and not an early event

The correction *improves* the rendering. "Unmet limit, approached everywhere, never a location" is
closer to `Oₙ` — v9's own **co-vanishing locus**, "a locus, never a position; nothing stands there" —
than "excised point" ever was. The chain's typing was better than the physics word it borrowed.

**A second instance of the Entry 003 pattern.** v9 dropped v7.7 r4's four-step measure derivation
(*"Postulate Q struck… forced in four steps"*) **without refuting it** — the same silent replacement
the prior audit flagged for v7.5→v7.7. The proposed protocol addition is no longer an inference from
one case. Logged as Divergence Ledger **Entry 004**.

---

## 2. Occupancy vocabulary: a rule stated but never enforced

`site_vocab_lint.py --chains` reports **four hits in v9**, and each of the two documents that carry
the assertive form also states the prohibition, a few paragraphs apart:

| Location | Text | Same document also says |
|---|---|---|
| `structural_v9.md:19` | "One pair at equality within a frame is a Pₙ — **occupiable at resolution**" | §5: "occupancy language does not type these loci" |
| `just_math_v9.md:7` | "Pₙ framed and load-borne (**occupiable at resolution**)" | Notation: "Occupancy language does not appear." |
| `just_ddj_v9.md:43` | "the turn along G around the **unoccupiable** center" | — |
| `just_physics_v9.md:29` | "Circulation organized around an **unoccupied** core" | (rendering register; carries its own constitutive guard on the same line) |

"Occupiable" is the retired `Cₙ`/`Sₙ±` word — the seating error's own vocabulary.

**But this is not a v9 slip.** Running the same lint against v7.7 returns **five hits**
(`just_ddj_v7.7_r3.md` ×3, `just_physics_v7.7_r1.md`, `structural_v7.7_r3.md`). So the rule
"occupancy vocabulary is struck as ill-typed," which `CLAUDE.md` has asserted since v7.7 and which
both chain sets restate in their own text, **has never been enforced in the chains themselves.** It
was enforced only on the public site, because that is the only place anything was checking.

Ranking the four v9 hits by strength: the two `occupiable at resolution` lines are the real ones —
same document, self-contradicting, and about the loci the rule governs. The DDJ hit is a
straightforward use of the struck word for `Oₙ`. The physics hit is the weakest: it describes a
*physical vortex core* in the rendering register and carries the constitutive guard ("nothing was
removed from the core; the exclusion is not historical") on the same line. It is reported rather than
exonerated because a lexicon guard that special-cases is a lexicon guard that drifts.

**Ruling requested.** Is `occupiable at resolution` the intended phrasing — i.e. has the ban been
narrowed to mean *only* "no occupancy talk about `Oₙ`/`P₀`," leaving `Pₙ` at frame resolution
describable that way? Or are these four lines slips? The lint will keep reporting them until told
otherwise; that is what it is for.

---

## 3. The parturition map lost the offset that made its own claim true

v9, math chain, tagged `[verified]`:

> **The parturition map.** w = z² carries the parent's orbit register to the child's: 2-to-1,
> ν-identified — the branch and its ν-image read as one structure in the child's register; **the seat
> maps to the child's origin.** O₍ₙ₊₁₎ reads Pₙ, as constitution, not site-selection.

Two separable claims, and they have different statuses (Part C, check C6):

- **The ν-identification is true and chart-independent.** `w(−z) = w(z)` for plain `z²`, verified.
- **"The seat maps to the child's origin" is false as a coordinate claim**, in either chart. Split
  chart (`z = a + ib`, the one the math chain declares): the seat is `z = √1ₙ`, so `w = 1ₙ`. Mode
  chart (`z = X + iY`): the seat is `1 + i`, so `w = 2i`. Neither is the origin. **Only v7.7 r4's
  form `w = z² − 2i·1ₙ` sends the seat to 0** — verified in the prior audit (B4) and again here.

So the `[verified]` tag now spans a **mixed claim**: one half is machine-checkable and holds, the
other is either false-as-coordinates or a *constitutional* claim — which is what the following
sentence suggests, since "O₍ₙ₊₁₎ **reads** Pₙ, as constitution, not site-selection" is precisely a
denial that a coordinate image is what is meant.

**Ruling requested.** Is "the seat maps to the child's origin" a coordinate statement (in which case
the `− 2i·1ₙ` offset should be restored) or a constitutional one (in which case it should not sit
under `[verified]`, which the chain defines as *machine-checked computation*)? This is a typing
question, not an arithmetic one; the arithmetic above is not in dispute.

---

## 4. Four stale cross-references to "math open item 10"

Counted from the transcribed chains, not asserted (Part C, C10):

| Document | Cites | Count |
|---|---|---|
| `just_math_v9.md` — open-items list | — | **9 entries** |
| `just_math_v9.md` | "item 10" | 3 |
| `structural_v9.md` | "math open item 10" | 1 |
| `just_ddj_v9.md` | "math open item **9**" | 2 |

All four "item 10" references mean the signed-register / involution fork, which **is** item 9. The
DDJ chain has the correct number, twice — so this reads as a renumbering that the DDJ chain caught up
with and the other two did not.

---

## 5. `1ₙ :: ℏ/2` breaks its own floor correspondence

v9 physics §1, tagged `[flagship]`, pairs:

- the complementarity floor `σ_a·σ_b ≥ 1ₙ/2`, saturated by the minimal traversal
- the uncertainty relation `Δx·Δp ≥ ℏ/2`, saturated by minimum-uncertainty states

and says they "share inequality-shape, saturation structure, and units." Match the two floors and the
proportion is one line: `1ₙ/2 ↔ ℏ/2`, therefore **`1ₙ :: ℏ`**. Under the header's own `1ₙ :: ℏ/2`, the
framework's floor would read `ℏ/4` — the factor of 2 is counted twice. v7.7's physics r1 had it right
("ℏ :: 1ₙ's physics face"). Wording, in the flagship entry.

---

## 6. Two structural observations (not errors)

**The audit head moved into a definition.** v7.7's open item 1 was **L1** — "no unframed distinction,"
called *the single head of the audit*, carrying four loads. In v9 it is the **Corollary** to the frame
Definition, and appears in no open-items list. The load did not vanish; it moved into a definition,
which is where audits do not look. Whether that is a real closure or a relabeling is Will's call —
but it should be a call, not a side effect of restructuring.

**The signed register re-types much of the verified geometry.** v9 rules that "the modes are
magnitudes, not signed quantities… the sign belongs to the chart," and its own **chart test** lists
*perpendicularity, straightness-as-driver, ambient space for the sphere, and the sign on a mode* as
having **already failed** — facts about a presentation. Math open item 9 draws the consequence: if the
sign is chart residue, then "both i² routes, orbit-necessity, the minimal traversal, the ν-centroid
instances" are **rendering**.

Both audit scripts compute in a signed chart throughout. Their arithmetic is untouched; what a `[PASS]`
*means* is not. Headers in `checks.py` and `cross_model_checks.py` now say so. One specific instance:
`checks.py` §7 (isotropy → S² → ℝ³, recorded as "Will's observation") is exactly v9's "ambient space
for the sphere" chart-test item, and v9's dimension count is structural open item 3, unadjudicated.

---

## 7. Transcription fidelity record

The `.md` files in `rsm/canonical/chains/v9/` were produced from the four PDFs with `pdftotext -enc
UTF-8 -nopgbrk`, then repaired and verified. **The repairs matter — one of them was a silently dropped
character.**

| Class | Found | Repair |
|---|---|---|
| **Dropped glyph** | `ℏ` failed to extract in **all** modes — 3 occurrences in the physics chain, leaving `1ₙ :: /2`, `Δx·Δp ≥ /2`, `e^{iS/ }` | Restored from the page images |
| **Wrong CJK codepoints** | 66 characters in the DDJ chain encoded as Kangxi/CJK *radicals* (e.g. 生 as U+2F63, 玄 as U+2F5E) — visually identical, but they break every search and grep | Targeted NFKC on the radical ranges only (a global NFKC would have destroyed the subscripts) |
| **Wrong codepoint, Latin** | RG scale written with the micro sign `µ` (U+00B5) rather than Greek `μ` (U+03BC) | Corrected |
| **Line-break hyphens dropped** | 14, e.g. `ontologicallogical`, `windingmeasure`, `measurementdependence`, `2-to1`, `return-ofplace`, `νidentification` | Restored |

**Verification:** word-sequence diff against the extracted text (similarity 0.992–0.998; every
remaining difference is either the repo's straight-quote convention or one of the repairs above) and
**CJK character-multiset equality** — 359 characters in the DDJ chain, exact match. Quote and
apostrophe style follows the repo convention (straight), matching all v7.7 chain files.

Preserved deliberately: the fullwidth solidus `／` between Chinese phrases (v7.7 uses it too), and
`亙` in the 恆/常 checksum item (v7.7 and v9 agree on this glyph).

---

## Rulings requested

All ontology, typing, or wording. The arithmetic is settled and re-runnable.

1. **Occupancy vocabulary (§2)** — are the four v9 lines slips, or has the ban been narrowed to
   exclude `Pₙ`-at-resolution? Note v7.7 carries five of its own; the rule has never been enforced in
   chain text.
2. **The parturition map (§3)** — coordinate claim (restore the `− 2i·1ₙ` offset) or constitutional
   claim (drop the `[verified]` tag)?
3. **The stale "item 10" references (§4)** — the DDJ chain has the right number.
4. **`1ₙ :: ℏ/2` vs `1ₙ :: ℏ` (§5)** in the physics flagship.
5. **The "excised point" physics (§1, §5 of the prior audit)** — adopt the geodesic-incompleteness
   wording?
6. **L1 → Corollary (§6)** — ratify as a closure, or re-open as an item?

Nothing here is a ruling. Ontology, referents and readings are Will's.
