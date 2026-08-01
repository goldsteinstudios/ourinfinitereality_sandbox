# RSM — Just-Physics Chain, Consolidated & Annotated (v7.6-candidate)

**Provenance.** Consolidates the Just-Physics Chain v7.5 against the v7.6-candidate math consolidation (which integrated the Signature Forcing Note v0.1's Cₙ/Sₙ± correction, verified Theorems 1–3, named the premise set Q/F/R/T, and corrected v0.1's osculation claim). Machine-drafted (Claude, Fable 5) at Will's request. Discipline unchanged: convergence register; physics vocabulary names structural facts the derivation has independently established; the convergence is the evidence; no single register is the evidence. All mathematical claims below were re-verified symbolically during drafting; physical facts recalled from memory are tagged *[verify against sources]* per the v0.1 note's own standard — I have no source access in this environment and citations should be independently checked.

**What this document does.** (1) Propagates the Cₙ/Sₙ± split through every physics correspondence and reports where it strengthens, weakens, or re-words each one. (2) Reports one finding of unusual weight: **the physics chain's own language was already pointing at Cₙ before the math correction existed** (§V.1) — a register-independence datum of exactly the kind the parallax method is supposed to produce. (3) Corrects one physical claim in v7.5 (the tokamak wording, §V.4) and sharpens one falsifiable prediction (divergence vs exclusion, §V.5). (4) Derives one new cross-register fact: the AM-GM relation between the two floors (§V.2). (5) Carries the status ledger and propagation notes.

**Annotation convention.** ⟦ANN⟧ blocks are editorial. Status tags per CAVP: *[derived]*, *[derived modulo named postulates]*, *[candidate]*, *[falsifiable]*, *[under test]*, *[open]*.

-----

# Part V — Verification and analysis report

**V.1 The physics register anticipated the correction.** v7.5's forbidden-center section reads: "The **zero-product position** — simultaneously precise conjugate quantities — is the forbidden center." The zero-product position is where both conjugate spreads vanish simultaneously — in the mode plane, the point (0ₙ, 0ₙ). That is Cₙ, the crossing of the asymptotes, not the vertex Pₙ = (√1ₙ, √1ₙ) that the sealed math chain carried as the forbidden center. Likewise "quantum ground states are non-zero in energy; a system cannot rest at the forbidden center" — the point the system cannot rest at is the phase-space **origin**, the classical rest point: Cₙ again. And the GR line — "singularities behave as centers the theory gestures toward but cannot inhabit" — gestures at a center of the geometry, not a vertex on a curve.

In every one of its forbidden-center instances, the physics register was already using the corrected referent while the math register carried the wrong one. Under the parallax method this is evidence of the strong kind: two registers compressing the same structure, one of which silently held the geometry the other had to be repaired into. It should be recorded as such, not merely patched. *[verified against the texts themselves]*

**V.2 New derived cross-register fact: the two floors and AM-GM.** The math consolidation established (coherence fact, verified): on Gₙ, Q_i = 1ₙ + 2b² ≥ 1ₙ, equality exactly at the seats — the gradient touches the distinction floor exactly where the modes sit. Its physical face assembles as follows, re-verified symbolically:

- The uncertainty relation Δx·Δp ≥ ℏ/2 is the **gradient-register floor**: the boundary hyperbola Δx·Δp = ℏ/2 is Gₙ itself under 1ₙ :: ℏ/2, and the forbidden region below it contains Cₙ.
- The **orbit-register floor** Q_i ≥ 1ₙ reads (natural units, symmetric quadratures) as (Δx² + Δp²)/2 ≥ ℏ/2 — the zero-point energy floor.
- The two floors are related by AM-GM: Δx² + Δp² − 2ΔxΔp = (Δx − Δp)² ≥ 0, so **the gradient floor implies the orbit floor, with equality exactly at Δx = Δp — the seat.** On the minimum-uncertainty hyperbola, energy minimizes at the seat with value exactly the conserved unit: E_min = ℏ/2, achieved by the symmetric minimum-uncertainty state (the ground/coherent state).

So the physical instantiation is precise: **the uncertainty relation is the Q_j floor; zero-point energy is the Q_i floor; AM-GM is the seats-touch-the-floor fact; and the ground state occupies the seat.** The seat is occupiable and occupied — by the ground state — while Cₙ (the rest point) is excluded. This upgrades v7.5's zero-point correspondence from *[candidate]* prose to a candidate with an exact formal skeleton, and it dissolves a latent problem in the old picture: under Pₙ-as-forbidden-vertex, the balanced minimum-uncertainty state would have been forbidden, but coherent states are not merely allowed, they are the most classical states there are. The correction was physically necessary, not just formally. *[structure derived; physical identification candidate; verify against sources]*

