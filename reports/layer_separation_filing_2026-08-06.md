# Layer separation policy — first enforcement pass

**Date:** 2026-08-06. Policy filed at `rsm/layer_separation_policy.md` (uploaded by Will;
standing governance). This report is the pass's Layer-3 record: what was swept, what was
evicted, what is flagged for ruling. **No rulings made; no OFFERED items promoted; no version
stamps changed.**

## Sweep scope and method

- Layer 1: the four v9.5 chain files (`rsm/canonical/chains/v9.5/*.md`, README excluded — see
  boundary cases).
- Layer 2: `staging/editorial/` (42 files).
- Patterns: register item codes (A-n/B-n/C-n, ruling codes), dated correction parentheticals,
  HTML comments, WITHDRAWN/STRUCK/SUPERSEDED/pending language, branch names, commit hashes.

## Evictions applied (Layer 1 — authorized unprompted by the policy)

1. **`just_ddj_v9_5.md` — two pending-rewrite comments removed.** Both read, verbatim:
   *"R5/R6 pending: 生 one form (woman → mother-woman, child); 相 = co-perception; rewrite in
   session"* — one above the 有無相生 entry, one above the Chapter 40 entry. Prohibited on two
   counts (register codes in content; `<!-- rewrite in session -->` comments). Pending status is
   carried by the register (`reports/open_items.md` D1, updated to preserve the comments' full
   text and record this eviction). The rewrites remain pending exactly as before.
2. **`just_math_v9_5.md` — one history clause stripped** from open item 3 (Dimension): "…which
   is chart**; the previously listed cascade is withdrawn**." The standing clause ("Exactly
   three" open, no standing candidate derivation; binding-extortion rests on chart) kept
   unchanged; the withdrawal is history and was already recorded in
   `reports/v9_5_patch_diff_report.md` (PATCH 14: the |1| cascade withdrawn, unattributed).

No dated correction parentheticals, no WITHDRAWN/STRUCK blocks, no branch names, no commit
hashes, and no register codes found anywhere else in the four chains. Structural and physics
chains: clean. **No version bump made** — the evictions remove markers and one history clause,
no claim changes; whether filing-pass edits warrant a stamp note is Will's call.

## Layer 2 findings — no evictions; boundary cases flagged

Clean of register codes throughout. The date hits are of four kinds, none evicted:

1. **Author colophons in Will's originals** (`Date: 2025-11-27 Author: Will Goldstein`,
   "Document created…"): creation metadata, not correction records. Not violations. Left.
2. **Pipeline frontmatter in the parables** (`generated_date`/`processed_date`): provenance-ish
   but original-file metadata, not change-history of a reading. Left; noted as a minor boundary
   case if Will wants frontmatter stripped from staged copies.
3. **History-as-pedagogy in the series essays** — the genuinely ambiguous class, flagged, not
   cut:
   - `series-12-on-energy.md` — the essay's declared subject *is* a retirement ("this one
     documents a retirement and attempts, in public, the replacement"). The history is the
     content. Left; if the policy is meant to reach it, that is a ruling, not a filing move.
   - `series-15-what-pi-names.md` — carries the standing caveat "this may deflate" (explicitly
     a *standing* form in the policy) but wraps it in filing history ("written when it was
     filed," "its old gloss struck…filed and unpromoted"). Mixed lines; stripping the history
     clauses would rewrite Will's expository prose. Flagged for ruling.
   - `series-06-on-the-unit.md` — "the early drafts…occasionally wrote '1 of reality,' and the
     phrase had to be struck": a history clause doing pedagogical work (showing *why* the
     unindexed unit is ill-typed). Flagged, same grounds.

   Common question for the ruling: does Layer 2's "corrections are applied silently" reach
   essays whose *topic* is a correction? The filing agent's read is no — that history narrated
   as exposition is content — but that read is not a ruling.

4. **`staging/editorial/MANIFEST.md`** — a tracking document (provenance, branch names, dates)
   living inside a content directory. Under the policy, tracking lives in `rsm/audit/` /
   `reports/` *and only there* — but the manifest is the staged set's own inventory and sits in
   the flat set deliberately (NotebookLM ingestion). Moving it breaks self-containment; leaving
   it breaks the letter of the policy. **Flagged for ruling; not moved.**

## Boundary case — `rsm/canonical/chains/v9.5/README.md`

The README is not a chain file (no assertions) but lives in the canonical directory and is
almost entirely change-history: patch summaries, ruling attributions, the diff trail, skip
records. Under the policy that is Layer-3 material. A compliant README would carry the file
table, "Not sealed," and a pointer to the register and diff trail — nothing else. **Not done
unprompted**: the README's orientation function is real, and gutting it is more than moving a
change-record. Flagged for ruling.

## Alongside

- Policy filed at `rsm/layer_separation_policy.md`; pointer added to `CLAUDE.md` Reference
  Locations.
- `reports/open_items.md` D1 updated (eviction recorded, comment text preserved).

## What this pass did not do

Rule on any flagged case · touch the series essays, parable frontmatter, MANIFEST, or README ·
bump any version stamp · promote anything. The policy's may-not list was the working constraint
throughout.
