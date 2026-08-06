# Diff report — the equals-sign thread, distributed

**Date:** 2026-08-06 · **Base:** v9.52 · **Branch:** `research-archive` (uncommitted)
**Source:** Will's working note *"The equals sign, re-read"* — provisional, self-tagged as a reading.
**Instruction:** distribute into the existing essays (not a new essay); recover the Euler paper and
bring it current.

**Authority convention.** Every insertion below is labelled: **[NOTE]** = Will's note, carried in
substance · **[CANON]** = sourced to a v9.52 chain sentence, a ruling, or a register item ·
**[DRAFTED]** = mine, standing for Will's ruling. `checks.py` re-run: pass, exit 0.

**Nothing was ruled, closed, or promoted.** No existing claim was deleted; the one stale tag found
was flagged in place rather than altered.

---

## 1. Files touched

| File | Change | Net |
|---|---|---|
| `staging/editorial/series-02-on-the-center.md` | +1 paragraph | the which-center question |
| `staging/editorial/series-03-on-opposites.md` | +1 bracketed update, +1 paragraph | survey update; the 非 wings |
| `staging/editorial/series-08-on-names.md` | +2 paragraphs | the move named; the tier pricing |
| `staging/editorial/series-15-what-pi-names.md` | +2 paragraphs | the second throat; A-n14 with its breaker |
| `staging/editorial/paper-euler-single-operation.md` | **new** | recovered and rebuilt at v9.52 |
| `rsm/audit/register_update_2026-08-06.md` | **new** | A-n14, A-n15, B-n8…B-n11, C-n3, C-n4 |

---

## 2. Essay 8 — *On Names* (the move named)

**Placement rationale.** The seed was already there, twice: "Even the written form of the equals
sign obeys it: two strokes, and the gap between them load-bearing," and the essay's closing line,
"keep the gap in the equals sign." Essay 8 is the series' methodological center, which is also
where the tier pricing has to live.

- **[NOTE]** The move stated as one move worn three times (非 / ±1 / Euler), with the recognition
  that `X = Y` at the balance line was never an assertion of sameness.
- **[NOTE]** The open question left standing — whether *every* equals sign has been doing this —
  kept as a question about reading rather than arithmetic.
- **[NOTE]** The three tiers (resistance / attestation / reading) and the one-hand-two-mirrors
  pricing, stated in full. This is the paragraph that must survive any downstream trim: it is what
  stops the lens from accreting evidential weight.
- **[CANON]** "the identities are unchanged and true" — the note's own constraint, and consistent
  with the math chain's typing of the two returns to the rendering.

**Not done:** the essay's tracking line (`tracks RSM r13, math r7`) was left alone. See §7.

## 3. Essay 15 — *What Pi Names* (the second throat)

**Placement rationale.** Essay 15 *is* the curing room, by its own header — "everything here is
held at [observation] grade by ruling, and the essay's job is to show what disciplined not-yet looks
like." It already carried the Euler cluster at the corrected form and its own deflation label. The
second throat and the flagged candidate belong nowhere else.

- **[NOTE]** The winding reading: e^{i·0} vs e^{i·2π}, one value, a whole turn apart; the sign true
  and blind in the same instant.
- **[CANON]** Typed to the resolution floor and the vantage rule (structural §5, §2). Register
  **A-n4** supplies the arithmetic.
- **[NOTE]** A-n14 filed in place with its breaker, and with the note's own warning about wires
  welded between drafts carried in substance.
- **[DRAFTED]** The sentence tying the breaker to the two-returns entry's self-typing
  ("close to what the two-returns entry already concedes") — the connection is mine; the two-returns
  typing is the chain's.

**Deliberately not written:** the essay does not say the wire holds. It says the chains stop short
of it. That gap is the point of the entry.

## 4. Essay 3 — *On Opposites* (the 非 wings)

- **[CANON]** A bracketed update recording that the 非 survey has run, what it found (~6 tokens in
  five chapters; the non-copular uses rhetorical/purposive/class-negating/predicative; **no token
  negates between conjugate opposites**), and that the chain's landing is a *third* reading — 非 as
  the divergence of two registers around a shared invariant.
- **[DRAFTED]** The explicit statement that this refuses the cross-axis reading (which essay 3 never
  proposed) without by itself confirming the within-axis one, and that the `[candidate, pre-survey]`
  tag is stale until Will rules. Filed as register **B-n10**.
