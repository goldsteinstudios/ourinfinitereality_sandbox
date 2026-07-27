# Cross-model audit: v7.5 and v7.7, checked on their own arithmetic

**Date:** 2026-07-27 · **Status:** audit record, not a chain. Nothing here enters canon.
**Re-runnable:** `python3 rsm/audit/cross_model_checks.py` (Parts A and B are this document's;
Part C is v9's).

> ## ⚠ READ THIS FIRST — superseded in part by v9 (same day)
>
> This audit was written before the v9 chains were in the repo. **It is not current criticism of
> v9.** Fates, verified in `v9_comparison_r1.md`:
>
> | Section | Fate in v9 |
> |---|---|
> | §1 — Lemma 4.4 is arithmetically false | **Not carried.** v9 dropped the apparatus and went further: the measure is now "definitional-by-register" and `[unaudited]`. |
> | §2 — Thm 6.1's silent quadratic-form restriction | **Stated in the open** by v9. |
> | §3 — the all-directions lemma's borderline reason | **Moot.** v9 dropped the four-step derivation entirely. |
> | §4 — appendix chart hygiene | **Appendix gone.** A sharper related issue replaces it (the parturition map's dropped offset). |
> | **§5 — the physics "excised point"** | **STILL LIVE, verbatim in v9.** The only finding here that still applies. |
>
> The closing section's protocol point (silent replacement) recurred at v7.7→v9 and is now
> Divergence Ledger **Entry 004**.

The `v7.5_vs_v7.6c_findings.md` audit compared two drafts against each other and priced claims partly
by which draft owned them. This pass does the opposite: every checkable claim in **both** drafts is
recomputed from scratch, and the verdict is whatever the arithmetic says. Two of the five v7.5
theorems nobody had ever machine-checked turn out to matter — one of them is false, and its falsity
changes how the v7.5→v7.7 transition should be described.

Division of labor holds throughout: **everything below is arithmetic.** Where a finding implies a
wording or ranking change, it is flagged as needing a ruling, not applied.

---

## Summary

| Claim | Owner | Verdict |
|---|---|---|
| Prop. 2.1 — split-complex parameterization | v7.5 | **holds** (exact) |
| Prop. 4.1 — density is not completeness | v7.5 | **holds** (logic; nothing to compute) |
| Thm. 5.1 — the five-case elimination table | v7.5 | **holds** (exact) |
| Thm. 7.1 — perpendicularity at the seat | v7.5 | **holds** (exact) |
| Thm. 6.1 — the generated inner product | v7.5 | **holds only among quadratic forms**; the restriction is silent |
| **Def. 4.3 + Lem. 4.4 — the conservation-cost argument** | **v7.5** | **FALSE** — see §1 |
| Appendix items 1–3, 5, 8–12, 14–19, 21–23 | v7.7 r4 | **all re-verified independently** |
| Theorems 1 (wall/door) and 2 (toll) | v7.7 r4 | **re-derived; hold**, including the general IVT form |
| Measure step 4 — "positivity selects Q_i" | v7.7 r4 | conclusion **holds**; stated reason is **borderline** — see §3 |
| Appendix items 5 and 23 use "z" for two charts | v7.7 r4 | **hygiene flag** — see §4 |
| Ten flagged physics claims, checked against sources | v7.7 r1 physics | **nine confirmed**, one imprecise — see §5 |

Nothing in v7.7's mathematics was refuted. The two v7.7 items that moved are wording matters with the
results intact; the physics chain has one wording fix that lands on *better* physics than it had.

---

## 1. v7.5's Lemma 4.4 is not circular. It is arithmetically false.

This is the substantive finding.

The prior audit left this as **Open item 1**: *"Can Prop. 3.4's radius `√1ₙ` be stated before `Q_i`
exists? If not, v7.5's conservation-cost argument was circular and r5's retreat to `F` + `T` is
correct."* `checks.py §9` answered the dependency question — yes, circular. But nobody checked
whether the lemma's central computation is *true*, and it is not.

**Definition 4.3** defines the conservation cost as the deviation of `XY` from `1ₙ` along a path, and
asserts that outward deviation "strictly increases cost, since `XY` exceeds `1ₙ` wherever the path
bulges beyond the standoff circle." **Lemma 4.4** then asserts that "a path holding radius exactly
`√1ₙ` throughout maintains `XY = 1ₙ` at every point and so has cost zero."

Both assertions are false, and the second is false by a wide margin:

- On the circle of radius `√1ₙ`, `XY = Q_j = 1ₙ·cos 2θ`. It equals `1ₙ` at exactly two points (the
  seats) and reaches `−1ₙ` at the conjugate seats. Maximum deviation along the claimed zero-cost arc
  is **2**, not 0. The path v7.5 calls costless is the path of *maximal* cost under v7.5's own
  definition.
- "Outward ⟹ `XY > 1ₙ`" fails immediately: at `(a,b) = (0,2)`, radius 2 is outside the standoff
  circle and `XY = −4`.
- The chart-ambiguity escape is closed. v7.5 says the arc is "centered at `P`," so I also checked the
  circle of radius 1 about `P = (1,1)` in the `(X,Y)` chart. `XY = 1ₙ` fails there too.

And the failure is not repairable by picking a different curve, because **no zero-cost spanning path
exists at all.** A cost-zero path holds `XY = 1ₙ` everywhere, so it lies entirely on `Gₙ`; on `Gₙ`,
`a² = 1ₙ + b² ≥ 1ₙ`, so `|a| ≥ 1` and `a` never reaches 0; a continuous path on `Gₙ` therefore cannot
change the sign of `a`, and the two seats have opposite signs. The cost functional does not select a
minimizer among admissible paths — its minimum is not attained by anything, and its stated minimum is
not a minimum.

**Consequences.**

1. **Open item 1 is closed, harder than expected.** The answer is not "circular, so the retreat is
   correct." It is: the argument was *both* circular and false, and the retreat was forced.
2. **Corollary 4.5 falls with it.** v7.5's existence, radius, and connectedness results for the orbit
   were all carried by Lemma 4.4. So v7.5's §9 spine — the arrow "unit circle forced by minimal
   traversal" — has no support.
3. **A pricing correction, needing a ruling.** The v7.5-vs-v7.6c audit §8 recorded the continuity
   change as *"a retreat, honestly declared"*, contrasting v7.5's derivation ("from an intrinsic cost
   with no metric assumed") favorably against r5's postulate. That comparison should be struck. There
   was nothing to retreat from. **Ruling requested: does `v7.5_vs_v7.6c_findings.md` §8 get a strike
   note, as §2 and §5-B already carry?**
4. **v7.7 is independently right here.** Theorem 1 (the wall: `Gₙ`'s two components are separated,
   and `e^{jφ}` preserves them) and Theorem 2 (the toll: every spanning path crosses into `Q_j < 0`)
   are the correct statements of exactly this ground. I re-derived Theorem 2 in its general form
   rather than just on the minimal traversal — by the intermediate value theorem any continuous
   spanning path avoiding `Oₙ` has `a = 0` somewhere, where `Q_j = −b² < 0` — and confirmed it on 200
   random spanning polylines. The chain states the result only on the minimal traversal; the general
   form is stronger and is now in the script.

**The pattern worth recording.** This is the machine-draft hazard running in the *opposite* direction
from the seating error. The seating error was a false closure that got flagged as a `[commitment]` and
audited. Lemma 4.4 was a false closure that got *no* flag, read as rigorous, was called the paper's
"engine" in its own §4 header, and survived into a document that called itself sealed — because its
prose was careful about the thing it was not doing (importing a metric) while being wrong about the
thing it was doing (computing a product). Careful hedging on one axis reads as rigor on all axes.

---

## 2. v7.5's Theorem 6.1 assumes what v7.7 names as open

v7.5 Thm. 6.1 concludes that the rotation-invariant conserved magnitude is `Q_i = a² + b²`, "unique up
to scale." Recomputed: among **quadratic forms**, rotation-invariance does force `β = 0, α = γ` — the
`a² − b²`, `ab`, and `a²` candidates each fail invariance, exactly as claimed. But `(a² + b²)²` is
*also* rotation-invariant and is not a quadratic form. The uniqueness claim silently quantifies over
quadratic forms only.

That restriction is precisely v7.7's **Finsler hole** — named in the r4 measure section, left open,
and made conditional on the generation principle (open item 2). So the two drafts make the same
assumption; v7.7 declares it and v7.5 does not. Credit to v7.7's r1 adversarial pass, whose retraction
(the counterexample `r²(2 + cos 4θ)` equals a rational function of frame objects, hence is framed, so
L1 does not exclude it) I verified numerically and exactly — including the stated parallelogram-law
failure of **−8**, which reproduces to machine precision.

---

## 3. The all-directions lemma is exactly non-strict where it needs to bite

r4's measure section, step 4: *"the all-directions lemma (a spanning path in the punctured plane
sweeps ≥ π of directions) forces positive-definiteness — of the two slices, positivity selects `Q_i`."*

The conclusion is right. The stated reason does not carry it.

- The sweep bound is true (300 sampled spanning paths, worst case exactly π — the endpoints are
  antipodal, so the direction from `Oₙ` turns by at least π).
- But `Q_j`'s positive cone `{|a| > |b|}` has angular measure **exactly π**. So "sweeps ≥ π of
  directions" is non-strict precisely at the case it must exclude. A path sweeping exactly π of
  directions is not, by that fact alone, forced out of `Q_j > 0`.
- What actually closes it: that cone is **disconnected** — two opposite sectors — so no continuous
  spanning path can stay inside it. Verified: of 368 spanning paths avoiding `Oₙ`, zero remained
  inside `Q_j > 0`.

**Ruling requested:** restate step 4's reason as connectedness of the positive cone rather than its
angular measure. The result is unaffected; the argument as written invites a reader to check an
inequality that is tight against the very case it rules out. This is the kind of step where an
auditor's "≥ π, and the cone is π, so… ?" is a real stall.

---

## 4. Chart hygiene in the r4 appendix (minor)

Appendix item 5 works in the mode chart `z = X + iY` (where `w = z² − 2i·1ₙ` sends `G` to the child's
x-axis, `B` to the y-axis, the seat to the child origin, `O` to the branch point at depth `2·1ₙ` —
all five verified). Appendix item 23 works in the split chart `z = a + ib` (where `Re z² = XY` and
`Im z² = (X² − Y²)/2` — verified exactly).

Each item is correct **in its own chart**. But both write the bare symbol `z`, and the appendix never
says the symbol switches referent between items. In the other chart, item 23's identities read
`Re z² = X² − Y²`, `Im z² = 2XY` — also verified, and not what item 23 says. Given that the framework's
own diagnosis of the seating error was *four merged types*, an unannounced chart switch inside the
verification appendix is worth one clarifying clause.

Not an error. Flagged because this appendix is the document an auditor will check first.

---

## 5. The physics chain's `[verify against sources]` obligation — discharged for ten claims

The physics chain carries a standing *"physics quantities and results cited here are from machine
memory and inherit a standing `[verify against sources]` obligation."* Ten of its load-bearing physics
statements were checked against textbooks, arXiv, and course notes. **Nine confirm as stated. One is
imprecise and should be reworded.** This is the accuracy axis that does not care which draft owns the
claim, so it belongs in this pass.

**Confirmed as written:** the free-vortex profile (`v_θ = Γ/2πr`, so `v·r` const, irrotational except
on the centerline) · Bekenstein–Hawking `S = k_B·A/4l_P²` and the area-not-volume scaling of the
holographic bound · Wick rotation as Lorentzian QFT ↔ Euclidean stat mech (one analytic object; the
periodic-imaginary-time path integral is `Tr e^{−βH}`) · the spinor double cover (2π acts as −1 on
spin-½, 4π is identity) · the mass shell `E² − (pc)² = (mc²)²` with `m = 0 ⟹ E = pc` on the null cone ·
`Δx·Δp ≥ ℏ/2` and coherent states as minimum-uncertainty saturators · RG coarse-graining running
UV→IR, so the chain's **directionality flag is correctly stated** · the Unruh effect as genuine
observer-dependence of particle number. Also confirmed: the v7.6c-legacy `Sp(2,ℝ) ≅ SU(1,1)` is a true
group isomorphism (for 2×2, symplectic = `det 1`, so `Sp(2,ℝ) = SL(2,ℝ) ≅ SU(1,1)` by Cayley
conjugation).

### The one hit — §5, "the big bang as parturition"

The chain reads the singularity through *"the manifold-excision fit (the singularity as excised point
— unmet origin, not early event)."* **Right in substance, wrong in type.** Standard GR does hold that
the singularity is not part of the spacetime manifold and is not an early event — but it is not a
*point that was excised*. There is no well-defined point to remove; the singularity is diagnosed by
**geodesic incompleteness**, boundary-attachment constructions (b-boundary and kin) are known to be
pathological, and in FLRW it is approached everywhere in space at once rather than at one location.

