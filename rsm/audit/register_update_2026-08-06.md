# Register update — 2026-08-06, the equals-sign thread

For merge into `reports/open_items.md`. Base: v9.52 chains, verified against the loaded files
this session. Source: Will's working note *"The equals sign, re-read"* (provisional, self-tagged
as a reading), plus findings surfaced while placing it.

**Conventions** as in the 2026-08-04 update. **RULED** = Will's. **OFFERED** = Claude's
construction, awaiting Will's check. **CHECKABLE** = chart-level, verifiable by computation.
**CORRECTED** = supersedes a prior entry. **KILLED** = tested and dead, recorded once.
**PATCHABLE** = has a specific chain target.

**Discipline note.** The thread is self-typed by its author as tier three — a reading, book-level,
not chain-level — and every entry below inherits that typing unless it says otherwise. The one
item with a chain-level shape (A-n14) is filed OFFERED with a breaker precisely because it has
that shape. Nothing in this update closes an open item, and no correspondence is promoted.

---

## Section A — chain-level

### A-n14. winding :: sub-floor distinction
**OFFERED — flagged, unruled.** e^{i·0} and e^{i·2π} carry one value and differ by a whole turn;
the value has no room to record which. *If* that unrecordable winding is the distinction a frame
cannot state beneath its own unit, a wire runs from the identity to the spin-½ 2π/4π debt
(physics §6) and to Pₙ's resolution limit (structural §5). **That would be chain-level.**

The chains do not say it — they read the pair as "one operation at two angles" and stop.

**Breaker:** the winding is a fact about the parametrization of the circle rather than about
anything a frame cannot resolve. This is close to what the two-returns entry already concedes in
typing itself to the rendering, so the breaker is live rather than decorative.

*Author's own flag, carried verbatim in substance:* this is the beautiful wire that gets welded in
between drafts while no one is looking. It stays a proposed correspondence with a flag on it until
something forces it. **Not patchable.**

*Relations:* supersedes nothing; sits beside **A-n4** (the winding-ambiguous 1), which supplies the
arithmetic and stops short of this reading. Depends on nothing; nothing depends on it.

