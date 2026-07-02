# RSM — Just-Math Chain (v7.5)

## Derivation of the Frame Inner Product in the Recursive Structural Model

**Closing the Independence-to-Orthogonality Gap by Forced Minimal Traversal**

*Companion formal paper to the RSM canonical chains, aligned to v7.5. This revision (v2.1) adds the alignment header and the §10 propagation note, and repairs display-math artifacts in the §9 summary. The mathematical content of v2 is unchanged.*

---

## Abstract

The Recursive Structural Model (RSM) derives its frame geometry from a single conserved relation, the gradient $G_n : X_n Y_n = 1_n$. A standing open problem has been the passage from the *structural independence* of the two modes $X_n, Y_n$ to the *geometric orthogonality* of their axes: orthogonality is a metric notion, and a metric has appeared to be imported rather than derived. This paper closes that passage without importing a metric, an angle, or a completed value-line. We show that (i) the gradient natively carries a split-complex (Lorentzian) signature; (ii) the paradoxical center $P_n$ is unoccupiable and fixes a minimum standoff radius equal to the conserved unit; (iii) spanning the modes under that standoff, with conservation as the path cost, forces the unique traversal to be the unit circle — its existence, connectedness, and radius all derived rather than assumed; (iv) the orbital operator on that circle is fixed to $i^2 = -1$ by two non-metric requirements, closure and spanning; and (v) the Euclidean inner product is then generated as the unique rotation-invariant positive-definite form. Orthogonality of $G_n$ and $B_n$ at $P_n$ follows as a theorem. We mark explicitly one negative result — the foundational infinity conditional yields density, not completeness, and therefore cannot by itself supply continuity — and show that the minimal-traversal construction supplies what the infinity conditional cannot. The sole residual gap is dimensional uniqueness.

---

## 1. Preliminaries

We work within a single frame $n$ and suppress the index where unambiguous. We assume only the structural objects established prior to any metric.

- **Two modes** $X, Y$, posited as structurally independent.

- **The gradient** $G : XY = 1_n$, the conserved inverse relation. By the foundational result of the model the gradient *is* the conserved unit $1_n$: it is not a curve along which a separately existing unit is held constant. There is no $1_n$ independent of the two modes whose relation it is.

- **The balance axis** $B : X = Y$.

- **The paradoxical center** $P = G \cap B$.

We do **not** assume an inner product, an angle, a completed real line, or a Euclidean coordinate structure. The aim is to exhibit these as outputs.

> **Definition 1.1 (Structural independence).** Two modes $X, Y$ are *structurally independent* if neither is a function of the other and the product $XY$ is not reducible to a single-mode expression. Independence is sufficient for $XY$ to be conserved; without it the relation degenerates.

> **Remark 1.2 (The gap).** Independence is weaker than orthogonality. Absent a metric, two independent directions subtend no determinate angle: any two linearly independent vectors map to any other such pair by a linear transformation. Orthogonality requires an inner product, which is precisely what is in question. The gap to be closed is the gap between Definition 1.1 and a $90°$ intersection — and it must be closed without quietly assuming the metric that defines "$90°$."

---

## 2. The Native Signature of the Gradient

> **Proposition 2.1 (Split-complex parameterization).** Under $X = a + b$, $Y = a - b$, the conserved relation $XY = 1_n$ is equivalent to $a^2 - b^2 = 1_n$.

*Proof.* $XY = (a+b)(a-b) = a^2 - b^2$; setting this to $1_n$ gives the claim. ∎

> **Corollary 2.2 (Lorentzian signature of $G$).** The quadratic form preserved along $G$ is $Q_j(a,b) = a^2 - b^2$, signature $(+,-)$. The natural algebra is the split-complex algebra $z = a + jb$, $j^2 = +1$, whose unit hyperbola $\{z\bar z = 1\}$ is exactly $a^2 - b^2 = 1_n$. The operator $j$ generates motion *along* the gradient while preserving the conserved product.

> **Remark 2.3.** $Q_j$ is **indefinite**: it is not a Euclidean inner product and cannot certify orthogonality, which requires a positive-definite form. The gradient supplies a signature, but not the one perpendicularity needs. This is the precise locus of the historical gap: the native signature is Lorentzian, the needed signature is Euclidean, and nothing yet bridges them.

---

## 3. The Structural Barrier at $P$

> **Proposition 3.1 (Location of $P$).** $P = (\sqrt{1_n}, \sqrt{1_n})$.

