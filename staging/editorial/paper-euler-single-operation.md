# Euler's Identity as Structural Grammar

*Recovered and brought current. Editorial — a reading, not a chain. Not sealed.*

```
Provenance
──────────
Original:  rsm/canonical/euler_single_operation.md
           last commit 2026-01-01 (7473b0a, "RSM v0.993: Single-operation Euler identity"),
           removed from main 2026-03-15 (98154a2, "Slim main to Astro site build"),
           surviving only on branches docset-pipeline and claude/catch-up-UKmEu.
Status of the original: stamped "Tier 1 (Locked)". It was neither.
Rebuilt:   2026-08-06 against v9.52.
Authority: strikes and corrections below each cite a ruling, a chain sentence, or a
           register item. Anything citing neither is drafting, marked [DRAFTED] and
           standing for Will's ruling. Nothing here is a ruling.
Path note: filed under staging/editorial/ rather than restored to rsm/canonical/.
           This is an expository reading; rsm/canonical/ holds chains. The path change
           is itself [DRAFTED] and reversible.
```

**Register, stated first.** Everything in this paper is explicit-register. It runs in a signed chart, on the circle slice, which is explicit as a complete object; the center it discusses is named by a sign-symmetric sum, and ν — componentwise negation — is explicit by the v9.2 ruling restated in v9.3's §0 terms. No result here is owed by the implicit register and none confirms it.

---

## 1. The two readings the identity licenses

The identity is usually met in the form **e^{iπ} + 1 = 0**, where the 1 stands as an independent term added to e^{iπ}.

It is not independent. Write it as what it is — a value of the same operation — and the anatomy shows. But *which* value is not settled by the notation, and this is the correction the original paper missed: **the familiar +1 is ambiguous between e^{i·0} and e^{i·2π}**, which share a value and differ by a whole turn. The identity therefore decodes two ways, and the chains carry both:

| Reading | Form | What it says |
|---|---|---|
| **Traversal** | e^{iπ} + e^{i·2π} = 0 | out and back — the far pole and the returned position, summing to the center |
| **Constitutional** | e^{iπ} + e^{i·0} = 0 | the same pair without traversal; no journey is asserted |

The traversal form is the v9.52 correction (PATCH 27); the constitutional reading is retained beside it. The winding-ambiguity clause is the correction's stated reason and is itself register item **A-n4, OFFERED** — strikable, and marked as such in the v9.52 diff report.

*The original paper carried only the constitutional form and presented it as the reading.* That is the single-instance form A-n4 supersedes. Corrected here.

## 2. One operation, two angles — and the general form

There is one operation, e^{iθ}, evaluated at two angles a half-turn apart. Both poles come from it; neither needs an operation of its own.

The generalization is where the content actually sits, and it belongs in the paper rather than in a footnote:

**e^{iθ} + e^{i(θ+π)} = 0, for every θ.**

Every point and its half-turn partner sum to the center. **No single θ produces 0** — the center is not on the circle. It is named only as the sum of a conjugate pair of poles, which is the ν-centroid, and Euler's identity is that structure's most famous instance. The chart's way of saying that a symmetric whole names the locus none of its members occupies.

This is the paper's one durable result, and its deflation risk is on the record: *opposite points sum to zero* is also just what symmetric points do. Until someone shows the reading carries weight the symmetry alone does not, it stays where essay 15 files it.

## 3. Two pairings on the unit circle, kept distinct

Fix z = e^{iθ} on the unit circle. Two involutions pair z with a second point; they are not the same involution, and this section's whole burden is to keep them apart.

### 3.1 The two pairings

**Pairing A — antipodal (ν).** Partner −z = e^{i(θ+π)}.

- Sum: z + (−z) = **0**, identically, for every θ.
- Product: z·(−z) = −e^{2iθ} — modulus 1, and real-and-equal-to-+1 only at z = ±i.
- Monic polynomial with these roots: w² − e^{2iθ} = 0. In the real case {+1, −1} (θ = 0): w² − 1 = 0.
- The pairing is **keyed to a vanishing sum.** The locus it names — the sum, 0 — is the origin O, which is not on the circle. This is the ν-centroid of §2.

