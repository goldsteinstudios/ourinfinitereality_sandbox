# Derivation of the Frame Inner Product in the Recursive Structural Model

### Closing the Independence-to-Orthogonality Gap via a Two-Algebra Construction

**Abstract.** The Recursive Structural Model (RSM) derives its frame geometry from a single conserved relation, the gradient $G_n: X_n Y_n = 1_n$. A standing open problem in the formal development has been the move from the *structural independence* of the two modes $X_n, Y_n$ to the *geometric orthogonality* of their axes: orthogonality is a metric notion, and a metric appears to be imported rather than derived. This paper closes that gap. We show that the gradient natively carries a split-complex (Lorentzian) structure, that the paradoxical center $P_n$ forbids direct traversal and thereby forces a distinct orbital operator, and that this operator is fixed to $i^2 = -1$ by two non-metric structural requirements — closure and spanning. The Euclidean inner product is then not assumed but *generated* as the unique metric under which the $i$-orbit is realizable. The perpendicularity of $G_n$ and $B_n$ at $P_n$ follows as a theorem rather than a stipulation. We isolate the one residue the construction does not remove: the uniqueness of dimension three.

-----

## 1. Preliminaries

We work within a single frame $n$ and suppress the index where unambiguous. We assume only the structural objects established prior to any metric:

- **Two modes** $X, Y$, posited as structurally independent variables.
- **The gradient** $G: XY = 1_n$, the conserved inverse relation. By the foundational result of the model, $G$ *is* the conserved unit $1_n$; it is not a curve along which a separately existing unit is held constant.
- **The balance axis** $B: X = Y$, the exchange-symmetry locus.
- **The paradoxical center** $P = G \cap B$.

We do **not** assume an inner product, a notion of angle, or a Euclidean coordinate structure. The aim is to show these are outputs of the construction, not inputs.

> **Definition 1.1 (Structural independence).** Two modes $X, Y$ are *structurally independent* if neither is a function of the other and the product $XY$ is not reducible to a single-mode expression. Independence is sufficient for the product $XY$ to be conserved; without it the conserved relation degenerates.

> **Remark 1.2.** Independence is weaker than orthogonality. In a space without a metric, two independent directions subtend no determinate angle: any two linearly independent vectors can be carried to any other such pair by a linear map. Orthogonality requires additional structure — an inner product — which is precisely what is in question. The gap to be closed is the gap between Definition 1.1 and a $90^\circ$ intersection.

-----

## 2. The Native Signature of the Gradient

We first show that the gradient carries a metric signature of its own, without external imposition, and that this signature is Lorentzian rather than Euclidean.

> **Proposition 2.1 (Split-complex parameterization).** *Under the substitution*
> $$X = a + b, \qquad Y = a - b,$$
> *the conserved relation $XY = 1_n$ is equivalent to the modulus condition*
> $$a^2 - b^2 = 1_n.$$

*Proof.* $XY = (a+b)(a-b) = a^2 - b^2$. Setting this equal to $1_n$ gives the claim. $\square$

> **Corollary 2.2 (Lorentzian signature of $G$).** The quadratic form preserved by motion along $G$ is $Q_j(a,b) = a^2 - b^2$, of signature $(+,-)$. The natural algebra of this motion is the split-complex algebra $z = a + jb$ with $j^2 = +1$, whose unit “circle” ${z : z\bar z = 1}$ is exactly the hyperbola $a^2 - b^2 = 1_n$.

> **Interpretation 2.3.** The operator $j$ generates the flow *along* the gradient: it slides a point along $G$ while preserving the conserved product. This is the model’s native motion. Crucially, $Q_j$ is **indefinite**: it is not an inner product in the Euclidean sense, and it cannot by itself certify orthogonality, which requires a positive-definite form. The gradient supplies a signature, but not the one the perpendicularity claim needs. This is the precise locus of the historical gap.

-----

## 3. The Structural Barrier at $P$

We now show that the gradient’s own motion is obstructed, and that the obstruction forces the introduction of a second, distinct operator.