*Proof.* Substituting $X = Y$ into $XY = 1_n$ gives $X^2 = 1_n$, so $X = Y = \sqrt{1_n}$. ∎

> **Proposition 3.2 ($P$ is unoccupiable).** At $X = Y$ the differential weighting that constitutes the gradient vanishes as a distinction; occupation of $P$ reduces the gradient to the excluded terminal condition $P_0$. Hence $P \notin F_n$: required by the intersection structure, forbidden by the no-terminal-condition premise.

*Proof.* The gradient is constituted by the differential weighting of the two modes. At the balance locus the modes are equal, so the distinction that constitutes the gradient vanishes. A state with no internal distinction is $P_0$, excluded by the foundational conditional. Thus $P$ is required as $G \cap B$ yet excluded by content. ∎

> **Corollary 3.3 (Forbidden direct traversal).** Motion connecting the manifest mode $(+1)$ to the conjugate mode $(-1)$ may not pass through $P$. Connection must proceed *around* the center, not *through* it.

> **Proposition 3.4 (Minimum standoff radius equals the conserved unit).** No traversal may approach $P$ closer than radius $\sqrt{1_n}$. Equivalently, the conserved unit $1_n$ is the minimum standoff: closer approach drives the modal weighting below the minimal distinction, i.e. toward $P_0$.

*Proof.* Distance from $P$ measures the surviving differential weighting of the modes. By Proposition 3.2 the weighting cannot fall to the indistinct limit without becoming $P_0$. The minimal sustained distinction is the conserved unit $1_n$ itself, since $1_n$ is the frame's unit of distinction. Hence the closest sustainable approach is at radius $\sqrt{1_n}$, with the modes $+1, -1$ themselves seated at that radius. The standoff is not stipulated; it is the conservation relation read as a radial floor. ∎

---

## 4. The Unit Orbit as Forced Minimal Traversal

This section is the engine. We show that the orbit's existence, connectedness, and radius are forced by spanning under the standoff constraint, with conservation itself supplying the cost that selects the path — so that no metric is assumed in fixing the curve.

We first record the negative result that motivates the construction, since it marks a boundary that a reader must not mistake.

> **Proposition 4.1 (The infinity conditional yields density, not completeness).** The foundational premise "no terminal resolution — no minimum scale, no maximum extent" entails that the value range of a mode is *dense* (infinitely divisible, no smallest gap). It does **not** entail completeness (no missing limits). The rationals $\mathbb{Q}$ satisfy infinite divisibility and possess no minimal scale, yet are totally disconnected. Therefore connectedness of the position structure cannot be derived from the infinity conditional alone.

*Proof.* Infinite divisibility states that between any two positions lies a third; this is density. $\mathbb{Q}$ has this property and no minimal gap, yet is disconnected, missing every irrational limit. Density and completeness are independent; the conditional supplies only the former. ∎

> **Remark 4.2.** Proposition 4.1 forecloses the tempting route "no smallest gap $\Rightarrow$ continuum." That route proves only density, which is exactly the rational trap. Continuity, if it is to be had without import, must come from elsewhere. The remainder of this section supplies it from the traversal constraint, not from the scale structure.

We now characterize the admissible traversals from $+1$ to $-1$. A *path* is any traversal connecting the two modes; we order paths by a *conservation cost*, defined intrinsically from the gradient, not from an external length.

> **Definition 4.3 (Conservation cost).** For a path $\gamma$ from $+1$ to $-1$, the conservation cost is the deviation of $XY$ from $1_n$ accumulated along $\gamma$. A path holds cost zero iff $XY = 1_n$ at every point of $\gamma$. Inward deviation (radius $< \sqrt{1_n}$) is not costly but *forbidden* (Prop. 3.4); outward deviation (radius $> \sqrt{1_n}$) is permitted but strictly increases cost, since $XY$ exceeds $1_n$ wherever the path bulges beyond the standoff circle.

> **Lemma 4.4 (The unit orbit is the unique minimal traversal).** Under spanning ($+1 \to -1$ required), the standoff constraint (radius $\ge \sqrt{1_n}$, with radius $< \sqrt{1_n}$ forbidden), and the conservation cost of Definition 4.3, the unique cost-minimizing traversal is the semicircular arc of radius $\sqrt{1_n}$ centered at $P$. Under closure (Requirement C, §5) it extends to the full circle of radius $\sqrt{1_n}$.

