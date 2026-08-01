# v9.3 — markdown transcription (August 2026)

Machine transcription of the five v9.3 PDFs into markdown. **Not sealed.** The PDFs in the
parent directory (`rsm/canonical/chains/v9.3/`) remain the source of record; this folder is a
transcription pass, awaiting a fidelity sign-off before any promotion to canonical markdown.

## Why this exists

v9.3 shipped **PDF-only**. `CLAUDE.md` records the practical cost: `site_vocab_lint.py --chains`
cannot read it (globs `.md`, falls back to v9.2), `git diff`/grep against v9.3 do not work, and
quoting requires `pdftotext -layout`. This pass restores the version-controlled `.md` form so the
ordinary diff/grep/lint workflows can point at current canon again.

## What is here

| File | Source PDF |
|------|-----------|
| `structural_v9_3.md` | `structural v9_3.pdf` |
| `just_math_v9_3.md` | `just math v9_3.pdf` |
| `just_physics_v9_3.md` | `just physics v9_3.pdf` |
| `just_ddj_v9_3.md` | `just ddj v9_3.pdf` |
| `v9_3_change_log.md` | `v9_3 change log.pdf` |
| `convert.py` | the extractor (below) |
| `verify.py` | the fidelity checker (below) |

## Method

Extraction is via **PyMuPDF** span data, not OCR — the PDFs carry real text (SF UI + PingFang for
CJK), so every character, subscript (`ₙ`, `₍ₙ₊₁₎`), CJK glyph, and math symbol comes across exactly.

Formatting is recovered **from the PDF's own fonts**, nothing invented:

- **Headings** by font size — 19.2 pt → `#`, 16.0 pt → `##`. (A wrapped two-line heading is rejoined.)
- **Italic** by the italic font flag → `*…*`. **The v9.3 source contains no bold** (only Regular and
  RegularItalic), so none is added — v9.3 deliberately carries emphasis through italics and heading
  size rather than the heavier bolding used in v9.2.
- **Paragraphs** rebuilt from line y-gaps (≈4 pt within a paragraph, ≈14 pt between); indented items
  become list bullets; hanging-indent continuation lines inherit their paragraph.
- **Soft-wrap hyphenation** normalized (`load-`/`bearing` → `load-bearing`, Latin and CJK).

### Manual reconstructions (the only hand-edited content)

Two-column **tables** cannot be read by linear extraction — the columns interleave. Both were rebuilt
by hand from the PDFs' exact span x/y coordinates:

1. **`just_physics_v9_3.md` §1** — the "three answers" Circulation / Physical régime table.
2. **`v9_3_change_log.md` §A** — the Ruling / Where table (15 rows, several with multi-line cells).

Everything else is the extractor's verbatim output.

## Verification

- **`convert.py`** regenerates the four prose chains from the PDFs.
- **`verify.py`** does a strict in-order token diff of markdown vs. raw PDF text. Result: the four
  chains are **token-for-token identical** to their PDFs (similarity 1.00000, 0 diffs).
- A **word-multiset** check across all five documents (including the two hand-built tables) confirms
  every PDF word is present and none was added.

Re-run from the repo root:

```
pip3 install pymupdf
python3 rsm/canonical/chains/v9.3/transcription_2026-08/convert.py "rsm/canonical/chains/v9.3/structural v9_3.pdf"
python3 rsm/canonical/chains/v9.3/transcription_2026-08/verify.py rsm/canonical/chains/v9.3/transcription_2026-08
```

## Not done in this pass

- No change to `CLAUDE.md`, `site_vocab_lint.py` (`CURRENT_CHAINS`), or the site `src/` — repointing
  the tooling at v9.3 is separate follow-up work.
- No ontology, referent, or reading was touched. This is a format conversion only; the PDFs govern.
