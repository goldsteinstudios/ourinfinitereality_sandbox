# Parallel session capture — 2026-08-07

**What happened.** Two sessions worked branch `research-archive` concurrently on 2026-08-06/07: a
desktop Cowork session (the audit, the equals-sign thread, the Euler recovery, the voice work, the
glyph inventory, the D5 scoping ruling) and a **mobile session on iPad/iPhone** (the layer separation
policy and its first enforcement pass, the code-tasks filing pass, two recovery pulls). Neither knew
about the other until the desktop session fetched.

**Merged** at `27e1b1f`, no conflicts, no overlapping files, `checks.py` passing. This report is the
Layer-3 record of the reconciliation.

---

## 1. What the mobile session did, and it stands

| Commit | Date | What |
|---|---|---|
| `34a7da6` | 08-06 | Filed `rsm/layer_separation_policy.md` (Will's upload, standing governance) and ran the first enforcement pass over the four v9.5 chains and 42 staging files |
| `d1dcddd` | 08-06 | Executed the 2026-08-06 code tasks: the 常→恆 register-marker ruling, the 恆/常 checksum deletion |
| `35f683e` | 08-07 | Recovery pull — the paradox-at-the-center documents, five files into `batches/recovery-pull-paradox-at-center/` |
| `bf10e68` | 08-07 | Recovered dropped tables: helix structure, chapter 76 |

**It closed two findings from `reports/chain_finalization_audit_2026-08-06.md`**, both annotated in
place there:

- **§1.2** — the DDJ chain's 恆/常 overstatement. Deleted, not softened, with the three strata
  correctly assigned. The audit had this as CONFIRMED against the survey; the fix matches the survey.
- **§1.5** — `CLAUDE.md`'s convergence-as-evidence sentence, which the audit flagged as describing an
  architecture the chains do not run. Rewritten to "a shared referent, not evidence for a claim."

It also **answers B-n12** in `rsm/audit/register_update_2026-08-06.md`. That flag read: the corrected
Euler §3 cites a "2026-08-06 identity ruling" for which this session holds no filed record. The record
exists — `reports/code_tasks_filing_2026-08-06.md` A1, with provenance on the taboo mechanism, the
Bundle A survey, and R18. **B-n12 is retired.**

And it cleared one of the first-draft blockers listed in `reports/voice_profile_2026-08-06.md` §6: the
two `<!-- R5/R6 pending -->` comments are out of canonical text, preserved verbatim in `open_items` D1.

---

## 2. Loose after the merge — three items

### 2a. An input was never captured
`reports/code_tasks_filing_2026-08-06.md` names its own source as *"Will's upload
`code_tasks_20260806.md`."* **That file is not in the repo.** Only the report about it is.

The policy document from the same working session *was* captured (`rsm/layer_separation_policy.md`,
also a Will upload). The task file was not. So the pattern is inconsistent rather than absent, which
is the harder kind to notice.

Consequence, already visible: the filing report records that *"the task file's A1 delegates that
filing to 'B1 below,' but the task file contains no B1 (its B section holds only B0)."* A gap in an
input that no longer exists cannot be checked. The report carried the record forward correctly, which
is the right response, but the underlying document is gone unless it is still on the device.

**Recommendation:** uploads that drive a filing pass are Layer-3 inputs and should land in
`rsm/audit/` or `reports/` alongside the report they produced. `code_tasks_20260806.md` should be
recovered from the iPad if it still exists.

### 2b. Two audit findings remain open, untouched by either session
- **§1.1** — `just_math_v9_5.md` line 60 still reads *"The relation between the two portions is
  carried by revolution of Gₙ about Bₙ."* Structural §6 and physics §1 both assign that to **descent**,
  with revolution only additionally admitted. This is R3's demotion, propagated into two chains of
  three, still absent from the one whose entry is named "Revolution."
- **§1.3** — the **Corollary** (v7.7's L1, formerly "the single head of the audit," carrying four
  loads) has no entry in `reports/open_items.md`. Verified again post-merge: zero occurrences.

### 2c. Two parallel records that do not reference each other
`rsm/audit/register_update_2026-08-06.md` (desktop: A-n13 corrected, A-n14, A-n15, B-n8…B-n12, C-n3,
D5) is still an **input file awaiting merge** into `reports/open_items.md`, on the 2026-08-04 pattern.
The mobile session's work updated `open_items` D1 directly. So the register now has one strand merged
and one strand pending, from the same two days.

**Recommendation:** the next `open_items` regeneration should take both, and should note that
2026-08-06/07 had two sources.

---

## 3. A standing note, since this will recur

Work now arrives on this branch from more than one device and more than one session, asynchronously.
Two consequences worth making habit:

1. **Fetch before starting a stretch of work.** The desktop session ran a full audit against a branch
   tip that was four commits stale by the time it finished, and reported two defects that were being
   fixed elsewhere while it wrote.
2. **The divergence was productive, and is data.** Per the ledger's standing posture: convergence
   between instances is priced near zero, divergence is the signal. Here the two sessions did not
   converge — they did *different* work, and one closed findings the other could only report. That is
   the collaboration working, not a coordination failure, and it should not be engineered away.

---

*Not sealed. §1 is verified against the merged tree; §2a is a gap; §2b re-verified post-merge.*