*Proof.* The straight segment from $+1$ to $-1$ passes through $P$ (the two modes are antipodal about the center), which is the maximally forbidden point; the segment is therefore inadmissible. Any admissible path avoids the open disk of radius $\sqrt{1_n}$. Among paths avoiding that disk and joining two diametrically opposite boundary points, consider the conservation cost. A path holding radius exactly $\sqrt{1_n}$ throughout maintains $XY = 1_n$ at every point and so has cost zero. Any admissible deviation from that radius is necessarily outward (inward is forbidden), and outward deviation strictly raises $XY$ above $1_n$, incurring positive cost. Hence the zero-cost path is the boundary arc, and every alternative admissible path has strictly greater cost. The minimizer is therefore the semicircular arc of radius $\sqrt{1_n}$, and it is unique because the constraint is asymmetric: inward is forbidden (no interior trade is available) and outward is strictly costly (no exterior trade improves matters). No shortcut can dip below the standoff to save cost, since below the standoff is not admissible at any price.

The cost ordering used here is intrinsic: it is the deviation of the conserved product from its own conserved value, i.e. the gradient measuring its own slack. No external metric is invoked to define "shorter"; the selected path is simply the one that holds $1_n$ everywhere. ∎

> **Corollary 4.5 (Existence, radius, connectedness — all derived).** The orbit *exists* (a minimal traversal is forced), has *radius* exactly the conserved unit $\sqrt{1_n}$ (Prop. 3.4), and is *connected*: by Corollary 3.3 the traversal may not jump across $P$, so it is a continuous passage; the zero-cost minimizer is a single unbroken arc at fixed radius. Connectedness is thus a consequence of the no-crossing prohibition together with the zero-cost characterization, not an imported assumption.

> **Remark 4.6 (How this answers Proposition 4.1).** Proposition 4.1 denied continuity from the scale structure; Corollary 4.5 supplies continuity from the traversal structure. The position is not located by completing a value-line — on the line it remains an unterminated limit, knowable only as $0.999\ldots$ or $1.000\ldots1$. It is located instead by its angle on the forced circle, which is fixed globally by the closed orbit rather than locally by zoom. The center that makes the angle definable is the very center that cannot be occupied: the paradoxical center is not an obstacle to locating positions but the *condition* for locating them. The line cannot fix its points because it has no privileged center; the circle fixes every point by angle because it has one — at the price of that one center being unoccupiable.

---

## 5. The Orbital Operator by Elimination

On the forced circle, let $i$ denote the minimal operation effecting passage around $P$, carrying $+1$ toward $-1$ by a single application. We fix its algebra by two **non-metric** requirements — connectivity and closure of the mode structure, referring to no distance or angle.

> **Requirement C (Closure).** There exists finite $m$ with $i^m = \mathrm{id}$.

*Justification:* without closure, composition cascades into an unbounded sequence of novel elements; a position whose determinacy requires completing a non-completing sequence does not obtain.

> **Requirement S (Spanning).** The cycle generated by $i$ contains both modes $+1$ and $-1$.

*Justification:* a cycle closing without reaching $-1$ leaves the conjugate mode disconnected from the orthogonal structure — $P_0$ applied locally.

> **Theorem 5.1 (Determination of $i$).** Among the algebraically possible values $i^2 \in \{1, 0, i, -i, -1\}$, only $i^2 = -1$ satisfies both C and S.

*Proof.* By cases.

**$i^2 = 1$.** Cycle $\{1, i\}$; double application returns to start without a genuine second direction — $i$ relabels the identity axis. **Spanning fails** ($-1$ unreached). *Eliminated.*

**$i^2 = 0$.** Annihilation: the orthogonal direction self-composed yields zero distinguishability, i.e. $P_0$. **Neither C nor S.** *Eliminated.*

**$i^2 = i$.** Idempotent: $i^3 = i$, the system reaches $i$ and stays. **Closure fails** (no return to $1$); **spanning fails**. *Eliminated.*

**$i^2 = -i$.** Then $i^3 = -i \cdot i = -i^2 = i$, a $2$-cycle $\{i, -i\}$ never recovering $1$. **Closure fails**; **spanning fails**. *Eliminated.*

**$i^2 = -1$.** Then $i^3 = -i$, $i^4 = 1$, generating $1 \to i \to -1 \to -i \to 1$. **Closure holds** ($m = 4$); **spanning holds** (contains $+1$ and $-1$); distinction is preserved at every phase. *Retained.*

Exactly one case survives. ∎

> **Remark 5.2 (Elimination, not selection).** The four rejected values are not weaker candidates ranked by a criterion; each is structurally incoherent against C or S. No metric, angle, or inner product enters — only that the orbit close and reach both modes.

