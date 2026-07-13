# Term ledger — the assignment problem

> **RESOLVED by v7.7 (2026-07-11).** The six strained terms now have fixed referents, ruled in Will's
> walkthrough and carried in `rsm/canonical/chains/v7.7/`:
> - *distinction* — one claim: the constitutive cut's magnitude = the frame's minimal unit; `Q_i`/`Q_j`
>   are the two real slices of one law `Q(z)=1ₙ` (structural chain §4–5; math r4 "one law, two slices").
> - *occupied* — struck: "occupied is ill-typed and does not appear"; the engine is `P` cannot be
>   *constituted as a frame*.
> - *met/unmet* — the core two-center typology (structural chain §5), stated bilingually.
> - the two `1ₙ` quantities — the slice identity.
> This document stands as the record of the assignment *problem* and how it was posed. It is an early,
> informal instance of the discipline now formalized in `divergence_ledger_r1.md`.

**Purpose.** The math chain cannot be rewritten until its strained words have fixed referents.
Drafting v8 over unfixed vocabulary reproduces the failure the audit found: r5's seating commitment
was one word (`mode`) doing three jobs — variable, axis, algebra element — with nobody having fixed
which.

**This document presents the problem. It does not solve it.** Every entry ends with a blank ruling
line. Nothing is marked resolved without Will's ruling recorded inline.

**Arithmetic lives in `checks.py`**, not here. Where an entry cites a computed fact, run
`python3 rsm/audit/checks.py` to see it derived, and to watch it fail if it is false.

---

## The test

For each strained term, try to fix **one** referent and check every sentence that uses it.

| Outcome | Diagnosis | Action |
|---|---|---|
| **A.** One assignment makes all sentences true | Ambiguity | Fix the referent. No paradox. |
| **B.** No single assignment works, but two *frame-indexed* assignments each do | Genuine inexpressibility | State bilingually (ledger E7). |
| **C.** Neither | Real contradiction | Log as an open gate. Do not patch. |

### Guard on R7

Ledger R7 says the framework predicts where its notation strains, so the correction history there is
"confirmation-shaped, not defect-shaped." **That claim can absorb any contradiction**, converting
every refusal into a confirmation — while parallax's own thesis is that the evidential unit is *a
register refusing its author*.

**R7 is earned only where row A has been shown to fail.** Everywhere else, "the language is straining"
and "we have not fixed our terms" are indistinguishable from the inside, and the second is likelier.

One worked example is already in hand. `Oₙ` "resists reference" (R7, S4) — and the reason turns out to
be ordinary: the angular coordinate is undefined at the origin, as it is at the north pole of any
globe. The strain had a cause. It did not need the meta-result.

---

## Term 1 — `distinction`

The load-bearing word, and the one on which three of my readings were refused.

**Occurrences**

| Location | Text |
|---|---|
| `v7.6c_r5.md:12` | "`1ₙ` is the frame's minimal unit of **distinction**, identical with the conserved product" |
| `v7.6c_r5.md:28` | "absolute in**distinguish**ability. What is not distinguishable does not obtain" |
| `v7.6c_r5.md:44` | "`0ₙ` (operational absence) and `1ₙ` (operational **distinction**)" |
| `v7.6c_r5.md:60` | "`1ₙ` is not imposed; it is the frame's minimal unit of **distinction**" |
| `v7.6c_r5.md:82` | "Postulate Q: any measure of sustained **distinction** is a quadratic form" |
| `v7.6c_r5.md:165` | "derive the sign-blindness of **distinction** magnitude" |
| `v7.5.md:55` | Prop. 3.2: "the differential weighting … vanishes as a **distinction**" |
| ledger C2 | "`Oₙ` … four-way **distinction** fails … `Pₙ` … **distinction** intact" |

**Candidate referents, and where each breaks**

