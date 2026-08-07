# The DDJ retranslation corpus — first read

Read 2026-08-07 at Will's instruction ("have you read them? if not you should"). Honest starting
position: I had not. I had touched three files incidentally during table recovery and never read
the corpus as a body. **Survey and findings only — nothing edited, nothing ruled.**

## What is there — 36 chapters, five lineages

| Lineage | Location | Count | Vintage | Character |
|---|---|---|---|---|
| **Site** | `src/content/translations/` | 10 (ch. 1, 2, 8, 11, 22, 25, 40, 42, 64, 76) | Dec 2025, versioned | The developed set: frontmatter with `version`, `confidence`, per-element `confidenceNotes`, change logs, key-term tables, Guodian attestation blocks |
| **Lexicon exports** | `archive/rsm-versions/v0.96`, `v0.971`, `v0.972` | ~33 chapters × up to 3 vintages | Nov–Dec 2025 | Chapter analyses in the structural-lexicon house style; NotebookLM-stripped (tables gone) |
| **dao_ch** | `archive/ddj/translations/dao_ch*.md` | 20 (ch. 1–16) | earlier | A separate translation lineage, not folded into the others |
| **ttc analyses** | `archive/ddj/ttc_chapter*.md` | 4 (ch. 11, 28, 36, 78) | Jul 2025 | Oldest stratum; ch. 28 and 36 exist **only** here |
| **corrected_** | `archive/ddj/translations/corrected_*.md` | 3 (ch. 1, 11, 42) | — | Revision passes over the dao_ch lineage |

Coverage: **chapters 1–12, 14, 16, 21, 22, 25, 28, 34, 36–42, 46, 48, 51, 52, 56, 64, 65, 76, 78,
81.** Chapters 28 and 36 have a single witness each (the July 2025 ttc analyses) — sole copies.

## The apparatus is better than the chains'

Worth saying plainly, because it bears on an acknowledged loss. v9.3 struck the epistemic tag
system, and `CLAUDE.md` records the cost: standing must now be read out of prose, per claim, with
nothing marking it. **The site translations never lost theirs.** Each carries per-element
confidence at named levels with reasons, a version history, and — in ch. 1 — an explicit
withdrawal recorded as content:

> 名's obtainedness is held OPEN in the current framework — an earlier version read 名 as settled,
> and that reading has been withdrawn. The live candidate is the 明/名 split.