> **Proposition 3.1 (Location of $P$).** $P = (\sqrt{1_n}, \sqrt{1_n})$.

*Proof.* Substituting $X = Y$ into $XY = 1_n$ gives $X^2 = 1_n$, hence $X = Y = \sqrt{1_n}$. $\square$

> **Proposition 3.2 ($P$ is unoccupiable).** At $X = Y$ the weighting that constitutes the gradient becomes structurally indistinct; occupation of $P$ reduces the gradient to the excluded terminal condition $P_0$ at the gradient’s level. Hence $P \notin F_n$: the center is structurally required (as $G \cap B$) yet cannot be inhabited.

*Proof sketch.* The gradient is constituted by the differential weighting of the two modes. At the balance locus the modes are equal, so the weighting that distinguishes them vanishes as a distinction. A state with no internal distinction is $P_0$, excluded by the foundational conditional. Thus $P$ is required by the intersection structure but excluded by the no-terminal-condition premise. $\square$

> **Corollary 3.3 (Forbidden direct traversal).** Motion generated by $j$ along $G$ cannot pass through $P$. To connect the manifest mode $(+1)$ to the conjugate mode $(-1)$, traversal must proceed *around* $P$ rather than *through* it.

The split-complex flow is therefore insufficient to realize the required connection between modes. A second operator — call it $i$ — must govern motion around $P$. We make **no geometric assumption** about $i$; we fix its algebra by structural requirements alone.

-----

## 4. The Orbital Operator by Elimination

Let $i$ denote the minimal structural operation that effects passage around $P$, carrying the manifest mode toward the conjugate mode by a single application. We require two properties, both **non-metric** — they refer only to the connectivity and closure of the mode structure, not to any notion of distance or angle.

> **Requirement C (Closure).** There exists a finite $m$ with $i^m = \mathrm{id}$. *Justification:* if no such $m$ exists, composition cascades into an unbounded sequence of novel elements, and a position whose determinacy requires the completion of a non-completing sequence does not obtain. A point that never closes is not a point.

> **Requirement S (Spanning).** The cycle generated by $i$ contains both modes $+1$ and $-1$. *Justification:* a cycle that closes without reaching $-1$ leaves the conjugate mode disconnected from the orthogonal structure — $P_0$ applied locally. The operator exists precisely to connect the modes; failing to reach $-1$ defeats its reason for existing.

> **Theorem 4.1 (Determination of $i$).** *Among the five algebraically possible values of $i^2$ in ${1, 0, i, -i, -1}$, only $i^2 = -1$ satisfies both Requirement C and Requirement S.*

*Proof.* We treat each case.

**Case $i^2 = 1$.** The cycle is ${1, i}$ with $i^2 = 1$. Double application returns to the start without producing a genuinely new direction: $i$ is a relabeling of the identity axis. Closure holds trivially, but **Spanning fails** — $-1$ is never reached. *Eliminated.*

**Case $i^2 = 0$.** Composition annihilates: the orthogonal direction compounded with itself yields zero distinguishability, i.e. $P_0$ directly. **Neither C nor S** holds. *Eliminated.*

**Case $i^2 = i$.** Idempotent: $i^3 = i^2 \cdot i = i \cdot i = i$, and the system reaches $i$ and remains there. **Closure fails** (no return to $1$); **Spanning fails** ($-1$ never reached). *Eliminated.*

**Case $i^2 = -i$.** Then $i^3 = i^2 \cdot i = -i \cdot i = -i^2 = i$, producing the $2$-cycle ${i, -i}$ that never recovers $1$. **Closure fails** in the strongest sense; **Spanning fails** ($-1$ never reached). *Eliminated.*

**Case $i^2 = -1$.** Then $i^3 = -i$, $i^4 = 1$, generating
$$1 ;\to; i ;\to; -1 ;\to; -i ;\to; 1.$$
The cycle **closes** ($i^4 = \mathrm{id}$, so C holds with $m=4$) and **spans** (it contains both $+1$ and $-1$, so S holds). It connects the modes through orthogonal intermediates and preserves distinction at every phase. *Retained.*

