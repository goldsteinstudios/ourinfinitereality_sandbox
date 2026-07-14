#!/usr/bin/env python3
"""
Vocabulary lint for the public site (src/).

Run:  python3 rsm/audit/site_vocab_lint.py

Scope note, deliberately narrow: this file checks WORDS, not geometry. It cannot tell
you whether a claim is true; it tells you whether the copy uses vocabulary the framework
has struck. checks.py is the arithmetic; this is the lexicon. Neither is a ruling.

Only bans with a traceable authority go in here. Each pattern cites where it comes from.
Adding a ban because it "sounds unrigorous" is exactly the drift this file exists to
catch, so: no unsourced entries.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"

# (regex, why it's banned, where the ban comes from)
BANS = [
    (
        r"\b(unoccupiable|unoccupied|occupiable)\b",
        "occupancy vocabulary: the skeleton is implicit-register — no motion, duration, "
        "or occupancy. The two centers are typed met vs unmet.",
        "structural_v7.7_r3.md:3; CLAUDE.md:64-78",
    ),
    (
        r"\b(can(?:no|')t be occupied|cannot be occupied|can(?:no|')t occupy|cannot occupy)\b",
        "occupancy vocabulary (the seating error, in its most common phrasing).",
        "CLAUDE.md:64-78",
    ),
    (
        r"\bplucked out\b",
        "picturesque falsehood: the exclusion is constitutive, not historical. "
        "Nothing was ever removed.",
        "math_chain_walkthrough_ledger_r1.md:239 (GUARD)",
    ),
    (
        r"\bGuodian [Vv]alidation\b",
        "the DDJ is the subject of translation, not a witness. The strips ATTEST; "
        "they do not validate the framework.",
        "just_ddj_v7.7_r3.md:5",
    ),
    (
        r"\bsealed\b",
        "v7.7 is not sealed; L1 is the open head of the audit.",
        "CLAUDE.md:121-122",
    ),
    (
        # Includes the regress sense ("no foundation to stand on"): P1 is about terminal
        # resolution, not about somewhere to put your feet. Canon states it as
        # "infinitely vast and infinitely divisible: no maximum extent, no minimum scale,
        # no terminal resolution in either direction."
        r"\bstandpoint\b|\b(?:stand|stood|standing)\s+on\b",
        "occupancy vocabulary wearing a coat. Canon's phrasing is 'cannot be constituted "
        "as a frame' / 'cannot become a frame of its own'. Nothing in this framework "
        "stands anywhere — not on a crossing, and not on a foundation.",
        "Will's rulings, site walkthrough 2026-07-14; structural_v7.7_r3.md:13, :90",
    ),
    (
        # The error that keeps coming back: pricing convergence as evidence. The registers
        # were built through each other, so their agreement is EXPECTED. A chain offers
        # coherence, never evidence; evidence lives only in preregistered predictions.
        r"converg\w*[^.]{0,80}\bevidence\b|\bevidence\b[^.]{0,80}converg\w*",
        "convergence-as-evidence. Divergences are the data; convergences are priced near "
        "zero (shared corpora / shared authorship). A chain offers coherence, not evidence.",
        "CLAUDE.md:134-136; just_ddj_v7.7_r3.md:5",
    ),
]

# A hit is a false positive when the line NEGATES or REPORTS the banned term rather than
# asserting it. "Not sealed" is the required claim, not a violation of it; and the
# framework's own history ("an earlier version called itself sealed") must be sayable.
EXONERATE = [
    r"(?:not|never|nothing|n't|isn't)\b[^.]{0,60}\bsealed\b",  # "not sealed", "nothing here is sealed"
    r"called itself sealed",                                    # reporting v7.5's error
    r"sealed since 168 BCE",                                    # the Mawangdui tomb, not the framework
]

EXTS = {".astro", ".md", ".mdx", ".ts", ".tsx", ".js", ".css"}


def main() -> int:
    if not SRC.is_dir():
        print(f"site_vocab_lint: no src/ at {SRC}", file=sys.stderr)
        return 2

    hits = []
    for path in sorted(SRC.rglob("*")):
        if path.suffix not in EXTS or not path.is_file():
            continue
        # Astro excludes underscore-prefixed content files; so do we.
        if path.name.startswith("_"):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(re.search(e, line, flags=re.IGNORECASE) for e in EXONERATE):
                continue
            for pattern, why, source in BANS:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    hits.append((path.relative_to(REPO), lineno, line.strip(), why, source))

    if not hits:
        print("site_vocab_lint: clean — no struck vocabulary in src/")
        return 0

    print(f"site_vocab_lint: {len(hits)} hit(s)\n")
    for rel, lineno, text, why, source in hits:
        print(f"{rel}:{lineno}")
        print(f"    {text[:110]}")
        print(f"    -> {why}")
        print(f"    -> authority: {source}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