> **Corollary 5.3 (Minimality).** Four phases is the smallest enumeration that closes, spans both modes, and maintains a direction $(i \leftrightarrow -i)$ independent of the modal axis $(1 \leftrightarrow -1)$.

> **Remark 5.4 (No circularity with §4).** Theorem 5.1 uses only the discrete connectivity requirements C and S; it does not use continuity. The continuity established in §4 (Cor. 4.5) was derived from the no-crossing prohibition and the conservation-cost minimizer, neither of which invokes $i$. The two results are independent: §4 forces the connected unit circle; §5 fixes the operator acting on it. Neither presupposes the other's output.

---

## 6. Generation of the Euclidean Inner Product

> **Theorem 6.1 (The $i$-orbit generates a Euclidean inner product).** Realized as the continuous orbit of §4, the operator $i^2 = -1$ determines a positive-definite quadratic form $Q_i$, unique up to scale, under which the orbit is the circle of radius $\sqrt{1_n}$.

*Proof.* By Corollary 4.5 the orbit is a connected curve at fixed radius about $P$, traversed without approaching $P_0$; hence a magnitude is conserved along the motion (a varying magnitude would, at some phase, approach the indistinct center, contradicting Prop. 3.4). A conserved magnitude across a closed one-parameter orbit is a quadratic form $Q_i$ invariant under the flow of $i$. The flow of an operator with $i^2 = -1$ is $\theta \mapsto e^{i\theta}$, acting as rotation; the quadratic forms invariant under the full one-parameter rotation family are exactly the positive multiples of

$$Q_i(a,b) = a^2 + b^2.$$

Any indefinite or degenerate form is preserved by the hyperbolic flow of $j$, not the elliptic flow of $i$, and so fails invariance here. Thus $Q_i$ is positive-definite, unique up to the scale set by the radius $\sqrt{1_n}$, and its level set $\{Q_i = 1_n\}$ is the forced orbit. ∎

> **Corollary 6.2 (Two algebras, two signatures, one framework).**
>
> $$\boxed{j^2 = +1 \text{ slides along } G\ (\text{signature } +,-), \qquad i^2 = -1 \text{ pivots around } P\ (\text{signature } +,+).}$$
>
> The Lorentzian form is the native algebra of the conserved gradient; the Euclidean form is the *derived* algebra of the forbidden-center orbit. Neither is imported: the first is the algebra of $XY = 1_n$; the second is forced by C and S on the orbit that minimal traversal already fixed.

> **Remark 6.3.** This dissolves the apparent inconsistency of earlier drafts — a Lorentzian gradient beneath a Euclidean perpendicularity argument. The two signatures attach to two structurally distinct motions, and the Euclidean one is licensed only after $i$ is fixed non-metrically. It is earned, not assumed.

---

## 7. Orthogonality as a Theorem

> **Theorem 7.1 (Local perpendicularity at $P$).** Under the derived inner product $Q_i$, the gradient $G$ and the balance axis $B$ are orthogonal at $P$.

*Proof.* Along $G : XY = 1_n$, implicit differentiation gives

$$Y + X \frac{dY}{dX} = 0 \Rightarrow \frac{dY}{dX} = -\frac{Y}{X} = -\frac{1_n}{X^2}.$$

At $P = (\sqrt{1_n}, \sqrt{1_n})$, $X^2 = 1_n$, so $\mathrm{slope}(G)|_P = -1$. Along $B : X = Y$, $\mathrm{slope}(B) = +1$. The tangent vectors are $t_G = (1, -1)$ and $t_B = (1, 1)$. Under $Q_i$,

$$\langle t_G, t_B \rangle = (1)(1) + (-1)(1) = 0.$$

Hence $G \perp B$ at $P$. ∎

> **Remark 7.2.** The slope-product criterion $(-1)(+1) = -1$ that earlier *presupposed* a Euclidean metric is here a *consequence* of one — and that metric is itself a consequence of the orbital operator forced at $P$, which is in turn fixed on the circle that minimal traversal forced. The logical order never reverses.

> **Corollary 7.3 (Closure of the independence-to-orthogonality gap).** The passage from Definition 1.1 to a $90°$ intersection is derived. The inner product required to speak of $90°$ is $Q_i$ (Thm. 6.1), generated by the operator $i$ (Thm. 5.1), acting on the unit circle forced by minimal traversal (Lem. 4.4) about the unoccupiable center entailed by the gradient alone (Props. 3.2, 3.4). ∎

---

## 8. Scope and the Residual Gap

