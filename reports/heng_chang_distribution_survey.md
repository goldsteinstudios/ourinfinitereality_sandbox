# 亙/恆/常 distribution survey — Guodian Bundle A

Input for the DDJ finalization pass (per R18, `rsm/audit/session_consolidation_2026-08-02.md`).
Run 2026-08-03 against `data/ddj/guodian_interactive.json` (Bundle A, 老子甲: 39 slips, 1,073
character positions, per-position guodian/received graph columns). **Framework-blind: this is a
distribution report, no correspondence is proposed.**

## Scope and provenance caveats, first

- **Bundle A only.** The machine-readable dataset covers 老子甲 alone. Bundles B (乙) and C (丙)
  are not in it; the only B/C material in the repo is the NotebookLM-exported inventories under
  `archive/rsm-versions/v0.971/` (weak provenance). **R18's "the Guodian has both, used
  differently" cannot be confirmed or refuted from Bundle A data alone** — see findings.
- **Dataset-level, not slip-level.** `tools/dedupe_guodian_slips.py` documents that this dataset's
  source CSVs are gitignored and off-disk — the dataset is currently unreproducible from tracked
  inputs. Everything below is corroboration at the level of *this transcription*, not slip-image
  verification. The slip-image errands stand.
- The dataset's "received" column is a normalization column (it shows 亙 at the 亙 positions);
  received-text comparisons below are against the classical received text, supplied by me and
  marked as such.

## Finding 1 — Bundle A attests exactly one graph of the family: 亙, four times

No position in either column carries 恆 (the 忄 form) or 常. The full inventory:

| Slip | Pos | Chapter | Strip context (dataset) | Received text at the slot |
|---|---|---|---|---|
| 6 | 14 | 46 | 智足之爲足此**亙**足矣 | 知足之足，**常**足矣 — received has **常** |
| 13 | 4 | 37 | 道(行人-graph)**亙**亡爲也 | 道**常**無為 — received has **常** |
| 18 | 11 | 32 | 道**亙**亡名 | 道**常**無名 — received has **常** |
| 24 | 3 | 16 | 至虛**亙**也 | 致虛**極** — received has **極**, not 常 |

Three of the four 亙 sit where the received text reads 常. The fourth sits where the received
reads **極** — a second, distinct merger target (see Finding 3).

## Finding 2 — the received text's 常-slots in Bundle A chapters: no clean 常 anywhere

Bundle A contains chapters 2, 5, 9, 15, 16, 19, 25, 30, 32, 37, 40, 44, 46, 55, 56, 57, 63, 64,
66. Within those, the received text's 常 tokens and what the strips show:

| Received line (ch.) | Received graph | Strip shows (slip/pos) |
|---|---|---|
| 知足之足，常足矣 (46) | 常 | **亙** (6/14) |
| 道常無為 (37) | 常 | **亙** (13/4) |
| 道常無名 (32) | 常 | **亙** (18/11) |
| 知和曰**常** (55) | 常 | **○ — unresolved graph** (34, in 和曰○) |
| 知**常**曰明 (55) | 常 | **和** (34, in 智和曰明) — a *lexical variant*, not a graph substitution |

**Bundle A, per this dataset, has zero readable 常.** The one candidate slot (ch. 55, first 常)
is an unresolved ○ in the transcription; the second received-常 slot reads 和 on the strip — the
strip says "knowing 和 is called 明" where the received says "knowing 常 is called 明."

**Consequence for R18:** within Bundle A, this dataset shows one word (亙), not two used
differently. R18's two-words claim therefore rests on one or more of: (a) **Bundles B/C** (no
machine-readable data in the repo); (b) **the ○ at slip 34 resolving to 常** (a slip-image
errand — if it resolves to 常, Bundle A attests both graphs, and in *different* lines, which
would confirm R18 exactly); (c) lines outside this dataset's coverage. Identifying which is the
first task of the finalization pass. The ○ at slip 34 is now **the highest-value single graph in
the survey.**

## Finding 3 — the A24 line: corroborated at dataset level, with one unresolved graph

The dataset's slip 24 opens: **至虛亙也獸𠁩○也** (positions 1–8), where the received ch. 16
reads 致虛**極**，守**靜**篤.

- 至虛**亙**也 — corroborates the essay-9/essay-5 claimed transcription 至虛恆也 (亙 being the
  attested graph the 恆 reconstruction points at), against received 極. **The first substitution
  in the claimed two-substitution drift is dataset-corroborated.**
- 獸𠁩○也 — 獸 (shòu) at the received 守 slot is a routine phonetic loan; **𠁩** is an
  unidentified graph at the received 靜 slot (the claimed reading is 中); **○** is unresolved at
  the received 篤 slot (the claimed reading is 篤). So the second clause is *partially*
  corroborated: the loan is clean, the two load-bearing graphs (𠁩 → 中?, ○ → 篤?) are exactly
  what the slip-image errand must resolve.
- The 也…也 stamps are present in the dataset at both clauses — consistent with the definitional-
  stamp reading, and stripped in the received line.

## Finding 4 — incidental but relevant: the 亡/無 pairing rides along

At two of the four 亙 lines the dataset also shows 亡 where the received has 無 (亙亡爲/道常無為;
亙亡名/道常無名) — the 亡→無 drift the DDJ chain already records, co-occurring with the 亙→常
merger in the same lines. Whatever process merged 亙 into 常 was operating on lines that also
carried the absence-word substitution. Noted for the finalization pass; no claim attached.

## What the finalization pass needs that this survey could not supply

1. **Bundle B and C data** — machine-readable transcriptions (the repo has none).
2. **The ○ at slip 34** (ch. 55) — slip image. If 常, R18 confirms within Guodian; if not, the
   two-words claim needs B/C.
3. **The 𠁩 and ○ on slip 24** — slip image; settles the A24 second clause (中? 篤?).
4. The 亙 graph forms themselves — whether the four A-bundle 亙 are one consistent hand/form
   (the dataset stores glyph crops at `public/glyphs/guodian/` for slips 6, 13, 18, 24 — the
   crops exist locally and can be eyeballed without external facsimiles; not done here, as graph
   identification is the philological errand, not the survey's).