| # | Referent | At `Pₙ` | At `Oₙ` | Verdict |
|---|---|---|---|---|
| 1 | conserved product `Q_j = X·Y` | `1ₙ` | `0` | Orientation-*dependent*: `Q_j` cannot be written without choosing `θ`. Cannot state a frame-independent distinction. |
| 2 | differential weighting `X − Y` | `0` | `0` | Fails to separate the two centers at all. But this is the quantity Prop. 3.2 actually invokes. |
| 3 | the measure `Q_i` (squared distance from `Oₙ`) | `1ₙ` | `0` | Orientation-invariant. Separates them. But it is a *metric* quantity, and the metric is derived downstream — possible circularity. |
| 4 | the four-way naming (C2's own phrase) | four names, distinct | the four coincide | Matches C2's wording. Formalized as freeness of the `⟨i⟩` action — **refused by Will**. |

**Will's ruling so far:** *"all `Pₙ` points are equidistant from `Oₙ`"* — a statement in `Q_i`,
not `Q_j`. And on the DDJ side: `此兩者同出而異名`, "these two emerge from the same source, and this is
what we call Distinction" — which makes distinction the **two-ness** (`異名`, the different-naming),
not a difference of values.

**Consequence if #2 is what Prop. 3.2 means.** Prop. 3.2's premise is sound (`X − Y = 0` at `Pₙ`) and
its conclusion is not: `X = Y = √1ₙ` does not drive `XY` toward `0`, so occupation of `Pₙ` does not
reduce the gradient to `P₀`. The proposition conflates referent #2 with referent #1.

**Bearing on O1.** "Minimal unit of distinction" reads as `Q_i` (the standoff, radius²). "The conserved
product" reads as `Q_j`. `checks.py §2` shows these are different quantities agreeing at exactly
`Gₙ ∩ Bₙ`. So `r5:12`'s "identical with" is **asserted, not argued**, and O1 is a real question with a
visible answer-shape: *two quantities, one coincidence, located at the seats.*

**Row:** likely **A** (ambiguity), pending the ruling.
**RULING:** _______________________________________________

---

## Term 2 — `occupied` / `non-occupiable`

**Occurrences**

| Location | Text |
|---|---|
| `v7.5.md:55` | "**Proposition 3.2 (`P` is unoccupiable)**" |
| `v7.6c_r5.md:18` | "`Pₙ` … **Occupied by the modes**; the site of generation" |
| `v7.6c_r5.md:66` | "## The origin as **unoccupiable** center" |
| `v7.6c_r5.md:70` | "`Oₙ` is required *as reference* and **unoccupiable** *as position*" |
| `v7.6c_r5.md:121` | aperture: "not sustainable as an **inhabited** state" |
| `v7.6c_r5.md:129` | "`Pₙ` … cannot **persist** as an inhabited terminal state" |
| `v7.6c_r5.md:163` | open item 1: "the **persistence** argument" |
| ledger R2 | strikes "occupied by the modes"; strikes *all* "cannot persist/dwell" |
| ledger E1 | "**`Pₙ`'s non-occupiability** is the single source of both rotation and recursion" |

**The problem.** R1 declares the skeleton implicit-register: no motion, duration, occupancy, or
"when." R2 accordingly strikes the whole family. **But E1's first sentence uses it.**

Either "non-occupiability" is a surviving term of art with an implicit-register meaning that does not
smuggle duration back in — in which case v8 owes it a definition — or E1 needs the re-wording R2
forces everywhere else, and its content survives as: *the incident pair at `Pₙ` is straight×curved, so
`Pₙ` cannot constitute a standing axis-pair.* One deficit, two discharges, no occupancy word.

**Row:** **A** if E1 is re-worded; **C** (a real internal contradiction in the ledger) if both stand.
**RULING:** _______________________________________________

---

## Term 3 — `met` / `unmet`

**Occurrences:** ledger C2, C3, C4.

**The problem.** C2 calls `Oₙ` an "unmet crossing" whose "arms approach asymptotically, never meet."
C4 types it `straight×straight`. Two crossing straight lines *do* meet — `xaxisₙ ∩ yaxisₙ = Oₙ` is a
genuine point. So "unmet" is unmet **by** something not yet named. The only candidate visible in the
text: `Pₙ ∈ Gₙ` (since `XY = 1ₙ` there) while `Oₙ ∉ Gₙ` (since `XY = 0`). On that reading, met/unmet
means *lies on the gradient, or does not*, and the "arms" are `Gₙ`'s, not the axes'.

**But C3 already gives this the bilingual form**: the same locus is *realized in the parent's
expression* and *unmet in the child's*. That is row **B** — the one case that looks genuinely
inexpressible in a single frame rather than merely unfixed. It behaves exactly like curvature, which
is frame-relative in the same way (ledger C4, and `parallax_v7.5.md:51`: "the parent's local ⊥ at `Pₙ`
becomes the child's global ⊥").

**Row:** **B**, probably. If so, v8 states it bilingually and no single sentence carries both halves.
**RULING:** _______________________________________________

---

## Term 4 — the glyph `1` (three roles)

Already named by ledger R5: **coordinate** (amplitude language), **magnitude** (measure language),
**phase-anchor** (orbit language), with `√` translating between the first two.

R5's house rule — *every equation declares its language* — should extend from equations to **terms**.

**Row:** **A**, and R5 already fixes it. Carried here so the checker can enforce it.
**RULING:** _______________________________________________

---

## Term 5 — `1ₙ` (two distinct quantities)

Distinct from Term 4. Not three roles of a glyph — **two different numbers**, both written `1ₙ`.

```
Q_j = a² − b² = X·Y    the conserved product; what j preserves
Q_i = a² + b²          what i preserves; the squared distance from Oₙ
```

They agree **only** where `b = 0`, i.e. exactly at `Gₙ ∩ Bₙ` (`checks.py §2`). `Q_i` is
orientation-invariant; `Q_j` requires a choice of `θ` before it can even be written.

Consequence: `Gₙ : XₙYₙ = 1ₙ` silently fixes `θ = 0`. **The chain's gradient is a chart choice wearing
the clothes of a definition.** Under T1's orientation-isotropy, no `θ` is preferred.

**Row:** **A**, and it *is* O1. Fixing this term answers node 5.
**RULING:** _______________________________________________

---

## Term 6 — `orbit` (two objects)

| Sense | What it is | Where |
|---|---|---|
| The minimal cycle | four **positions**: `1 → i → −1 → −i` | `v7.5.md:119`; `v7.6c_r5.md:109-115` |
| The circle | a **locus**: all points at `√1ₙ` from `Oₙ` | `v7.5.md:83`, `:89`, `:133-139` |

r5 itself keeps them apart in one sentence — *"Four algebraic elements, three structural positions;
**intermediates are path**"* (`:115`) — and then uses "the orbit" for both.

This is what caught my claim that "the orbit and the `Pₙ`-locus are the same set." Within one frame
`Bₙ` meets `Gₙ` at two points and the quarter-turn gives two more: **four**. The circle appears only
when sweeping orientations, and whether its non-cardinal points are actual `Pₙ` rather than candidates
is **open item 8**, not something the geometry settles.

**Row:** **A**.
**RULING:** _______________________________________________

---

## Notation collision to fix

`R3` denotes both a ledger ruling ("X/Y carry no interpretation in the skeleton") and the space `ℝ³`.
Given that this whole exercise concerns undeclared notation: rulings keep `R1..R7`; the space is
always written `ℝ³`.

---

## What the checker will enforce, once the rulings are in

1. Each term appears in the chain only under its ruled referent, with its language declared (R5).
2. No `[derived]` claim depends on an untagged premise.
3. `just_math_v8.md` contains no CJK characters, no physics vocabulary, no `::` — independence.
4. No occupancy vocabulary (`occupied`, `unoccupiable`, `persist`, `dwell`) survives in the skeleton,
   unless Term 2 is ruled a surviving term of art with a duration-free definition.
