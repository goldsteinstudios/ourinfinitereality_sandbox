# v9.53 patch diff report (chain patch set 6)

Applied 2026-08-07, in place on `rsm/canonical/chains/v9.5/`. **One content patch, math chain
only, plus the stamp sweep.** Authority: **R3 (2026-08-02)** — no new ruling. Source finding:
`reports/chain_finalization_audit_2026-08-06.md` §1.1.

This is a propagation, not a step. R3 demoted revolution from *forced* to *admitted* and assigned
the relation between the two mode-dominant regions to **descent**. The structural chain and the
physics chain both carried the demotion at v9.5. The math chain did not — the one chain whose
entry is named "Revolution."

## PATCH 29 — the Revolution entry (`just_math_v9_5.md`, line 60)

Replaced in full, exact-match verified against the v9.52 text.

**Before:**

> **Revolution**. The relation between the two portions is carried by revolution of Gₙ about Bₙ.
> A half-turn about B realizes σ_B as continuous motion, so the two portions exchange with nothing
> passing through b = 0. …

**After:**

> **Revolution**. The relation between the two portions is carried by descent (the Recursion entry
> below), whether or not any motion realizes it. What the rendering additionally admits is
> revolution of Gₙ about Bₙ: a half-turn about B realizes σ_B as continuous motion, so the two
> portions exchange with nothing passing through b = 0. …

**The wording was taken, not invented.** Structural §6 ("Rotation") reads *"the relation is carried
by descent (§7) … whether or not any motion realizes it. What the structure additionally admits is
revolution"*; physics §1 reads *"the relation between them is carried by descent. What the structure
admits besides is revolution."* The patch says the same thing in the math chain's own vocabulary —
**portions** not regions, **rendering** not structure (the math chain is a rendering and does not
speak for the spine), and an internal pointer to its own Recursion entry rather than to structural
§7, since no rendering cites another chain.

**Unchanged in the entry:** the half-turn realizing σ_B, the exchange with nothing passing through
b = 0, the direction-the-plane-lacks requirement, the open dimension count, the ring of orientations
and the one-selection-one-branch reading. Nothing downstream of the entry was touched.

## PATCH 30 — stamp sweep

All four titles and closing lines v9.52 → **v9.53** (structural, math, physics, DDJ — verified, one
hit each). README retitled with the patch-set note. `CLAUDE.md` canon block (two places) and the
open-items register's canon pointer → v9.53.

## One tracking correction

`reports/open_items.md`, "Removed at regeneration": the **A6-old** row states that "the v9.5 chains
state revolution as admitted, the relation carried by descent." That was true of two chains of
three when written. The row now carries the qualification and the date the third caught up. **The
ruling did not change; the record of it was ahead of the text** — which is the reason a closed-item
row is worth re-reading against the chains rather than trusted as a summary of them.

## Verification

- `carried by descent` — one occurrence in each of the three chains that state it (structural,
  physics, math).
- `carried by revolution` — **zero occurrences in the v9.5 set.** It survives in four superseded
  files, correctly: `v9.4/just_math_v9_4.md:60` (the text this patch supersedes) and three in
  `v9.3/transcription_2026-08/` — the structural chain's pre-demotion "structurally forced"
  wording, the math chain's, and the v9.3 change log's section-B entry submitting
  revolution-as-forced for adversarial read. That entry is where R3 came from. History, left alone.
- `python3 rsm/audit/checks.py` — **PASS**. (A rendering fact outright; the script computes in a
  signed chart. Nothing here depends on it.)
- Version stamps: four titles and four colophons at v9.53, one hit each.

## What this patch set is not

**No open item closed. No OFFERED or CHECKABLE item promoted. No ruling made.** The register is
the same length it was at v9.52.

## Considered and excluded — each awaiting a ruling, none applied

- **Audit 1.3 / E4 — the Corollary has no register entry.** Load-bearing in structural §4's floor
  argument; it was v7.7's L1, "the single head of the audit," carrying four loads. Creating the
  entry is a register act, not a propagation.
- **E2 — `just_ddj_v9_5.md` line 11 vs line 27.** Line 27 names 恆 as the register marker; line 11
  still glosses 常. A gloss, not a quotation, so the quotation-vs-gloss HOLD does not cover it —
  but which way it resolves is Will's. Same sentence sits in `CLAUDE.md` 313–315.
- **E3 — C7 vs B-n11.** C7 names only the 非 tokens; B-n11 asserts C7 also gates the 有/亡
  grasping-hand reading. False of C7 as written. Either C7 widens or B-n11 corrects; both are
  rulings.
- **E1 — the ±1 face/value fix** is owed in `series-02` and `series-08`. Essay-layer, and the
  distribution is reversible pending the book-level ruling.
- **PATCH 25** — the two horns' closure behavior. Drafted at v9.51, skipped then, skipped here.
  Register item A-n12.
- **The share-noun (B4)** — "the constitutive share" is HELD, replacement unruled.
- **The [M] re-tag policy (B3)** — candidate list filed, flips unmade.
- **A-n13, A-n14, A-n15** and the σ_B/ν write-up — all OFFERED or HELD; A-n13 stands CORRECTED
  after the conjugate/antipodal weld (divergence ledger Entry 006) and has no chain target.

## Standing, unaffected by this set

`rsm/audit/register_update_2026-08-06.md` is **still unmerged** into `reports/open_items.md`. The
register now carries one merged strand and one pending from the same two days; the next
regeneration should take both.

Diff trail: `v9_4_patch_diff_report.md` → `v9_4_1…` → `v9_4_2…` → `v9_5…` → `v9_51…` →
`v9_52…` → **this file**.