Exactly one case survives both requirements. $\square$

> **Remark 4.2 (Method is elimination, not selection).** The four rejected values are not weaker candidates ranked against a criterion; each is shown structurally incoherent against C or S. What remains is the unique coherent possibility. No metric, angle, or inner product entered the argument — only the demands that the orbit close and that it reach both modes.

> **Corollary 4.3 (Minimality).** Four phases is the smallest enumeration that closes, spans both modes, and maintains a direction $(i \leftrightarrow -i)$ independent of the modal axis $(1 \leftrightarrow -1)$. The retained structure is therefore minimal as well as unique.

-----

## 5. Generation of the Euclidean Inner Product

We now show that the operator fixed in §4 *generates* a positive-definite metric, rather than presupposing one.

> **Theorem 5.1 (The $i$-orbit generates a Euclidean inner product).** *The realization of $i^2 = -1$ as a continuous, distinction-preserving orbit determines a positive-definite quadratic form $Q_i$, unique up to scale, under which the orbit is the unit circle $S^1$.*

*Proof.* Extend the discrete cycle ${1, i, -1, -i}$ of Theorem 4.1 to a continuous one-parameter family generated by $i$. Distinction preservation requires that no phase of the orbit collapse toward $P_0$, i.e. that the “size” of the orbiting element be conserved across the motion; were it not conserved, some phase would approach the indistinct center, contradicting the unoccupiability of $P$ (Prop. 3.2). A conserved size across a closed one-parameter orbit is, by definition, a quadratic form $Q_i$ invariant under the flow of $i$.

The flow of an operator with $i^2 = -1$ is $\theta \mapsto e^{i\theta}$, acting as rotation. The quadratic forms invariant under all such rotations are exactly the positive multiples of
$$Q_i(a,b) = a^2 + b^2,$$
the positive-definite Euclidean form; any indefinite or degenerate form fails to be preserved by the full one-parameter family (an indefinite form is preserved by the *hyperbolic* flow of $j$, not the *elliptic* flow of $i$). Hence $Q_i$ is positive-definite, and is unique up to the overall scale set by the orbit radius. The orbit ${Q_i = r^2}$ is the circle $S^1$. $\square$

> **Corollary 5.2 (Two algebras, two signatures, one framework).** The framework carries two operators serving two structural functions:
> $$\boxed{,j^2 = +1 \text{ slides along } G \text{ (signature } +,-),; \qquad i^2 = -1 \text{ pivots around } P \text{ (signature } +,+),.}$$
> The Lorentzian form is the native algebra of the conserved gradient; the Euclidean form is the *derived* algebra of the forbidden-center orbit. Neither is imported: the first is the algebra of $XY = 1_n$, the second is the algebra forced by C and S at $P$.

> **Remark 5.3.** This dissolves the apparent inconsistency noted in earlier drafts — that the gradient is Lorentzian while the perpendicularity argument is Euclidean. The two signatures are not in competition; they attach to two structurally distinct motions. The Euclidean signature is licensed only after $i$ is fixed by non-metric requirements, so it is earned, not assumed.

-----

## 6. Orthogonality as a Theorem

With the Euclidean inner product $Q_i$ now derived, the perpendicularity of $G$ and $B$ at $P$ is no longer a stipulation resting on a smuggled metric. It is a computation in the metric the framework has generated.

> **Theorem 6.1 (Local perpendicularity at $P$).** *Under the derived inner product $Q_i$, the gradient $G$ and the balance axis $B$ are orthogonal at $P$.*

*Proof.* Along $G: XY = 1_n$, implicit differentiation gives
$$Y + X\frac{dY}{dX} = 0 ;\Rightarrow; \frac{dY}{dX} = -\frac{Y}{X} = -\frac{1_n}{X^2}.$$
At $P = (\sqrt{1_n}, \sqrt{1_n})$, $X^2 = 1_n$, so $\mathrm{slope}(G)|_P = -1$. Along $B: X = Y$, $\mathrm{slope}(B) = +1$. The tangent vectors are $t_G = (1, -1)$ and $t_B = (1, 1)$. Under $Q_i$,
$$\langle t_G, t_B \rangle = (1)(1) + (-1)(1) = 0.$$
Hence $G \perp B$ at $P$. $\square$

