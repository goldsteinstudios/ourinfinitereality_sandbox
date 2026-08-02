# v9.4 patch diff report

Applied 2026-08-02. Base: the v9.3 markdown transcriptions
(`rsm/canonical/chains/v9.3/transcription_2026-08/`), untouched and kept as the v9.3 record.
Result: `rsm/canonical/chains/v9.4/` (new directory; markdown is the canonical layer from this
version forward; the v9.3 PDFs are deprecated as canon, not regenerated — recorded in
`rsm/canonical/chains/v9.4/README.md`).

Line references: **old** = `…/transcription_2026-08/<chain>_v9_3.md`, **new** =
`…/v9.4/<chain>_v9_4.md`. Patch text was applied verbatim as approved, including its markdown
emphasis (the v9.3 transcriptions carry no bold because the PDFs had none; patched passages now
do — noted, not smoothed).

---

## Structural chain (`structural_v9_3.md` 121 lines → `structural_v9_4.md` 149 lines)

**Title** — old L1 `# RSM — The Structural Chain (v9.3)` → new L1 `…(v9.4)` (mechanical
consequence of "version the result v9.4").

**PATCH 1 — §0 subsection added.** Inserted after old L15 ("…explicit whether it succeeds or
fails.") and before `## Premises` (old L17). New L17–25: the five paragraphs "**Accuracy and
precision.**" / "It follows that refinement does not converge…" / "Call the invariant's presence…
**accuracy**… **precision**…" / "**This is not approximation.**…" / "**Consequence.**…" —
verbatim from the patch. `## Premises` now at new L27.

**PATCH 2 — §2 subsection replaced.** Old L47–53 deleted in their entirety:
> "The two senses of smaller. Two distinct relations must not share a word:" · "- Fineness —
> motion along the gradient toward a mode's small end. In-frame, unbounded, terminal excluded by
> the law." · "- Descent — the constitution of a child. Across-frame, inward only, not motion
> along anything." · "Vastness and fineness are the gradient's two ends, both in-frame, exchanged
> by the mode-swap. Descent is neither of them."

Replaced at new L57–63 with the four "**Vantage.**" paragraphs, verbatim from the patch.

*Consequential verification (as instructed — reported, not rewritten):*
- §4's "the child is not smaller — the child is the approach that does not finish, continuing"
  survives unchanged (new L77) and now leans on Vantage. ✓
- **No other v9.3/v9.4 chain passage cites "the two senses of smaller" by name.** Citations that
  do exist, outside the four chains: the **v9.3 change log §B item 8** ("The two senses of smaller
  (fineness / descent)… Flagged before, never ruled" — a historical record of v9.3, left as is);
  **CLAUDE.md** line ~186 (describes v9.2's introduction of the term; CLAUDE.md not updated, per
  "do not update any other document"); **v9.2 chain + README** (history). The editorial corpus
  references the *distinction* (e.g. `series-07`) but not the subsection by name.

**PATCH 3 — §7 opening replaced.** Old L97 (one paragraph: "One locus, two frame-readings… What
the parent cannot resolve is what the child measures from.") deleted. Replaced at new L107–121
with "**The two transfers.**" (two bulleted transfers; splitter/split assignment), "**The origin
follows.**" (the derived identity **O₍ₙ₊₁₎ = xAxis₍ₙ₊₁₎ ∩ yAxis₍ₙ₊₁₎ = Gₙ ∩ Bₙ = Pₙ**), the
vantage-rule sentence, the type-identification paragraph (retained content from the old opening,
per the patch), and "**The parent persists entire.**" — verbatim from the patch. The remainder of
§7 (Orientation, new L123; the rooted tree, new L125; what a child shares, new L127) stands
unchanged.

**PATCH 4 — §5 disconnection replaced.** Old L81:
> "The disconnection. Since no point of B obtains, removing B leaves the X-dominant and the
> Y-dominant regions of the frame with no path between them. Within frame n the two mode-dominant
> regions are *related* — each is the other under the mode-swap — but not *connected*. No
> traversal joins them."

→ new L91 (the direct justification: "Crossing… requires passing through the condition X = Y —
and that condition is the mode-collapse, which does not obtain. The transit condition is itself
the excluded condition…"), verbatim. The no-point-of-B-obtains fact stands independently at new
L87 (§5 Bₙ paragraph), as the patch notes.

**PATCH 4 consequential — §6 sentence replaced (R3).** Old L91, within the Rotation paragraph:
> "'No through, only around,' with the going-around structurally forced rather than merely
> preferred."

→ new L101: "'No through, only around': revolution is a motion the structure admits — the
mode-swap performed as motion rather than as relabeling — and the relation between the regions is
carried by descent (§7) whether or not any motion realizes it."

*Reported, not fixed:* the replacement's phrase "the mode-swap performed as motion rather than as
relabeling" now occurs **twice in the same paragraph** — the preceding sentence (unchanged from
v9.3) already contains it verbatim. Applied as approved; flagged for the next drafting pass.
*Also reported:* the Rotation paragraph still opens "…the relation **cannot be carried by a
path. It is carried by revolution**" (old text, not in the patch's scope) — under R3
(available-not-forced) that opening sentence may now sit oddly beside the replacement's "carried
by descent (§7) whether or not any motion realizes it." Not edited; flagged.

**PATCH 5 — verification only (both checks pass).**
- "the first distinction" — **zero instances** in the structural chain (grep).
- "each obtained tree is rooted" — stated per-tree (§2, new L53), inside "Because P₀ is unframed,
  R₁ has no parent: each obtained tree is rooted," adjacent to "Nothing here counts the roots,
  and nothing here excludes more than one" (new L55). No instance to report.

**PATCH 6 — Open items rewritten.** Old L113–119 (four items) → new L139–147 (five items),
verbatim from the patch: item 1 loses anchoring-by-constitution; item 2 is the new
resolved-negative entry; items 3–4 renumbered (cross-frame unit relation; the dimension route with
its equidistance/measure-content caveat); item 5 = branching beyond the balance, v9.3 text
unchanged as instructed.

**PATCH 9 — closing line.** Old L121 → new L149: `*v9.4 — the chains state the framework as
currently known. Unresolved material lives in the open-items register, not in the chains.*`

---

## Just-math chain (`just_math_v9_3.md` 111 lines → `just_math_v9_4.md` 109 lines)

**Title** — old L1 `(v9.3)` → new L1 `(v9.4)`.

**PATCH 7a — Anchoring paragraph deleted.** Old L87, in "The engine (realized)":
> "Anchoring. Every frame beneath n's unit and in relation to n is parent-seeded: 'beneath 1ₙ' is
> defined only relative to the parent's unit, so a sub-unit frame is by definition one the parent
> seeds; a free-floating sub-unit frame is a contradiction in the typing."

Deleted in its entirety (ruled a dodge, not a derivation — R14). "The engine (realized)" now runs
L81–85 (Denials; No address) directly into "## What this chain does not owe" (new L87).

**PATCH 7b — Open items item 1.** Old L95 "…the anchoring argument." → new L93 "…
anchoring-by-constitution (resolved negative at the structural chain; downstream consequences
open)."

**PATCH 9 — closing line.** Old L111 → new L109, same replacement as structural.

*Not touched, per instruction:* the parturition map (Theorems, new L65 — still "O₍ₙ₊₁₎ reads Pₙ
and yAxis₍ₙ₊₁₎ reads Bₙ" with w = z²), the x-axis transfer, and everything else in §7's
counterpart — **deferred by Will.** Noted: the math chain therefore currently states the
one-transfer recursion while the structural chain states two transfers; that asymmetry is the
deferred work, not an error in this patch.

---

## Just-physics chain (`just_physics_v9_3.md` 109 lines → `just_physics_v9_4.md` 109 lines)

**Title** — old L1 `(v9.3)` → new L1 `(v9.4)`.

**PATCH 9 — closing line** (the only content change; the patch set's "no physics edits" exclusion
read as no *substantive* edits, PATCH 9 naming all four chains explicitly). Old final line → new
final line, same replacement.

*Checked for R3 exposure:* the physics chain does not carry the forced-revolution phrasing — its
§1 says the relation "is carried by Gₙ revolving about Bₙ" without a necessity claim. No physics
passage needed the R3 rewording.

---

## Just-DDJ chain (`just_ddj_v9_3.md` 105 lines → `just_ddj_v9_4.md` 107 lines)

**Title** — old L1 `(v9.3)` → new L1 `(v9.4)`.

**PATCH 8a — three-forms taxonomy deleted.** Old L61, in "The cluster: 玄／牝／玄牝":
> "The three generative forms, one ratio, three mechanisms, never conflated: (1) entailment-生 ::
> the ground, P₀ : O₁ (道生一 — 道 is not a mother; P₀ has no prior state); (2) parturition-生 ::
> Pₙ → Pₙ, O₍ₙ₊₁₎ (severance with a persisting parent); (3) 相生 :: mutual constitution within
> the frame. 生 ≠ 相生; entailment-生 ≠ parturition-生."

Deleted in its entirety (R5, R6).

*Reported, not fixed (the patch forbids rewriting the Ch. 40 entry):* the Ch. 40 entry's closing
sentence (new L59) still reads "…and **the three-forms taxonomy below is untouched**" — after 8a
that reference **dangles** (the taxonomy is gone). The entry is flagged R5/R6-pending directly
above it, so the dangling reference sits inside the section already marked for session rewrite.

**PATCH 8b — pending flags.** The instruction "flag both entries with a single editorial comment"
was applied as: the same single comment placed at each of the two entries (both readings of
"single" recorded; this one errs toward both-flagged):
- new L41, under `## 有無相生 [G — Ch. 2, slip A15; …]`
- new L49, under `## Chapter 40 [G — slip A37; the scored test]`
Comment text, verbatim: `<!-- R5/R6 pending: 生 one form (woman → mother-woman, child); 相 =
co-perception; rewrite in session -->`
No other text in either entry was altered.

**PATCH 8c — 恆/常 checksum appended.** Old L97 → new L97: the entry now ends "…invariance-
within-frame (常). — deferred to the DDJ finalization pass; the strips attest both graphs, used
differently; the received text merged a distinction the Chu scribes maintained."

**PATCH 9 — closing line.** Old L105 → new L107, same replacement.

---

## Verifications and flags, consolidated

| # | Item | Status |
|---|---|---|
| 1 | PATCH 2 check: "the two senses of smaller" cited by name elsewhere | **No chain passage.** Change log §B item 8 (v9.3 historical record), CLAUDE.md, v9.2 history cite it — reported, untouched. |
| 2 | PATCH 5 check: "the first distinction" in structural §2 / chain | **Zero instances.** |
| 3 | PATCH 5 check: rootedness stated per-tree | **Yes** ("each obtained tree is rooted"; "nothing here counts the roots"). |
| 4 | §6 duplication: "the mode-swap performed as motion rather than as relabeling" now appears twice in the Rotation paragraph | Reported; applied as approved. |
| 5 | §6 opening "the relation cannot be carried by a path. It is carried by revolution" vs. R3's available-not-forced | Reported; outside patch scope. |
| 6 | DDJ Ch. 40 "the three-forms taxonomy below is untouched" now dangles | Reported; entry is R5/R6-flagged and awaits session rewrite. |
| 7 | Math chain still states the one-transfer recursion (yAxis only) vs. structural's two transfers | The deferred counterpart, by instruction — not an error. |
| 8 | Emphasis inconsistency: patched passages carry bold; the surrounding transcription carries none (source PDFs had none) | Reported; patch wording applied verbatim as approved. |
| 9 | The involution section (structural, unnumbered) still says the mode-swap is "a motion the structure admits **and requires**" | Reported; the sentence is about the mode-swap-as-rotation (v9.2 ruling), not about revolution carrying the region relation — but under R3 the word "requires" may deserve a look in the next pass. Not edited. |
| 10 | CLAUDE.md, the open-items register, the transcription NOTES, and all editorial documents still describe v9.3 as current | **Deliberately untouched** per "do not update any other document." The v9.4 README carries the canonicity statement. |

Applied, verified, and stopped, per instruction. No editorial repairs, no summary regeneration, no
other documents updated.
