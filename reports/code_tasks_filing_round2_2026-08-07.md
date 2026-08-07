# Code tasks 2026-08-06 — round 2 filing record

Source now captured at `rsm/audit/code_tasks_20260806.md` (the §2a gap from
`reports/parallel_session_capture_2026-08-07.md`, closed). Round 1 ran on the mobile session and is
recorded at `reports/code_tasks_filing_2026-08-06.md`. This round completes the items round 1 could
not reach, because C1–C3 target the Euler paper and essay insertions, which merged **after** that
pass ran. Mechanical only. **Nothing ruled; no OFFERED or CHECKABLE item promoted; every HOLD held.**

---

## Already applied, verified in the merged tree — no action taken

| Task | State |
|---|---|
| **A1** register-marker gloss | Applied. `just_ddj_v9_5.md:27` now reads 恆, [M]-attested; received 常 as the post-taboo form (避諱, Emperor Wen); Guodian attests 亙. Trailing checksum pointer gone. |
| **A2** delete the 恆/常 checksum bullet | Applied. Checksum list is five items. |
| **A3** remove both R5/R6 pending comments | Applied. Zero occurrences. |
| **B0** convergence sentence | Applied. `CLAUDE.md:11` now reads "a shared referent, not evidence for a claim; the framework runs from a conditional and accumulates no confirmation." |

---

## Executed this round

**C1 — §3-WITHDRAWN deleted** from `staging/editorial/paper-euler-single-operation.md`. Whole block,
28 lines. Content preserved in divergence-ledger Entry 006, as stated.