- **[NOTE]** The wings paragraph: 相背, two wings from a shared spine; not "is not" but *not the
  same, sharing an origin*; 可 on one wing, 恆 on the other.
- **[CANON]** The exposure stated in full: Shuowen is Han, ~8 centuries downstream; no witness for a
  reconstructed stage; the Guodian graphs unverified — errand **C7**. Filed as **B-n11**, and
  cross-referenced to the removed v9.2 etymology guard, whose standing caveat still applies.

**Note on the note.** Will's text reads the two wings as 可 / **恆** rather than 可 / 常. That is
the paleographically careful choice and it was preserved verbatim. It also sits against the DDJ
chain's own 恆/常 line, which the 2026-08-06 audit found overstated relative to the survey — see
`reports/chain_finalization_audit_2026-08-06.md` §1.2. No change made here; flagged for the DDJ
finalization pass (D2).

## 5. Essay 2 — *On the Center* (the which-center question)

**Placement rationale, and it is more than filing convenience.** Essay 2's second sentence already
says the two centers' difference "kept trying to deflate." The note's third option —
unoccupiability as such, O and Pₙ and the invariant as one fact — *is* that deflation, arriving in
new clothes. Putting the question anywhere else would lose that.

- **[NOTE]** The three candidate referents (O / Pₙ / unoccupiability as such), with the note's own
  accounting: available, not free.
- **[CANON]** "made against structural §5" — §5 is titled and structured around keeping the two
  centers apart.
- **[NOTE]** "choosing is the depth, not a formality," carried in substance.
- **[DRAFTED]** The framing that the attempt "arrives dressed as an insight rather than as an
  error." Filed as register **A-n15**.

## 6. The Euler paper — recovered and rebuilt

`staging/editorial/paper-euler-single-operation.md`.

**Recovery facts (all verified by `git log` / `git ls-tree`):** original at
`rsm/canonical/euler_single_operation.md`; last commit **2026-01-01** (`7473b0a`); removed from main
**2026-03-15** (`98154a2`); present on `docset-pipeline` and `claude/catch-up-UKmEu`, **absent from
`research-archive`**. Stamped "Tier 1 (Locked)". Register **A-n3 / A-n4 / A-n6** cite it as live and
A-n4 records an in-session patch on 2026-08-04 for which **no commit exists on any branch.** Filed
as **C-n3**.

**Corrections applied:** the single-instance form → the v9.52 pair (traversal
`e^{iπ} + e^{i·2π} = 0`, constitutional at θ = 0 retained beside it, PATCH 27); the general form
`e^{iθ} + e^{i(θ+π)} = 0` added, with "no single θ produces 0"; **A-n13** added (the conjugate-pair
polynomial, Euler as the family at θ = π, the pentagon at θ = π/5, the {−1,0,1} claim falsified in
place, the 五行 anachronism flag).

