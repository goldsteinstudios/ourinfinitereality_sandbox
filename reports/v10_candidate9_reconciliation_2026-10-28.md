# v10.0 Candidate 9 — filing and reconciliation against v9.53

**Filed 2026-10-28.** Seven markdown files received and placed at
`rsm/canonical/chains/v10/`. **Canon remains v9.53** at `rsm/canonical/chains/v9.5/`; the set
self-describes as "Candidate 9," and promoting it is a ruling, not a filing act. Machine
verification: `rsm/audit/v10_checks.py` (new, re-runnable, **39 pass / 0 fail**).

Nothing in v10 was edited. This report is the Layer-3 record: what the set answers, what it
restructures, what it drops without refuting, where it reverses a standing ruling, and what
verification found.

---

## 1. The mathematics verifies — all of it

`rsm/audit/v10_checks.py` checks every claim in v10 that is machine-checkable. **39 pass, 0 fail.**
Independently confirmed, not merely re-read:

| Claim | Status |
|---|---|
| Φ's three reference assignments: Φ(G)={v=0}, Φ(B)={u=0}, Φ(P)=(0,0) | exact |
| det DΦ = 1/(2xy) | exact, numerically, at three points |
| uv=1 pulls back to (ln x)² − (ln y)² = 4 | exact |
| u=v>0 pulls back to y=1, x>1; Φ⁻¹(1,1) = (e², 1); general a → (e^{1/a}, 1) | exact |
| child sector {u>0,v>0} = {x>1, 1/x<y<x} | set-equality verified on test points |
| g(∂ᵤ,∂ᵤ) = g(∂ᵥ,∂ᵥ) = 1 and **g(∂ᵤ,∂ᵥ) = 0 everywhere** | exact at four points incl. (1,1) |
| Euclidean ⟨∂ᵤ,∂ᵥ⟩ = x² − y², vanishing only on x=y | exact |
| α=β=½ form ≡ ½(dx²/x² + dy²/y²) | exact, algebraically |
| Milne comparison: both tangents at (1,1) null, inner product −2e^{2v} | exact |
| XY = a² − b₁² | exact |
| balance ring (cos θ, 1, sin θ) on both ρy=1 and ρ²=y² | exact |
| ℝᵈ∖L ≃ S^{d−2}; d=2 disconnected, d=3 π₁≅ℤ, d≥4 simply connected | correct topology |
| **φ is the unique positive point on xy=1 with x−y=1**; ln φ = 0.48121183; golden angle = 137.50776405° | exact, uniqueness proved (x²−x−1=0 has one positive root) |
| L_N = N sin(π/N) is the inscribed N-gon perimeter at diameter 1; → π from below, never equal at finite N | exact |
| **E²−(pc)² = (mc²)² ⟺ ((E+pc)/mc²)((E−pc)/mc²) = 1**; x_n = e^φ with φ = artanh(v/c) | exact at five β values |
| on Gₙ: u = φ, v = 0, so gₙ = dφ² — the rapidity metric | exact |

Two results deserve calling out as genuinely new and clean:

- **The relativistic frame (06 Paper 2) is the strongest correspondence in the set.** The
  energy-momentum hyperbola *is* a reciprocal frame — not by analogy: the factorization is exact,
  the light-cone modes are e^{±φ} in rapidity, P=(1,1) is literally the rest frame, and the
  intrinsic metric reduces to dφ², the standard rapidity metric. The speed-of-light horizon at
  infinite intrinsic distance then falls out rather than being asserted. Unlike the physics
  chain's `1ₙ :: ℏ/2` and spinor correspondences, **this one stands on the frame's own arithmetic,
  not on a borrowed chart** — which is precisely the independence problem the 2026-08-07
  state-of-play named ("the second list is the impressive half").
- **φ as the unit-difference point is new, exact, and unique.** The coincidence x·y=1 ∧ x−y=1 has
  exactly one positive solution, and it is φ. The golden-angle packing consequence is arithmetic,
  not decoration.

**What the verification does *not* establish**, stated in the script's own scope note: the
metric's form is forced only *inside* the adopted quadratic Riemannian class, which is `[DEF]`;
d=3 follows from *requiring* connectivity **and** nontrivial winding, and that requirement is a
premise; and nothing in `[TEXT]` or `[CORR]` is reachable by script.

---

## 2. What v10 answers that v9.53 left open