**Pairing B — conjugate (reflection across the real axis).** Partner z̄ = e^{−iθ}.

- Sum: z + z̄ = 2cos θ = 2a.
- Product: z·z̄ = 1 = Q_i, the circle-slice invariant.
- Monic polynomial with these roots: z² − 2cos θ·z + 1 = 0.
- The pairing is **keyed to a fixed product.** Its constant term is Q_i; its linear coefficient is the trace, −2a.

**Correction carried in place.** The prior §3 said this polynomial "carries both slices at once." It does not. Its constant term is the circle-slice invariant Q_i = 1; its trace is 2a, which is not a slice invariant. The two-slice object is the math chain's form Q(z) = 1ₙ, a different object; the "both slices" phrasing borrowed that language and does not apply to the pair-polynomial. Withdrawn.

### 3.2 The overlap is a single point

{z, −z} = {z, z̄} requires −z = z̄, i.e. cos θ = 0, i.e. **z = ±i**. At z = ±i both polynomials reduce to w² + 1. This one point is the entire overlap: everywhere else an antipodal pair and a conjugate pair are different pairs of points. The two families are keyed to different elementary symmetric functions — Pairing A to the sum (0), Pairing B to the product (+1) — and the elementary symmetric functions agree only where the pairs themselves agree, at ±i.

### 3.3 Euler is a Pairing-A fact, not a member of Pairing B

e^{iπ} + 1 = 0 is a statement that a **sum vanishes**: the pair {e^{iπ}, e^{i·0}} = {−1, +1}, roots of w² − 1 = 0, product −1, sum 0. It is Pairing A.

It is not in Pairing B, and the exclusion is exact: {−1, +1} has product −1, while every Pairing-B pair has product +1, so no value of θ places {−1, +1} in z² − 2cos θ·z + 1. The prior §3 located Euler at θ = π of Pairing B; at θ = π Pairing B degenerates to the double point −1 — (z + 1)² = z² + 2z + 1 — whose content is e^{iπ} = e^{−iπ} = −1, a distinct statement from the vanishing-sum identity. **Euler's identity therefore lives with the §2 centroid, in Pairing A.** This section from 3.4 onward is Pairing B throughout, and claims no membership overlap with Euler beyond the single point 3.2 identifies.

### 3.4 The pentagon is a Pairing-B recurrence, and it stands — CHECKABLE

At θ = π/5 the conjugate pair sums to 2cos(π/5) = φ. At θ = 2π/5 it sums to 2cos(2π/5) = 1/φ. The two pair-sums satisfy

- φ · (1/φ) = 1 — **product one**, and
- φ − 1/φ = 1 — **difference one**.

Product one and difference one is the φ-defining relation x − 1/x = 1 (equivalently x² − x − 1 = 0), which the corpus files as **A-n9**; here it recurs one level up, at the **pair-sums** rather than the pair-members. This is a genuine self-similar recurrence **internal to Pairing B**, and it is why five is distinguished rather than decorative. It is **not** a recurrence shared with Pairing A: Euler does not sit in this family (3.3), so the recurrence must not be described as "the law reappearing" across both constructions. The self-similarity is real and it is local to the conjugate family. *(The A-n9 identification is inherited from the prior §3 and cross-referenced, not independently re-derived here; the φ arithmetic above is verified.)*

### 3.5 Retained findings

**The {−1, 0, 1} uniqueness claim is falsified in place. [CANON]** The corpus's assertion that the pentagon equation is the unique equation with coefficients drawn from {−1, 0, 1} is false: its middle coefficient is −2cos(π/5) = −φ, and −φ ∉ {−1, 0, 1}.

**Register strikes, retained. [CANON]**

- The "Master Identity" register framing is superseded — both sides retired; no equation is 恆-register. *(恆 is [M]-attested — the Mawangdui silks are where it reads. It must not be read back onto the Guodian layer, which attests 亙.)*
- **Anachronism flag, standing:** the 五行 framing must not enter DDJ material; the tomb's 五行 manuscript is a separate Zisi-school text.

### 3.6 Restatement of register item A-n13

Prior A-n13 asserted one polynomial family carrying both Euler and the pentagon, tagged OFFERED / CHECKABLE. **Amended:**

