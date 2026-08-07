# Code tasks — 2026-08-06 filing pass

> **Provenance note (Layer 3, added on capture 2026-08-07).** This is Will's task-file upload that
> drove the 2026-08-06 filing pass. It was named as the source in
> `reports/code_tasks_filing_2026-08-06.md` but never landed in the repo; the gap was found at
> `reports/parallel_session_capture_2026-08-07.md` §2a and closed here. Text below is the upload
> verbatim. **Known defect, recorded at the time and now checkable:** A1 delegates the ruling's
> provenance filing to "B1 below," and the B section contains only B0 — there is no B1. The filing
> report carried the provenance forward in lieu of it.

Governed by `layer_separation_policy.md` (upload alongside this). Mechanical only. Every judgment call is marked HOLD — do not act on those; surface them and stop. Do not rule, do not promote OFFERED/CHECKABLE, do not write history into content.

## A. Content edits — Layer 1 (chains)

**A1. DDJ chain — file the 常→恆 ruling (content only; rationale is Layer 3, do not add it)**
`rsm/canonical/chains/v9.5/just_ddj_v9_5.md`:

- Register-marker gloss (the `**常** :: frame-independent, parameter-free …` line): change the marker from 常 to 恆. State it as: 恆, [M]-attested; received 常 is the post-taboo form of 恆 (避諱, Emperor Wen); Guodian attests 亙. Remove the trailing pointer "see the checksum item on 恆/常" — that item is being deleted (A2).
- Do not add why the ruling was made. The provenance (survey, taboo mechanism, C1 flip) is filed in Layer 3 by B1 below.

**A2. DDJ chain — delete the dissolved checksum item**
Same file, "Open checksum items": delete the entire `恆/常` bullet. The ruling dissolves it — there is no two-graph distinction to adjudicate. Do not soften it; delete it.

**A3. DDJ chain — remove pending-comment contamination**
Same file: delete both `<!-- R5/R6 pending: … rewrite in session -->` comments (they appear twice). This is Layer-3 material in a Layer-1 file. The pending status of the R5/R6 rewrites is already held at register D1; confirm D1 records it (B2), then remove the comments. The chain's colophon already says unresolved material lives in the register.

**HOLD — for Will, do not auto-apply:** whether to convert received-text 常 quotations elsewhere in the chain (道可道非常道, etc.) to 恆, or keep the quotations as received-常 with a single "read as 恆" note. This is a finalization-pass judgment about quotation vs gloss, not a mechanical edit. Leave the quotations untouched and flag this for the DDJ finalization pass.

## B. Content edits — meta layer (CLAUDE.md)

**B0. Revise the convergence-is-evidence sentence**
`CLAUDE.md`: locate "The convergence of independent imperfect pointings is the evidence." Revise so convergence is described as multiple independent pointings at one pattern — not as evidence for a claim. The framework runs from a conditional; it does not accumulate confirmation. Preserve all falsifier / kill-condition language elsewhere (Prediction 1, the Planck floor) — that is HELD and is a different category from the strike. Meta layer, not a chain.

## C. Content cleanup — Layer 2 (editorial); deletions only, records already in Layer 3

**C1. Euler paper — strip the failure block**
`staging/editorial/paper-euler-single-operation.md`: delete the entire `§3-WITHDRAWN` section. Its content is fully preserved in divergence-ledger Entry 006 — this is a deletion, not a relocation. The corrected §3 (§3.1–3.7) stays; it reads clean without the withdrawal block beneath it.

**C2. Euler paper — strip dated correction-notes; keep live caveats**
Same file. For each item below, keep the corrected statement, delete the change-history parenthetical (all preserved in Layer 3 as noted):

- §3.1 "carries both slices" correction — keep the Q_i/trace statement; delete the "originates in A-n13 … 2026-08-06 drafting" note. (Record: register A-n13.)
- §3.5 恆-register strike — keep the live caveat (恆 [M]-attested; must not propagate onto the Guodian 亙 layer). Delete the filing-history ("this session holds no filed record," "installed as ruled," "held at D2"). (Record: register B-n12.)
- §3.6 the "filing note" about Entry 006 / the σ_B construction — delete from the paper. Keep, as content, only the one-line open statement: whether the two families relate beyond z = ±i remains open, no candidate. (Record: ledger Entry 006.)
- §4 ±1 bullet — keep "the middle is the locus O; the integer 0 is the value written at O." Delete the "Corrected 2026-08-06 … first draft said |0|" parenthetical. (Record: B-n9.)
- §5 note-on-original-paper — keep the two narrowing cautions (the 玄-mapping is one hand; the original was non-canon). Delete the "rewritten 2026-08-06 … Struck" change-note. (Record: register A-n15.)

**HOLD — for Will:** the top provenance code-block (commit hashes, branch archaeology). By the policy this is Layer-3 material; but minimal recovery front-matter ("recovered, rebuilt at v9.52") may be acceptable editorial content. Do not delete unilaterally — flag for Will's call, and if he says move it, its home is register C-n3, which already holds the full version.

**C3. Essay insertions — verify status caveats only, change nothing**
`staging/editorial/series-0{2,3,8}-*.md`, `series-15-*.md`: confirm the inserted brackets are status (`[candidate, pre-survey]`, `[reading; illustration]`, `[open — unruled]`), which are content and stay. If any bracket is change-history rather than status, list it — do not edit.

## D. Verify — report back, change nothing

- **D1.** In the full repo (the uploaded bundle is thin — prerequisite `f93145c` absent — and cannot resolve these), confirm the two provenance hashes back M4/C-n3: `7473b0a72322c67adb2a70ebc480ae868434cb74` (claimed 2026-01-01, author `goldsteinstudios`) and `98154a2d7033cb34188407bd64a0151faef2c6ec` (claimed 2026-03-15); and the "13 refs" enumeration (`git for-each-ref`).
- **D2.** Recover the 2026-08-04 in-session Euler patch text from session record / reflog / stash. Reconcile against the rebuilt paper before either is trusted. If unrecoverable, say so and close the residue as lost.

## E. Survey — enumerate only, no edits

- **E1.** B-n9 sweep: list every location the ±1 / integer-middle exhibit appears. The face/value fix is applied only in the Euler paper §4; the rest is owed to the editorial pass.
- **E2.** 常/恆 blast radius: list every staged or canonical file carrying 常 or 恆 as a register marker, so A1's downstream is visible before finalization.
- **E3.** Confirm errand C7 gates both the 非 tokens and the 有/亡 (grasping-hand / fled-thing) graphic claim in essay 3 — same Han-projection class, one errand.
- **E4.** Report whether the Corollary (formerly L1) has a register entry; if not, note the gap. Do not create the entry — just report. (This is the 2026-08-06 audit finding 1.3.)

## F. Do not

- Do not rule A-n15 (which center), A-n14 (the winding wire), or the σ_B/ν positive write-up (verified as arithmetic; its promotion to a stated result is HELD for Will).
- Do not edit the math chain's Revolution wording (audit 1.1) — confirmed defect, unruled.
- Do not alter essay content; the distribution is reversible pending the book-level ruling.
- Do not promote anything tagged OFFERED or CHECKABLE.
- Do not write rationale, dates, or history into any Layer-1 or Layer-2 file.