**Strikes, each with authority, tabled in the paper itself:** `玄 :: 0` (contradicts DDJ chain
玄 :: Pₙ) · per-constant assignments of e, i, π (physics' retired class; `i :: 名` is the retired
v7.5 form) · π as "quantum of polarity change" (measure-downstream; also asserts a minimum, which
P1's antecedent denies — recast to **A-n3**) · 無為/為 as pole-assignments **[DRAFTED]** ·
反者道之動 in received form (the strip reads **返** with the 也者…也 stamp) · the 有無相生 gloss
(held, **D1**) · the five-constants foil as celebration (struck by ruling, v9.52 README) ·
"Tier 1 (Locked)" (no such tier survives v9.3).

**Carried forward unchanged:** the single-operation insight itself, and §5's observation that no θ
produces 0 — the paper's real contribution, now stated in the general form the original never
reached.

**[DRAFTED] and reversible:** the path. Filed under `staging/editorial/` rather than restored to
`rsm/canonical/`, because it is an expository reading and `rsm/canonical/` holds chains. Putting a
tier-three document back in the chain directory is how the original came to be stamped "Locked."

---

## 7. Standing exposures this work did not fix

1. **Version skew.** All four essays track v7.7-era revisions (`RSM r13, math r7, physics r1+4,
   DDJ r6d`); canon is v9.52. The insertions are v9.52-correct, so each essay now carries two
   vintages. Tracking lines were **not** updated — doing so silently would assert a full-essay
   reconciliation that has not happened. The staging MANIFEST already records the skew.
2. **The 恆/常 conflict** (audit §1.2) is untouched and now has a second document leaning on it.
3. **Essay 3's stale tag** is flagged, not fixed — B-n10.
4. **C7** gates the first exhibit of the whole thread. Until the facsimiles are read, the 非 wing is
   illustration.
5. **The 2026-08-04 Euler patch text** is still unaccounted for. If it exists in a session record,
   it should be reconciled against the rebuild before either is trusted.

## 7a. Round two — adversarial read, 2026-08-06, and what it cost

The distribution above was reviewed in the project chat the same day. Four findings; all four
verified here before acting, all four accepted. Recorded because the pattern matters more than the
patch.

**H1 — the headline, and it was in the recovered document rather than the ephemeral note.** The
rebuilt Euler paper's §3 welded two different pairings: A-n13's polynomial z² − 2cos θ·z + 1 has
roots e^{±iθ}, the **conjugate** pair (product always +1), while the entire thread runs on the
**antipodal** pair (sum always 0). {+1, −1} has product −1 and so is in the conjugate family at no
θ; at θ = π that family degenerates to a double root at −1 with pair-sum **−2**, and no centroid
appears in it anywhere. The section was stamped **OFFERED / CHECKABLE** and had not been checked.
Withdrawn; a corrected §3 written in the soundness lane and installed after re-verifying every
arithmetic claim in it; failure record retained in place at §3-WITHDRAWN; divergence ledger
**Entry 006**. The rewrite caught a further inherited error the withdrawal had missed — "carries
both slices at once" is false of the pair-polynomial, and that phrasing originates in **A-n13
itself**, not in the drafting. A-n13 recorded **CORRECTED**, not held pending.

**H2 — the repair reached past the near object for the wrong far one.** The ±1 middle is the locus
**O**, and the integer 0 is the value the rendering writes there. The first draft said "what does
not obtain is what |0| notates" — but |0| is the empty face of **P₀**, beneath the register split,
and structural §5 exists to keep that apart from a frame's origin. If a P₀ face were ever wanted
for the −1/0/+1 line it would be the **sign-collapse** face, which is literally that line collapsed.
Corrected in the paper; **B-n9** rewritten. The sweep to wherever else the exhibit travels is owed.

**H3 — retrojection struck.** "The original paper already answered this question" is false: the
question was born in this session's thread. What stands is narrower and was narrowed twice — once
on review, once again here, since the original was never canon-chain material and so cannot
straightforwardly represent *the framework* wavering. **A-n15** rewritten.

**M4 — a universal negative downgraded, and both hashes confirmed real.** "No commit exists on any
branch" became "not found across the 13 refs in this clone," enumerated. `7473b0a72322…`
(2026-01-01, author `goldsteinstudios`) and `98154a2d7033…` (2026-03-15) both verified by
`git cat-file` / `git log`. **C-n3** rewritten.

**A second failure, self-reported, not in the review.** The Shuowen-is-Han guard was applied to the
非 material being inserted and not to the structurally identical 有/亡 hand/fled-thing claim two
lines above it in the same essay — the guard treated as a property of the edit rather than of the
page. Errand **C7** now gates both. Logged in Entry 006 because it is cheap to repeat and invisible
in a diff.

**One flag raised in the other direction.** The corrected §3 carries the register-marker strike as
"no equation is **恆**-register," citing a 2026-08-06 identity ruling. Installed as ruled and
flagged filing-side: no filed record of that ruling exists in this session, 恆/常 is held at **D2**,
and [M] is right for 恆 but must not propagate onto the Guodian layer, where Bundle A attests
**亙** and carries no 恆 and no readable 常. Filed as **B-n12**. This is the second document now
leaning on that fault line.

**The operating rule that fell out of both rounds, proposed for ruling.** Route what a Cowork
instance *distributes, recovers, files and tags* straight through — the bookkeeping held, the
promotion discipline held, nothing was welded into canon and nothing was closed. Route what it
*generates or repairs* — every CHECKABLE item, every object-identity call about which center or
which face — back through the soundness lane first. **The CHECKABLE tag is the handoff.** Note the
asymmetry the two rounds establish: the grammar guards (`::`, the strike list) caught nothing here,
because both failures were arithmetic and object-identity, not prose. Those guards do not cover the
soundness lane and should not be trusted to.

## 8. What would falsify the placement

If Will rules the lens is not book-level — that it is either chain-level (via A-n14 holding) or not
worth carrying — the distribution is wrong in a specific way: four essays would each carry a
fragment of something that should be one document, or nothing. The distribution was chosen on
instruction and is reversible; each insertion is a contiguous block bounded by existing text, and
`git diff` isolates all four.