- A-n13 now records **two pairings** — antipodal (sum-keyed; home of the §2 centroid identity, Euler included) and conjugate (product-keyed; home of the pentagon/φ recurrence) — coinciding as pairings only at z = ±i.
- The pentagon recurrence (product-one / difference-one on the pair-sums, 3.4) is **CHECKABLE and checks**.
- The unifying claim is **withdrawn as an error, not held as OFFERED.** It does not await a ruling; it is false as stated (3.3), and the register records it as **CORRECTED** rather than carrying it pending.
- **What remains genuinely open:** whether any structural relation connects the two families beyond their single point of coincidence at ±i. Filed as a question, no candidate — and specifically not the winding wire of §6, which is a separate item.

### 3.7 What did not change

The §2 centroid identity — no single θ produces 0; the center is named only as a vanishing sum and is not on the circle — is untouched, and is where Euler lives. Everything in this section is explicit-register and chart-level. No quantity is owed by the framework and none confirms it; the pairings, the pentagon recurrence, and the falsification are facts about the rendering, true as stated, and are read *of* it rather than claimed to be it.

## 4. What the equals sign is doing — the expository lens

*Reading, tier three. Nothing under it is new; every structural fact it uses predates it and lives in the chains.*

One move, worn three times: take a mark the received reading treats as sameness or as negation, and re-read it as two poles flanking a center none of them occupy.

- **非** — two wings turning from a shared spine (相背); not a door closing, but *not the same, sharing an origin*. Illustration pending facsimile, not attestation: the 相背 analysis is Shuowen's, which is Han. See essay 3 and errand C7.
- **±1 and the middle** — the pair obtains; what the pair names in its sum does not. The integer 0 obtains perfectly well, so the exhibit has to be stated carefully or it reads as a false claim about arithmetic. The clean statement needs no P₀ face at all: **the middle is the locus O, which nothing occupies, and the integer 0 is the value the rendering writes at O.** If a P₀ face is wanted for the −1/0/+1 line, the fitting one is the **sign-collapse** face, −1 = 0 = +1 — arithmetic's own face of total indistinguishability, and literally this line collapsed. Not the empty face |0|, which is beneath the register split where O is a frame's origin.
- **Euler** — the zero in the throat of the sign rather than at the end of an addition: the pivot the flip turns on, and the one position no point of the circle occupies.

And the recognition that makes it a thread: the framework's own notation was doing this from the start without saying so. `X = Y` at the balance line never asserted that the modes are the same. It marks the locus where they would coincide, and which therefore does not obtain.

**The equals sign has two throats**, and the second is the live edge:

1. **A center never reached** — the locus the poles flank and none occupies.
2. **A revolution never registered** — e^{i·0} = e^{i·2π}. Same value; one stood still and one went all the way around. The difference is a whole turn the value cannot see. The sign is true and blind in the same instant.

**Pricing, non-negotiable.** The framework authored both the `=` reading and the glyph reading. Their agreement is one hand holding two mirrors — pedagogy, never convergence, never evidence. The three tiers stay apart: resistance (the strips refusing; carries weight, blind to the reader), attestation (checkable, projection-flagged), reading (free, deep, conditional — all of the above).

## 5. The open question this presses on — unclosed

**Which center does the gap name?**

- **O** — the co-vanishing crossing, explicit register, where the ν-pair sums to nothing. The integer exhibit and Euler's zero both pin here.
- **Pₙ** — the mode-swap balance, structural, at (√1ₙ, √1ₙ) in rendering coordinates. The register-reading of 非 points here, at the invariant.
- **Unoccupiability as such** — O, Pₙ and the bare invariant as one fact. Available; not free. It is made against structural §5, which spends a section keeping the two centers apart.

Euler settles the integer thread (→ O). The rest is open, and choosing is the depth of the thread rather than a formality at its end. It is a question about referents, so it is Will's and not the mathematics'.

**Note on the original paper.** The original's §5 assigned **`玄 :: 0`** — the center as the sum of poles, i.e. 玄 at **O**. Current canon reads **玄 :: Paradox :: Pₙ**, with 玄牝 :: P₀. That is a direct contradiction and the strike is entered below on its own authority.