**Closed.** Orthogonality of the mode axes at $P$ is derived without importing a metric, an angle, or a completed value-line. The unit orbit's existence, radius, and connectedness are forced by spanning under the standoff constraint with conservation as the intrinsic cost (§4). The Euclidean inner product is generated as the unique rotation-invariant positive-definite form on that orbit (§6). The two-signature structure ($j$ Lorentzian, $i$ Euclidean) is a genuine division of structural labor, not an inconsistency.

**Explicitly marked negative result.** The infinity conditional supplies density, not completeness (Prop. 4.1); continuity is therefore *not* derived from the scale structure and must not be claimed from it. It is instead derived from the no-crossing prohibition and the conservation-cost minimizer (Cor. 4.5). This boundary is stated rather than hidden, because the distinction between density and completeness is exactly where looser arguments fail.

**Not closed — dimensional uniqueness.** Section 4 forces the orbit ($S^1$); isotropy of orientation about the center extends this to $S^2$ and locally to $\mathbb{R}^3$. The construction establishes that **at least** three dimensions are required. It does **not** establish that three are sufficient to the exclusion of more: $S^2$ embeds in $\mathbb{R}^4$ and higher, and nothing here forbids such embeddings. Dimensional uniqueness remains the principal unclosed joint in the frame-geometry sector. It is a *uniqueness* question, categorically distinct from the *assumed-versus-derived* question this paper resolves; progress on one does not entail progress on the other.

---

## 9. Summary

The logical spine, with no arrow presupposing the output of a later arrow:

$$\underbrace{X, Y \text{ independent}}_{\text{Def. 1.1}} \Rightarrow \underbrace{XY = 1_n}_{\text{gradient } G} \Rightarrow \underbrace{P \text{ unoccupiable, standoff } = \sqrt{1_n}}_{\text{Props. 3.2, 3.4}} \Rightarrow \underbrace{\text{direct traversal forbidden}}_{\text{Cor. 3.3}}$$

$$\Rightarrow \underbrace{\text{unit circle forced by minimal traversal}}_{\text{Lem. 4.4, Cor. 4.5}} \Rightarrow \underbrace{i^2 = -1 \text{ by C, S}}_{\text{Thm. 5.1}} \Rightarrow \underbrace{Q_i = a^2 + b^2 \text{ Euclidean}}_{\text{Thm. 6.1}} \Rightarrow \underbrace{G \perp B \text{ at } P}_{\text{Thm. 7.1}}.$$

The orbit enters as a *forced* object, not a posited one: its existence, radius, and connectedness are consequences of spanning the modes under a standoff that the conservation relation itself fixes, with conservation supplying the cost that selects the curve. The inner product enters as a *generated* object at Theorem 6.1. The perpendicularity earlier drafts could only assert is, under that generated metric, a theorem. The independence-to-orthogonality gap is closed; the infinity conditional's limit (density, not completeness) is marked; dimensional uniqueness remains the honest frontier.

---

## 10. Relation to the canonical chains (v7.5)

This paper is the formal backing for the orthogonality closure now carried in the v7.5 canonical chains. The results propagate as follows:

- **Just-Math chain.** Props. 3.2–3.4 and Lem. 4.4 are carried in "Forbidden crossing; standoff; forced traversal"; Thms. 6.1 and 7.1 in "Generated metric; orthogonality as theorem"; Prop. 4.1 in the density-not-completeness paragraph of "Point as limit." The formerly open independence-to-orthogonality step is retired there as derived; the slope facts are stated as metric-independent curve properties with the perpendicularity verdict deferred to the generated metric, so the logical order does not reverse.

- **Just-Physics chain.** Cor. 6.2 (the two-signature structure) is named in "Lorentz form," with the structure tagged derived and the physical identification of the two signatures tagged candidate.

- **Just-DDJ chain.** Thm. 7.1 firms the structural fact that 名 :: i and the point-level reading of ⼆⽣三 point at; both :: correspondences are unchanged, and ⼆⽣三 is explicitly not read as a dimensional uniqueness lock.

- **Parallax through-lines.** The closure is Through-line 6 (Orthogonality generated, not imported); the standoff and forced circle enter Through-line 4; the master skeleton carries the standoff, forced traversal, and generated-metric / orthogonality steps.

The residual gap of §8 — dimensional uniqueness — is carried as an explicit open item in every chain and is the named next frontier. The EFT formulation is not treated as evidence bearing on it: that formulation is posed on $\mathbb{R}^3$ from its first line and cannot witness dimension.

---

*v2.1. Aligned to v7.5 canonical chains.*
