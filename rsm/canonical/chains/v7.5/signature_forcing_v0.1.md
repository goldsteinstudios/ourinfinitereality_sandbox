# RSM — The Gradient-to-Orbit Passage: Signature Forced by Spanning

**Draft v0.1 — exploratory companion note, written against the v7.5 chains and Orthogonality paper v2.1.**

*Derivation register except where tagged. Machine-drafted (Claude, Fable 5) at Will's request. Per the parallax document's own discipline, an LLM-derived result is weaker evidence than an externally verified one; nothing below should enter canon without independent checking, and the physics remarks in §8.5 cite standard results from memory that must be verified against sources.*

---

## 0. What this note does

The v2.1 review identified a gap in Lemma 4.4: the "zero-cost circle" does not hold XY = 1ₙ in any coordinate system the paper establishes, and the modes are antipodal about the origin, not about Pₙ. This note locates that equivocation precisely and then rebuilds the passage from the gradient to the orbit, deriving as much as the model's own commitments permit.

### Main results

- **Theorem 1 (Mode disconnection).** The conservation locus has two connected components; the two modes lie in different components; the gradient flow preserves components. Spanning is topologically impossible within the conservation class. The orbit is not posited — its *necessity* is derived.

- **Theorem 2 (Forced degeneration).** Every spanning path crosses the null cone and enters the region where the native measure is negative. The Lorentzian form cannot serve as the traversal's distinction measure on any admissible path.

- **Theorem 3 (Signature forcing).** Any quadratic distinction measure that is positive along a spanning path is positive-definite. **Euclidean signature is forced by spanning + the exclusion of P₀**, with no metric, angle, or completed value-line imported.

- **Proposition 4 + Postulate R.** Symmetry and seat calibration fix the measure to Q = a² + γb²; a one-parameter gauge freedom γ remains; a register-agreement postulate (internally motivated, but a postulate) fixes γ = 1, yielding the circle, and everything in v2.1 §§5–7 then proceeds soundly.

**The price.** The construction only closes if the orbit's center is the conservation structure's center of symmetry — the point where both modes are at 0ₙ, the crossing of the asymptotes — and **not** the vertex Pₙ = (√1ₙ, √1ₙ). In the frame's own coordinates, G ∩ B is *two* points, ±√1ₙ, and they are the seats of the two modes; the current Pₙ coincides with the manifest mode's seat. §2 makes this exact; §7 traces the upstream corrections it forces.

---

## 1. Setting and assumptions

Work within one frame; suppress n where unambiguous. The plane carries **linear structure only** — no inner product, no angle, no arc length.

- **Mode coordinates** X, Y; **split-complex coordinates** a = (X+Y)/2, b = (X−Y)/2, so X = a+b, Y = a−b.

- **Gradient** G: XY = 1ₙ ⟺ Q_j(a,b) := a² − b² = 1ₙ (v2.1 Prop 2.1). The native measure Q_j is the split-complex modulus; the j-flow e^{jφ} (hyperbolic rotation) preserves it.

- **Balance axis** B: X = Y ⟺ b = 0 (the a-axis).

- **Exchange symmetry** σ_B: X ↔ Y ⟺ b ↦ −b. This is the chain's own named symmetry of Bₙ ("swapping Xₙ and Yₙ leaves the position unchanged").

- **Mode conjugation** ν: (X,Y) ↦ (−X,−Y) ⟺ (a,b) ↦ (−a,−b). Licensed by "both modes equally obtained; neither latent."

### Seats

G ∩ B = {(√1ₙ, √1ₙ), (−√1ₙ, −√1ₙ)}. In split-complex coordinates these are ±√1ₙ on the a-axis — the two **vertices** of the hyperbola. Identify:

- **s₊ = (√1ₙ, 0)**: the seat of the manifest mode (+1 direction),
- **s₋ = (−√1ₙ, 0)**: the seat of the conjugate mode (−1 direction).

*Interpretive commitment, flagged:* this places the conjugate mode on the negative branch of G (X, Y both negative, product still 1ₙ). The chains say the modes are "seated at radius √1ₙ" with values ±1 but do not plot the conjugate seat; this reading is the one under which the chains' own notation (manifest = 1, conjugate = −1) becomes literal in the split-complex plane. Everything below depends on it.

### Center

