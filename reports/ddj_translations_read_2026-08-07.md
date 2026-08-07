# The DDJ chapter retranslations — first read

**Read:** the ten site-facing translations at `src/content/translations/chapter-{01,02,08,11,22,25,40,42,64,76}.md`, in full. All ten are stamped **December 2025**, all self-declare `confidence: strong`, all but one are `version 1.0` (ch. 1 is 1.2, ch. 11 is 2.0). Current canon is **v9.52, August 2026** — eight months downstream. **Nothing edited. Nothing ruled.**

**Not yet read, inventoried:** three further generations. `archive/ddj/translations/dao_ch1–16_translation.md` (16 files) · `archive/rsm-versions/v0.96/0{20–32}-chapter-XX-111725.md` (13 files, NotebookLM export, 2025-11-17) · `translations/chapters/chapterNN_*.md` on `claude/glyph-composer-v3-fQABj` (**45 files, 2025-11-26 → 2025-12-08 — the largest and newest set**, including variants: `chapter11_direct`, `chapter11_wheel_reread`, `chapter11_scythe_corrected`, `chapter22_pi_operation`, `chapter25_sphere_proof`, and four `_clean_2025-12-08` files). The site set is a ten-chapter selection from that layer.

---

## 1. What is contradicted by ruling — not merely stale

**Ch. 40 — 弱 glossed "yielding, soft," `confidence: strong`.** The DDJ chain reads this slot as **溺, attested-uninterpreted**: *"The graph is 溺, not 弱 (the inventory's 弱 was the received normalization). The interpretive ladder is mandatory and unfilled … A37 is the highest-projection-risk location in the corpus. No `::` is assigned."* The chapter file assigns a reading at strong confidence where canon forbids assigning one at all — and its own Guodian table at the foot of the page prints 溺 without reconciling it. **Sharpest item in the set.** Register B10, errand C8.

**Ch. 1 and Ch. 2 — 玄 as "the generative crossing."** Corrected by ruling 2026-07-29 to *the paradoxical center*, because 玄 is paradox and 牝 is generative; folding "generative" into 玄 makes 玄牝 read generative-generative and dissolves the P₀ assignment. Both files still carry it. See §4 — this is worse than two files.

**Ch. 1 — "met, and never constitutable as a frame of its own."** "Met at resolution" was **struck by ruling** at v9.3, replaced by the resolution-limit typing. The word survives here.

**Ch. 25 — 王 as "the conscious agent."** The DDJ chain: *"域中有四大: the fourth term 王 not yet derived."* The physics chain: *"**No entry: consciousness.** Nothing in the skeleton selects experience."* This gloss imports the single thing the framework explicitly excludes, into an undderived slot, twice on the page.

**Ch. 11 — 利 as "the harvest-capacity (the π-operation)."** Per-constant assignment. Physics, *not carried over*: *"per-domain assignments of i, π and e, which are substitution rather than correspondence."* Retired class.

**Ch. 8 — 利 as "cuts-paths-through, arc-operation (禾+刂 = scythe)."** The scythe reading sits in the **craft cluster set aside whole 2026-08-03 (D3)**, and Will's own recorded worry is against it: *"I'm a little worried that I've over-focused on the scythe given that Chu era people used sickles not scythes."* Chapter 8's central gloss rests on it.

## 2. Superseded, not contradicted

- **常 as the register marker** (ch. 1, 2, 40, and the key-term tables). A1 moved this to **恆** on 2026-08-06. The chapter files predate it. Ch. 1's confidence note already anticipates the move — *"Consistent with Guodian 恆 variant"* — so this is a propagation lag, not a disagreement.
- **Ch. 42 — 三 as "closure."** Canon: *"三 :: the pair plus its bond — the text's own gloss in the next line, 沖氣以為和."* And physics §1 explicitly refuses a third component read out of 二生三. "Closure" reads as a third thing rather than as the bond.
- **Ch. 2 — the six pairs with received verbs 生/成/形/傾/和/隨.** The v9.5 attestation finding: the strips state them as **six 也-stamped definitions with six distinct verbs 生城型浧和墮**, and 相生 is the first clause's verb only. Also R21: the strips read **先**, not 前.
- **Ch. 25 — 逝 translated unflagged.** Errand C1 lists *"the ch. 25 逝-slot graph — the received 逝 is an editor's supply."*
- **Ch. 1 — internal contradiction, one file.** The translation line renders 同謂之玄 as *"the paradoxical origin"*; the key-terms table three inches later says 玄 is *"not the origin; the origin is the unmet one."* `CLAUDE.md` already records this file as contradicting itself; it still does.

