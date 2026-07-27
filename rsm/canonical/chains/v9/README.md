# RSM v9 — the current working set

This is the **current working set** for the Recursive Structural Model. It supersedes v7.7 (and,
through it, v7.5 and v7.6-candidate, which remain in place as history). All four documents close
**"Not sealed."**

**Provenance.** Transcribed 2026-07-27 from the four PDFs dated 2026-07-25
(`rsm chain v9.pdf`, `rsm math chain v9.pdf`, `rsm physics chain v9.pdf`, `rsm ddj chain v9.pdf`).
`.md` is the version-controlled form; the PDF renders are not vendored. Transcription was verified
word-by-word and by CJK-character multiset against the source — see `rsm/audit/v9_comparison_r1.md`
for the fidelity record and the repairs made to PDF extraction artifacts.

## The four-document architecture

| File | Register | Role |
|---|---|---|
| `structural_v9.md` | logic only | The spine. Premises, the frame Definition and its Corollary, the two centers, the engine, recursion, the two tests. |
| `just_math_v9.md` | derivation | The explicit realization: coordinates, algebra, theorems. |
| `just_physics_v9.md` | rendering | A map plus a refusals ledger. **Every entry states a break-condition**; the predictions section is the only evidential one. |
| `just_ddj_v9.md` | correspondence | The Dao De Jing as **subject of translation**, generatively upstream of the framework — so agreement carries no public evidential weight. |

## Premises

- **P1 — the Conditional.** Reality is infinitely vast and infinitely divisible: no terminal
  resolution in either direction.
- **P2 — the Bridge.** What obtains is distinguishable.
- **Definition (frame).** A frame `Rₙ` is the coinherence of one distinction: two conjugate modes,
  their reciprocal relation, their balance, and their origin — arriving together or not at all. One
  constitutive pair per frame.
- **Corollary.** Every distinction constitutes a frame; distinction beneath a frame's unit is
  therefore another frame, not a smaller item within this one.

Everything else is what P1 and P2 jointly require. Where a further assumption operates, it is named
in the open items.

## Status tags (v9's own definitions — they mark epistemic standing, not history)

- **[derived]** — follows from the premises
- **[candidate]** — proposed, not forced
- **[open]** — named and unresolved
- **[unaudited]** — machine-closed, awaiting the author's adversarial read
- **[verified]** — machine-checked computation (math chain)
- **[G]** / **[R]** — Guodian-attested / received-text or Mawangdui only (DDJ chain)

## What changed from v7.7

- **L1 became the Corollary.** v7.7's open item 1 — "no unframed distinction," called *the single
  head of the audit* and carrying four loads — is in v9 a corollary of the frame Definition, and
  appears in no open-items list. The load did not vanish; it moved into the definition.
- **The measure is no longer derived.** v7.7 r4 struck Postulate Q by forcing `Q_i` in four steps.
  v9 re-types the measure as **definitional-by-register** and tags it `[unaudited]`; the
  non-quadratic candidate that "fails only the parallelogram condition" is stated in the open.
  Consequently **"orthogonal" is a rendering fact** — the skeleton says *independent*.
- **P₀ re-typed.** No longer "absolute indistinguishability" (v7.7) but the **master pair at
  equality and cancellation** — explicitly *not* indistinction, which is only one side.
- **The modes are magnitudes, not signed quantities.** The sign belongs to the chart. The structural
  status of the signed register is math open item 9 — see the guards below.
- **Two new tests** (structural §8): the **chart test** and the **grammar test**.
- **The engine restated**: the child frame is *the pursuit of exactness continuing below the floor*;
  recursion is exactness, permanently deferred.

## Guards for anyone (human or AI) working here

- **The chart test:** does the claim survive changing the drawing? Perpendicularity,
  straightness-as-driver, ambient space for the sphere, and the sign on a mode **each failed it** —
  each was a fact about a presentation, not about the structure.
- **The grammar test:** does the word's grammar assert what the framework denies? Agentive verbs for
  structural facts, transfer-language for non-events, removal narratives for constitutive exclusions,
  staging conjunctions for simultaneous constitution, reified infinities. Both failures look like
  clarity from the inside; that is why the tests are written down.
- **The characteristic AI failure mode is *find a matching set, declare an identity*.** See
  `../../../audit/divergence_ledger_r1.md` (the active filter). Its complement is equally live: a
  false closure that carries *no* flag and reads as rigorous (Entry 003).
- **Verify geometry against `../../../audit/checks.py` and `../../../audit/cross_model_checks.py`** —
  both exit non-zero on a false claim. **But note:** they compute in a *signed* chart, which v9 holds
  open (math item 9). A `[PASS]` there is a fact about the rendering, not necessarily about the
  structure.
- **Occupancy language does not type these loci.** Met/unmet are frame-reading statuses. Run
  `python3 rsm/audit/site_vocab_lint.py --chains` before relying on any chain text.

## Open items

**Structural (6):** the unaudited closures · the cross-frame unit relation `1ₙ ↔ 1₍ₙ₊₁₎` · dimension
count · branching beyond the balance · priority and uniqueness of the first distinction · the
involution.

**Math (9):** the unaudited closures · the cross-frame unit relation · dimension three · cross-frame
expression · Definition T · the tree-question · branching beyond seats · quantitative complementarity ·
**the signed register's structural status.**

> **Cross-reference note (unruled).** The math chain cites "open item 10" three times, and the
> structural chain cites "math open item 10" once, but the math open-items list has **nine** entries.
> The DDJ chain cites "math open item **9**" — which is the signed-register/involution item all four
> references mean. Flagged in `../../../audit/v9_comparison_r1.md`; not corrected here, because chain
> text is the author's.
