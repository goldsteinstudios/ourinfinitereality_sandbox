# Verification notes — arithmetic only

> **Dispositions confirmed by Will's walkthrough (v7.7).** The premise questions these notes tracked
> are now ruled: **Postulate Q** struck (N8, conditional on the generation principle), **FU** dissolved
> (N9, kernel = σ-invariance theorem), **Postulate F** dissolved (N10, via L1), **Postulate R** deleted.
> The "FU renames R" and "v7.5 radius is circular" findings below are absorbed into that walk. See
> `math_chain_walkthrough_ledger_r1.md` (supplements r2–r7). `checks.py` now also carries the Divergence
> Ledger's image-9 check (§10).

**Run:** `python3 rsm/audit/checks.py` (stdlib only; exits non-zero if any claim fails).

Nothing here is a ruling. These are computations, re-runnable and disbelievable. Ontology, referents,
and readings are Will's. Where a finding touches **nodes 6–22 of the walkthrough — unwalked — it is
reported, never propagated.**

Two quantities are written `1ₙ` in both chains. Throughout:

```
Q_j(a,b) = a² − b² = X·Y     the conserved product; what j preserves     (gradient)
Q_i(a,b) = a² + b²           what i preserves; squared distance from Oₙ  (orbit)
X = a + b,  Y = a − b        so  X = Y  ⟺  b = 0  (the balance axis Bₙ)
```

---

## 1. `just_math_v7.5.md` contradicts itself — CONFIRMED

Substituting `X = Y` into `XY = 1ₙ` gives `X = Y = ±√1ₙ`, so `Gₙ ∩ Bₙ` is **two** points,
`(1,1)` and `(−1,−1)` in `(X,Y)`. Their midpoint is `(0,0)`.

- **Prop. 3.1** (`just_math_v7.5.md:51`) names `P = (√1ₙ, √1ₙ)`. It lists only one of the two.
- **Lemma 4.4** (`:85`) says the modes are *"antipodal about the center"* `P`.

A pair with midpoint `(0,0)` is not antipodal about `(1,1)`. `P` names the intersection point and the
origin in one argument.

Independently ruled by the walkthrough ledger, **E3**: *"the conjugate pair `+1`/`−1` is antipodal…
the straight path between conjugates passes through `Oₙ`."* And logged by parallax r1, corrections
ledger entry 4: *"the geometry refused the orbit about `Pₙ`; the orbit centers on `Oₙ`."*

## 2. `1ₙ` names two different quantities — CONFIRMED (ledger O1)

`just_math_v7.6c_r5.md:12`: *"`1ₙ` is the frame's minimal unit of distinction, **identical with the
conserved product**."* The identity is **asserted, not argued.**

Computed: on the circle about `Oₙ`, `Q_i` is constant at `1ₙ` while `Q_j` sweeps `1ₙ·cos 2θ`. They
agree at exactly `θ = 0°, 180°` — i.e. `b = 0` — i.e. exactly at `Gₙ ∩ Bₙ`. Nowhere else.

So "minimal unit of distinction" (a `Q_i` claim: the standoff, radius²) and "the conserved product"
(a `Q_j` claim) are **two quantities with one coincidence, located at the seats.** Whether that
coincidence is derived or stipulated is O1, and it is Will's.

Further: `Q_i` is orientation-invariant; `Q_j` cannot be written down without first choosing an
orientation. `Gₙ : XₙYₙ = 1ₙ` therefore fixes `θ = 0` silently — the gradient is a chart choice
wearing the clothes of a definition.

## 3. E2 seat-phase structure — CONFIRMED

`seatₖ = √1ₙ·iᵏ`. `Q_i = 1ₙ` at all four; `Q_j = (−1)ᵏ1ₙ`. Seats `k = 0,2` lie on `Gₙ`
(`Pₙ` and `ν(Pₙ)`); seats `k = 1,3` lie on the conjugate family. The double cover appears in the
enumeration, as the ledger states.

## 4. Orbit–gradient contact — CONFIRMED