**C := (0ₙ, 0ₙ)** — the crossing of the two asymptotes, the center of symmetry of G, the unique fixed point of ν, the locus where both modes are at operational absence simultaneously. C is the frame's local face of P₀ and is unoccupiable directly by the foundational exclusion; no new argument is needed. (The asymptotes X = 0ₙ and Y = 0ₙ are already the chain's "unreachable pole-directions"; C is their intersection, and the null cone Q_j = 0 is exactly the asymptote pair.)

### Postulate Q (quadratic distinction measures)

Any measure of sustained distinction on the frame is a quadratic form in the mode amplitudes. This is carried implicitly by the native register (Q_j is quadratic, forced by the algebra of the conserved product) and by v2.1 Thm 6.1's own "conserved magnitude = quadratic form" step. It is used here explicitly and marked as a postulate, not derived.

---

## 2. The diagnosis, made exact

Three separate defects in the v2.1 construction, all instances of one confusion:

**(a) Pₙ coincides with a mode seat.** Pₙ = (√1ₙ, √1ₙ) = s₊. The "standoff of the modes from Pₙ" is zero for the manifest mode and maximal for the conjugate. No closed curve about Pₙ passes through both seats symmetrically.

**(b) The segment step names C while writing P.** The proof of Lemma 4.4 asserts "the straight segment from +1 to −1 passes through P (the two modes are antipodal about the center)." The seats ±√1ₙ are antipodal about **C**, and the segment between them passes through C. The sentence is true of C and false of the vertex. The proof was using the correct center throughout while calling it Pₙ.

**(c) Two conservation relations equivocated.** {XY = 1ₙ} (hyperbola) and {a² + b² = 1ₙ} (circle) are distinct loci meeting only at the seats. A path holding "radius √1ₙ" does not hold XY = 1ₙ except at isolated points, so Definition 4.3's cost is not zero on the circular arc. Phrasing the standoff as a *radius* imported Q_i at the moment it was supposed to be derived.

**What survives untouched:** Prop 2.1 (split-complex parameterization); Thm 5.1 (i² = −1 by elimination, *given* a closed spanning orbit); the rotation-invariance argument of Thm 6.1 (*given* the rotation flow); the computation of Thm 7.1 (*given* Q_i). **What falls:** Lemma 4.4 and Cor 4.5 as stated; Props 3.2–3.4 as statements about the orbit's center. Whether the vertex retains a distinct forbidden status at the weighting level (Prop 3.2's "differential weighting vanishes at X = Y") is a separable question deferred to §7.1; what is settled is that the vertex is not the orbit's center.

---

## 3. Theorem 1 — Mode disconnection

**Theorem.** The conservation locus L = {Q_j = 1ₙ} has exactly two connected components, L₊ = L ∩ {a > 0} and L₋ = L ∩ {a < 0}, with s₊ ∈ L₊ and s₋ ∈ L₋. The gradient flow e^{jφ} maps each component to itself. Hence no motion within the conservation class connects the two modes.

*Proof.* On L, a² = 1ₙ + b² ≥ 1ₙ, so |a| ≥ √1ₙ > 0 and a never vanishes on L; the sign of a is constant on each connected component, and each of {a ≥ √1ₙ}, {a ≤ −√1ₙ} is a connected branch (graph of a = ±√(1ₙ + b²) over b ∈ ℝ). The flow e^{jφ}: (a,b) ↦ (a cosh φ + b sinh φ, a sinh φ + b cosh φ) preserves Q_j, is continuous in φ, and is connected to the identity; it therefore preserves each component. ∎

**Consequence.** The gradient register cannot realize spanning. If the two modes are to co-obtain in one structure — the chain's spanning requirement — a second register is not optional but structurally required. This upgrades "direct crossing forbidden" (a prohibition) to a topological impossibility (no path exists within conservation at all), and it derives the *need* for the orbit rather than positing the orbit.

*Convergence remark [convergence register].* 相⽣ — mutual parturition of the modes — is not realizable on the gradient. It obtains only through the mediator structure derived below. This is Through-line 5 ("two modes require a third position") sharpened from a closure-minimum observation to a disconnection theorem.

---

## 4. Theorem 2 — Forced degeneration of the native measure

**Theorem.** Every continuous spanning path γ: [0,1] → ℝ² ∖ {C} with γ(0) = s₊, γ(1) = s₋ passes through points where Q_j = 0 (the null cone) and through points where Q_j < 0.

*Proof.* The coordinate a(t) is continuous with a(0) = √1ₙ > 0 and a(1) = −√1ₙ < 0, so a(t₀) = 0 for some t₀. There, Q_j = −b(t₀)². If b(t₀) = 0 the path is at C, excluded; so Q_j(γ(t₀)) < 0 strictly. Since Q_j(γ(0)) = 1ₙ > 0, the intermediate value theorem gives null-cone crossings at points distinct from C. ∎

