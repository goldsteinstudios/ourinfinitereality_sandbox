# v9.4.1 patch diff report (patch set 2)

Applied 2026-08-02, in place on `rsm/canonical/chains/v9.4/`. Result versioned **v9.4.1**
(drafting corrections within v9.4; same directory; titles and closing lines re-stamped). Line
references are to the files as they now stand.

---

## PATCH 10 — structural §6 Rotation + involution scoping

**Rotation paragraph replaced** (structural, L111). Old (the patch-set-1 state, carrying diff
flags 4 and 5):

> "Rotation. The frame's two mode-dominant regions are related without being connected (§5), and
> the relation cannot be carried by a path. It is carried by revolution: Gₙ revolving about Bₙ. A
> half-turn about B exchanges the modes — the mode-swap performed as motion rather than as
> relabeling — so revolution relates the two regions without anything passing through the locus
> that cannot be occupied. 'No through, only around': revolution is a motion the structure admits
> — the mode-swap performed as motion rather than as relabeling — and the relation between the
> regions is carried by descent (§7) whether or not any motion realizes it. The plane's own
> exchange is reflection across B…"

New: the approved paragraph — descent carries the relation ("the divider becomes the child's
axis") whether or not any motion realizes it; revolution is what the structure **additionally
admits**; the mode-swap phrase now appears once; "No through, only around." stands as a bare
slogan. The reflection/orientation material is unchanged. **Flags 4 and 5 cleared.**

**Involution scoping** (structural, L145): "a motion the structure admits and requires" → "a
motion the structure admits" — R3 applied to the one remaining "requires." **Flag 9 cleared.**

## PATCH 11 — math chain: the recursion theorem

**Deleted** (Theorems, old text in full):

> "The parturition map. The recursion is that O₍ₙ₊₁₎ reads Pₙ and yAxis₍ₙ₊₁₎ reads Bₙ, as
> constitution and not site-selection. w = z² realizes it, 2-to-1 with the two preimages differing
> by ν. The two preimages are not two things bound into one; they are one branch compared from the
> child's side — indexed comparison performed across a frame boundary. This is how a sign can be
> measured while being explicit."

**Replaced** (new L65–67) with the two approved paragraphs: **"The recursion (two transfers)."**
(both transfers; O₍ₙ₊₁₎ = Gₙ ∩ Bₙ = Pₙ citing structural §7; no map realizes the transfers and
none is owed; chart-level modeling is a rendering question, unasked) and **"Indexed comparison
across the frame boundary."** (the surviving ν-index content; the measurement compares indices,
it does not detect a second obtainer).

### Verification report 1 — remaining "parturition" / "w = z²" references in the four chains

