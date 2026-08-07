# Chain finalization audit — v9.52

**Read against:** `rsm/canonical/chains/v9.5/` (four chains), `reports/open_items.md`,
`reports/heng_chang_distribution_survey.md`, `rsm/audit/checks.py` (run: all checks pass, exit 0).
**Question asked:** what stands between each chain and being finalizable *as a separate logic chain*.

**Nothing here is a ruling.** No open item is closed, no candidate promoted, no reading proposed.
Findings are sorted by whether the register already carries them. Items are cited by name.
Arithmetic went to the scripts; everything ontological is left standing for Will.

---

## Part 1 — Findings the register does not carry

These are the audit's actual output. Each was verified against the chain text or a primary artifact;
the verification is named with the finding.

### 1.1 The math chain's Revolution theorem is out of step with the other two — CONFIRMED

R3 (2026-08-02) demoted revolution from forced to admitted, and the relation between the two
mode-dominant regions was re-seated on **descent**. Two chains carry the demotion; one does not.

| Chain | What carries the relation |
|---|---|
| `structural_v9_5.md` §6 | "the relation is carried by **descent** (§7) … What the structure **additionally admits** is revolution" |
| `just_physics_v9_5.md` §1 | "the relation between them is carried by **descent**. What the structure **admits besides** is revolution" |
| `just_math_v9_5.md`, Theorems | "**Revolution**. The relation between the two portions **is carried by revolution** of Gₙ about Bₙ." |

The math chain asserts as a theorem what the spine assigns elsewhere and offers revolution as an
additional admission. This is the exact modal distinction R3 was about, surviving in the one chain
whose entry is named "Revolution." Verified by grep across all three files; wording quoted verbatim.

This is a propagation gap, not a new dispute — but it is a propagation gap in a *theorem statement*,
which is where the corpus's own history says silent replacements hide.

### 1.2 The DDJ chain's 恆/常 line contradicts its own survey — CONFIRMED · **RESOLVED 2026-08-06**

> **Closed by the parallel session** (iPad/iPhone), commit `d1dcddd`, recorded at
> `reports/code_tasks_filing_2026-08-06.md` A1–A2. The offending sentence was **deleted**, not
> softened, along with the whole checksum item. The replacement is correct on all three strata:
> **恆** as the register marker, [M]-attested; the received **常** as the post-taboo form under
> Emperor Wen's 避諱; the Guodian stratum attesting **亙**. Provenance for the ruling rests on the
> taboo mechanism, the Bundle A distribution survey (亙 ×4, readable 常 ×0, 恆 ×0), and R18.
> The chain's open checksum list is now five items. **This finding is closed; the text below is
> the original report, retained as the record.**


`just_ddj_v9_5.md`, open checksum items: "**the strips attest both graphs, used differently**; the
received text merged a distinction the Chu scribes maintained."

`reports/heng_chang_distribution_survey.md`, Finding 2: "**Bundle A, per this dataset, has zero
readable 常.**" The one candidate slot (ch. 55) is slip 34's unresolved ○; the second received-常
slot reads 和. Finding 1: the family appears as one graph, 亙, four times.

Register B2 states the footing correctly ("Independent 常 is unconfirmed") and reports the conflict
under its standing rule that the chains govern. So the register deferred to the chain — while the
evidence sits on the register's side. The chain currently makes a manuscript claim its own survey
does not support, and it is the strongest-sounding sentence in the checksum list.

This is philological, checkable, and blocks DDJ finalization independently of any ruling. It closes
either by softening the chain sentence to the survey's footing, or by slip 34's ○ resolving to 常
(errand C1, which the survey names "the highest-value single graph in the survey").

### 1.3 The Corollary — formerly L1 — has no register entry — CONFIRMED

`grep -i "corollary\|L1\|unframed" reports/open_items.md` returns nothing.

v7.7's L1 ("no unframed distinction") was, in that version's own words, the single head of the audit,
carrying four loads. At v9 it became the Corollary of the frame Definition. It is load-bearing in
current canon — structural §4's floor argument runs through it ("any distinction beneath it is, by
the Corollary, another frame"), and the math chain's unit/floor section repeats the move — and it
appears in no open-items list, in no chain's open items, and in no register section.

`CLAUDE.md` flags the pattern ("Definitions are where audits don't look"). The register, which is the
artifact that is supposed to hold the flag, does not have an entry for it. Whether the Corollary is
sound is not this audit's business; that it has no line in the ledger is.

### 1.4 The independence property the set claims is not the property the set has — CONFIRMED

`CLAUDE.md`: "no rendering cites another rendering's theorems — that is what makes their independence
real." Measured against v9.5:

**Physics → math.** Math-chain rendering objects appearing in the physics chain, none of which occur
in the spine: `Q_i` (1), `Q_j` (3), `slice` (3), `null cone` (2), split coordinates, the split action
`e^{jφ}`, the Amplitude Floor, the complementarity floor, the minimal traversal, the two returns.
Sorting the physics entries by what survives deletion of every math-chain object:

- **Structurally independent:** §1 circulation sorting, §2 time, §7 excluded cores, §8 frames/RG
  lineage, §9 irreversibility, §10 the Bekenstein sort (a negative result), §6's complementarity
  headline and superposition-as-unselected-circulation.
- **Downstream of the math chain's chart:** §3 `1ₙ :: ℏ/2`, §3 the slice invariant `:: c`,
  §4 `E = mc²`, §5 Wick, §6 the two returns `::` the spinor double cover, §11's arithmetic.

The second list is where the chain's most striking physics sits. The chain is honest about the typing
in three places ("the correspondence runs between a physical result and a result about the
framework's chart"; "this relates a physical structure to a chart feature"; "the correspondence runs
between two things of the same type") — but it flags them as *typing* concerns, never as independence
concerns, and the set-level independence claim is stated nowhere that the qualification reaches.

**Math → DDJ.** `just_math_v9_5.md` line 51, closing the Archimedean demonstration: "Indexed
statements of one invariant: **可名 of a single 常名**." A rendering closing its cleanest exhibition
in another rendering's vocabulary.

**Physics → DDJ.** `just_physics_v9_5.md` line 23: the corpus's Z-axis reading is refused because
"**三** is the pair with its bond, not a third axis" — and the sentence that follows makes it govern
the whole chain ("every entry below is written on that reading"). The structural fact (one
distinction, two modes) is sufficient on its own; as written, the DDJ gloss is carrying the refusal.

**DDJ → math.** The slice identity in 此兩者同出而異名, and the explicit two-returns cross-reference
in the 反/復 checksum.

None of this is fatal and none of it is dishonest. It does mean the sentence in `CLAUDE.md` is
currently false of the set, and that a reader told the renderings are independent will find, on
inspection, one chain that largely is (given the spine), one that is about half, and one whose
flagship entries are not.

### 1.5 The evidential architecture stated in CLAUDE.md is not the one the chains run — **RESOLVED 2026-08-06**

> **Closed by the parallel session** (iPad/iPhone), in the same commit range. `CLAUDE.md`'s
> `::` doctrine no longer says *"The convergence of independent imperfect pointings is the
> evidence."* It now reads: *"…marks one pattern pointed at from several registers — a shared
> referent, not evidence for a claim; the framework runs from a conditional and accumulates no
> confirmation."* That is the architecture the chains actually run, stated at the top of the
> orienting document. **Closed; the text below is the original report, retained as the record.**


`CLAUDE.md`: "The convergence of independent imperfect pointings is the evidence."

But: the physics chain's headnote disclaims it outright — "no quantity here is owed by the framework
and none confirms it" — and its posture is predictions-only. The DDJ chain is typed as generatively
upstream, so its agreement "carries no public evidential weight," leaving resistance as its one
channel. The math chain is a realization, not a witness.

So no chain in v9.5 claims evidential weight from convergence, and two disclaim it explicitly. The
convergence sentence describes an earlier architecture. Whatever is right here, the book and the site
cannot inherit both framings, and the choice is upstream of nearly every framing decision in either.

### 1.6 Physics runs on one live prediction of four

Its evidential channel is predictions. Prediction 1 (unitarity vs. objective collapse) is a genuine
kill-condition and stands. Prediction 2 is "currently unseparated from standard predictions; the
separation is owed before this counts." Predictions 3 and 4 are marked unbuilt. A predictions-only
chain with one prediction is finalizable only if that is what it says it is.

### 1.7 Smaller items, all editorial

- **Structural §4 states the law flat.** "X·Y = 1ₙ" arrives with the class-selection argument, which
  excludes additive laws — not with the uniqueness-up-to-reparametrization step or the anchoring that
  selects the product form specifically. Both live in the math chain, which flags the anchoring in
  place ("The chart is anchored by the very thing it excludes. The native-magnitudes step is
  unsettled"). The spine lists it in open item 1 and satisfies its own discipline that way; a reader
  of §4 alone meets a derivation with no flag on the load-bearing step.
- **A third thing written "1".** `CLAUDE.md` already warns that `Q_j` and `Q_i` are both written `1ₙ`.
  The math chain's notation adds `|1|`, P₀'s full face, sitting "at the unbounded end" — a numeral
  notation for a face, beside `1ₙ`, a frame's finite unit. The guard sentence exists ("numeral
  notations name faces, never values"); the collision is a live reader hazard for any public-facing
  document, and the |1| cascade was withdrawn as unattributed at v9.5.
- **The presentation set differs between spine and math** — two faces in structural §1, three in the
  math notation (the sign-collapse added). This is probably register-correct, since sign is explicit,
  but nothing says so, and it reads as a discrepancy. One clause fixes it.
- **The units clause in physics §3** — "the conserved product of conjugate spreads carries the
  dimensions of action" — sits against the same chain's headnote, "no quantity here is owed … and
  none confirms it." Whether a dimensional match counts as a quantity for that purpose is a question
  the chain does not answer, and register item A17's `c` entry already records a cost that weakens
  this exact clause (the inequality-shape finding surviving separately).
- **The register has no path in CLAUDE.md.** Every chain closes by pointing at "the open-items
  register"; `reports/open_items.md` appears in no Reference Locations entry. Only the diff-report
  trail is indexed.

---

## Part 2 — What the register already carries, ranked by finalization leverage

Sorted by how many downstream results move if the item closes. Nothing here is new; the ranking is.

**1. Definition T (A8, math open item 5) — the one shared gate, and unattempted.** The register's own
dependency line: "T2, the two returns, the minimal traversal, the complementarity floor — all
rendering results partly because T is chart-bound." The complementarity floor is what physics §3's
`1ₙ :: ℏ/2` stands on; the two returns is what physics §6's spinor entry stands on. So T is the
common gate on the math chain's chart-typed theorems and, through them, on the physics chain's two
flagship correspondences. **Necessary, not sufficient** — the floor also waits on the winding measure
(A11) and quadraticity (A12), and the two returns are a fact about the circle slice, which is
explicit as a complete object regardless. It has not been attempted since it was flagged
(v9.3 change log §C).

**2. Quadraticity of the measure (A12) — the metric gate.** Everything metric is downstream:
the circle and sphere renderings, the equidistance route to dimension, the complementarity floor's
geometry, perpendicularity. Until it is forced, the math chain cannot state "orthogonal" as more than
a rendering fact — the skeleton says *independent*.

**3. The native-magnitudes step (A1) — the law gate.** If the anchoring does not legitimate, the
product form is one representative of an equivalence class selected by convention, and the spine's §4
onward is a rendering rather than the spine. Open since v9, unchanged.

**4. Dimension (A5) — the slot is empty.** "At least three" stands on two routes, both using
equidistance, hence downstream of item 2. "Exactly three" now has **no standing candidate
derivation** — both prior candidates were withdrawn at v9.5, which is a worse position than the
"two rival derivations, unadjudicated" it replaced. Physics inherits it as the (1,1)-vs-(1,3)
signature strain, and the spin-½ orientation-space candidate is gated on it.

**5. The cross-frame cluster — four items, one hole.** A3's residue (shared-gradient commensurability),
A4 (the cross-frame unit relation), A9 (cross-frame expression), A10 (the tree-question). Together
they are the framework's missing account of any relation between frames that is not parent-child.
A4 additionally gates physics §11's stronger reading and the Bekenstein reach (A16). For a book this
is the most *visible* hole, because siblings and cousins are what a reader asks about first.

**6. The DDJ finalization set.** Two literal `<!-- R5/R6 pending -->` comments sit in the canonical
chain text (lines 41 and 49) under D1's hold. 溺 carries no `::` and its interpretive ladder is
unfilled (B10, errand C8). Six open checksums. D1 also records the v9.5 attestation finding that the
strips state the six Ch. 2 pairs as six 也-stamped definitions with six distinct verbs (生城型浧和墮),
where the chain generalizes to "each arising mutually" — parked, not resolved.

**7. Errands, which close with artifacts rather than rulings.** C1 (slip images, batched — carrying
1.2 above), C3 (Mawangdui facsimiles, gating the Ch. 40 dating and the [M] flips), C4 (Bundles B/C
transcriptions), C5 (the seven missing NotebookLM source images — the register calls this the
highest-value absent asset in the corpus, and it is a local-machine recovery, on no branch).

---

## Part 3 — Per-chain summary

**Structural (the spine).** Closest to finalizable, and the only chain whose remaining gaps are all
either listed or definitional. Blockers: the native-magnitudes step under §4's law; the empty
exactly-three slot; the parametric environment (new at v9.5, and sitting inside §0, which heads every
chain); the unregistered Corollary (1.3). The cross-frame cluster is stated as open in place.

**Just-Math.** Four of its nine theorems are stated without chart dependence (Disconnection,
Revolution, Recursion, Indexed comparison); five are chart- or sign-dependent, three saying so
verbatim. That ratio is the chain's honest headline, and it is the thing a reader will not expect
from a document called the derivation. Blockers: the Revolution wording (1.1); Definition T;
quadraticity; the native-magnitudes step.

**Just-Physics.** Splits cleanly into entries that stand on the spine and entries that stand on the
math chain's chart (1.4). Blockers: that split, stated or repaired; one live prediction of four
(1.6); the s-orbital strain, the two arrows, and the Planck floor, each of which the chain already
carries in place as an exposure rather than a gap.

**Just-DDJ.** Not a logic chain in the same sense as the other three, by its own doctrine — a
translation with one evidential channel, resistance, currently cashed twice (the 非 survey; the
Ch. 40 preregistered test, scored positive, dating unconfirmed pending C3). Blockers: the 恆/常
overstatement (1.2); the two pending-comment markers in canonical text; 溺; the checksums.

---

## What this audit did not do

No open item was closed, no candidate promoted, no correspondence proposed, no reading offered.
Findings 1.1–1.3 are verified against text or artifact and are reported as defects rather than as
disputes. Findings 1.4–1.6 are structural observations about the set, and each has a framing
decision inside it that is Will's, not the audit's. `checks.py` passes; nothing in this document
rests on arithmetic it did not verify.

Candidate next artifact, if wanted: divergence-ledger entries for 1.1 and 1.2, which are the two
findings shaped like the ledger's standing protocol.