**Consequence.** The native measure vanishes and reverses sign on **every** admissible traversal. It cannot serve as the traversal's measure of sustained distinction — not as a matter of choice but of arithmetic. v2.1 Remark 2.3 observed that "the gradient supplies a signature, but not the one perpendicularity needs"; Theorem 2 derives that the needed signature must differ, because the traversal necessarily visits the native measure's degenerate and negative regions.

---

## 5. Theorem 3 — Signature forcing

This is the central result.

**Setup.** By Postulate Q, the traversal's distinction measure is a quadratic form Q_t on the plane. By the exclusion of P₀, Q_t > 0 at every point of any obtaining traversal — a traversal point carrying zero distinction does not obtain (the chain's own floor principle, used here only for positivity). By the spanning requirement and Theorem 1, a traversal from s₊ to s₋ avoiding C exists off the gradient.

> **Lemma (all directions).** A continuous path from s₊ to s₋ in the punctured plane ℝ² ∖ {C} sweeps an interval of directions of length ≥ π; consequently every line through C contains a nonzero point of the path.

*Proof.* Directions are rays under positive scaling — linear structure only, no metric. On the punctured plane the angular coordinate admits a continuous lift θ(t) along γ (topology of ℝ² ∖ {pt}; equivalently, IVT on the projective angle). Since s₋ = −s₊, θ(1) − θ(0) = π + 2πk for some integer k, so the connected image of θ contains an interval of length ≥ π. An interval of directions of length π contains, for every line through C, at least one of that line's two rays. Hence every such line meets γ at some p ≠ 0. ∎

**Theorem.** Q_t is positive-definite.

*Proof.* Let v ≠ 0. The line ℝv meets γ at p = λv with λ ≠ 0, and Q_t(p) > 0 by the floor. Then Q_t(v) = Q_t(p)/λ² > 0. Since v was arbitrary, Q_t is positive on all nonzero vectors. ∎

**Reading.** Positive-definiteness — the Euclidean signature — is **forced** by two commitments the framework already carries: the modes must be spanned, and no point of an obtaining traversal can be indistinct. No metric, no angle, no completed value-line, and no orbit enter the argument; the *existence* of any admissible traversal whatsoever suffices. The historical gap ("the native signature is Lorentzian, the needed signature is Euclidean, and nothing yet bridges them") is bridged: the bridge is the traversal's own existence. Status: **[derived]**, modulo Postulate Q.

Note the logical order relative to v2.1: there, positive-definiteness was extracted from magnitude conservation on the orbit, which presupposed the orbit. Here it precedes the orbit entirely. The orbit is then recovered as the minimal traversal (§6), not used as a premise.

---

## 6. Proposition 4 — The form up to one constant; Postulate R — calibration

**Proposition 4.** (i) Invariance of Q_t under the exchange symmetry σ_B (b ↦ −b) forces the cross term to vanish: Q_t = α a² + γ b², with α, γ > 0 by Theorem 3. (ii) Seat calibration — the traversal departs and arrives at the seats carrying the minimal sustained distinction, and at the seats the native register assigns exactly 1ₙ — gives Q_t(s±) = 1ₙ, hence α = 1.

*Proof.* (i) For Q_t = αa² + 2βab + γb², invariance under b ↦ −b gives β = 0. (ii) Q_t(±√1ₙ, 0) = α·1ₙ = 1ₙ. ∎

### The residual gauge freedom, stated plainly

Every requirement so far — closure, spanning, i² = −1 by elimination, existence of an invariant positive form — is satisfied for *every* γ > 0. Explicitly, the operator with matrix J_γ = [[0, −√γ], [1/√γ, 0]] in the (a,b) basis satisfies J_γ² = −I, generates a one-parameter group preserving a² + γb², and its orbit through s₊ is the ellipse a² + γb² = 1ₙ, which closes, spans, and visits an apex at (0, √(1ₙ/γ)). The abstract construction therefore has a one-parameter family of realizations. This also sharpens v2.1 Thm 6.1: "unique up to scale" holds only after coordinates are chosen in which i is the standard rotation — i.e., which positive form the flow preserves depends on how i acts, which is exactly the γ freedom.

### Postulate R (register agreement / conjugate parity)

