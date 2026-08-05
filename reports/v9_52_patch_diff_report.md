# v9.52 patch diff report (chain patch set 5)

Applied 2026-08-04, in place on `rsm/canonical/chains/v9.5/`. Single content patch, math chain
only, plus the stamp sweep. Register source: A-n4.

## PATCH 27 — the two-returns theorem (`just_math_v9_5.md`, Theorems)

Replaced in full, exact-match verified against the v9.51 text. What changed:

- **The displayed instance:** e^{iπ} + e^{i·0} = 0 → **e^{iπ} + e^{i·2π} = 0** — the traversal
  reading ("out and back: the far pole and the returned position"), per Will's ruling ("going
  from π to 0 makes no sense — at the very least it should be e^{iπ} + e^{i·2π} = 0, out and
  back"). The constitutional reading (the same pair at θ = 0, without traversal) is retained
  beside it.
- **Struck by ruling:** "not five constants in miraculous conjunction" (editorial voice, no
  derivational content) and the reinstatement narrative ("its right form was typed in an earlier
  chain and dropped in transit" — provenance, belongs in a change log, not a chain).
- **Unchanged:** Q_j = 1ₙ·cos 2θ, the double cover, the general form e^{iθ} + e^{i(θ+π)} = 0,
  the no-single-θ point, the ν-centroid tie, the rendering typing.

**Flag carried from the patch set (note 3):** the winding-ambiguity clause ("the familiar **+1**
is ambiguous between e^{i·0} and e^{i·2π}…") is **Claude's, not Will's** — register A-n4, OFFERED
and chart-checkable, included because the corrected form otherwise appears without its reason.
**If Will strikes it, the passage reads directly from "compressed" to "The traversal reading
is."** The register's A-n4 entry now carries this note.

## PATCH 28 — stamp sweep, confirmed

All four titles and closing lines v9.51 → **v9.52** (structural, math, physics, DDJ — verified,
one hit each). README retitled with the patch summary; `CLAUDE.md` canon block and the register's
canon pointer → v9.52; register item A-n4 carries the applied-note.

## Post-check (report only, not fixed)

- **`e^{i·0}`** — one occurrence in the four chains: `just_math_v9_5.md`, inside PATCH 27's own
  replacement text (the winding-ambiguity clause names both windings). By design.
- **"five constants"** — zero occurrences in the four chains.

## Out of scope, unchanged

PATCH 25 (two-horns placement, awaiting ruling) · the share-noun · the R5/R6 rewrites · the [M]
re-tag policy · the DDJ finalization items · the slip-image batch · the 為 survey · all OFFERED /
editorial register items, including A-n13 (no chain target).
