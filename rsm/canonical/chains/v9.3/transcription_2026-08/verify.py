#!/usr/bin/env python3
"""Fidelity check: the markdown must contain exactly the PDF's words, in order.
Compare token streams of (raw PDF text) vs (markdown with markup stripped).
Both are normalized for soft-wrap hyphenation. Any diff is a transcription defect."""
import sys, fitz, re

def norm_tokens(text):
    # join soft-wrapped compounds: 'word-\n next' -> 'word-next'
    text = re.sub(r"(?<=\S)-\s+", "-", text)
    toks = text.split()
    return toks

def raw_tokens(pdf):
    doc = fitz.open(pdf)
    t = "".join(p.get_text("text") for p in doc)
    doc.close()
    return norm_tokens(t)

def md_tokens(md):
    s = open(md).read()
    s = re.sub(r"^#{1,6}\s+", "", s, flags=re.M)   # headings
    s = re.sub(r"^\s*[-*]\s+", "", s, flags=re.M)   # list bullets
    s = s.replace("|", " ")                          # table pipes
    s = re.sub(r"^\s*:?-+:?\s*$", "", s, flags=re.M) # table divider rows
    s = s.replace("*", "")                            # italic markers
    return norm_tokens(s)

def diff(a, b, label):
    import difflib
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
    ratio = sm.ratio()
    print(f"\n=== {label}: raw={len(a)} md={len(b)} tokens  similarity={ratio:.5f}  diffs={len(ops)} ===")
    shown = 0
    for tag, i1, i2, j1, j2 in ops:
        ra = " ".join(a[i1:i2])
        rb = " ".join(b[j1:j2])
        print(f"  [{tag}] raw@{i1}:{i2} {ra!r}  ->  md@{j1}:{j2} {rb!r}")
        shown += 1
        if shown >= 40:
            print("  ...(more)"); break
    return len(ops)

if __name__ == "__main__":
    pairs = [
        ("rsm/canonical/chains/v9.3/structural v9_3.pdf", sys.argv[1] + "/structural_v9_3.md"),
        ("rsm/canonical/chains/v9.3/just math v9_3.pdf",  sys.argv[1] + "/just_math_v9_3.md"),
        ("rsm/canonical/chains/v9.3/just physics v9_3.pdf", sys.argv[1] + "/just_physics_v9_3.md"),
        ("rsm/canonical/chains/v9.3/just ddj v9_3.pdf",   sys.argv[1] + "/just_ddj_v9_3.md"),
    ]
    total = 0
    for pdf, md in pairs:
        total += diff(raw_tokens(pdf), md_tokens(md), md.split("/")[-1])
    print(f"\nTOTAL non-equal blocks: {total}")