The conjugate conservation structure {Q_j = −1ₙ} — the hyperbola of conserved product −1ₙ, with vertices m± = (0, ±√1ₙ) on the mediator axis — stands to the mediator axis exactly as {Q_j = +1ₙ} stands to the mode axis. Its seats carry one unit of sustained distinction, and the two registers agree wherever both assign a determinate unit: Q_t(m±) = 1ₙ.

**Corollary.** γ = 1. Hence

$$Q_t = Q_i = a^2 + b^2,$$

its unit level set is the circle of radius √1ₙ about C through the four seats {s₊, m₊, s₋, m₋} = {±√1ₙ, ±√1ₙ·j}, and the minimal traversal — the path holding the floor with zero slack — is that circle (any admissible path has Q_i ≥ 1ₙ pointwise; the one holding equality is the unit circle, unique up to the choice of mediator half, i.e. orientation ±i).

Everything in v2.1 §§5–7 now proceeds with C in place of Pₙ: i² = −1 by the unchanged elimination; Q_i rotation-invariant; the mode axis and mediator axis orthogonal at C; and **G orthogonal to B at the seats** — the tangent of G at s₊ is the b-direction (implicit differentiation of a² − b² = 1ₙ at b = 0 gives da = 0), B is the a-direction, and ⟨(0,1),(1,0)⟩_{Q_i} = 0.

### Honest accounting

