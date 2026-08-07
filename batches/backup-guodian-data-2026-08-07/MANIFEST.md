# Backup — the Guodian structured data

**Pulled 2026-08-07** from `~/claudecode/ourinfinitereality_sandbox/data/ddj/` on `wills-imac-local`.
Four files, 1.13 MB. **Backup only. Not canon, not a relocation, not a change to the `data/` exclusion.**

| File | Size | Device mtime |
|---|---:|---|
| `guodian_interactive.json` | 656 KB | 2026-07-15 |
| `guodian_chapter_mappings.json` | 370 KB | 2026-06-09 |
| `verified_transcriptions.json` | 77 KB | 2026-06-09 |
| `character_dictionary.json` | 30 KB | 2026-07-08 |

## Why

`.gitignore` excludes `data/` wholesale, under the comment *"Directories removed from main (live on
other branches)."* That was a branch-hygiene decision. Its side effect is that the project's
irreplaceable primary data has **no copy in any branch of any repository**.

`guodian_interactive.json` is the dataset `reports/heng_chang_distribution_survey.md` runs on — the
survey behind R18, B2, and the 恆/常 footing. That report states the problem itself:

> *"`tools/dedupe_guodian_slips.py` documents that this dataset's source CSVs are gitignored and
> off-disk — the dataset is currently unreproducible from tracked inputs."*

So the survey's evidence existed in exactly one place, on one machine, unreproducible. It does now
exist in two.

## Still unbacked, and it is the bigger one

**`data/ddj/Guodian Strip Glyphs/` — 1,717 image files, 3.1 MB, sole copy.**

Counted on the device 2026-08-07. In no branch of any repo. `archive/INVENTORY.md` finding F called
this out at the consolidation:

> *"**The Guodian glyph corpus has no git backup.** `data/` is gitignored on every branch, and
> `git ls-tree` confirms zero branches track a single glyph PNG. The archive copy was the only
> redundancy; after dedup, `data/ddj/Guodian Strip Glyphs/` (1,717 files) is the sole copy.
> **This warrants a real backup decision.**"*

That was written 2026-08-01 and nothing followed. It was not pulled here because `device_bash`
failed repeatedly and `device_stage_files` caps at 50 files per call — 1,717 files is 35 calls.

**One command on the iMac fixes it:**

```
cd ~/claudecode/ourinfinitereality_sandbox/data/ddj && \
tar czf ~/guodian-strip-glyphs.tgz "Guodian Strip Glyphs"
```

That produces roughly a 3 MB tarball. Hand it back and it lands in this directory as a single
tracked file — the whole corpus, one blob, versioned.

Also unbacked in the same directory and not pulled: `calligraphy/` and `guodian_strips_full/`,
both unexamined.

## Note on the `data/` exclusion

Nothing here overturns it. These are copies filed under `batches/`, following the recovery-pull
convention. If `data/` should stop being excluded, that is a ruling, and this backup does not make
it.

---

*Not sealed. Sizes and counts are from the device listing of 2026-08-07.*