**A5 — "exactly three" gets a standing candidate derivation.** v9.53's register says the slot is
**empty**: *"'Exactly three' is open with no standing candidate derivation — the binding-extortion
schema rests on the binding requirement, which is chart; the |1| cascade is withdrawn."* v10
supplies one that is not chart-bound: ℝᵈ∖L ≃ S^{d−2}, so d=2 is disconnected and d≥4 has trivial
π₁; connectivity plus protected integer winding selects d=3 **uniquely**. The topology is correct.
The premise to audit is whether the structure *requires* protected winding — but the slot is no
longer empty, and this is the first candidate in the register's history that doesn't rest on a
chart.

**The status-tag apparatus returns.** v9.3 deleted the entire epistemic tag system (38 instances
→ zero), and `CLAUDE.md` records the compounding cost: *"Epistemic standing must now be read out
of prose, per claim, with nothing marking it."* v10 reinstates a seven-tag vocabulary —
`[PREM] [DEF] [MATH] [CORR] [TEXT] [OBS] [OPEN]` — and, crucially, **uses it inline at the claim**,
including compound tags (`[MATH under DEF]`, `[DEF; MATH; CORR]`) that mark exactly what a result
is conditional on. This is a direct answer to a documented loss, and the compound form is better
than what v9.2 had.

**The 玄 ruling is observed correctly.** v10 writes 玄 for local paradox (Pₙ) and 玄牝 for the
generative paradox (P₀) — compositional, with "generative" carried by 牝, never folded into 玄.
The phrase "generative crossing" appears nowhere in the set. **v10 does not carry the defect the
2026-08-07 corpus read found live in 26 places of site copy** on both branches.

**恆 is used throughout** — 恆亡/恆又, 恆道, 恆無/恆有 — consistent with the 2026-08-07 ruling that
the register marker is 恆, with 常 as the post-taboo form.

**The transmission story adopts systematization over scribal error** — "lossy graphic compression,"
hardened standardization, "Guodian must be read forward from the bamboo rather than backward
through Mawangdui standardization." That is the conclusion of
`reports/transmission_mechanism_assessment.md` (2026-08-05), independently arrived at. See §5 for
the one correction it still needs.

---

## 3. Dropped without refutation — the silent-replacement check

Ledger Entries 003 and 004 established the protocol: **when a revision replaces a prior lemma or
derivation without refuting it, check the prior one before pricing the swap.** v10's ledger runs
D01–D09 with **two** open questions (O01 glyph census, O02 cross-frame coupling). v9.53's register
runs A1–A16, B, C and D sections. The difference is not a closure record — the items are simply
not present. Enumerated, so the next pass can rule each:

| v9.53 item | Status in v10 |
|---|---|
| **A8 — Definition T (traversal)** | **Absent entirely.** v10 contains no traversal object. The 2026-08-07 state-of-play ranked this **#1 by leverage** — "the shared gate on all four of the math chain's chart-typed theorems," unattempted since v9.3 flagged it. v10 neither restates nor refutes it; it builds a metric geometry in which the question is not posed. Whether that dissolves A8 or evades it is the single most important ruling this set needs. |
| **A1 — the native-magnitudes step** | **Answered by declaration.** v10 §3 sets k=1 via "a dimensionless normalized chart χₙ(1ₙ)=1" and tags the whole reciprocal class `[DEF]`. The anchoring v9.53 wanted *legitimated* is now *adopted*. That is a defensible move and an honest one — but it closes A1 by re-typing it, not by deriving it. |
| **A12 — quadraticity of the measure** | **Still open, and v10 says so.** "Adopt the quadratic Riemannian metric class (**[DEF]**)." The uniqueness is of the *form inside* that class. Important consequence: v10's claim that "perpendicularity is an intrinsic metric fact `[MATH]`" is conditional on A12, and must not be read as retiring v9.53's "orthogonal is a rendering fact." |
| **A4 / A3-residue / A9 / A10 — the cross-frame cluster** | **Partially absorbed into O02** (physical constraints on αₙ, βₙ across frames). The qualitative questions — what relation holds between frames that share a rendering without shared ancestry; how a parent states a fact about a child's interior; sibling commensurability — are not addressed. |
| **The Corollary (v7.7's L1)** | **Absent.** Still has no register entry either (audit 1.3 / E4, confirmed twice). Load-bearing in structural §4's floor argument. |
| **P₀'s threefold presentation set** | **Reduced to two faces.** v9.5's PATCH 14 established {|0|, |1|, **−1 = 0 = +1** — the sign-collapse, the trivial ring, "arithmetic's face of total indistinguishability"}. v10 has |0| and |1| only; the sign-collapse face is gone, unmentioned. |
| **PATCH 25, the share-noun (B4), the [M] re-tag policy (B3)** | Not addressed; v10's vocabulary doesn't use "the constitutive share." |

---

## 4. One standing ruling reversed — Euler

**v10 writes $e^{i\pi} + 1 = 0$.** The v9.52 ruling (PATCH 27, Will's own words in the patch set)
was that *"going from π to 0 makes no sense — at the very least it should be
$e^{i\pi} + e^{i\cdot 2\pi} = 0$, out and back"*, and the math chain was changed to the traversal
form on that authority, with "five constants in miraculous conjunction" struck at the same time.

v10 reverts to the `+1` form and reads the `+1` as the manifest unit 1ₙ (有) rather than as
e^{i·0} — so it is not a straight repeat of the error, and the winding ambiguity is sidestepped
rather than re-asserted. But **the traversal reading is absent from the set**, and the form Will
ruled against is the one displayed. This is the one place v10 contradicts a live ruling rather
than restructuring around an open item. Flagged, not edited.

Also worth noting: v10's Euler passage is close in spirit to the material PATCH 27 struck as
editorializing ("Starting from the manifest unit 1 … travels through a half-turn of π to the
conjugate pole"). The reading may well be the better one — but it needs to be ruled in, not
inherited.

---

## 5. The paleography: 23 slip citations checked, 8 match

v10's `03_Laozi_Correspondence.md` §5 and §2–3 cite ~24 specific Guodian positions in Bundle A
notation (A.slip.position). Checked against `data/ddj/guodian_interactive.json` — the same dataset
the 恆/常 survey and the v9.5 PATCH 16 attestation ran on:

**8 match · 14 mismatch · 1 position does not exist.**

Matches: **A.2.19 欲 · A.8.12 非 · A.1.22 慮 · A.8.2 好 · A.1.3 棄 · A.1.25 季 · A.1.26 子 ·
A.16.17 浧** (guodian 浧 / received 盈 — exactly as v10 says).

The mismatches fall into two very different classes, and the distinction matters:

**(a) Off-by-one or wrong-slip citations — the claimed glyph exists nearby.** These look like
indexing slips, and most resolve:

| Cited | Claimed | Dataset at that position | Where the glyph actually is |
|---|---|---|---|
| A.18.18 | 天 (of 天坨) | ○ (unreadable) | **天 is at A.18.17** — one position earlier; .18 is an unresolved ○ |
| A.18.3 | 萬 | 也 | A.19.3, A.12.25, A.13.14, A.14.8, A.17.14, A.24.9 |
| A.20.4 | 勿 | 夫 | **A.19.4**, A.12.26, A.13.15, A.14.9 … |
| A.5.5 | 心 | 也 | **A.35.5** — same position, slip 35 not 5 |
| A.10.11 | 皆 | 者 | A.15.11, A.15.20 |
| A.2.4 | 谷 | 足 | **A.3.4**, A.2.27, A.3.11 … |
| A.3.31 | 川 | *no such position* | **A.8.31** — same position, slip 8 not 3 |
| A.31.3 | 曰 | ○ | A.31.21 (same slip), A.21.27, A.22.5 … |
| A.25.8 | 曰 | 未 | as above |
| A.22.2 | 天 | 爲 | A.4.22, A.5.7, A.7.2, A.15.9, A.17.30 … |
| A.7.8 | 巳 | 已 | 巳 absent; **已** sits at the cited position |

The 天坨 case is worth isolating: v10's reading pairs 天 with a second graph at A.18.18, and the
dataset marks that position **unreadable (○)**. That is one of the open ○ positions already on the
slip-image errand list. v10 reads a glyph there. **That reading cannot be corroborated from
tracked data at all** — it needs the facsimile.

**(b) Claimed glyphs that are not in Bundle A at all** — 恆, 海, 偽, 惖, 巳. Of these, one is a
finding rather than a typo:

> **恆 is cited at A.28.3 and is not attested anywhere in Bundle A.** The dataset has 玄 at that
> position. This is independently corroborated: `reports/heng_chang_distribution_survey.md`
> established that Bundle A attests **亙 four times** (slips 6, 13, 18, 24) with **zero readable
> 恆 and zero 常**. v10's own §5 table describes a 恆 glyph's brush-stroke structure ("boundary
> bars 二 with crescent moon 月 and the sideways T ⊢") at a slip where the strips read 亙 — and
> the v9.53 DDJ chain already states that **the Guodian stratum attests 亙**, with 恆 as the
> **[M]** form. The 恆 glyph description belongs to the Mawangdui layer or to a non-A bundle, not
> to Bundle A slip 28.

The other four (海, 偽, 惖, 巳) may well be in Bundles B/C, Taiyi Shengshui, Wuxing or Xing Zi Ming
Chu — v10's O01 census would settle it — but they are cited in **Bundle A notation**, which is
wrong as written.

**The honest caveat, stated as every prior attestation report has stated it:** this corroborates
against the repo's transcription, **not against slip images**. The 2026-08-07 state-of-play records
that `guodian_interactive.json` "was unreproducible from tracked inputs." So a mismatch is evidence
of disagreement between v10 and the dataset, not proof that v10 is wrong — **except** for 恆, where
a second independent survey agrees with the dataset and the v9.53 chain already rules 亙 for this
stratum.

**Scale of exposure.** v10's visual-paleography claims go considerably further than anything in
v9.53 — reading 道 as a water-carrier scene with a bamboo pole, suspension strings, a 3-D-shaded
bucket and a switchback trail; reading a whole biological lifecycle out of 女/巳/妃/母/子/好/棄.
The v9.53 chain, by contrast, holds **溺 as "attested-uninterpreted"** with a mandatory
three-rung interpretive ladder, and calls A37 "the highest-projection-risk location in the
corpus." These new readings are the same risk class, at roughly ten times the surface area, and
**the 1,717-glyph image corpus backed up on 2026-08-07 at
`data/ddj/Guodian Strip Glyphs/` is exactly the instrument for checking them.** That is now a
tractable errand, not a wish.

---

## 6. Smaller corrections

- **"Shuwen Tongzi"** (03 §1) is a garbled romanization. The policy is 書同文字, *shū tóng wénzì*.
- **The Qin-event framing needs the Galambos correction.** v10 places "the Qin imperial
  standardization of script" as the single event standing between 300 and 168 BCE. Galambos (*The
  Myth of the Qin Unification of Writing in Han Sources*, 2004) argues the archaeology shows no
  sudden shift and that orthographic uniformity as an idea is substantially an Eastern-Han
  retrospective — with Xu Shen's "Qin standard" partly a Han reconstruction. The defensible form,
  per `reports/transmission_mechanism_assessment.md` §1, is **Qin-through-Han consolidation**: a
  multi-century hardening whose agent overlaps the canonizers. v10's *mechanism* is right; its
  *date and agent* are the traditional story.
- **The s-orbital strain is not acknowledged.** v10's Paper 2 argues the electron "cannot collapse
  into the proton at Oₙ" and that the atom is a void held open by orbit. The physics chain carries
  the opposite exposure in the open: *"quantum mechanics places the electron's density maximum **at
  the nucleus** for every s-state — the center, in physics' own best description, is not spatially
  avoided there."* That is logged as "first-order strain against the framework's most important
  object." Paper 2 walks into it without naming it.
- **Li Bing** (04 §3) — the Dujiangyan engineer is conventionally **Li Bing (李冰)**, so the name
  is right; the date (~256 BCE) postdates Guodian's closure (~300 BCE), which the
  `technology_index_anachronism_check.md` flagged as a reason not to lean on Dujiangyan for
  era-contemporary Chu evidence. 04 is observational phenomenology, so this is a framing note
  rather than an anachronism: the system is Warring States but *later* than the slips.
- **"Candidate 9"** implies candidates 1–8. None are in the repo. If they exist, the set has a
  provenance trail worth landing; if they were drafting iterations, saying so closes the question.

---

## 7. What this set needs, ranked

1. **Rule on A8 (Definition T).** v10 builds a geometry in which traversal is never posed. Either
   that dissolves the #1-leverage open item or it evades it. Nothing else in the set depends on
   more.
2. **Rule on the Euler form** — traversal reading in, or the `+1` form ruled back.
3. **Fix the slip citations**, then run O01 against the backed-up glyph images. 15 of 23 are wrong
   as written and most are off-by-one; the 恆 citation is substantively wrong and already settled
   against by two independent surveys.
4. **Decide what v10 is.** If it supersedes v9.53, the open-items register needs re-basing — it
   cites v9.5 chains by section and line throughout, and §3 above is the list of items that would
   otherwise vanish silently. If it sits beside v9.53 as a consolidation candidate, say so in the
   README and the register's canon pointer stays.
5. **Layer check.** The set is clean of change-history — no dated corrections, no WITHDRAWN blocks,
   no register codes in prose. It passes the layer separation policy as filed.

---

*Not sealed. `rsm/audit/v10_checks.py` and `rsm/audit/checks.py` both exit 0. Every mismatch in §5
is re-runnable against `data/ddj/guodian_interactive.json`. Nothing here is a ruling.*