A general inner product on the plane has three degrees of freedom. The exchange symmetry (the chain's own) removes one; seat calibration removes one; **the imported content is reduced from an entire metric to a single constant**, and that constant is fixed by a parity principle with strong internal motivation — it is "both equally obtained, neither latent" lifted from the mode pair to the pair of conservation structures with products ±1ₙ, and it is the exact structural shape of 此兩者同出⽽異名. But Postulate R is a postulate. Status: signature **[derived]**; diagonal form and α = 1 **[derived]**; γ = 1 **[postulate, internally motivated]**.

---

## 7. Corrections this forces upstream

### 7.1 Pₙ splits into two objects

- **Cₙ — the center**: the origin of the (a,b) plane; both modes at 0ₙ; the crossing of the asymptotes; the unique fixed point of mode conjugation; the frame's local face of P₀. Required as the center of symmetry of the entire structure; unoccupiable by the foundational exclusion. **This is the orbit's center and the referent of "required but unoccupiable."**

- **Sₙ± = G ∩ B — the seats**: occupiable, indeed occupied; the positions of the two modes; the points where gradient and orbit meet (and osculate, §8.1).

Whether the balance locus retains a weighting-level forbidden character (v2.1 Prop 3.2: at X = Y the differential weighting vanishes) is a separable claim at a different structural level and is deferred — note only that at the seats the modes are equal and nonzero, which is equal weighting, not indistinction; the argument that equal weighting collapses to P₀ needs restatement if it is to be kept.

### 7.2 Restatements

Lemma 4.4, Cor 4.5, and Props 3.3–3.4 restate about Cₙ, where their proofs become sound (the segment step of Lemma 4.4 is true of Cₙ). The standoff is the floor Q_i ≥ 1ₙ about Cₙ, now derived in the right order: signature first (Thm 3), form second (Prop 4 + R), minimal traversal last.

### 7.3 The recursion needs re-grounding [open; exploratory]

Pₙ → O₍ₙ₊₁₎ currently generates the child at the vertex. With the correction, the natural candidates are Cₙ (child origin at the parent's center of symmetry) or the seats (where gradient and orbit osculate). One possibility the corrected geometry itself suggests: a child gradient taking the parent's mode axis and mediator axis as its asymptotes has the form a·b = 1₍ₙ₊₁₎, and its seats lie on the parent's null cone — the child's modes obtain exactly where the parent's native distinction vanishes. Generation would then be a 45° register rotation per step, alternating gradient and conjugate, with the unit relation 1₍ₙ₊₁₎ vs 1ₙ computable from the geometry. This is offered because it is what the corrected picture naturally proposes, not because it is derived; status: under test, below the rigor of everything in §§3–6.

### 7.4 DDJ correspondences to re-weigh [convergence register; Will's domain]

The corrected center is a *surrounded void*: the empty hub the thirty spokes converge on (Ch. 11), the vessel's usable emptiness, the bellows' empty middle (Ch. 5), 道沖 (Ch. 4). Arguably a cleaner referent for ⽞ than a vertex on the curve. 守中 :: the a-axis passing through the void, descriptive as before. And Theorem 1 gives 相⽣ concrete content: mutual parturition is realizable *only* through the orbit register. These are re-weighings to be done under the :: discipline against the Guodian layer, not assertions.

---

## 8. Derived consequences (post-metric coherence facts)

Everything in this section presupposes Q_i and is offered as coherence, not foundation.

### 8.1 Osculation and the 1₍ₙ₊₁₎ anchor

G is tangent to the orbit at the seats, and more: the curvature of G at its vertex is 1/√1ₙ (parametrize (√1ₙ cosh t, √1ₙ sinh t); κ(0) = 1/√1ₙ), so the orbit is the **osculating circle** of the gradient at the seats — second-order contact. The standoff radius equals the gradient's radius of curvature at the balance point. The chain's open item "1₍ₙ₊₁₎ is determined by the curvature of Gₙ at Pₙ" acquires a concrete formula: standoff(n) = radius of curvature of Gₙ at its seat = √1ₙ. (Curvature is a metric notion; this cannot ground the construction, but it is exact once Q_i is in hand.)

### 8.2 Register oscillation and the double cover

On the orbit (a, b) = √1ₙ(cos θ, sin θ):

$$Q_j = 1_n \cos 2\theta.$$

The native register reads the orbiting position as oscillating at **twice** the orbital frequency: +1ₙ at the mode seats, 0 at the null-cone crossings (45° + k·90°), −1ₙ at the mediator seats. One traversal cycle = two native cycles. This gives an exact structural referent to the chain's "e^{i·0} and e^{i·2π}: same value, different structural depth," and it is the double-cover signature stated in the frame's own terms.

### 8.3 Sum and difference — 同出⽽異名

With register shares u = a², v = b²:

- Q_i = u + v (conserved on the orbit)
- Q_j = u − v (conserved on the gradient)

The two algebras' invariants are the **sum and the difference of the same pair**. Two expressions, same origin, different register. [Convergence remark under ::; Will to weigh against 此兩者同出⽽異名.]

### 8.4 The null cone's derived role

The orbit crosses the asymptote directions exactly where the native register reads zero: at 45°, all sustained distinction is orbit-register distinction. The traversal is precisely the device that carries distinction through the gradient's blind directions.

### 8.5 Physics [candidate; verify against sources — machine memory, no citations checkable]

The corrected picture is the standard phase-space geometry of **minimum-uncertainty Gaussian states**. In the (x, p) plane of a harmonic oscillator: the i-flow is the free evolution (phase rotation); the j-flow is the squeeze transformation (x ↦ e^r x, p ↦ e^{−r} p), whose orbits are the hyperbolas xp = const with two branches; the two generators sit together in Sp(2,ℝ) ≅ SU(1,1). The forbidden Cₙ is the classical rest point, excluded by the floor Δx·Δp ≥ ħ/2 — the frame's conserved unit reading as 1ₙ :: ħ/2; zero-point motion is the minimal orbit about the point the system cannot occupy — the chain's existing zero-point correspondence, now with the full geometry attached. And quadrature variances of a squeezed state under free evolution oscillate at 2ω — the cos 2θ fact of §8.2 appearing as textbook physics. If this holds up against sources, it is the framework's cleanest single physics convergence: both algebras, the floor, the forbidden center, the orbit, and the double frequency in one standard structure.

---

## 9. What this note does not close

1. **Postulate Q** — that distinction measures are quadratic forms. Carried by the native register and by v2.1's own Thm 6.1 step, but not derived.

2. **Postulate R** — γ = 1 by register agreement / conjugate parity. Internally motivated; still a postulate. Without it the construction is closed only up to the mediator scale.

3. **The seating of the conjugate mode** on the negative branch of G is an interpretive commitment the chains underdetermine; Theorems 1–3 depend on it.

4. **The recursion re-grounding** (§7.3) is open, and the 45°-cascade proposal is exploratory.

5. **Dimensional uniqueness** — untouched, as before.

### Summary of status shifts proposed for the chains

- **Independence-to-orthogonality**: from [derived] to [derived: signature and diagonal form; postulate: mediator scale γ = 1].
- **Orbit existence**: from posited-then-repaired to [derived as necessity (Thm 1) + minimal traversal under the derived form].
- **Pₙ**: split into Cₙ [required, unoccupiable, orbit center] and Sₙ± [seats, occupiable].

The framework's credibility has rested on exactly this kind of explicit downgrade-and-repair; this note is written to that standard.

---

*Draft v0.1. Machine-drafted (Claude, Fable 5). Requires independent verification before entering canon.*