`Q_i|_{Gₙ} = 1ₙ + 2b²`, so `Q_i ≥ 1ₙ` on `Gₙ` with equality only at `b = 0`. The orbit meets the
gradient at `±Pₙ` **and nowhere else**, with a shared tangent and opposite-sign curvature off the
contact point (r5's "mirror osculation").

## 5. Every `Pₙ` is the nadir of its own gradient — CONFIRMED (Will's)

For every orientation `θ`, the rotated pair `(G_θ, B_θ)` meets at radius exactly `√1ₙ`, and that
point is the minimum of `Q_i` along `G_θ`. Hence *"all `Pₙ` points are equidistant from `Oₙ`"*.

**Caution.** Sweeping `θ` traces a circle of **candidates**. Within one frame there are **four**
`Pₙ`: `Gₙ ∩ Bₙ` gives two, the quarter-turn gives two more. Whether the rest of the circle is
populated is open item 8 (branching-at-any-position) and is **not** settled here. DDJ r4 says the
same from the other side: "a two-parameter continuum of *candidate* child-origins… the geometry gives
the sphere and does not license firing everywhere on it."

## 6. Isotropy forces `ℝ³`, then reaches a fixed point — CONFIRMED (Will's)

Two modes give a plane. Rotating the circle through every orientation about the shared origin sweeps a
sphere that leaves the plane: **`ℝ³` is forced.** Rotating the *sphere* through every orientation
returns the sphere: nothing further is swept. The construction stops at three.

**This does not close dimensional uniqueness.** `S²` still embeds in `ℝ⁴`; in four dimensions the same
demand would carry `S²` to `S³`, equally stable. The framework never *generates* `ℝ⁴` — which is not
the same as excluding it. It relocates the burden. Do not write it into a chain as a closure.

## 7. FU family-invariance is vacuous — CONFIRMED. Nodes 6–22, unwalked.

`Q_t = α·a² + γ·b²`. FU asserts the seats carry the distinction magnitude `|c|`.

- Primary family (`XY = +μ1ₙ`, seats at `b = 0`): native `Q_j(seat) = +μ`. FU gives `α = 1`. The
  native reading agrees. **No work is done.**
- Conjugate family (`XY = −μ1ₙ`, seats at `a = 0`): native `Q_j(seat) = −μ`, which would give
  `γ = −1` — not positive-definite. Only by reading the seat as carrying `+μ` does `γ = +1`.

`μ` cancels for every `μ`, trivially. **The entire content is the sign-blindness kernel**, not the
family invariance. So FU does not discharge Postulate R; it renames it.

**But**: rotating `XY = 1ₙ` by 90° gives `XY = −1ₙ`. The "two families" are **one gradient at two
orientations**, so the sign-blindness kernel *is orientation-isotropy restated*. If T3's
no-unframed-distinction lemma derives isotropy, it derives the kernel — **by T3, not by family
invariance.** That is a live route to discharging a premise, and it belongs to the walkthrough.

## 8. v7.5's standoff argument presupposes the metric it derives — CONFIRMED. Nodes 6–22.

Dependency check, not arithmetic:

| Where | What it says |
|---|---|
| Prop. 3.4 (`:61`) | "No traversal may approach `P` closer than **radius** `√1ₙ`" |
| Lem. 4.4 (`:85`) | "avoids the open **disk** of radius `√1ₙ`"; "**outward** deviation" |
| Rem. 2.3 (`:45`) | `Q_j` is **indefinite** — "cannot certify orthogonality" |
| Thm. 6.1 (`:133`) | `Q_i`, the positive-definite form, is **derived here** |

"Radius", "disk", and "outward" require a positive-definite form. `Q_j` is not one; `Q_i` is not yet
available. §§3–4 measure distance with a metric earned in §6.

⇒ v7.5's "forced traversal" is **not** a closure, and should stop being listed as one.
⇒ r5's retreat to Postulate F + Definition T is the correct repair.

---

## Claims of mine that did not survive

Recorded so they are not silently reused. All four share one mechanism: *a set was found that matched,
and an identity was declared.* That is the seating error.

1. *"`Pₙ` is unoccupiable because `Xₙ = Yₙ` cancels the duality."* Wrong quantity — that is `Q_j`, and
   `Q_j = 1ₙ ≠ 0` at `Pₙ`. Also wrong vocabulary, per ledger R2.
2. *"`Pₙ` and `Oₙ` are forbidden twice, once from each frame; `|1|` from below, `|0|` from above."*
   Withdrawn. Ledger C3: the locus is *realized* in the parent's expression. Realized is not forbidden.
3. *"Distinction is the freeness of the `⟨i⟩` action."* Refused by Will.
4. *"The orbit and the `Pₙ`-locus are the same set."* Withdrawn — conflates the four-position minimal
   cycle `1 → i → −1 → −i` with the continuum circle. See §5.