That is exactly the per-claim standing marker the chains now lack, already working in production.
If footnotes are adopted (Will's suggestion, same session), this frontmatter is the model to copy
rather than invent. **Note the layer question it raises:** `changes:` blocks and "an earlier
version read…" are change-history living in content files. Under the layer policy that is Layer 3
— but these are the site's own versioning apparatus, not stray correction notes, and the policy
was written for chains and staging. Flagged as a boundary case, not touched.

## Finding 1 — the 玄 ruling is violated across live site copy, and the guard CLAUDE.md claims does not exist

The ruling (`CLAUDE.md`): **玄 is paradox; 牝 is generative; 玄牝 is the generative paradox.** The
compound is compositional, "so **'generative' must not be folded into 玄**, or 玄牝 reads as
generative-generative and the argument dissolves."

`CLAUDE.md` then states this was fixed: *"Site copy that glossed Pₙ as 'the generative crossing'
was corrected 2026-07-29 to the paradoxical center, and `site_vocab_lint.py` now enforces it."*

**Both halves of that sentence are false in this repository.**

- **"generative crossing" appears 26 times repo-wide**, including live site content on *both*
  `research-archive` and `origin/main`: `chapter-01.md`, `chapter-02.md`, `objects/origin.mdx`,
  `objects/tree.mdx`, `objects/wheel.mdx`, `essays/topology-of-being-alive.md`, and on `main`
  additionally **`src/pages/index.astro` (×2) and `src/pages/docs/rsm/rosetta-stone.astro` (×4)**
  — the homepage and the page that teaches the discipline before any chain appears.
- **"paradoxical center" appears nowhere in `src/`** on either branch — only in audit files and
  the v9.4 chain.
- **`rsm/audit/site_vocab_lint.py` contains no 玄 rule whatsoever.** Its only "generative" string
  is an unrelated authority note about the DDJ being subject of translation. It also still reads
  `CURRENT_CHAINS = CHAINS / "v9"` — four versions behind canon.

`chapter-01.md` carries it three ways: a confidence element titled *"玄 (generative center)"* at
level **strong**, a key-term gloss *"玄 :: the generative crossing"*, and a change-log line
*"Clarified 玄 as generative center."* `chapter-02.md` embeds it inside the 弗居 note — the entry
the chain calls the strongest `[G]`-stratum correspondence in the framework.

This is the failure class `CLAUDE.md` itself warns about — "do not mistake a clean run for clean
text" — one turn worse: the guard named as the remedy was never built. **Reported, not fixed:**
the wording that replaces it is a ruling, and the blast radius spans two branches including the
site's front door.

## Finding 2 — chapter-by-chapter drift against current canon

Each is reported, none repaired.

**Chapter 1**
- Key terms: *"常 | cháng | implicit / frame-independent / pre-distinction"* — **stale as of
  today's ruling**; the register marker is 恆.
- *"無名天地之始"* is translated off the **received 天地**. The chain's 始/母 entry sources its
  reading to the Mawangdui manuscripts (萬物 in both clauses) and treats the received 天地 as the
  substitution it rejects. The translation follows the reading canon declines.
- *"此兩者同出而異名"* → "emerge together yet **illuminate** differently." 異名 is *differ in
  name*; "illuminate" imports the 明 sense — awkward given that the same file's confidence note
  makes the 明/名 split the live open candidate.

**Chapter 2**
- Six pairs given in received graphs with received verbs (生/成/形/傾/和/隨). The v9.5 PATCH 16
  attestation check found the strips read **生/城/型/浧/和/墮**, every clause 也-stamped. The
  site's own argument — "varying verbs suggest structural analysis, not rhetorical flourish" — is
  *strengthened* by the strip readings. **A free upgrade, not a correction.**
- **前後 is not what the strips read.** They have **先**, and the 後-slot graph is unresolved (○)
  in the dataset. The site presents 前後 as attested; the chain carries the exposure and the
  errand.

**Chapter 40**
- The Guodian line is quoted accurately, **溺** included — but the confidence block rates *"弱 as
  yielding (not weakness)"* **strong** with no mention that 溺 is an open DDJ checksum item, read
  in the chain as attested-uninterpreted. The strongest claim in the file sits on the graph the
  chain refuses to interpret.
- *"反 … Character shows 又 (hand) flipping under 厂 (cliff) = rotation"* rated **strong** — a
  reading-structure-off-the-graph argument, and 反/復 is itself an open checksum item.
- *"生於 as co-generation (not linear causation)"* rated **strong**, and *"Consistent with Chapter
  2's 相生."* The 相生 rewrite (R5/R6) is **held by ruling**, co-perception set aside; the chain's
  own Ch. 40 entry is flagged pending. The site states as settled what canon holds open.
- The Guodian line as quoted — 天下之勿生於又，**生於亡** — drops the second 又/有 that the
  received text repeats. This is precisely the Ch. 40 variant the chain scores, and the file
  presents both texts side by side **without noting that they differ in the load-bearing place.**

## What I would read next, and why

Not read this pass: the 20 `dao_ch` files (a whole lineage, unreconciled with the site set), the
four ttc analyses (ch. 28 and 36 are sole copies), and the ~33 lexicon-export chapters. The
question worth answering there is whether the dao_ch lineage contains readings the later sets
dropped **without refuting** — the silent-replacement pattern the divergence ledger tracks at
Entries 003 and 004, which has now happened twice in the chains. A translation corpus with five
lineages and no reconciliation record is exactly where it would happen a third time unnoticed.

## Standing

Nothing edited. Finding 1 needs a ruling (the replacement wording) and spans two branches.
Finding 2's items are each small, but three of them — ch. 1's 常, ch. 2's verbs and 前後, ch. 40's
溺 — are places where the site is *more confident than canon*, which is the direction that
matters.
