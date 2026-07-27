#!/usr/bin/env python3
"""
Vocabulary lint for the public site (src/) and, with --chains, for the canonical chains.

Run:  python3 rsm/audit/site_vocab_lint.py            # site copy (src/)
      python3 rsm/audit/site_vocab_lint.py --chains   # the current chain set
      python3 rsm/audit/site_vocab_lint.py --chains rsm/canonical/chains/v7.7
      python3 rsm/audit/site_vocab_lint.py --all      # both

Scope note, deliberately narrow: this file checks WORDS, not geometry. It cannot tell
you whether a claim is true; it tells you whether the copy uses vocabulary the framework
has struck. checks.py and cross_model_checks.py are the arithmetic; this is the lexicon.
Neither is a ruling.

Only bans with a traceable authority go in here. Each pattern cites where it comes from.
Adding a ban because it "sounds unrigorous" is exactly the drift this file exists to
catch, so: no unsourced entries.

Why --chains exists (added 2026-07-27): the occupancy ban was written for site copy, but
v9 shipped "occupiable at resolution" in two chains and "the unoccupiable center" in a
third -- the retired Cn/Sn+- vocabulary, the seating error's own word, in the documents
the site is drafted FROM. A lexicon guard that only watches the downstream copy watches
the wrong end. Chain hits are reported, never rewritten: chain text is the author's.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
CHAINS = REPO / "rsm" / "canonical" / "chains"
CURRENT_CHAINS = CHAINS / "v9"          # update when the working set moves

# (regex, why it's banned, where the ban comes from)
BANS = [
    (
        r"\b(unoccupiable|unoccupied|occupiable)\b",
        "occupancy vocabulary: met/unmet are frame-reading statuses only; occupancy "
        "language does not type these loci.",
        "structural_v9.md sec.5; just_math_v9.md Notation; CLAUDE.md 'The two centers'",
    ),
    (
        r"\b(can(?:no|')t be occupied|cannot be occupied|can(?:no|')t occupy|cannot occupy)\b",
        "occupancy vocabulary (the seating error, in its most common phrasing).",
        "CLAUDE.md 'The two centers'",
    ),
    (
        r"\bplucked out\b",
        "picturesque falsehood: the exclusion is constitutive, not historical. "
        "Nothing was ever removed.",
        "math_chain_walkthrough_ledger_r1.md:239 (GUARD); just_physics_v9.md sec.5",
    ),
    (
        r"\bGuodian [Vv]alidation\b",
        "the DDJ is the subject of translation, not a witness -- and generatively "
        "upstream of the framework. The strips ATTEST; they do not validate.",
        "just_ddj_v9.md, Evidential posture",
    ),
    (
        r"\bsealed\b",
        "v9 is not sealed; the unaudited closures are open item 1 in both chains.",
        "structural_v9.md header; just_math_v9.md header",
    ),
    (
        # Includes the regress sense ("no foundation to stand on"): P1 is about terminal
        # resolution, not about somewhere to put your feet.
        r"\bstandpoint\b|\b(?:stand|stood|standing)\s+on\b",
        "occupancy vocabulary wearing a coat. Nothing in this framework stands anywhere "
        "-- not on a crossing, and not on a foundation.",
        "Will's rulings, site walkthrough 2026-07-14; structural_v9.md sec.3, sec.5",
    ),
    (
        # The error that keeps coming back: pricing convergence as evidence. The registers
        # were built through each other, so their agreement is EXPECTED.
        r"converg\w*[^.]{0,80}\bevidence\b|\bevidence\b[^.]{0,80}converg\w*",
        "convergence-as-evidence. Divergences are the data; convergences are priced near "
        "zero (shared corpora / shared authorship). A chain offers coherence, not evidence.",
        "CLAUDE.md 'Working with AI'; just_ddj_v9.md, Evidential posture",
    ),
]

# A hit is a false positive when the line NEGATES the banned term, REPORTS it as history,
# or STATES THE RULE ITSELF. "Not sealed" is the required claim, not a violation of it;
# and a chain saying "occupancy language does not type these loci" is the ban, not a breach.
EXONERATE = [
    r"(?:not|never|nothing|no|n't|isn't)\b[^.]{0,60}\bsealed\b",   # "not sealed"
    r"called itself\s*[\"'“‘]?sealed",                     # reporting v7.5's error
    r"sealed since 168 BCE",                                        # the Mawangdui tomb
    # The rule being stated, in any of its canonical phrasings:
    r"occupancy language\b[^.]{0,60}\b(?:does not|never|is struck|not type)",
    r"\b(?:struck|retired|banned|ill-typed|forbidden)\b[^.]{0,80}\boccupiab",
    r"\boccupiab\w*\b[^.]{0,80}\b(?:struck|retired|is the seating error|ill-typed)",
    r"for calling\b[^.]{0,60}\boccupiable",                         # reporting the Cn/Sn+- retirement
    # Negated "stand on": the framework asserting that there is nothing to stand on.
    r"(?:nothing|not|never|no)\b[^.]{0,40}\bto stand on\b",
]

EXTS = {".astro", ".md", ".mdx", ".ts", ".tsx", ".js", ".css"}


def scan(root: Path, label: str) -> list:
    """Return a list of (relpath, lineno, text, why, authority) for one tree."""
    hits = []
    if not root.is_dir():
        print(f"site_vocab_lint: no {label} at {root}", file=sys.stderr)
        return hits
    for path in sorted(root.rglob("*")):
        if path.suffix not in EXTS or not path.is_file():
            continue
        # Astro excludes underscore-prefixed content files; so do we.
        if path.name.startswith("_"):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(re.search(e, line, flags=re.IGNORECASE) for e in EXONERATE):
                continue
            for pattern, why, source in BANS:
                m = re.search(pattern, line, flags=re.IGNORECASE)
                if m:
                    hits.append((path.relative_to(REPO), lineno,
                                 excerpt_around(line, m), why, source))
    return hits


def excerpt_around(line: str, m: "re.Match", width: int = 130) -> str:
    """Show the matched term in context, not the first N chars of a long paragraph."""
    lo = max(0, m.start() - width // 2)
    hi = min(len(line), m.end() + width // 2)
    return ("…" if lo > 0 else "") + line[lo:hi].strip() + ("…" if hi < len(line) else "")


def report(hits: list, label: str, note: str = "") -> int:
    if not hits:
        print(f"site_vocab_lint: clean — no struck vocabulary in {label}")
        return 0
    print(f"site_vocab_lint: {len(hits)} hit(s) in {label}\n")
    for rel, lineno, text, why, source in hits:
        print(f"{rel}:{lineno}")
        print(f"    {text}")
        print(f"    -> {why}")
        print(f"    -> authority: {source}\n")
    if note:
        print(note)
    return 1


def main(argv) -> int:
    args = [a for a in argv[1:]]
    do_chains = "--chains" in args or "--all" in args
    do_src = "--all" in args or not do_chains

    # optional explicit path after --chains
    chain_root = CURRENT_CHAINS
    if "--chains" in args:
        i = args.index("--chains")
        if i + 1 < len(args) and not args[i + 1].startswith("-"):
            chain_root = Path(args[i + 1])
            if not chain_root.is_absolute():
                chain_root = REPO / chain_root

    rc = 0
    if do_src:
        rc |= report(scan(SRC, "src/"), "src/")
    if do_chains:
        note = ("Chain hits are REPORTED, not rewritten: chain text is the author's.\n"
                "This is lexicon-only and explicitly not a ruling. Log rulings in\n"
                "rsm/audit/ and see v9_comparison_r1.md for the standing items.")
        rc |= report(scan(chain_root, str(chain_root.relative_to(REPO))),
                     str(chain_root.relative_to(REPO)), note)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
