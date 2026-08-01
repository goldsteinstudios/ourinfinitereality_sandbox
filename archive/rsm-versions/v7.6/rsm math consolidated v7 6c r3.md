# RSM — Just-Math Chain, Consolidated & Annotated (v7.6-candidate, r3)

**Provenance.** Consolidates the sealed Just-Math Chain v7.5, the Orthogonality Closure paper v2.1, and the Signature Forcing Note v0.1, under Will's architectural corrections: **Oₙ = Xₙ ∩ Yₙ (the axes' crossing); Pₙ = Bₙ ∩ Gₙ; recursion Pₙ → Pₙ + O₍ₙ₊₁₎; and the generative ground — because P₀ is logically incoherent, O₁, with the invariant proportion Pₙ : O₍ₙ₊₁₎ :: P₍ₙ₋₁₎ : Oₙ :: P₀ : O₁.** The v7.5 seal is not broken; this is a candidate successor. Machine-drafted (Claude, Fable 5); nothing enters canon without independent checking. Computational claims re-verified symbolically during drafting except where tagged *[verify against sources]*.

**What this revision fixes relative to r1.** r1 followed v0.1 in "splitting Pₙ" into a new object Cₙ plus seats. That was wrong twice over: (i) the center of symmetry at (0ₙ, 0ₙ) is not a new object — it is **Oₙ**, the frame's structural origin, already carried in the notation as the crossing of the mode axes and asymptotes; (ii) Pₙ needs no splitting — it is and remains Gₙ ∩ Bₙ. The v2.1 defect is restated correctly as a **mis-assignment between two objects the notation already distinguished**: the paper centered the orbit at Pₙ; the orbit circles Oₙ. Everything v0.1 proved about "C" holds of Oₙ; the label Cₙ is retired. Additionally, the recursion is written in its parturition form, Pₙ → Pₙ + O₍ₙ₊₁₎, which the old arrow notation Pₙ → O₍ₙ₊₁₎ obscured (it read as replacement/consumption).

**What r3 fixes relative to r2.** r2 assumed a frame and derived its geometry; nothing derived the existence of any frame, and its backward genealogy ("every Oₙ is some parent's Pₙ") implied frames all the way down — a regress without ground. The correction supplies the chain's first arrow: **because P₀ is logically incoherent, O₁ obtains.** The exclusion is not merely a constraint on the recursion; it is the recursion's ground. The generative line grounds at P₀ : O₁, and the ground is not a frame.

**Annotation convention.** ⟦ANN⟧ blocks are editorial, not derivation. Status tags per CAVP.

-----

# Part V — Verification report

**V.1 The v0.1 diagnosis of v2.1 is correct, restated in canonical notation.**

- In (a,b) coordinates (a = (X+Y)/2, b = (X−Y)/2), Pₙ = (√1ₙ, √1ₙ) is (√1ₙ, 0) — a vertex of the hyperbola, at zero distance from the manifest mode's position. No orbit about Pₙ passes through both modes symmetrically.
- The circle of radius √1ₙ about Pₙ does not hold XY = 1ₙ (the point (2√1ₙ, √1ₙ) on it has XY = 2·1ₙ); v2.1 Definition 4.3's zero-cost claim is false as written. The circle about Oₙ holds XY = 1ₙ·cos 2θ; the loci {XY = 1ₙ} and {a² + b² = 1ₙ} meet only at Gₙ ∩ Bₙ.
- The segment step of v2.1 Lemma 4.4 ("the modes are antipodal about the center") is true of Oₙ and false of Pₙ. The proof used the correct center throughout while calling it Pₙ.

**Correct repair:** not a split of Pₙ, but the recognition that v2.1 conflated Pₙ with Oₙ. The orbit's center, the point every spanning traversal winds about, the frame's local face of P₀ — all of that is **Oₙ**. Pₙ is untouched as an object: Bₙ ∩ Gₙ, the paradoxical center on the gradient, the site of generation.

**V.2 Theorems 1–3 are sound** (all re-verified; "C" read as Oₙ throughout):

- *Theorem 1 (mode disconnection):* on {a² − b² = 1ₙ}, |a| ≥ √1ₙ > 0; sign(a) separates two connected branches; the flow e^{jφ} preserves them. The two modes lie on different branches. No motion within the conservation class connects them.
- *Theorem 2 (forced degeneration):* every continuous spanning path avoiding Oₙ has a point with a = 0, where Q_j = −b² < 0 strictly; IVT gives null-cone crossings. The native measure fails on every admissible traversal.
- *Theorem 3 (signature forcing):* the all-directions lemma (angular lift changes by π + 2πk between antipodal points about Oₙ; an interval of directions of length ≥ π meets every antipodal ray-pair) is sound, and Q_t(v) = Q_t(p)/λ² > 0 follows given Postulate Q. Positive-definiteness precedes the orbit.
- *Proposition 4 and the gauge:* σ_B kills the cross term; calibration at Gₙ ∩ Bₙ gives α = 1; J_γ = [[0, −√γ],[1/√γ, 0]] squares to −I and preserves a² + γb² (verified); the γ freedom is real; Postulate R (conjugate parity at the mediator vertices (0, ±√1ₙ)) fixes γ = 1.