## 3. What is in these files and *not* in the chains — recovery candidates

This is the part worth acting on. The translations are not just behind canon; they carry apparatus canon lost.

**The 妙/徼 operationalization.** Ch. 1 states the two observation stances as a *procedure*: **妙 = fix the center, vary the boundary; 徼 = fix the boundary, vary the center**, with the note *"neither stance produces knowledge derivable from the other. They are geometrically orthogonal."* The DDJ chain has 妙 :: relational pattern and 徼 :: boundary and calls the methodology lines *"the parallax method stated inside the text"* — but it does **not** carry the fix/vary formulation. This is the parallax method made procedural, and the parallax methodology document is the strand that stopped at v8.1 and never came forward. **Strongest single recovery in the set.**

**A working per-claim confidence apparatus.** Every file carries `confidenceNotes` — per *element*, with a level and a reason. Ch. 1 has five entries; two are `plausible` and honestly hedged, including a correct statement that 名's obtainedness is held open and the live candidate is the 明/名 split. This is precisely the epistemic tagging v9.3 deleted and that `CLAUDE.md` mourns as *"the only tag recording who owed what."* It is alive, granular, and per-claim here — better than what the chains had before the purge.

**A per-chapter change log.** `version`, `lastUpdated`, and a `changes` array with dated notes. Ch. 1 records three revisions and what each did.

**Four chapters the DDJ chain does not touch at all** — 8, 22, 64, 76. Ch. 64 is Bundle A's curriculum unit and the chain discusses the *anthology*, not the chapter.

**Pedagogy the chains have no room for.** Ch. 40's breath demonstration for co-generation; ch. 2's explicit "what this is NOT saying" block, which pre-empts the relativism misread.

## 4. A guard that is not guarding — CONFIRMED

`CLAUDE.md` states, of the corrected 玄 gloss: *"Site copy that glossed `Pₙ` as 'the generative crossing' was corrected 2026-07-29 to **the paradoxical center**, and `site_vocab_lint.py` now enforces it."*

**It does not enforce it.** Verified three ways:

1. `grep -rn "generative crossing" src/` → **12 occurrences across 8 files**, including `src/pages/index.astro` (the homepage) and `src/pages/docs/rsm/rosetta-stone.astro` (the page that teaches the discipline), plus `chapter-01.md`, `chapter-02.md`, three `objects/*.mdx`, and an essay.
2. `python3 rsm/audit/site_vocab_lint.py` → **"clean — no struck vocabulary in src/"**.
3. `BANS` in the script contains seven patterns — occupancy ×2, "plucked out", "Guodian validation", "sealed", "standpoint/stand on", and the convergence-as-evidence regex. **There is no pattern for "generative crossing."** The rule was described in `CLAUDE.md` and never written into the script.

`CLAUDE.md` separately warns *"do not mistake a clean run for clean text: it ran clean on `src/` while the site glossed 玄 as 'the generative crossing' in eight places."* That warning is still accurate, and the count has grown from eight to twelve. Reported, not fixed — adding a ban is a change to a guard, which is a claim, and the policy's filing lane does not rule.

## 5. Reading

The set is good work and it is eight months stale in specific, listable ways. Nothing in §1 or §2 requires re-translation; each is a gloss or a confidence level to adjust against a ruling that already exists. The apparatus in §3 is the opposite problem — it should be flowing *upstream* into the chains, not waiting for the chains to reach it.

The order that seems to follow: fix §1 first, because those are strong-confidence claims against standing rulings and two of them (溺, 王-as-conscious-agent) are the kind a hostile reader would lead with. Then decide §3's recoveries, because the 妙/徼 operationalization has been sitting unused since December in a file the chains do not read.

Then, and separately: the 45-file set on `claude/glyph-composer-v3-fQABj` has not been read and is newer than the site's ten. Its `_clean_2025-12-08` variants suggest a later editorial pass that never reached `src/`.

---

*Not sealed. §1–§2 are read against v9.52 and the register; §4 is verified by the three checks named.*