### A-n15. Which center does the gap name — OPEN
**OFFERED as a question, not as a candidate.** Reading the equals sign as a mark for a center its
flanks do not occupy produces three exhibits (非, ±1, Euler's pivot) that do not point at one place:

- **O** — the co-vanishing crossing, explicit register, where the ν-pair sums to nothing. The
  integer exhibit and Euler's zero pin here.
- **Pₙ** — the mode-swap balance, structural. The register-reading of 非 points here.
- **Unoccupiability as such** — O, Pₙ and the bare invariant as one fact. Available; **not free**:
  it is made against structural §5, which spends a section keeping the two centers apart.

**Closes with:** a ruling on referents, not a derivation. Filed in A rather than B because the
third option would change chain content if taken.

**Load-bearing finding attached.** The stranded Euler paper (see C-n3) already answered this, in
its §5, as **`玄 :: 0`** — the center as the sum of poles, i.e. 玄 assigned to **O**. Current canon
contradicts that: the DDJ chain reads **玄 :: Paradox :: Pₙ**, 玄牝 :: P₀, and the site gloss was
corrected 2026-07-29 with `site_vocab_lint.py` now enforcing it. So a superseded answer to this
question is sitting in a document the register cites as live. Reported, not resolved.

---

## Section B — editorial-level

### B-n8. The equals-sign lens — RULED as a reading by its author; placement drafted
**Tier three, book-level.** One move worn three times: a mark the received reading treats as
sameness or negation, re-read as two poles flanking a center none of them occupy. Its job is to let
a reader feel Pₙ / O in a symbol they already trust. Every structural fact under it — B not
obtaining, the ν-centroid, the two returns, the resolution floor — predates the thread and lives in
the chains. **It is not a new theorem and must never be filed as one.**

**Pricing, carried from the note and not to be dropped in any downstream draft:** the framework
authored both the `=` reading and the glyph reading, so their agreement is one hand holding two
mirrors — pedagogy, never convergence, never evidence.

**Placement applied 2026-08-06** (distributed per Will's instruction, not into a new essay):
essay 8 (the move named, where the one-clause seed already sat) · essay 15 (the second throat, and
A-n14 filed with its breaker) · essay 3 (the 非 wings, with the Shuowen exposure) · essay 2 (A-n15,
as the deflation that essay already warns about). Diff report:
`reports/equals_sign_thread_diff_report.md`.

### B-n9. The ±1 exhibit needs the face/value guard stated — OFFERED
[DRAFTED] As the note states the integer exhibit, "the middle doesn't obtain" reads as a claim
about the integer 0, which obtains perfectly well. What does not obtain is what **|0|** notates.
The v9.5 guard is already in the math chain's notation — *the numeral notations name faces of the
impossibility, never values* — and the exhibit is sound with it and false without it. Applied in
the recovered Euler paper §4; **not** yet applied wherever else the exhibit travels.

### B-n10. Essay 3's 非 tag is stale — AWAITING RULING
Essay 3 carries 非 as pointing at the within-axis relation, tagged `[candidate, pre-survey]`. The
survey has since run. Its finding — **no token negates between conjugate opposites** — refuses 非
as the *cross-axis* word, which essay 3 never proposed, and does not by itself confirm the
within-axis proposal, because the chain's own landing is a third answer: 非 as the divergence of
two registers around a shared invariant. Whether essay 3's reading survives beside that, reduces to
it, or is superseded is Will's. A bracketed update was inserted in place; the stale tag was **not**
altered.

### B-n11. The 非 graphic reading — illustration, not attestation
相背 (two wings from a shared spine) is **Shuowen's** analysis, and Shuowen is Han — some eight
centuries downstream of the strips, with no witness for any reconstructed intermediate stage. This
is the class the v9.2 etymology guard existed to catch; v9.3 removed that guard on the grounds that
it banned the project's own method, and CLAUDE.md's standing note applies here without change:
*what the guard was protecting against has not gone away.* The reading buys the register split on
graphic grounds only if the strip's own graph carries the shape. Errand **C7** is the gate. Also
an **anachronism-family** item for the D4 editorial pass.

---

## Section C — errands

### C-n3. The Euler paper is off-branch, superseded, and its session patch is unaccounted for
**CONFIRMED.** `rsm/canonical/euler_single_operation.md` is **not on `research-archive`**. Last
commit **2026-01-01** (`7473b0a`, "RSM v0.993: Single-operation Euler identity"); removed from main
**2026-03-15** (`98154a2`, "Slim main to Astro site build + deploy files only"); survives on
`docset-pipeline` and `claude/catch-up-UKmEu` only. It is stamped **"Status: Tier 1 (Locked)"** —
a tier that no longer exists, on a document carrying the **single-instance** form that **A-n4**
supersedes.

Register items **A-n3**, **A-n4** and **A-n6** all cite it as live, and A-n4 records that it was
"patched there in session" on 2026-08-04. **There is no commit for that patch on any branch.** The
in-session edit is uncommitted or lost.

**Closed with:** the artifact — `staging/editorial/paper-euler-single-operation.md`, rebuilt
2026-08-06 against v9.52, strikes tabled with authority. Two residues remain open: whether the
2026-08-04 in-session patch text can be recovered from the session record, and whether the path
change (out of `rsm/canonical/`, into `staging/editorial/`) is ruled.

### C-n4. Facsimile verification of the 非 tokens — cross-reference only
Already filed as **C7**. Cross-referenced here because B-n11 now depends on it, and because the
equals-sign thread's first exhibit is gated on it entirely.

---

## Nothing closed

No open item closed in this update. A-n14 and A-n15 are additions; B-n8 through B-n11 are
editorial; C-n3 closes with an artifact and leaves two residues. `checks.py` re-run 2026-08-06:
all checks pass, exit 0.