A relativist would mark "excised point" wrong. Proposed replacement, preserving the reading:

> the singularity is not a point of the manifold at all — an unmet limit diagnosed by geodesic
> incompleteness, not an excised location and not an early event

**The correction improves the rendering rather than costing it.** "Unmet limit, approached everywhere,
never a location" is closer to `Oₙ` than "excised point" ever was — `Oₙ` is the *unmet* crossing whose
arms approach asymptotically. The chain's own typing was better than the physics word it borrowed.
That is worth noting because it is the shape the framework says it wants: the target register refusing
the loose wording and the refusal landing on the more accurate reading.

**Two cosmetic notes, ruling optional.** §7's superfluid-vs-superconductor core contrast is the
textbook statement, but strictly it is the *condensate/order-parameter* density driven to zero, and
³He-B cores are filled with a distinct superfluid phase — which sits closer to the entry's own
"co-presence" reading than the simple case does. §2's Wick rotation is written `t ↦ iτ`; `t ↦ −iτ` is
the more common convention. Both are defensible.

**Rulings requested:** adopt the §5 rewording? Add the §7 parenthetical? Neither is arithmetic;
both are the chain's to state.

---

## What this says about the two-model comparison

The prior audit's method was to read the drafts against each other and let disagreement locate the
error. That worked for the seating error, where the drafts genuinely disagreed. It could not have
found Lemma 4.4, because **v7.7 does not contradict v7.5 there — it silently replaces it.** r5 and
v7.7 swapped in Definition T and stopped mentioning the conservation cost. Read comparatively, that
looks like a retreat from strength. Read arithmetically, it is a correction of a falsehood.

So: divergence between drafts is the data, per the Divergence Ledger — but silent *convergence on a
replacement* is also data, and it is the harder signal to see. When a later draft quietly drops an
earlier draft's load-bearing lemma rather than arguing with it, that is worth a check.

**Suggested ledger protocol addition, for ruling:** when a revision replaces a prior lemma without
refuting it, the prior lemma gets checked before the replacement is priced as a retreat.

---

## Rulings requested (all ontology/pricing; the arithmetic is settled)

1. **§1.3** — strike or annotate `v7.5_vs_v7.6c_findings.md` §8's characterization of the continuity
   change as a "retreat"?
2. **§3** — restate r4 measure step 4's reason as connectedness rather than angular measure?
3. **§4** — add a chart-declaration clause to the r4 appendix?
4. **§5** — adopt the geodesic-incompleteness rewording in the physics chain, and the §7 parenthetical?
5. **The protocol addition** above — does silent replacement join the Divergence Ledger's standing
   checks? (Logged as Divergence Ledger **Entry 003**, pending ruling.)

Arithmetic verdicts above are machine-checked and re-runnable. Nothing here is a ruling; ontology,
referents and readings are Will's.