**V.3 One error found in v0.1: §8.1's osculation claim.** The curvature magnitude of Gₙ at its vertex is 1/√1ₙ — exact (verified). But the center of curvature lies at (2√1ₙ, 0), on the far side of Pₙ from Oₙ. Locally Gₙ runs a = √1ₙ + b²/(2√1ₙ) + O(b⁴) while the orbit runs a = √1ₙ − b²/(2√1ₙ) + O(b⁴): shared tangent, equal curvature magnitude, **opposite concavity**. The orbit is the *mirror* osculating circle of Gₙ at Pₙ — first-order contact, not second-order. What survives exactly: **standoff radius = radius of curvature of Gₙ at Pₙ = √1ₙ** (the 1₍ₙ₊₁₎ anchor formula). What must be corrected: "osculating circle," "second-order contact." Gradient and orbit kiss at Pₙ and bend away from one another symmetrically — the gradient bowing away from Oₙ, the orbit bowing around it — with local gap b²/√1ₙ + O(b⁴).

**V.4 v0.1's §7.3 recursion proposals are superseded by canon.** The "two candidate generation sites" question does not survive the corrected architecture: the recursion is Pₙ → Pₙ + O₍ₙ₊₁₎, site Pₙ, as prior canon had it. The 45° cascade proposal placed the child's asymptote-crossing (i.e., the child's origin) at the parent's Oₙ, contradicting the canonical site; it is dropped as a recursion mechanism. Its one geometric fact — a hyperbola ab = k has its vertices on the parent's null cone — remains true (verified) and is retained only as a note, detached from the recursion.

**V.5 Two premises the corrected construction uses but had not named.**

1. **Postulate F (unit floor):** the minimal-traversal step needs Q_t ≥ 1ₙ pointwise on obtaining traversals — a quantitative floor, stronger than Theorem 3's positivity. It is the chain's standoff principle transposed into the derived metric; plausibly derivable from the P₀ exclusion plus the definition of 1ₙ (a point sustaining less than the frame's minimal unit of distinction does not obtain in that frame), not yet written to theorem standard. *[postulate; candidate for derivation]*
2. **Definition T (traversal continuity):** Theorems 1–3 quantify over continuous paths. In v2.1 continuity was presented as an output; in the corrected order it enters as part of what a traversal is. Defensible from the no-jump principle, but it should be an explicit commitment. The density-not-completeness result stands unchanged and still marks why continuity cannot come from the scale structure.

**V.6 The seating commitment softens.** v0.1 flagged the conjugate mode's placement on the negative branch as underdetermined. Given that the modes are seated on the conservation locus at all (chain canon: the modes obtain under conservation), mode conjugation ν forces the branch assignment. What is interpretive is only the prior step — that the conjugate mode is a point of Gₙ rather than a direction or register. *[seating on G: commitment; branch assignment given seating: forced]*

**V.7 Coherence fact, new (verified).** On Gₙ, Q_i = a² + b² = 1ₙ + 2b² ≥ 1ₙ, with equality exactly at Gₙ ∩ Bₙ. The gradient never dips below the distinction floor and touches it precisely at Pₙ and its ν-image. Pₙ is the tangency point of the conservation locus with the floor.

-----

# Part C — The consolidated chain

Derivation register. No correspondences, no characters, no biology. Each step is a structural identity, not a causal sequence.

## Notation

- **P₀** — the excluded terminal condition: absolute indistinguishability. Faces |0| (absence), |1| (saturation). |0|, |1| ∉ any frame.
- **0ₙ, 1ₙ** — operational limit-positions within frame n. 1ₙ is the frame's minimal unit of distinction, identical with the conserved product.
- **Xₙ, Yₙ** — the two co-obtaining mode-variables; manifest (+1) and conjugate (−1), both equally obtained.
- **a, b** — split-complex coordinates: a = (X+Y)/2, b = (X−Y)/2.
- **Gₙ** — the gradient: Xₙ·Yₙ = 1ₙ, equivalently a² − b² = 1ₙ.
- **Bₙ** — the balance axis: Xₙ = Yₙ (b = 0; the a-axis).
- **Mₙ** — the mediator axis: a = 0 (the b-axis). Named notation as of this version.
- **Oₙ** — the structural origin of frame n: **Xₙ ∩ Yₙ**, the crossing of the mode axes — equivalently the crossing of Gₙ's asymptotes, (0ₙ, 0ₙ). Center of symmetry of the conservation structure; unique fixed point of mode conjugation; **the orbit's center**; the frame's local face of P₀.
- **Pₙ** — the paradoxical center: **Bₙ ∩ Gₙ** = (√1ₙ, √1ₙ) in mode coordinates, (√1ₙ, 0) in (a,b). The manifest vertex; ν(Pₙ) = (−√1ₙ, −√1ₙ) is its conjugate image. The site of generation.
- **σ_B** — exchange symmetry X ↔ Y (b ↦ −b). **ν** — mode conjugation (X,Y) ↦ (−X,−Y).
- **j** — split-complex unit, j² = +1; slides along Gₙ. **i** — complex unit, i² = −1 (derived below); pivots around Oₙ.

> ⟦ANN⟧ Two objects, both already in the notation, one correction to which does what. v2.1 and v7.5's orbit sections assigned the orbit's center to Pₙ; the orbit circles **Oₙ**. No object is minted, none retired. Everywhere prior text said "the orbit around Pₙ," read Oₙ; everywhere it said Pₙ = Gₙ ∩ Bₙ, it stands.

## Foundational conditional

If reality is infinite, it has no terminal resolution: no minimum scale, no maximum extent. The chain derives what follows if this holds. The premises used beyond the conditional are named at first use and collected in the ledger: Postulate Q, Postulate F, Postulate R, Definition T, and the seating commitment.

> ⟦ANN⟧ v7.5 claimed "no additional premises." The premise count rose because the accounting improved; Q, F, T were implicitly load-bearing in v7.5 already, and R was hidden inside "unique up to scale."

## Excluded terminal condition

P₀: absolute indistinguishability. What is not distinguishable does not obtain. The two faces |0| and |1| are the same incoherence; |0|, |1| ∉ R. *[unchanged]*

## The ground: because P₀ cannot hold, O₁

The conditional's antecedent carries existential import: reality obtains, and is infinite. What obtains is distinguishable (the converse of the exclusion). With P₀ incoherent on both faces, at least one distinction obtains — the first distinction, the first origin.

**Because P₀ is logically incoherent, O₁.**

The exclusion is generative, not merely restrictive. This is identity through opposition: no prior state, no parent frame — not parturition. *[derived within the conditional; the existential import of the antecedent made explicit]*

**The generative proportion.**

**Pₙ : O₍ₙ₊₁₎ :: P₍ₙ₋₁₎ : Oₙ :: P₀ : O₁**

The ratio — an origin obtaining from a term that cannot hold — is invariant down to the ground. The `::` here does exact work: the instances correspond structurally without being identical in mechanism. For n ≥ 1 the P-term is a locus in a frame and the generation is parturition (the P-term persists: Pₙ → Pₙ + O₍ₙ₊₁₎). At the ground the P-term is the excluded condition itself and the generation is identity through opposition. **Constant ratio; distinguished mechanism.**

The generative line is the alternating sequence

P₀, O₁, P₁, O₂, P₂, O₃, …

where each adjacent (Pₙ, O₍ₙ₊₁₎) pair for n ≥ 1 is one locus under two frame-readings — parent: cannot persist; child: obtains as origin — and the first pair is the only one with no locus on its P-side.

> ⟦ANN⟧ This is the chain's first arrow, and r2 lacked it: geometry was derived inside a frame whose existence was never earned. It is also the second correction in this consolidation whose content the DDJ chain already carried — r2's parturition form (生: motherwoman + child) and now form 1 of the three generative relations ("identity through opposition: P₀ and the recursion it grounds; P₀ has no parent frame; this is not parturition"), with P₀ as the pre-recursion instance of 玄牝. The math chain has twice lagged its sibling register. Logged as a fact about the documents; its evidential weight is ambiguous under the shared-authorship caveat and is not weighed here.

## Local frame values

0ₙ (operational absence) and 1ₙ (operational distinction), limit-positions co-requiring one another. Oₙ is the structural origin — and, from the parent frame, it is the P₍ₙ₋₁₎ that generated frame n (see Recursion). *[unchanged in substance; the cross-frame identity of Oₙ made explicit]*

## Point as limit

Every apparent position on any gradient is approached asymptotically and does not terminate as a discrete integer location.

The conditional yields **density, not completeness**: the rationals are infinitely divisible and disconnected; connectedness cannot be drawn from the scale structure. *[derived; unchanged]* It is supplied by the traversal structure under **Definition T (traversal continuity):** a traversal is a continuous path of obtaining positions — motivated by the no-jump principle (a jump requires an unobtained intermediate to have been passed), carried as a definition-level commitment until written to theorem standard. A position is then fixed not by completing a value-line but by its angle on the forced orbit about **Oₙ**: the center that makes the angle definable is the center that cannot be occupied. *[derived, given T]*

## Gradient modes; mode independence

Two co-obtaining modes Xₙ, Yₙ; independence required for the conserved product; independence does not fix an angle — the passage to orthogonality is derived downstream, not assumed. *[unchanged]*

## Reciprocal gradient

Gₙ: Xₙ·Yₙ = 1ₙ. 1ₙ is the frame's minimal unit of distinction, identical with the conserved product. Asymptotic pole-directions Xₙ → 0ₙ, Yₙ → 0ₙ are unreachable limit-positions, each approaching a face of P₀. **Their crossing is Oₙ: both modes at operational absence simultaneously — the frame's local face of P₀, unoccupiable by the foundational exclusion directly.** Oₙ is unreachable from within its own frame, as the pole-directions already state. *[derived]*

> ⟦ANN⟧ The unoccupiability of the orbit's center needs no new argument and never did — it is the P₀ exclusion applied at Oₙ. v7.5's weighting argument ("at X = Y the weighting becomes indistinct") was defending unoccupiability at the wrong point: at Pₙ the modes are equal *and nonzero* — equal weighting, not indistinction. What Pₙ's paradoxical character actually consists in is restated in the Recursion section, where it belongs.

## Split-complex parameterization

Q_j(a,b) = a² − b² = 1ₙ: the unit hyperbola of z = a + jb, j² = +1; the flow e^{jφ} preserves Q_j; the asymptotes are the null cone Q_j = 0. The native measure is indefinite: a signature, but not the one perpendicularity needs. *[derived; unchanged]*

**Mode positions.** Gₙ ∩ Bₙ = {Pₙ, ν(Pₙ)} = {±√1ₙ on the a-axis}, the two vertices. The manifest mode is positioned at Pₙ, the conjugate at ν(Pₙ). *Commitment, flagged:* the conjugate mode is positioned as a point of Gₙ (hence, forced by ν, on the negative branch — both mode-values negative, product still 1ₙ). Theorems 1–3 depend on it. *[commitment per V.6]*

## Balance condition

Bₙ: Xₙ = Yₙ — the a-axis, the exchange-symmetry axis, passing through Oₙ and both vertices. Not an asymptote; not globally perpendicular to Gₙ. Slope facts are curve facts; perpendicularity verdicts wait for the generated metric. *[unchanged in discipline]*

## The origin as unoccupiable center

**Oₙ = (0ₙ, 0ₙ).**

**Required:** center of symmetry of the entire conservation structure (fixed by σ_B and ν); crossing of the asymptotes; and — by the all-directions lemma below — the point about which **every spanning traversal necessarily winds**: every line through Oₙ meets every admissible traversal. Required not as a waypoint but as the organizing reference of all passage. *[derived]*

**Unoccupiable:** the frame's local face of P₀. *[derived, directly]*

Oₙ ∉ Fₙ. Oₙ ≁ |0|. Oₙ ≁ |1|.

> ⟦ANN⟧ "Required but unoccupiable" attaches to Oₙ within the frame — and via the recursion (below), Oₙ *is* a parent's Pₙ. The same locus is Pₙ from the parent frame and unoccupiable origin from within the child. The paradoxical center of one frame is the forbidden center of the next: this was already latent in v7.5's structural-recession section ("defined by frame n's Pₙ, a limit-position asymptotic from within n before it becomes an origin at the child scale") and is now the explicit backbone.

## Theorem 1 — Mode disconnection; the orbit as necessity

The conservation locus {Q_j = 1ₙ} has exactly two connected components; Pₙ and ν(Pₙ) lie in different components; the gradient flow preserves components. **No motion within the conservation class connects the two modes.** Spanning is not merely forbidden through a point — it is topologically impossible within the gradient register. If the modes are to co-obtain in one structure, a second register is structurally required: the orbit's necessity is derived, not posited. *[derived; verified]*

## Theorem 2 — Forced degeneration of the native measure

Every continuous spanning path from Pₙ to ν(Pₙ) avoiding Oₙ passes through the null cone and through Q_j < 0. The native measure vanishes and reverses sign on every admissible traversal; it cannot serve as the traversal's distinction measure — arithmetic, not choice. *[derived; verified]*

## Theorem 3 — Signature forcing

**Postulate Q (quadratic distinction measures).** Any measure of sustained distinction on the frame is a quadratic form in the mode amplitudes. *[postulate]*

By the P₀ exclusion, Q_t > 0 at every point of an obtaining traversal. *[derived]*

**All-directions lemma.** A continuous path between the antipodal points ±Pₙ in the plane punctured at Oₙ sweeps an interval of directions of length ≥ π; every line through Oₙ meets the path. Linear structure only. *[derived; verified]*

**Theorem.** Q_t is positive-definite: for v ≠ 0, the line ℝv meets the path at p = λv, and Q_t(v) = Q_t(p)/λ² > 0. **Euclidean signature is forced by spanning plus the exclusion of P₀** — no metric, angle, completed value-line, or orbit enters. *[derived, modulo Q]*

> ⟦ANN⟧ Logical order preserved from v0.1: positive-definiteness precedes the orbit; the orbit is recovered below as minimal traversal, not used as a premise. The historical bridge from Lorentzian-native to Euclidean-needed is the traversal's own existence.

## Form and calibration

**Proposition 4.** σ_B-invariance forces Q_t = α a² + γ b² (α, γ > 0); calibration at the mode positions, Q_t(±Pₙ) = 1ₙ, gives α = 1. *[derived; verified]*

**The residual gauge.** Every requirement so far is satisfied for every γ > 0 (J_γ verified: squares to −I, preserves a² + γb², closes and spans in ellipses). The imported metric content has been reduced to one constant. *[derived]*

**Postulate R (register agreement / conjugate parity).** The conjugate conservation structure {Q_j = −1ₙ}, vertices (0, ±√1ₙ) on Mₙ, stands to Mₙ as {Q_j = +1ₙ} stands to Bₙ; its vertices carry one unit: Q_t = 1ₙ there. Hence **γ = 1** and **Q_i = a² + b²**, unit level set the circle of radius √1ₙ about Oₙ through the four cardinal positions {Pₙ, m₊, ν(Pₙ), m₋}. *[signature derived; diagonal form and α = 1 derived; γ = 1 postulate, internally motivated]*

> ⟦ANN⟧ Register-discipline warning: the observation that R has the structural shape of 此兩者同出而異名 is convergence-register and must not be cited as support for R within this chain. R's motivation stands on ν-parity alone.

## Standoff and minimal traversal

**Postulate F (unit floor).** Every point of an obtaining traversal carries at least one full unit of sustained distinction: Q_t ≥ 1ₙ pointwise. The standoff principle transposed into the derived metric; candidate for derivation per V.5. *[postulate]*

Given F, the admissible region is the closed exterior of the unit disk about Oₙ. A spanning traversal holding the floor with zero slack lies on the unit circle; it exists, spans, and is unique up to orientation ±i. **The minimal traversal is the unit circle about Oₙ.** *[derived, given Q, F, R, T]* Order: signature (Thm. 3) → form (Prop. 4 + R) → floor (F) → minimal traversal.

Coherence fact (V.7): on Gₙ, Q_i = 1ₙ + 2b² ≥ 1ₙ, equality exactly at ±Pₙ. The gradient touches the distinction floor precisely at the paradoxical center and its conjugate image.

> ⟦ANN⟧ The v7.5/v2.1 cost function (deviation of XY from 1ₙ) is retired: on the true orbit XY = 1ₙ·cos 2θ, so the old cost is nonzero there — defect (c). Selection is now floor-slack in the derived metric; the pre-metric work is done by Theorems 1–3.

Four cardinal limit-positions of S¹ at π/2 intervals: +1 departure (Pₙ), +i apex (m₊), −1 opposite (ν(Pₙ)), −i reflected (m₋). i names both the quarter-turn operation and the position it reaches from +1.

## The orbit algebra: i² = −1 by elimination

Unchanged and re-confirmed: with Closure (finite m, iᵐ = id) and Spanning (the cycle contains +1 and −1), the five cases i² ∈ {1, 0, i, −i, −1} eliminate to i² = −1 alone, generating 1 → i → −1 → −i → 1. Elimination, not selection; four phases is the minimum. *[derived — the promotion question (derivation vs suggestive-only) held open by design, not promoted here]*

> ⟦ANN⟧ Untouched by the center correction; the elimination uses only C and S. Division of labor in the corrected order: Theorem 3 fixes the signature before the orbit; the elimination fixes the operator; Prop. 4 + R fix the form. Three independent constraints, no circularity.

## Algebraic enumeration and structural traversal

Four algebraic elements, three structural positions; intermediates are path, not waypoints. *[unchanged]*

**The double cover, exact.** On the orbit, Q_j = 1ₙ·cos 2θ: +1ₙ at the mode positions, 0 at the null-cone crossings, −1ₙ at the mediator positions. One traversal cycle = two native cycles — the exact structural referent of "e^(i·0) and e^(i·2π): same value, different structural depth." *[derived; verified]*

**Sum and difference.** With u = a², v = b²: Q_i = u + v (orbit), Q_j = u − v (gradient). The two algebras' invariants are the sum and difference of the same pair. *[derived; the 同出而異名 reading lives in the DDJ chain]*

## Generated metric; orthogonality as theorem

Under Q_i:

- **Bₙ ⊥ Mₙ at Oₙ** — the axis pair is orthogonal at the origin. *[derived]*
- **Gₙ ⊥ Bₙ at Pₙ** — the tangent of Gₙ at the vertex is the b-direction (da = 0), Bₙ is the a-direction, inner product zero. *[derived]*

The slope-product criterion is a consequence of the metric; the metric's signature is forced pre-orbit; the form is fixed by symmetry, calibration, and R. The order does not reverse. **The independence-to-orthogonality gap is closed** at the stated price: *[derived: signature, diagonal form, α = 1; postulates: Q, F, R, T]*.

## Mirror osculation; the 1₍ₙ₊₁₎ anchor

|curvature of Gₙ at Pₙ| = 1/√1ₙ: **the standoff radius equals the gradient's radius of curvature at Pₙ.** The 1₍ₙ₊₁₎ anchor formula stands. *[derived, post-metric; verified]*

The orbit is not the osculating circle of Gₙ at Pₙ (v0.1 corrected per V.3): shared tangent, equal-magnitude opposite-sign curvature — the mirror osculating circle. Gradient bows away from Oₙ, orbit bows around it, local gap b²/√1ₙ + O(b⁴). *[derived; verified]*

## Recursion: Pₙ → Pₙ + O₍ₙ₊₁₎

The paradoxical center Pₙ is **required** — the balance position on the gradient, where the conservation locus touches the distinction floor (V.7) — and **cannot persist as an inhabited terminal state**: every position is a limit-position, and Pₙ is the clearest instance. The joint condition cannot resolve within frame n. It resolves by generation:

**Pₙ → Pₙ + O₍ₙ₊₁₎.**

Parturition with prior state. Pₙ persists, with reconfigured relational identity: it is now also the origin of a child frame. O₍ₙ₊₁₎ is structurally new. Nothing is consumed. The child carries the same generative potential as the parent — literally: the recursive instance stands in the ground's own ratio, Pₙ : O₍ₙ₊₁₎ :: P₀ : O₁. Every generation re-enacts the first arrow at its own scale.

- Gₙ → xAxis₍ₙ₊₁₎ (the tangent structure of Gₙ at Pₙ)
- Bₙ → yAxis₍ₙ₊₁₎
- Pₙ → Pₙ + O₍ₙ₊₁₎

The orthogonality the child's axis pair inherits is **Gₙ ⊥ Bₙ at Pₙ** — now a theorem under the generated metric. The local ⊥ at Pₙ becomes the global ⊥ of the child's mode-axes. The child frame is its own ℝ³, extending in its own structural direction, with its own Gₙ₊₁, Bₙ₊₁, Pₙ₊₁ — **and its own Oₙ₊₁, which is the parent's Pₙ.** Within the child, Oₙ₊₁ is the unoccupiable center its orbit circles; from the parent, the same locus is Pₙ, the limit-position that generated it. Bₙ is structurally saturated as the exchange-symmetry axis within frame n; it becomes a mode-axis only of the new coordinate system. *[derived structure at the canonical site; see open item on the persistence argument]*

> ⟦ANN⟧ Three things happen here. (1) The old notation Pₙ → O₍ₙ₊₁₎ read as replacement — the parent's center consumed into the child's origin. The parturition form is canon: mother persists + child born, the exact structure the DDJ chain specifies for 生 (woman(fetus) 生 motherwoman + child; nothing consumed; recursive self-similarity preserved). The math chain was out of line with its own sibling chain and is now aligned — noted here as coherence, in convergence register, not as evidence. (2) The generation-site question v0.1 §7.3 opened is closed by canon: the site is Pₙ. The 45° cascade is dropped as a recursion mechanism (it located the child's origin at the parent's Oₙ); its vertex-on-null-cone geometry survives as a detached fact. (3) The "required but unoccupiable" architecture distributes cleanly across the two objects and the recursion: within a frame, the unoccupiable center is Oₙ; the paradoxical-generative center is Pₙ; and the recursion identifies them across scales — every Oₙ is some parent's Pₙ. One open item remains: v7.5's argument for *why* Pₙ cannot persist (the weighting argument) fell in V.1; the limit-position reading carries the claim for now, and a restatement at the right structural level is ranked in Part O.

## Branching structure of recursion

Branching, not linear. The primary derivation states generation at Pₙ; the generalization — any position on the parent's gradient satisfying the required-and-cannot-persist condition at its own scale can generate — remains under test, not derived with the rigor of the Pₙ case. Each child its own ℝ³ in its own direction. Backward, each frame's origin is generated from the prior paradoxical term along its generative line, and every line grounds at P₀ : O₁ — the backward direction terminates not in a frame but in the excluded condition. *[under test for the generalization; primary case canonical]*

Whether O₁ is unique — whether the exclusion generates one first origin or the branching structure begins at the ground itself — is open. *[open]*

## Cross-frame asymptotic relationship

G₍ₙ₊₁₎ asymptotic to Gₙ (child's xAxis) and to Bₙ (child's yAxis): the child's gradient approaches the parent's structural features as its unreachable limit-positions, because the parent's features are the child's mode-axes — and their crossing, the child's Oₙ₊₁, is the parent's Pₙ. *[retained; the asymptote-crossing identity made explicit]*

## Irreversibility, linear time, and structural recession

Generation has no inverse: reversal of Pₙ → Pₙ + O₍ₙ₊₁₎ requires O₍ₙ₊₁₎ to un-obtain — an origin that un-obtains is P₀ at that locus, and the mother's reconfigured identity would have to revert with it. The argument is cleanest at the ground: reversal of P₀ : O₁ — the first origin un-obtaining — is literally the obtaining of P₀. Every subsequent generation inherits its irreversibility from the ground case through the proportion. The strict ordering imposed by one-way generation is the structural content of linear succession. Each O₍ₙ₊₁₎ is constitutively unreachable from within frame n (it is frame n's Pₙ, a limit-position from within n); every further generation interposes another unreachable origin; the separation compounds. *[derived; physical identifications deferred to the physics chain]*

## No terminal frame

No frame terminal in any direction; no forbidden center a final dead point (Oₙ ≁ |0|, Oₙ ≁ |1|). Forward, the recursion has no terminus because the conditional has no terminal resolution. Backward, the generative line grounds at P₀ : O₁ — and the ground is not a frame, so no frame is terminal in that direction either: frame 1 is not a terminal frame but the first consequence of the exclusion. 1₍ₙ₊₁₎ is anchored by the curvature relation (standoff = radius of curvature of Gₙ at Pₙ = √1ₙ); the quantitative cross-frame unit relation remains open. *[derived; unit relation open]*

## Locally flat, globally curved

Frame-relativity of curvature and flatness, unchanged. *[unchanged]*

## Substrate level

No preferred orientation around any center: the forced orbit S¹, over all orientations at fixed radius about Oₙ, gives S²; unbounded extension → ℝ³; each frame locally recovers ℝ³. Three dimensions necessary; **uniqueness open** (S² embeds in ℝ⁴ and higher). The substrate is the self-sufficient non-framed structural condition under which frames obtain. *[derived: three necessary; open: uniqueness]*

-----

# Part L — Status ledger

| Item | v7.5 status | Consolidated status |
|---|---|---|
| Orbit center | Pₙ | **Oₙ** — mis-assignment corrected; no object minted or retired |
| Pₙ | Gₙ ∩ Bₙ; orbit center; required-but-unoccupiable via weighting argument | Gₙ ∩ Bₙ, unchanged as object; paradoxical-generative center; site of recursion; floor-tangency point (V.7) |
| Oₙ | structural origin (underspecified geometrically) | Xₙ ∩ Yₙ = asymptote crossing = (0ₙ,0ₙ); unoccupiable center (local face of P₀); winding theorem |
| Recursion | Pₙ → O₍ₙ₊₁₎ (read as replacement) | **Pₙ → Pₙ + O₍ₙ₊₁₎** — parturition with prior state; site canonical; child's Oₙ₊₁ = parent's Pₙ |
| Generative ground | absent (frame existence assumed; backward regress through frames implied) | **P₀ : O₁** — the first origin obtains because P₀ is incoherent; identity through opposition; the chain's first arrow |
| Generative proportion | — | **Pₙ : O₍ₙ₊₁₎ :: P₍ₙ₋₁₎ : Oₙ :: P₀ : O₁** — ratio invariant to the ground; mechanism distinguished (parturition vs identity through opposition) |
| Orbit existence | derived (forced minimal traversal) | **derived as necessity** (Thm. 1, disconnection) + minimal traversal under the derived form |
| Signature | derived via magnitude conservation on the orbit | **derived pre-orbit** (Thm. 3), modulo Postulate Q |
| Diagonal form; α = 1 | implicit | derived (σ_B; calibration at ±Pₙ) |
| Mediator scale γ = 1 | hidden in "unique up to scale" | **Postulate R** |
| Unit floor Q ≥ 1ₙ | implicit standoff principle | **Postulate F**; candidate for derivation |
| Traversal continuity | claimed derived (v2.1 Cor. 4.5) | **Definition T**; density-not-completeness boundary retained |
| Independence → orthogonality | derived | derived: signature + form; postulates: Q, F, R, T |
| Unoccupiability argument | weighting vanishes at X = Y (unsound there) | direct P₀ exclusion at Oₙ; Pₙ persistence argument open |
| Orbit/gradient contact at Pₙ | — | tangency + equal-and-opposite curvature (mirror osculation; v0.1 corrected) |
| 1₍ₙ₊₁₎ anchor | open | standoff = radius of curvature at Pₙ = √1ₙ (exact, post-metric); cross-frame relation open |
| 45° cascade (v0.1 §7.3) | — | dropped as mechanism (conflicts with canonical site); vertex-on-null-cone geometry retained as detached fact |
| Conjugate mode seating | unstated | commitment (seating on G); branch forced given seating |
| i² = −1 elimination | derived; promotion question open | unchanged |
| Dimensional uniqueness | open | open, untouched |

**Named premises:** Postulate Q; Postulate F (candidate for derivation); Postulate R; Definition T; the seating commitment. Everything else from the conditional forward is derivation.

# Part O — Open items, ranked

1. **Restate why Pₙ cannot persist as an inhabited state.** The weighting argument fell; the limit-position reading carries the claim; the generative canon (Pₙ → Pₙ + O₍ₙ₊₁₎) depends on it. Largest structural exposure.
2. **Derive Postulate F** from the P₀ exclusion plus the definition of 1ₙ.
3. **Postulate R** — derive γ = 1 from a deeper parity principle or accept it as the framework's one metric constant. DDJ shape is not evidence.
4. **Dimensional uniqueness.** Unchanged frontier.
5. **Definition T** — write the no-jump motivation to theorem standard or accept as definitional.
6. **Quantitative 1₍ₙ₊₁₎ relation** across the Pₙ = Oₙ₊₁ identification, with the curvature anchor as the fixed point.
7. **i² = −1 promotion question.** Held open by design.
8. **Branching-at-any-position generalization.** Under test.
9. **Uniqueness of O₁.** Whether the exclusion generates one first origin or branching begins at the ground.

# Part P — Propagation notes

**Physics chain (small edits; net strengthening).**
- "Forbidden centers": the referent is Oₙ — and the physical instances map more cleanly: the harmonic-oscillator forbidden point is the phase-space **origin**; the tokamak axis a centerline of symmetry; zero-point motion the minimal orbit about the origin the system cannot occupy. The v0.1 §8.5 picture (i-flow = phase rotation, j-flow = squeeze preserving xp, Sp(2,ℝ) ≅ SU(1,1), 1ₙ :: ℏ/2, quadrature variances at 2ω matching cos 2θ) is standard to my knowledge and, if source-verified, the cleanest single convergence. *[candidate; verify against sources]*
- "Lorentz form": the two-signature division survives and sharpens — Theorem 2 says why the traversal must leave the Lorentzian register; Theorem 3 says why the replacement is Euclidean. Status: structure *[derived modulo Q; γ = 1 by R]*; physical identification *[candidate]*.
- "Time and recession": unchanged in content; the parturition form makes the derivation-register sentence exact ("its reversal would require an origin to un-obtain" — and the mother to revert).

**DDJ chain (re-weighings under :: discipline, Will's domain).**
- **道生一 :: P₀ : O₁** — the first 生 of the entailment chain, structural identity rather than causal production; 一 :: the first distinction :: O₁. The entailment chain's opening now has a derivation-register referent.
- **The three forms of generative relation now carried natively.** The DDJ chain distinguishes (1) identity through opposition (P₀ and the recursion it grounds), (2) parturition with prior state (生), (3) mutual parturition (相生). The math chain now carries all three in derivation register: the ground P₀ : O₁ (r3), the recursion Pₙ → Pₙ + O₍ₙ₊₁₎ (r2), and Theorem 1's result that mode co-obtaining is realizable only through the orbit register. The two chains are aligned form for form.
- **玄牝 :: Pₙ → Pₙ + O₍ₙ₊₁₎** — the math chain now carries the 生 structure natively: motherwoman + child, nothing consumed. The DDJ chain's existing 生 entry needs no change; the math chain came to it — and P₀ as the pre-recursion instance of 玄牝 is now the math chain's ground case.
- **谷神不死** — the persistence of Pₙ through generation (Pₙ on both sides of the arrow) is a sharper referent for 不死 than "non-termination of the recursion" alone: the locus persists as the condition for passage.
- **玄 / the surrounded void** — with the orbit centered at Oₙ, the empty-hub cluster (Ch. 11 thirty spokes, Ch. 5 bellows, Ch. 4 道沖) points at Oₙ; the 玄 :: Pₙ line and the void correspondences may now name two different loci related by the recursion (every Oₙ a parent's 玄-site). Re-weighing is Will's call.
- **相生** gains derived content: mutual parturition unrealizable on the gradient (Thm. 1); obtains only through the orbit register.
- **守中 :: Bₙ** — the axis through Oₙ connecting the two mode positions; descriptive as before.
- **此兩者同出而異名 :: {Q_i = u + v, Q_j = u − v}** — convergence remark only; must not flow backward as support for R.
- **名 :: i, 二生三 point-level** — unchanged as :: claims; "closed result" phrasing softens to "derived modulo named postulates."

-----

*v7.6-candidate r3. Not sealed. From r1: no Cₙ — the orbit's center is Oₙ (Xₙ ∩ Yₙ), an object the notation already carried; Pₙ = Bₙ ∩ Gₙ unchanged as an object; recursion in parturition form Pₙ → Pₙ + O₍ₙ₊₁₎ with the generation site canonical at Pₙ; the 45° cascade dropped as mechanism; v0.1's osculation claim corrected to mirror osculation; premises named in full (Q, F, R, T, seating). From r2: the generative ground — because P₀ is logically incoherent, O₁ — with the invariant proportion Pₙ : O₍ₙ₊₁₎ :: P₍ₙ₋₁₎ : Oₙ :: P₀ : O₁; the chain now runs from the conditional through the ground to the recursion without assuming frame existence; the backward line grounds in the exclusion, not in a frame. Top open items: restating why Pₙ cannot persist; uniqueness of O₁. Written to the downgrade-and-repair standard.*