**V.3 Theorem 1's physical instances.** The mode-disconnection theorem (the conservation locus has two branches; the j-flow cannot connect them) has two standard physical faces, both re-checked at the level I can check:

- **Phase-space:** the squeeze flow (x ↦ eʳx, p ↦ e⁻ʳp) preserves the product xp *and the signs of x and p*: no squeezing carries a state to its phase-space conjugate (−x, −p). Only the i-flow — phase rotation, i.e. dynamical evolution — does, and the half-period map is exactly mode conjugation ν: e^{iπ}(x,p) = (−x,−p). Spanning is realized by the orbit register and only by it; in Sp(2,ℝ), the squeeze subgroup does not contain −I, the rotation subgroup does. *[verified symbolically; group-theoretic framing verify against sources]*
- **Mass shell:** with a :: E, b :: p, the invariant hyperbola a² − b² = m² has two sheets (E > 0, E < 0); the j-flow is the boost; orthochronous Lorentz transformations (connected to the identity) preserve sheets. No boost connects the particle sector to the negative-energy sector; physics connects them only through a different register (the field structure — Feynman–Stückelberg reading of the negative sheet as antiparticles). The seats (±m, 0) are the rest states of the two sectors; Cₙ is the origin of energy-momentum — nothing there — unoccupiable by any state. *[candidate; standard physics from memory, verify against sources]*

Both instances give 相生's derived content (from the math consolidation: mutual parturition is unrealizable on the gradient, obtains only through the orbit register) concrete physical shape: inversion of a mode is never achieved by sliding along the conservation relation; it requires the second register. *[candidate]*

**V.4 One correction to v7.5: the tokamak wording.** "Tokamak plasma cannot occupy the **magnetic-field axis**" is wrong as stated: the magnetic axis is the degenerate flux surface at the center of the plasma cross-section, and plasma density and temperature typically *peak* there — it is the most occupied place in the machine. What confined plasma cannot occupy is the torus's **axis of symmetry** — the central column through the hole, around which the toroidal winding organizes. The corrected wording is also the structurally apt one: the axis of symmetry is the Cₙ-analogue (unoccupied center of symmetry about which the traversal winds), while the magnetic axis is seat-like (the occupied locus the structure organizes onto). Recommend the fix; the candidate survives it and reads better. *[correction; verify against sources]*

**V.5 Prediction 6 must be split.** v7.5: "Energy cost of approaching any paradoxical center diverges." The corrected geometry distinguishes two behaviors that this sentence conflates:

- **Divergence** attaches to the **pole-directions** (the asymptote faces of P₀): sliding along the gradient toward either pole, Q_i diverges — on xp = ℏ/2, forcing Δx → 0 drives E = (Δx² + Δp²)/2 → ∞. Squeezing costs divergent energy. *[verified on the formal skeleton]*
- **Exclusion** attaches to the **center**: Cₙ is not approached at diverging cost along any admissible path; it is floored out entirely (Postulate F — the region below the floor does not obtain at any price). The old "inward is not costly but forbidden" line of the math chain said this correctly; the prediction's wording did not.

Revised prediction 6 (proposed): *6a. The energy cost of driving either mode of a conserved pair toward its pole-direction diverges. 6b. No physical system occupies its structure's center of symmetry at any energy; approach is bounded by a floor, not priced by a divergence.* Both remain falsifiable; 6b is in fact the sharper claim. *[falsifiable, reworded]*

**V.6 Speculative but natural: the orbit register and Euclidean methods.** The two algebras (j split-complex/Lorentzian; i complex/Euclidean) map in standard physics onto the Minkowski and Wick-rotated (Euclidean) sectors, and the standard device for computing traversals that no real-time classical path achieves — tunneling amplitudes, instantons — is precisely passage to the Euclidean register. Theorem 1 (no path within the conservation class) plus orbit-register traversal is structurally the instanton pattern: connection between classically disconnected configurations, computed in the signature the i-algebra carries. Offered as a candidate correspondence only, at the outer edge of what the derivation licenses; it should not enter the chain body until the mapping is made exact. *[candidate; exploratory; verify against sources]*

-----

# Part C — The consolidated chain

Convergence register. Physics vocabulary names structural facts the derivation has independently established.

## Foundational conditional

If physical reality has no terminal resolution in either direction, then neither a minimum length nor a maximum extent obtains. *[unchanged]*