Two cautions on how much to make of it. First, treating "what 玄 maps to" as the same question as "which center the gap names" is itself a reading — a character wired to a math center by interpretation, one hand, not by anything established. Second, the original was never canon-chain material, whatever its self-stamp said, so this is not straightforwardly *the framework* having wavered between O and Pₙ. It is one non-canon document, stamped Locked, sitting on the axis A-n15 now runs along. Whether that counts as evidence of wavering turns on whether the stamp ever meant anything — a question about the corpus, not about the centers.

## 6. The candidate to watch — flagged, unruled

**winding :: sub-floor distinction.** If the 2π-vs-0 winding is the distinction the value cannot state, a wire runs from Euler's return straight to spin-½'s 2π/4π debt (physics §6) and to Pₙ's resolution limit (structural §5). That would be **chain-level**.

It is not in the chains. They read the two returns as "one operation at two angles" and stop.

**Breaker:** it dies if the winding is a fact about the parametrization of the circle rather than about anything a frame cannot resolve — close to what the two-returns entry already concedes in typing itself to the rendering.

Status: proposed correspondence, flagged, unruled. This is the shape of thing that gets welded in between drafts while nobody is watching.

---

## Struck from the original, with authority

| Struck | Authority |
|---|---|
| **`玄 :: 0`** (§5, "the structural meaning of 玄") | DDJ chain v9.5: 玄 :: Paradox :: Pₙ; 玄牝 :: P₀. The original assigns 玄 to O. Direct conflict with canon. |
| **Per-constant assignments** — e :: mode of change, i :: 名 (distinction), π :: gradient measure (§9 table) | Physics chain, "Not carried over": *per-domain assignments of i, π and e, which are substitution rather than correspondence.* `i :: 名` is additionally the retired v7.5 form; 名 obtainedness is held open. |
| **π as "the quantum of polarity change"** (§6) | Math chain: π's numeric content enters with the measure, downstream. A quantum-of-change reading also asserts a minimum, which P1's antecedent denies. Recast: A-n3 — C/D incommensurate (around vs the forbidden through), C/r = 2π exactly (around vs the licensed reach), the closure constant as exchange rate. |
| **無為 :: e^{i·0} / 為 :: e^{iπ}** (§4) | [DRAFTED] Reads as a per-pole substitution of the retired class. Current DDJ chain: 無為 :: aligned persistence; 為 :: effortful action under misalignment. Removed pending a typing ruling rather than carried. |
| **反者道之動 in the received form** (§7) | DDJ chain, Ch. 40 [G, slip A37]: the strip reads **返** (walker radical) and carries the **也者…也** definitional stamp — 返也者道僮也. The received text strips the stamp to a bare assertion. 反/復 remains an open checksum. |
| **The 有無相生 gloss** (§8, "neither cancels until summed") | Held by ruling — register D1; the R5/R6 rewrites are flagged pending in the v9.5 DDJ chain and co-perception is set aside. Additionally: the v9.5 attestation finding that the strips state the six Ch. 2 pairs as six 也-stamped definitions with six distinct verbs (生城型浧和墮), 相生 being the first clause's verb only. |
| **The five-constants foil, as celebration** | v9.52 README: the "five constants" editorializing and the reinstatement narrative struck by ruling. The standard form is stated in §1 as the thing being re-read, without the postcard. |
| **"Status: Tier 1 (Locked)"** | No such tier survives. v9.3 removed the epistemic tag apparatus entire; standing is read from prose. A locked stamp on a document carrying a superseded form is the failure mode the tag removal was supposed to make visible. |

## Carried forward, unchanged

The single-operation insight itself — that the two poles are one operation at two angles, and that non-action is the operation at θ = 0 rather than the absence of it — survives intact, and it is the original paper's real contribution. So does §5's core observation, that no θ produces 0 and the center is reachable only as a sum. Both are now stated in the general form (§2), which the original did not reach.

## What this paper does not claim

No quantity is owed by the framework and none confirms it. Nothing here is a derivation; the chain-level facts it uses — the ν-centroid, the two returns, the resolution floor, B not obtaining — all predate the reading and live in the chains. The identity and the winding fact are chart facts, true as stated. The re-reading is a reading *of* them, and not a claim that they are "really" something else.