> **Remark 6.2.** The slope-product criterion $\mathrm{slope}(G)\cdot\mathrm{slope}(B) = (-1)(+1) = -1$ that earlier appeared to *presuppose* a Euclidean metric is here a *consequence* of one — and that metric is itself a consequence of the orbital operator forced at $P$. The logical order is: independence $\Rightarrow$ conserved gradient $\Rightarrow$ forbidden center $\Rightarrow$ orbital operator $i^2=-1$ (by C, S) $\Rightarrow$ Euclidean $Q_i$ $\Rightarrow$ orthogonality. No step imports the conclusion of a later step.

> **Corollary 6.3 (Closure of the independence-to-orthogonality gap).** The move from Definition 1.1 (structural independence) to a $90^\circ$ intersection is fully derived. The inner product required to speak of $90^\circ$ is the form $Q_i$ of Theorem 5.1, generated by the operator $i$ of Theorem 4.1, which is fixed by the non-metric requirements C and S at the center $P$ whose existence follows from the gradient alone. $\blacksquare$

-----

## 7. Scope and the Residual Gap

We state plainly what the construction does and does not establish.

**Closed.** The orthogonality of the mode axes at $P$ is derived without importing a metric. The Euclidean inner product is generated as the unique rotation-invariant positive-definite form licensed by the orbital operator, which is itself fixed by closure and spanning — both non-metric. The two-signature structure ($j$ Lorentzian, $i$ Euclidean) is shown to be a genuine division of structural labor rather than an inconsistency.

**Not closed — dimensional uniqueness.** Theorem 5.1 generates $S^1$ in the orbital plane, and isotropy of orientation about the center extends this to $S^2$ and hence locally to $\mathbb{R}^3$. The construction establishes that **at least** three dimensions are required for the orbit-plus-orientation structure. It does **not** establish that three are *sufficient to the exclusion of more*: $S^2$ embeds in $\mathbb{R}^4$ and higher, and the present argument contains nothing that forbids such embeddings. Dimensional uniqueness therefore remains open and is, after this paper, the principal unclosed formal joint in the frame-geometry sector.

> **Remark 7.1.** The residual gap is of a different character than the one closed here. The independence-to-orthogonality gap was a question of whether a needed structure (the metric) was derived or assumed; it is now derived. The dimensionality gap is a question of *uniqueness* — whether the derived structure is forced to be minimal. These should not be conflated, and progress on one does not entail progress on the other.

-----

## 8. Summary

The logical spine of the closure is:

$$
\underbrace{X, Y \text{ independent}}*{\text{Def. 1.1}}
;\Rightarrow;
\underbrace{XY = 1_n}*{\text{gradient } G}
;\Rightarrow;
\underbrace{P = G\cap B \text{ unoccupiable}}*{\text{Prop. 3.2}}
;\Rightarrow;
\underbrace{\text{direct traversal forbidden}}*{\text{Cor. 3.3}}
$$
$$
;\Rightarrow;
\underbrace{i^2 = -1 \text{ by C, S}}*{\text{Thm. 4.1}}
;\Rightarrow;
\underbrace{Q_i = a^2 + b^2 \text{ Euclidean}}*{\text{Thm. 5.1}}
;\Rightarrow;
\underbrace{G \perp B \text{ at } P}_{\text{Thm. 6.1}}.
$$

Each arrow is a derivation, and no arrow presupposes the output of a later arrow. The inner product enters the framework at Theorem 5.1 as a generated object, and the perpendicularity that earlier drafts could only assert is, under that generated metric, a theorem. The independence-to-orthogonality gap is closed; dimensional uniqueness remains the honest frontier.