**C1a — one unenumerated deletion, reported because it was not on the list.** §3's opening line was a
filing note (*"Drop-in replacement for the prior §3, written in the soundness lane 2026-08-06 … retained
beneath, in §3-WITHDRAWN, as the record"*). C1 deleted its referent, leaving a dangling pointer. Removed
under the policy's standing authority to move history out of content. **Deliberately kept:** the
"the prior §3 said / located" references in §3.1, §3.3 and §3.4. C2's own instruction for §3.1 keeps
that framing, which settles them as content — they state what a reader might wrongly believe and why
it fails, not who edited when.

**C2 — five correction-notes stripped, corrected statements kept:**

| § | Deleted | Kept |
|---|---|---|
| 3.1 | the "originates in A-n13, not the 2026-08-06 drafting" note | the Q_i/trace statement and the withdrawal |
| 3.5 | "this session holds no filed record", "installed as ruled", "held at D2", the survey and B2 citations | the live caveat: 恆 is [M]-attested, the Mawangdui silks are where it reads, must not be read back onto the Guodian layer, which attests 亙 |
| 3.6 | the whole "Filing note" paragraph (Entry 006, the σ_B construction, who offered it) | the one-line open statement: whether the two families relate beyond z = ±i is open, no candidate |
| 4 | "Corrected 2026-08-06 … the first draft said |0|" | the middle is the locus O; the integer 0 is the value written at O; and the sign-collapse face as the fitting one if a P₀ face is wanted |
| 5 | "rewritten 2026-08-06 … Struck" | both narrowing cautions — the 玄-mapping is one hand; the original was never canon |

**C3 — verified, nothing edited.** All eight brackets across the four essays are status, not
change-history:

`series-02`: `[curing-pile observation, not canon]`, `[open — a question about referents, unruled]` ·
`series-03`: `[candidate]`, `[candidate, pre-survey]`, `[candidate; the anchor 去彼取此 is received-only, [R]]`, `[reading; illustration, not attestation]` ·
`series-08`: `[reading — expository; nothing under it is new]` ·
`series-15`: `[observation]`

No change-history brackets found. **One caveat, not a bracket:** `series-03` carries an inline
`[Update, and it needs a ruling: the 非 survey has since run …]` paragraph. It is partly status (what
the survey found, what remains unruled) and partly history (that the tag above it is stale). Flagged,
not edited — it was inserted by ruling and F forbids altering essay content.

---

## D — verifications

**D1 — both hashes confirmed real; 13 refs confirmed.**

- `7473b0a72322c67adb2a70ebc480ae868434cb74` — 2026-01-01, author **goldsteinstudios**, *"RSM v0.993: Single-operation Euler identity."* Claim matches on all three fields.
- `98154a2d7033cb34188407bd64a0151faef2c6ec` — 2026-03-15, *"Slim main to Astro site build + deploy files only."* Matches.
- `git for-each-ref` → **13**: 2 local heads, 11 remote-tracking. The "not found across 13 refs" phrasing in C-n3 is accurate for this clone.

**D2 — the 2026-08-04 in-session Euler patch is UNRECOVERABLE from here. Close the residue as lost.**

The reason is structural, not a search failure. **This working copy was cloned fresh on 2026-08-06 at
18:16 UTC.** Its reflog therefore begins at that clone and contains 11 entries, all from this session.
There is no stash, no dangling object, and no commit touching the Euler paper after 2026-01-01 except
the 2026-03-15 removal. A patch made in a chat session on 2026-08-04 and never committed leaves no
trace in a clone made two days later — the reflog records this repository's operations, not another
session's.

Where it could still exist: the 2026-08-04 chat session record itself, or a working copy on the
device that was live that day. Neither is reachable from this container. **Recommend closing C-n3's
second residue as lost**, and noting in its place that the rebuilt paper was verified against the
canon it claims to implement rather than against the lost patch.

---

## E — surveys, no edits

**E1 — the ±1 / integer-middle exhibit, every Layer-1/2 location.** The face/value fix is applied in
one of four.

| Location | State |
|---|---|
| `paper-euler-single-operation.md` §4 | **Fixed.** O as the locus, 0 as the value written there, sign-collapse named as the fitting face |
| `series-02-on-the-center.md` line 8 ("the pair ±1"), lines 10 and 18 (sign-collapse) | **Owed.** Uses the exhibit inside the which-center paragraph |
| `series-08-on-names.md` line 12 ("the integers wear it — −1 and +1, which obtain, naming in their sum a middle that does not") | **Owed.** This is the exhibit's clearest statement and it does not carry the guard |
| `just_math_v9_5.md` line 7 (Notation, the threefold presentation set) | **Not owed.** States the faces correctly as notation; makes no claim about the integer |

Register entry B-n9 already records the sweep as outstanding; this is its enumeration.

**E2 — 常/恆 blast radius. A1 changed the marker at one line; six lines in the same file still use 常
as the marker, and one of them is a gloss rather than a quotation.**

| File | Line | Use | Type |
|---|---|---|---|
| `just_ddj_v9_5.md` | **11** | *"**可 and 常 are the explicit and implicit registers.** 常 is what holds frame-independently, parameter-free"* | **Gloss, not quotation.** Directly contradicts line 27, which now names 恆 as the marker. This is the sharpest item in the survey |
| `just_ddj_v9_5.md` | 27 | 恆 as marker, [M]-attested | The A1 edit |
| `just_ddj_v9_5.md` | 13, 23, 63 | 道可道非常道, 名可名非常名 | Quotations — the HOLD's subject |
| `just_ddj_v9_5.md` | 21 | 常道 :: the entailment as such; 可道 :: any framed statement | Gloss on quoted terms — borderline |
| `just_ddj_v9_5.md` | 35 | 常名 :: XY = 1 | Gloss on a quoted term — borderline |
| `just_ddj_v9_5.md` | 39 | 常無欲以觀其妙 (already notes the Mawangdui 恆無欲 parsing) | Quotation, already carries the 恆 variant |
| `CLAUDE.md` | 313–315 | *"可 and 常 are §0's explicit and implicit registers: 常 is what holds frame-independently"* | **Meta layer. Same gloss as line 11, same contradiction.** Not a chain, so outside A1's scope, but it now disagrees with canon |
| `staging/editorial/series-09-on-balance.md` | — | carries 常/恆 | Layer 2; editorial pass |

Superseded chains (v9.4, v9.3, v9.2, v9, v7.x) also carry 常 throughout and are history — no action.

**E3 — C7 does NOT gate both. Gap confirmed.** `reports/open_items.md` C7 reads, in full:
*"The 非 survey's Guodian graphs — Facsimile verification of the ~6 tokens behind 'no token negates
between conjugate opposites' (the exposure the DDJ chain carries in place)."* It names the 非 tokens
only. The 有/亡 grasping-hand / fled-thing claim in `series-03` is the same Han-projection class and is
not named anywhere in C7. Register entry **B-n11** asserts C7 gates both; **that assertion is
currently false of C7's text.** Either C7's scope is widened or B-n11 is corrected. Reported, not
fixed — F forbids editing the register's content here.

**E4 — the Corollary has no register entry. Gap confirmed, re-verified.** Zero occurrences of
"Corollary" in `reports/open_items.md`. Formerly L1, "the single head of the audit," carrying four
loads; load-bearing in structural §4's floor argument and in the math chain's unit/floor section.
This is audit finding 1.3, still open. Not created, per instruction.

---

## HOLDs — surfaced, not acted on

1. **A-HOLD, received-常 quotations.** Untouched. E2 above is its enumeration. Note the survey found
   something the HOLD did not anticipate: **line 11 is a gloss, not a quotation**, and it contradicts
   line 27 outright. The quotation-vs-gloss decision the HOLD reserves does not cover it, because it
   is not a quotation — it may need deciding before the finalization pass rather than in it. Same
   text in `CLAUDE.md` 313–315.
2. **C-HOLD, the Euler paper's top provenance block.** Untouched. Full version is in register C-n3.

## Not touched, per F

A-n15, A-n14, the σ_B/ν write-up, the math chain's Revolution wording (audit 1.1), essay content, and
anything tagged OFFERED or CHECKABLE.

---

*Not sealed. Executions are verifiable by diff; D1 re-runs; D2's negative rests on the clone date,
stated above.*
