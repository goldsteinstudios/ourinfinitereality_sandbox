#!/usr/bin/env python3
"""Faithful PDF->markdown for the v9.3 chains.
Emphasis recovered from the PDF's own fonts: heading = larger size, italic = italic flag.
No bold invented (source has none). Paragraphs rebuilt from line y-gaps; indented
blocks become list items; paragraphs split across page breaks are stitched conservatively.
"""
import sys, fitz, re

ITALIC = 2
BODY_MARGIN = 68.0
HYPHEN_JOIN = re.compile(r"(?<=[^\s—–])-$")  # word-final ASCII hyphen (soft-wrap compound); allows CJK before

def join_lines(a, b):
    """Join a continuation line b onto a. A line ending in a word-final ASCII hyphen is a
    soft-wrapped compound (Latin or CJK before it): keep the hyphen, drop the space. Else a space."""
    if HYPHEN_JOIN.search(a):
        return a + b.lstrip()
    return a + " " + b
INDENT_MIN = 80.0          # x0 above this => list/indented item
SAME_PARA_GAP = 8.0        # vertical gap below this => same paragraph
HEAD_H1 = 18.0
HEAD_H2 = 14.0

def is_italic(s):
    return bool(s["flags"] & ITALIC) or "Italic" in s["font"] or "Oblique" in s["font"]

def line_md(line):
    """Line text with contiguous italic runs wrapped in *...* (marks kept inside word boundaries)."""
    runs, cur, buf = [], None, ""
    for s in line["spans"]:
        it = is_italic(s)
        if it != cur:
            if buf:
                runs.append((cur, buf))
            buf, cur = "", it
        buf += s["text"]
    if buf:
        runs.append((cur, buf))
    out = []
    for it, txt in runs:
        if it and txt.strip():
            lead = txt[:len(txt) - len(txt.lstrip())]
            trail = txt[len(txt.rstrip()):]
            out.append(f"{lead}*{txt.strip()}*{trail}")
        else:
            out.append(txt)
    return "".join(out)

def collect_lines(doc):
    """Yield (page_index, y0, y1, x0, size, md_text) for every non-empty line, in reading order."""
    for pno, page in enumerate(doc):
        d = page.get_text("dict")
        lines = []
        for b in d["blocks"]:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                if not any(s["text"].strip() for s in l["spans"]):
                    continue
                x0, y0, x1, y1 = l["bbox"]
                sz = max(s["size"] for s in l["spans"])
                lines.append((y0, y1, x0, sz, line_md(l)))
        lines.sort(key=lambda t: (round(t[0]), round(t[2])))
        for y0, y1, x0, sz, txt in lines:
            yield pno, y0, y1, x0, sz, txt

def build_paragraphs(doc):
    paras = []  # (kind, text)  kind in {h1,h2,p,li}
    cur = None  # dict with text, x0, kind, page, ended_y
    prev_page = None
    prev_bottom = None

    def flush():
        nonlocal cur
        if cur is not None:
            cur["text"] = re.sub(r"\s+", " ", cur["text"]).strip()
            paras.append((cur["kind"], cur["text"]))
            cur = None

    for pno, y0, y1, x0, sz, txt in collect_lines(doc):
        if sz >= HEAD_H2:
            level = "h1" if sz >= HEAD_H1 else "h2"
            txt = re.sub(r"\s+", " ", txt).strip()
            # merge a wrapped heading (consecutive same-level heading lines) into one
            if paras and paras[-1][0] == level and cur is None:
                paras[-1] = (level, join_lines(paras[-1][1], txt))
            else:
                flush()
                paras.append((level, txt))
            prev_page, prev_bottom = pno, y1
            continue
        # a paragraph is NEW only on a page change or a real paragraph gap; kind is set
        # once at the start, so hanging-indent continuation lines inherit it.
        new_para = cur is None or pno != prev_page or (y0 - prev_bottom) >= SAME_PARA_GAP
        if new_para:
            flush()
            cur = {"text": txt, "x0": x0, "kind": "li" if x0 > INDENT_MIN else "p"}
        else:
            cur["text"] = join_lines(cur["text"], txt)
        prev_page, prev_bottom = pno, y1
    flush()
    return paras

SENT_END = re.compile(r"[.!?”’)\]]\s*$")  # a trailing ':' (esp. '::') is a lead-in, not a sentence end

def stitch_pages(paras):
    """Conservatively merge a paragraph that was split across a page break:
    prev is body text not ending in sentence punctuation, next body starts lowercase/dash."""
    out = []
    for kind, text in paras:
        if out and kind in ("p", "li") and out[-1][0] in ("p", "li"):
            ptext = out[-1][1]
            if not SENT_END.search(ptext) and (text[:1].islower() or text[:1] in "—–-‘“(" ):
                out[-1] = (out[-1][0], join_lines(ptext, text))
                continue
        out.append((kind, text))
    return out

def render(paras):
    lines = []
    for kind, text in paras:
        text = re.sub(r"\*(\s+)\*", r"\1", text)  # merge adjacent italic runs across joined lines
        if kind == "h1":
            lines.append(f"# {text}\n")
        elif kind == "h2":
            lines.append(f"## {text}\n")
        elif kind == "li":
            lines.append(f"- {text}\n")
        else:
            lines.append(f"{text}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    doc = fitz.open(sys.argv[1])
    paras = stitch_pages(build_paragraphs(doc))
    sys.stdout.write(render(paras))
