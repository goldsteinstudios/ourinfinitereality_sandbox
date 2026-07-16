"""
Build the Guodian unresolved-graph slots dataset

Joins three independent witnesses to every position where the gxdq.com
transcription prints ○, and emits them for the /guodian-slots working tool.

The witnesses are NOT merged. Each is labelled by source and shown as-is,
including where they disagree. Nothing here decides what a graph is.

  gxdq   data/ddj/gxdq/slots_tool.html   237 slots (A 153 / B 53 / C 31).
         Its ○ means "this editor had no codepoint for the graph" -- NOT
         "the graph is unidentified". Source editor unattributed.
  local  public/data/guodian_interactive.json   Bundle A only. Often names a
         graph that gxdq leaves as ○.
  CHUBS  data/CHUBS_repo/glyphs/<transcription>/   THUNLP/Chujian, Apache-2.0.
         The folder name is the transcription; the flat extraction into
         public/glyphs/guodian/ discarded it. Bundle A only in practice
         (898 glyphs; B has 11, C has 4).

ALIGNMENT. gxdq slot ids are per-slip indices (A1.1 = first slot on slip 1),
not slip positions, so they must be aligned to get a glyph. Alignment walks a
slip's tokens and matches them index-for-index against the local
transcription's entries. It is only trusted when both agree on how many
characters the slip holds; otherwise the slot is emitted unaligned, with no
glyph, rather than guessing. Roughly 29/39 Bundle A slips align.

Do not "improve" this by falling back to a fuzzy match. A slot showing the
wrong glyph is worse than a slot showing none.
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SLOTS_HTML = PROJECT_ROOT / "data" / "ddj" / "gxdq" / "slots_tool.html"
PRIORITY = PROJECT_ROOT / "data" / "ddj" / "gxdq" / "priority.txt"
LOCAL_JSON = PROJECT_ROOT / "public" / "data" / "guodian_interactive.json"
CHUBS_DIR = PROJECT_ROOT / "data" / "CHUBS_repo" / "glyphs"
OUT = PROJECT_ROOT / "public" / "data" / "guodian_slots.json"

# A (reading) or <emendation> annotates the character before it; it is not
# itself a slip position. Nor is editorial punctuation or a lacuna box.
GLOSS = re.compile(r"[（(][^）)]*[）)]|[〈<][^〉>]*[〉>]")
PUNCT = "，。？；：、！?,."
CHUBS_FILE = re.compile(r"郭店簡_01([ABC])-老子[甲乙丙]_(\d+)_01[ABC]-(\d+)-(\d+)\.png")


def positions_in(text: str) -> str:
    """The characters of a plain run that actually occupy slip positions."""
    text = GLOSS.sub("", text)
    return "".join(c for c in text if c not in PUNCT and c != "□")


def load_gxdq() -> dict:
    html = SLOTS_HTML.read_text(encoding="utf-8")
    m = re.search(r"^const DATA = (\{.*\});\s*$", html, re.M)
    if not m:
        raise SystemExit("could not find the DATA blob in slots_tool.html")
    return json.loads(m.group(1))


def load_chubs() -> dict:
    """(bundle, slip, position) -> CHUBS transcription, from the folder name."""
    labels = {}
    if not CHUBS_DIR.exists():
        return labels
    for folder in CHUBS_DIR.iterdir():
        if not folder.is_dir():
            continue
        for png in folder.glob("郭店簡_01*-老子*.png"):
            m = CHUBS_FILE.match(png.name)
            if m:
                labels[(m.group(1), int(m.group(2)), int(m.group(4)))] = folder.name
    return labels


def load_local() -> dict:
    """slip -> [entries sorted by position], Bundle A only."""
    if not LOCAL_JSON.exists():
        return {}
    data = json.loads(LOCAL_JSON.read_text(encoding="utf-8"))
    return {
        s["slip"]: sorted(s["characters"], key=lambda c: c["position"])
        for s in data["slips"].values()
    }


def load_priority() -> dict:
    """slot id -> why it is canon-adjacent."""
    out = {}
    if not PRIORITY.exists():
        return out
    for line in PRIORITY.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 4 and "—" in parts[-1]:
            out[parts[0].strip()] = parts[-1].split("—", 1)[1].strip()
    return out


def align_slip(toks, entries):
    """
    Map each token to a local entry by index. Returns None unless gxdq and the
    local transcription independently agree on the slip's length.
    """
    seq = []
    for t in toks:
        if t["t"] == "s":
            seq.append(t)
        else:
            seq.extend([None] * len(positions_in(t["v"])))
    if not entries or len(seq) != len(entries):
        return None
    return list(zip(seq, entries))


def main():
    gxdq = load_gxdq()
    chubs = load_chubs()
    local = load_local()
    priority = load_priority()

    slots, aligned_slips, unaligned_slips = [], [], []

    for bundle in gxdq["bundles"]:
        bid = bundle["id"]
        for slip in bundle["slips"]:
            n = slip["slip"]
            entries = local.get(n, []) if bid == "A" else []
            pairs = align_slip(slip["toks"], entries)

            if bid == "A":
                (aligned_slips if pairs else unaligned_slips).append(n)

            # context: the whole slip as gxdq prints it, ○ for each slot
            context = "".join(
                "○" if t["t"] == "s" else t["v"] for t in slip["toks"]
            )

            for tok, entry in (pairs or [(t, None) for t in slip["toks"] if t["t"] == "s"]):
                if tok is None or tok.get("t") != "s":
                    continue
                row = {
                    "id": tok["id"],
                    "bundle": bid,
                    "slip": n,
                    "mark": tok["k"],           # loan | emend | bare
                    "gxdq_reads": tok.get("e"),  # gxdq's editorial reading
                    "context": context,
                    "aligned": entry is not None,
                    "position": None,
                    "glyph_path": None,
                    "local_graph": None,
                    "local_received": None,
                    "chubs": None,
                    "priority": priority.get(tok["id"]),
                }
                if entry is not None:
                    row["position"] = entry["position"]
                    row["glyph_path"] = entry["glyph_path"]
                    row["local_graph"] = entry["guodian"]
                    row["local_received"] = entry["received"]
                    row["chubs"] = chubs.get((bid, n, entry["position"]))
                slots.append(row)

    named = [s for s in slots if s["aligned"] and s["local_graph"] not in (None, "○")]
    out = {
        "metadata": {
            "slots": len(slots),
            "by_bundle": {b: sum(1 for s in slots if s["bundle"] == b) for b in "ABC"},
            "aligned": sum(1 for s in slots if s["aligned"]),
            "with_glyph": sum(1 for s in slots if s["glyph_path"]),
            "named_by_local": len(named),
            "priority": sum(1 for s in slots if s["priority"]),
            "aligned_slips_A": sorted(aligned_slips),
            "unaligned_slips_A": sorted(unaligned_slips),
            "sources": {
                "gxdq": "gxdq.com transcription; editor unattributed; unverified against slip images",
                "local": "data/ddj/verified_transcriptions.json (Bundle A only)",
                "chubs": "CHUBS / THUNLP Chujian, Apache-2.0; folder name is the transcription",
            },
        },
        "slots": slots,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    m = out["metadata"]
    print(f"slots            : {m['slots']}  {m['by_bundle']}")
    print(f"aligned          : {m['aligned']}")
    print(f"with a glyph     : {m['with_glyph']}")
    print(f"named by local   : {m['named_by_local']}  (gxdq prints ○, local names the graph)")
    print(f"canon-adjacent   : {m['priority']}")
    print(f"unaligned slips A: {m['unaligned_slips_A']}")
    print(f"\nwrote {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