## Excluded terminal condition

Two faces of P₀: a terminal minimum scale (a Planck floor read as absolute smallest length) and a terminal maximum extent — both structurally excluded. Within any physical regime, operational absence and operational distinction are limit-states approached asymptotically. The vacuum is not absolute nothing; apparent scale-limits are boundaries of currently inhabited frames. *[derived; unchanged]*

## Inverse conservation: the Gₙ form in physics

Xₙ · Yₙ = 1ₙ: two co-varying quantities whose product is the regime's conserved unit. Clean instances as equalities:

- Wavelength × frequency = c (EM radiation in vacuum). *[good fit]*
- Pressure × volume = constant (Boyle's law, fixed T); the full ideal gas law is not an instance except isothermally. *[good fit at fixed T; correction retained from v7.5]*

**Branch occupancy is register-dependent** *(new)*: variance- and magnitude-registers (λ, f; P, V; Δx, Δp) are confined to the positive branch — the conjugate branch is formal there. Amplitude-registers (x, p as signed phase-space coordinates; E, p on the mass shell) physically occupy both branches, and there the mode-disconnection theorem has direct physical content (§V.3). A correspondence stated in one register-type must not borrow branch structure from the other. *[discipline note]*

## Bound relations, floors, and the forbidden center

The uncertainty relations Δx·Δp ≥ ℏ/2, ΔE·Δt ≥ ℏ/2 are floors, not equality conservations. The boundary hyperbola is Gₙ under 1ₙ :: ℏ/2; the forbidden region below it contains the zero-product position — both conjugate spreads simultaneously vanishing — which is **Cₙ**: required as the structure's center of symmetry, unoccupiable in fact. The two structures (equality conservation, bounded floor) remain distinct — and are now *related*: the floor is the gradient-register face of Postulate F, and the orbit-register floor (Q_i ≥ 1ₙ :: zero-point energy) follows from it by AM-GM, with equality exactly at the seat (§V.2). *[forbidden center derived; specific operators candidate; AM-GM relation verified on the formal skeleton]*

**The seat is occupied.** The symmetric minimum-uncertainty state — the ground/coherent state — sits at Δx = Δp with E = ℏ/2: the physical occupant of Sₙ. The structure is not "everything shuns the center"; it is "the modes sit at the seats, the ground state among them, while the center about which they sit does not obtain." *[candidate; formally exact skeleton]*

Forbidden centers across regimes, referents corrected to Cₙ-analogues:

- Quantum systems cannot rest at the phase-space origin; zero-point motion is the minimal orbit about the point the system cannot occupy. *[candidate]*
- GR singularities behave as centers the theory gestures toward but cannot inhabit. *[candidate]*
- Confined tokamak plasma cannot occupy the torus's **axis of symmetry** (wording corrected from "magnetic-field axis," which is occupied — indeed peak-occupied; §V.4). *[candidate; corrected]*

## Mass and energy

E = mc²: within a child frame, mass and energy as the two modes and c² as 1₂ — observed correspondence, not derived inverse-form conservation. Placement convergence-register, not core. Untouched by the center correction. *[candidate; unchanged]*

## Lorentz form and the two signatures

Under Xₙ = a + b, Yₙ = a − b, the conservation becomes a² − b² = 1ₙ — the 1+1 invariant interval. The formal correspondence xy = 1 ↔ X² − T² = 1 is exact. *[derived]*

The two signatures are one division of structural labor: split-complex j (signature +,−) native to the gradient; complex i (signature +,+) generated on the orbit. Status updated per the math consolidation: *[derived modulo Postulate Q, with the mediator scale γ = 1 by Postulate R]* — the "derived" tag of v7.5 was slightly overclaimed and is repriced, not weakened in substance. Theorem 2 adds the physical sharpening: the native Lorentzian measure vanishes and reverses sign on **every** spanning traversal — the necessity of the second signature is arithmetic, not preference. *[derived modulo Q]*

The identification of the two algebras with the spacetime interval (Lorentzian) and the local spatial metric (Euclidean, as generated orbit metric) remains *[candidate]*. The mass-shell instance (§V.3) — two sheets, boosts preserve sheets, seats at rest states ±m, Cₙ at the origin of energy-momentum — is proposed as the cleanest physical instance of the disconnection theorem in this register. *[candidate]*

The 3+1 extension X² + Y² + Z² − T² = 1ₙ remains formal; physical significance open. Time enters through the signature, not as a fourth spatial axis. *[unchanged]*

## Time and recession

Irreversibility of generation (an origin cannot un-obtain), strict ordering as the structural content of linear succession, compounding recession of origins: **all retained as derived — the argument depends only on origins obtaining, not on the generation site, and survives the recursion re-grounding untouched.** *[derived]*

The candidate reading of accelerating cosmological recession as structural recession of origins (recession without expanding medium, distinct from a dark-energy term) is retained as the strongest cosmological candidate; its distinguishing signature against ΛCDM remains open. One added flag: any *quantitative* development of this candidate now waits on the recursion re-grounding (which site generates, and the 1₍ₙ₊₁₎ unit relation), which is the math chain's top-ranked open item. *[candidate; quantitative development blocked on re-grounding]*

## Locally flat, globally curved

GR's local-Minkowski / global-Lorentzian structure as one instance of the locally-flat / globally-curved dynamic; the local spatial metric as the generated orbit metric. Status: the generated-metric claim now reads *[derived modulo Q, F, R, T]*; the spacetime identification *[candidate; strong]*. *[substance unchanged]*

## Three-dimensional substrate at every scale

Each regime locally recovers ℝ³; local axis orthogonality is the derived metric of the forbidden-center orbit — about Cₙ — not imported. Recursion produces new coordinate systems, each its own ℝ³, not higher dimensions. Three necessary; uniqueness open (S² embeds in ℝ⁴ and higher). The EFT formulation is not evidence here: posed on ℝ³ from its first line. *[derived: three necessary, metric modulo named postulates; uniqueness open; unchanged in substance]*

## Recursion across physical regimes

Regimes nest as a branching structure of new coordinate systems generated at parents' forbidden centers; no regime terminal in either direction. **Inherits the re-grounding flag**: whether generation sites are Cₙ-analogues (centers of symmetry) or seat-analogues (occupied balance loci) is open in the math chain, and physical instances should not be sorted into that scheme until it settles. The branching-at-any-position generalization remains under test. *[derived structure; site open; generalization under test]*

## Toroidal structures under privileged gradients

Where a single gradient operates and direct crossing is forbidden, persistent structure organizes around an axis or centerline. Referent discipline added: the unoccupied organizing axis is the Cₙ-analogue (torus's axis of symmetry; the tree's pith axis as centerline of the flow, with the arboreal detail in its own essay); occupied density maxima (magnetic axis; cambial tissue) are seat-analogues. Whether all persistent life is toroidal remains open. *[candidate; open; wording corrected per V.4]*

## Energy as misalignment cost

Energy as the cost of misalignment between a structural object's symmetry and the privileged gradient at its scale — minimum at alignment, increasing with misalignment. The divergence clause is re-worded per V.5: cost **diverges toward the pole-directions** (squeezing along the gradient toward either asymptote); the **center is excluded by the floor, not priced by a divergence**. Zero-point energy as the Q_i floor — the cost of not being at the center — now carries the exact skeleton of §V.2 rather than prose only. This remains the physical home of the 無為/為 correspondence carried in the DDJ chain. *[candidate; skeleton verified]*

## The oscillator as the flagship convergence *(new section, promoted from v0.1 §8.5 with the two-level discipline added)*

The corrected geometry is the standard phase-space geometry of the harmonic oscillator, at **two distinct levels that must not be conflated**:

- **Amplitude level** — the (x, p) plane: i-flow = free evolution (phase rotation); j-flow = squeezing (preserves xp, preserves branch); half-period evolution = mode conjugation ν; Q_i = energy; the energy shell = the orbit; xp on the shell oscillates as −E·sin 2θ — the double-cover fact as textbook physics; Cₙ = the classical rest point. *[verified symbolically on the formal skeleton]*
- **Variance level** — the (Δx, Δp) quadrant: Gₙ = the minimum-uncertainty hyperbola with 1ₙ :: ℏ/2; the floor structure of §V.2; the ground state at the seat.

Both levels instantiate the same geometry; they are different probes of it (parallax within a single system). If the standard-physics identifications hold against sources, this is the framework's cleanest single convergence: both algebras, both floors, the forbidden center, the occupied seat, the orbit, and the double frequency in one elementary system. *[candidate; verify against sources]*

## Probes and the parallax method

Retained unchanged (fMRI, CT, optical, electron, mass-spec as aspect-disclosing probes) — with §V.1 added as a reflexive instance: the physics and math registers acted as parallax probes of the framework itself, and the physics register carried the correct center before the math register did. *[method; V.1 recorded]*

## Six falsifiable predictions (revised numbering preserved)

1. No persistent physical structure without a paradoxical center — referent: an unoccupied center of symmetry (Cₙ-analogue), distinct from occupied seats. *[falsifiable; referent clarified]*
2. Persistence proportional to gradient depth at boundaries. *[falsifiable; unchanged]*
3. Terminated recursion co-inherent with a hardened surface. *[falsifiable; unchanged]*
4. Power-law scaling between nesting levels in persistent recursive structures. *[falsifiable; unchanged]*
5. At least three spatial dimensions necessary for structural persistence. *[falsifiable; unchanged]*
6. Split per V.5 — **6a.** Energy cost of driving either mode of a conserved pair toward its pole-direction diverges. **6b.** No physical system occupies its structure's center of symmetry at any energy: approach is bounded by a floor, not priced by a divergence. *[falsifiable; reworded — 6b is the sharper claim]*

-----

# Part L — Status ledger

| Item | v7.5 status | Consolidated status |
|---|---|---|
| Forbidden-center referent | Pₙ (vertex) in math; effectively Cₙ in physics prose | **Cₙ throughout**; physics register recorded as having anticipated the correction (V.1) |
| Uncertainty floor | bounded-floor structure, distinct from conservation | retained, plus **derived relation to the orbit floor via AM-GM**, equality at the seat |
| Zero-point energy | candidate, prose | candidate with exact formal skeleton: Q_i floor; ground state at the seat |
| Minimum-uncertainty balanced state | (implicitly forbidden under old Pₙ) | **occupied seat** — latent contradiction dissolved |
| Tokamak instance | "magnetic-field axis" (physically wrong) | **axis of symmetry** (corrected); candidate retained |
| Two-signature structure | derived | derived modulo Q; γ = 1 by R (repriced per math ledger); Theorem 2 adds arithmetic necessity |
| Lorentz-form disconnection | — | mass-shell two-sheet instance proposed *[candidate]* |
| Spanning-by-orbit-only | — | squeeze-vs-rotation instance; ν = half-period *[verified skeleton; candidate identification]* |
| Irreversibility / linear time / recession | derived / candidate | unchanged; recession's quantitative development flagged as blocked on recursion re-grounding |
| Local ℝ³ metric | derived | derived modulo Q, F, R, T |
| Prediction 6 | single divergence claim | split into 6a (divergence at poles) / 6b (exclusion at center) |
| Wick/instanton reading | — | exploratory candidate, held out of chain body (V.6) |

# Part O — Open items, ranked

1. **Source-verify the oscillator flagship** (Sp(2,ℝ) ≅ SU(1,1); squeeze conventions; 2ω quadrature oscillation; coherent-state facts). Highest value-per-effort: if it holds, it becomes the chain's anchor convergence.
2. **Recursion re-grounding** (inherited from math): blocks quantitative structural-recession work and the sorting of physical regimes into generation sites.
3. **Structural recession vs ΛCDM**: distinguishing empirical signature — unchanged, still the largest open physical stake.
4. **Mass-shell / antiparticle reading of the conjugate branch**: make exact or demote; currently the best amplitude-register instance of Theorem 1.
5. **Prediction 6b operationalization**: state what would count as a system occupying its center of symmetry, so the exclusion claim is testable rather than definitional.
6. **Dimensional uniqueness**: unchanged frontier.

# Part P — Propagation notes

**To the math chain (v7.6-candidate):** add a one-line remark that the physics register's forbidden-center language anticipated Cₙ (V.1) — it is a datum about the parallax method itself and belongs where the method's evidential logic is discussed. The AM-GM floor relation is register-neutral mathematics and could be promoted into the math chain's coherence-facts as: on Gₙ, Q_i ≥ 2·(geometric mean)² with equality at the seats — same content, derivation register.

**To the DDJ chain:** two re-weighings beyond those already listed. (1) The occupied-seat point gives 守中 a sharper descriptive referent: the balance axis passes through the void *and through the occupied seats* — holding to the center as it stands is dwelling at the seat about the void, not approaching the void. (2) 無為 as aligned persistence now has the seat as its exact structural locus: minimum cost, floor-touching, the ground state's residence. Both under :: discipline, Will's domain, not asserted here.

-----

*v7.6-candidate. Not sealed. Enters review with: all forbidden-center referents corrected to Cₙ; the physics register's anticipation of the correction recorded as parallax evidence; the AM-GM two-floor relation derived and verified; the occupied-seat resolution of the coherent-state tension; the tokamak wording corrected; prediction 6 split; the oscillator promoted to flagship-candidate pending source verification; status tags repriced to the named premise set (Q, F, R, T). Written to the downgrade-and-repair standard.*