| Chain | Location | Exact wording | Note |
|---|---|---|---|
| **just_math** | L85, "The engine (realized)" | "…trans-frame, generation — the child is the pursuit of exactness continuing below the floor, its origin the approached locus read from below, its axis the parent's balance line, **realized by the parturition map**. Recursion is exactness, permanently deferred." | **The one remaining in-chain citation of the deleted theorem, in the math chain itself.** Reported, not fixed (outside the patch's specified deletion). The engine paragraph now cites a theorem the chain no longer contains — the natural target of the deferred §7-counterpart session. |
| **just_physics** | L53, §6 spin entry | "Two candidate accounts, possibly one. **First, from the current math chain: the parturition map's two preimages are one branch compared from the child's side — an indexed comparison performed across a frame boundary — so a measured sign would be evidence of a comparison made from a register the measurement sits inside.**" and, closing the pairing: "The two candidates rhyme rather than compete: **the parturition realization w = z² is itself two-to-one, the model double cover.**" | The expected citation, wording captured verbatim as requested. Two exposures now live: (a) "from the current math chain" is no longer true — the math chain carries the indexed-comparison content but not the map; (b) the "rhyme" clause leans on w = z² specifically. Needs the session drafting the patch set anticipates ("the spin-entry consequence is live"). |
| **just_physics** | L71, §9 | "…the two arrows: **parturition-irreversibility** and frame-scale shear are rival renderings, unresolved…" | A term use (naming a rendering), not a citation of the map. No w = z² dependence. Reported for completeness. |
| **just_ddj** | — | *(none)* | The only DDJ "parturition" reference was in the three-forms paragraph deleted by PATCH 8a. Clean. |
| **structural** | — | *(none)* | Clean. |

No other `w = z²` citation exists in any chain. (The v9.4 `README.md` mentions both terms in its
deferred-work list — a version document, not a chain; left as is.)

### Verification report 2 — the two-returns theorem

Verified standing (just_math L71): "**The two returns** — computation checked; the claim belongs
to the rendering. Along the circle, Q_j = 1ₙ·cos 2θ: the invariant returns at π, the position at
2π. A double cover — a fact about the circle slice. Euler's identity is this fact compressed…"

**It does not reference the deleted material.** Its double-cover claim is grounded entirely in the
circle slice (Q_j = 1ₙ·cos 2θ); neither "parturition" nor w = z² appears. The one indirect echo is
in the *physics* spin entry, whose "rhyme" clause connects the spinor double cover to w = z² — that
dependency is recorded in report 1, and it belongs to the physics entry, not to the theorem.

## PATCH 12 — housekeeping

**12a — emphasis normalization.** Applied across all four chains, mechanical class only:
paragraph lead-in labels and entry heads, matching the patched passages' convention. 54 single
replacements + one recurring label, every one verified to hit exactly once (or the counted total):

- *structural* (14): P1 — the Conditional · P2 — the Bridge · Definition (frame) · Corollary ·
  The law · Scale · O — the co-vanishing locus · Bₙ — the balance line · Pₙ — the paradox ·
  Generation has no address · Rendering guard · Orientation · What a child shares with its
  parent · The involution.
- *just_math* (10): Scale and lineage · Placement, stated · Disconnection · Revolution ·
  T2 — crossing · The two returns · i² = −1, two routes · The ν-centroid · Complementarity
  floor · No address.
- *just_physics* (21 + 7): entry heads (1ₙ :: ℏ/2 · The slice invariant :: c · Superposition as
  unselected circulation · The two returns :: the spinor double cover · Horizon interiors ::
  circulation failure · Information as non-orientable… · The s-orbital strain, kept visible ·
  One thing the corpus material cannot bring with it · The sorting is the entry) · evidential
  labels (Mechanism note, load-bearing · Named strain/strains · Directionality flag) · the
  refusals-ledger labels (Deferred / No entry / Refused typing / Retired / Parked / Excluded
  class / Not carried over… / Banned) · **"Where it would fail:" bolded at all 7 occurrences**.
- *just_ddj* (9): One discipline throughout · Attestation, carried · Line 2 · Lines 3–4 · The
  methodology lines […] [R] · The engine lines are definitions · 溺 — attested-uninterpreted ·
  The preregistered test, scored positive · Chapter 2 is also the method.

**Judgment cases — reported, not decided** (each would require a ruling on what counts as a
defined term / object name at first use):

1. **First-use symbol bolding** — 1ₙ (structural §4 / math "The frame, the unit, the floor"),
   P₀/O/B/P/G, X and Y, σ_B, ν at their definitional first uses. Bolding symbols is a notation
   convention, not mechanical formatting; not applied.
2. **The faces** — "the empty face" / "the full face" (structural §1; math Notation). Candidate
   defined terms; their v9.2 ancestors (|0|/|1|) were bold. Not applied.
3. **Named objects mid-prose** — "the Amplitude Floor" (math, first named at "the branch
   a ≥ √1ₙ — the Amplitude Floor"), "the mode-expressible domain," "a resolution limit"
   (structural §5), "the ring of orientations" (structural §7). All are names introduced inside
   sentences; bolding them changes sentence rhythm, and which are *names* vs. descriptions is a
   judgment. Not applied.
4. **Thesis-sentence leads** — structural §3's "The modes are magnitudes." (bulleted thesis,
   bolded in v9.2), physics §7's "Circulation organized around an unoccupied core:", the DDJ
   非-entry's "The corpus contributes here by resistance…", physics spin entry's mid-paragraph
   "The debt:". Each is arguably a label and arguably a sentence; not applied.
5. **The physics Predictions list** — items 1–4 lead with claim-names ("Unitarity as the floor's
   dynamical face."). Bolding them would style predictions like entries; left for a ruling.

**12b — canon pointers.** `CLAUDE.md`: section heading updated to v9.4.1 + a CANON UPDATE block
inserted at the top of "The Chains" (naming the markdown layer canonical, deprecating the v9.3
PDFs as canon, summarizing the headline changes; the v9.3 description below it is marked
retained-as-history); "Reference Locations" first bullet now points at `chains/v9.4/` with v9.3
demoted to superseded; "Working with RSM Content" item 1 updated. **The rest of CLAUDE.md
deliberately untouched** — it still contains v9.3-era detail (e.g. "quote v9.3 via pdftotext,"
the tag-removal history); the CANON UPDATE block scopes it. The open-items register
(`reports/open_items.md`): a canon-pointer block added at the head, naming v9.4.1, noting PATCH 6
rewrote the structural list after compilation (affects items A2/B9 and A5), and that regeneration
is a separate task. **Content untouched.**

**12c — confirmed untouched.** `git status` over `rsm/canonical/chains/v9.3/` (including the
change log and the transcription layer) and `rsm/canonical/chains/v9.2/`: no modifications.

## Version stamps

All four titles: `(v9.4)` → `(v9.4.1)`. All four closing lines: `*v9.4 — …*` → `*v9.4.1 — …*`.
`rsm/canonical/chains/v9.4/README.md` retitled v9.4.1 with a patch-set-2 summary block. Directory
name stays `v9.4/` (drafting correction within v9.4, per instruction).

## Flags carried forward (for the deferred sessions)

| # | Item | Owner |
|---|---|---|
| 1 | Math engine L85 "realized by the parturition map" — cites a deleted theorem | The deferred math §7-counterpart session |
| 2 | Physics §6 spin entry: "from the current math chain" now false; the "rhyme" clause leans on w = z² | The anticipated spin-entry session drafting |
| 3 | DDJ Ch. 40 "the three-forms taxonomy below is untouched" still dangles (R5/R6-flagged section) | The 有無相生 / Ch. 40 session rewrite |
| 4 | Five emphasis judgment classes above | A defined-terms ruling |
| 5 | The notation warrant (又亡相生 :: XY = 1) — ruled, wording not drafted | Session drafting |
| 6 | Open-items register regeneration from the v9.4.1 chains | Separate task, per the patch set |

Applied, verified, and stopped.
