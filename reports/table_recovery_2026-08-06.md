# Table recovery — round 1 (2026-08-06)

Against `reports/recovery_needed.md` §1 (the NotebookLM exports dropped every markdown table).
Twelve files uploaded from the iMac's `research/archive/icloud_import/`. **Two clean recoveries
applied; one blocked as a version decision; the rest are misses.** Nothing ruled, no prose edited
— restoration only, and only where the original was verified a content superset of the staged
copy.

## The filter that sorts them (use this to find the rest)

A file whose first lines read

```
# <name>.md
notebook: Our Infinite Reality <version>
source_id: <uuid>
```

**is a NotebookLM export — already table-stripped, and already in the repo.** Uploading these
adds nothing. The files worth pulling are the ones **without** that header: true originals, with
their tables and code blocks intact. Of the twelve uploaded, three lacked the header and two of
those were live recoveries.

## Applied

**1. `staging/editorial/expansion-helix-structure.md`** ← `helix_structure.md` (true original,
December 2025). Verified: prose byte-identical after normalization; the original is a strict
superset. All four sections listed in `recovery_needed.md` §1 restored —

- **The Convergence** — the four-substrate table (rain chain / spiralized zucchini / DNA / 陰陽)
- **RSM Mapping** — the six-row helix-element ↔ RSM-component table (including
  `Empty axis → O (origin, unoccupiable center)` and `Two intertwined strands → G ⊥ B`)
- **The Complete Picture** — the six-line substrate code block
- **The Stretched Zucchini** — the flat-ribbon → twisted → end-on `☯` code block

Plus two tables not named in the errand: the DNA base-pairing table and the 常/動 element-role
table. **Consequence for the recovery pull:** the rain-chain draft sent to Will on 2026-08-06 was
the stripped version; this is now the complete document, and the pull copy at
`batches/recovery-pull-paradox-at-center/02_helix_structure_rain_chain.md` is superseded by it.
*Flag, not repaired:* the restored RSM Mapping table types O as "unoccupiable" — the retired
`Cₙ`/`Sₙ±` vocabulary — and reads G ⊥ B as orthogonal, which canon prices as a rendering fact.
Both are pre-canon drafting, left as written.

**2. `staging/editorial/expansion-chapter76-v0972.md`** ← `chapter76_20251126.md` (true original,
333 lines vs the export's 132). Verified superset by aggressive normalization: every staged line
is present in the original; the five apparent exceptions are blockquote line-splits ("When humans
live, they are yielding and pliable. / When they die, they are hard and stiff." — one line in the
export, two in the original), not divergent text. Restored: **Character-by-Character
Decomposition** and **Key Structural Terms** (the two consecutive headings that had zero content
between them) and the tabular parts of **The Complete Teaching** — 62 table-pipes where the
staged copy had none.

## Blocked — a version decision, not a recovery (for Will)

**`staging/editorial/expansion-packed-hanging.md`** ← `The_Packed_Hanging_Discovery.docx`. This
upload is **not the original of the staged file** — it is a sibling draft, and it is *older*:

| | Staged copy (`077-packed-hangingmd`, v0.971) | Upload (`.docx`, notebook 0.97) |
|---|---|---|
| RSM Integration / Sphere Proof / Generation Sequence | present | **absent entirely** |
| Ch. 37 為無為 reading | "implicitly enacts-void… the void-creating operation" | "non-acts… The pattern doesn't do anything" |
| Translation Implications lists | headings dangle, empty | **filled** (常: 道常無為, 知常曰明, 復命曰常; 可: 道可道, 可以為天下母) |
| Key Term Summary | heading, empty | analogous list under "The Complete Picture" (常可無有玄道) |
| **The Four Recursion Types Mapped** | heading, empty | **absent — not recoverable from this file** |

So the upload could fill two of the three gaps, but only by **transplanting content from an
earlier draft whose reading of 為無為 the staged version has since moved off**. That is a version
merge, not a table restoration, and it is exactly the silent-replacement shape the ledger tracks
(Entries 003/004). **Not applied.** Either the true v0.971 original turns up, or Will rules the
transplant. The Four Recursion Types table needs the real original regardless.

## Misses — already in the repo, nothing gained

| Upload | Why |
|---|---|
| `069helixstructure.md` | Export header (notebook 0.97), 0 tables — same stripped family as the repo copy |
| `06_technology_index.md` | Export header (v.972), 0 tables. Still missing the two Universal Failure Modes, the cross-substrate table, and the Reading Your Tools list. **Craft family — set aside; not chased** |
| `technology_index_anachronism_check.md` | **Byte-identical to `reports/technology_index_anachronism_check.md`** — this repo's own report, round-tripped |
| `040chapter76_20251126.md` | Export header (v.972), 0 tables — superseded by recovery 2 above |
| `chapter76.md` (site frontmatter) | **Byte-identical to `src/content/translations/chapter-76.md`** — already in the repo |
| `025chapter40_11.4.25.md` | Export header (notebook "The Map Under The Map"), 0 tables |
| `030chapter40_20251126.md` | Export header (v.972), 0 tables |
| `011chapter05_20251126.md` | Export header (v.972), 0 tables |
| `024chapter05_11.17.25.md` | Export header (v.96), 0 tables |

## Still outstanding after this round

- **Chapter 40** — no true original uploaded; both candidates are stripped exports.
- **Chapter 05** — same; both stripped.
- **Packed/hanging** — needs the genuine v0.971 original (or a ruling on the transplant).
- **Technology index** — craft family, set aside.
- The ten `v0.96` filename-only stubs (`041`–`050`) — PNG chart records, unaffected by this round.
