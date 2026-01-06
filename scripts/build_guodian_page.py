#!/usr/bin/env python3
"""
Build Guodian Bundle A visualization HTML page.

Generates an interactive HTML page displaying all 39 bamboo slips
with high-resolution glyph images and character transcriptions.
"""

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def load_verified_transcriptions():
    """Load verified character transcriptions."""
    path = PROJECT_ROOT / "data" / "ddj" / "verified_transcriptions.json"
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_slip_inventory():
    """Load slip inventory with glyph file mappings."""
    path = PROJECT_ROOT / "data" / "ddj" / "guodian_slip_inventory.json"
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def get_slip_chapter_mapping():
    """Return slip-to-chapter mapping from archaeological analysis."""
    return {
        1: [(19, 1, 30)],
        2: [(46, 1, 31)],
        3: [(66, 1, 31)],
        4: [(66, 1, 31)],
        5: [(66, 1, 31)],
        6: [(46, 1, 25), (30, 26, 31)],
        7: [(30, 1, 31)],
        8: [(15, 1, 31)],
        9: [(15, 1, 31)],
        10: [(15, 1, 31)],
        11: [(64, 1, 31)],
        12: [(63, 1, 31)],
        13: [(37, 1, 31)],
        14: [(37, 1, 34)],
        15: [(2, 1, 33)],
        16: [(2, 1, 31)],
        17: [(2, 1, 31)],
        18: [(32, 1, 25)],
        19: [(32, 1, 29)],
        20: [(32, 1, 31)],
        21: [(25, 1, 31)],
        22: [(25, 1, 31)],
        23: [(25, 1, 31), (5, 20, 31)],
        24: [(16, 1, 31)],
        25: [(64, 1, 31)],
        26: [(64, 1, 16)],
        27: [(56, 1, 31)],
        28: [(56, 1, 31)],
        29: [(56, 1, 10), (57, 11, 31)],
        30: [(57, 1, 31)],
        31: [(57, 1, 31)],
        32: [(57, 1, 22)],
        33: [(55, 1, 31)],
        34: [(55, 1, 31)],
        35: [(55, 1, 20), (44, 21, 31)],
        36: [(44, 1, 31)],
        37: [(40, 1, 29)],
        38: [(9, 1, 25)],
        39: [(9, 1, 20)],
    }

def build_char_lookup(transcriptions):
    """Build lookup table: (slip, position) -> (guodian_char, received_char)."""
    lookup = {}
    for chapter_str, data in transcriptions.items():
        positions = data.get("positions", {})
        for pos_key, chars in positions.items():
            if "_" in pos_key:
                parts = pos_key.split("_")
                slip = int(parts[0])
                position = int(parts[1])
            else:
                continue

            guo_char = chars[0] if chars[0] else ""
            rec_char = chars[1] if chars[1] else ""
            lookup[(slip, position)] = (guo_char, rec_char)

    return lookup

def get_chapter_for_position(slip_num, position, slip_chapters):
    """Determine which chapter a slip position belongs to."""
    chapters = slip_chapters.get(slip_num, [])
    for chapter, start, end in chapters:
        if start <= position <= end:
            return chapter
    return None

def generate_html(inventory, char_lookup, slip_chapters):
    """Generate the complete HTML page."""

    # Chapter themes for display
    chapter_themes = {
        2: "Co-emergence",
        5: "The Bellows",
        9: "Completion",
        15: "Practitioner",
        16: "Return to Root",
        19: "Abandon Cleverness",
        25: "Sphere Proof",
        30: "Without Forcing",
        32: "Uncarved Block",
        37: "Self-transformation",
        40: "Oscillation Engine",
        44: "Two Knowings",
        46: "Know Sufficiency",
        55: "Infant Energy",
        56: "Six Operations",
        57: "Self-organization",
        63: "Act on Non-acting",
        64: "Tree from Sprout",
        66: "Valley Principle",
    }

    html_parts = []

    # Header
    html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guodian Bundle A | ~300 BCE Laozi</title>
    <style>
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --bg-tertiary: #1a1a1a;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-muted: #666;
            --accent: #8b5cf6;
            --accent-dim: #6b4fb3;
            --gold: #d4a574;
            --green: #4ade80;
            --red: #f87171;
            --border: #2a2a2a;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 300;
            color: var(--gold);
            margin-bottom: 0.5rem;
        }

        h1 .chinese {
            font-size: 3rem;
            margin-right: 1rem;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .stat {
            text-align: center;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 600;
            color: var(--accent);
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        /* Navigation */
        .nav-bar {
            position: sticky;
            top: 0;
            background: var(--bg-primary);
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            z-index: 100;
        }

        .nav-content {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .nav-btn {
            padding: 0.4rem 0.8rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }

        .nav-btn:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border-color: var(--accent-dim);
        }

        .nav-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        /* Slip display */
        .slip-grid {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .slip-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }

        .slip-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border);
        }

        .slip-id {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--gold);
        }

        .slip-chapters {
            display: flex;
            gap: 0.5rem;
        }

        .chapter-tag {
            padding: 0.25rem 0.75rem;
            background: var(--accent-dim);
            border-radius: 999px;
            font-size: 0.8rem;
            color: white;
        }

        .slip-stats {
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        /* Glyph strip */
        .glyph-strip {
            display: flex;
            flex-wrap: wrap;
            padding: 1.5rem;
            gap: 0.5rem;
            justify-content: flex-start;
        }

        .glyph-cell {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 70px;
            padding: 0.5rem;
            background: var(--bg-primary);
            border-radius: 6px;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }

        .glyph-cell:hover {
            border-color: var(--accent);
            transform: scale(1.05);
        }

        .glyph-cell.loan {
            border-color: var(--gold);
            background: rgba(212, 165, 116, 0.1);
        }

        .glyph-cell.missing {
            opacity: 0.3;
        }

        .glyph-img {
            width: 50px;
            height: 60px;
            object-fit: contain;
            image-rendering: -webkit-optimize-contrast;
            background: #1a1a1a;
            border-radius: 4px;
        }

        .glyph-pos {
            font-size: 0.65rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        .glyph-chars {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 0.25rem;
        }

        .glyph-guodian {
            font-size: 1.2rem;
            font-family: "Noto Serif TC", "Songti SC", serif;
            color: var(--text-primary);
        }

        .glyph-received {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .glyph-received.different {
            color: var(--gold);
        }

        /* Chapter summaries */
        .chapter-summary {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
        }

        .chapter-summary h2 {
            color: var(--gold);
            margin-bottom: 1.5rem;
            font-weight: 400;
        }

        .chapter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }

        .chapter-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1rem;
        }

        .chapter-card h3 {
            color: var(--accent);
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }

        .chapter-card .theme {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .chapter-card .slips {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        /* Footer */
        footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
        }

        /* View toggles */
        .view-toggle {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }

        .toggle-btn {
            padding: 0.5rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }

        .toggle-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        /* Legend */
        .legend {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .legend-swatch {
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid;
        }

        .legend-swatch.loan {
            background: rgba(212, 165, 116, 0.2);
            border-color: var(--gold);
        }

        .legend-swatch.standard {
            background: var(--bg-primary);
            border-color: var(--border);
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            h1 {
                font-size: 1.8rem;
            }

            h1 .chinese {
                font-size: 2.2rem;
            }

            .glyph-cell {
                width: 55px;
            }

            .glyph-img {
                width: 40px;
                height: 48px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><span class="chinese">郭店老子甲</span> Guodian Bundle A</h1>
            <p class="subtitle">~300 BCE Bamboo Slip Laozi | The Oldest Extant Dao De Jing</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">39</div>
                    <div class="stat-label">Bamboo Slips</div>
                </div>
                <div class="stat">
                    <div class="stat-value">1073</div>
                    <div class="stat-label">Character Glyphs</div>
                </div>
                <div class="stat">
                    <div class="stat-value">18</div>
                    <div class="stat-label">DDJ Chapters</div>
                </div>
            </div>
        </header>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-swatch standard"></div>
                <span>Standard character</span>
            </div>
            <div class="legend-item">
                <div class="legend-swatch loan"></div>
                <span>Phonetic loan / variant</span>
            </div>
        </div>

        <nav class="nav-bar">
            <div class="nav-content">
''')

    # Navigation buttons for each slip
    for slip_num in range(1, 40):
        html_parts.append(f'                <button class="nav-btn" onclick="scrollToSlip({slip_num})">Slip {slip_num}</button>\n')

    html_parts.append('''            </div>
        </nav>

        <main class="slip-grid">
''')

    # Generate each slip
    for slip_num in range(1, 40):
        slip_data = inventory.get(str(slip_num), {})
        glyphs = slip_data.get("glyphs", [])
        chapters = slip_chapters.get(slip_num, [])

        chapter_list = list(set(ch for ch, _, _ in chapters))
        chapter_tags = "".join(
            f'<span class="chapter-tag">Ch. {ch}{" - " + chapter_themes.get(ch, "") if ch in chapter_themes else ""}</span>'
            for ch in chapter_list
        )

        html_parts.append(f'''            <section class="slip-container" id="slip-{slip_num}">
                <div class="slip-header">
                    <div class="slip-id">Slip {slip_num}</div>
                    <div class="slip-chapters">{chapter_tags}</div>
                    <div class="slip-stats">{len(glyphs)} glyphs</div>
                </div>
                <div class="glyph-strip">
''')

        for glyph in glyphs:
            pos = glyph["position"]
            filename = glyph["filename"]

            # Look up character
            guo_char, rec_char = char_lookup.get((slip_num, pos), ("", ""))

            # Determine if this is a loan/variant
            is_loan = guo_char and rec_char and guo_char != rec_char
            loan_class = " loan" if is_loan else ""

            # Image path
            img_path = f"/glyphs/bundle-a/{filename}"

            # Character display
            guo_display = guo_char if guo_char else "?"
            rec_class = "different" if is_loan else ""
            rec_display = f"({rec_char})" if is_loan and rec_char else ""

            html_parts.append(f'''                    <div class="glyph-cell{loan_class}" title="Slip {slip_num}, Position {pos}">
                        <img class="glyph-img" src="{img_path}" alt="Slip {slip_num} Pos {pos}" loading="lazy">
                        <span class="glyph-pos">{pos}</span>
                        <div class="glyph-chars">
                            <span class="glyph-guodian">{guo_display}</span>
                            <span class="glyph-received {rec_class}">{rec_display}</span>
                        </div>
                    </div>
''')

        html_parts.append('''                </div>
            </section>
''')

    # Chapter summary section
    html_parts.append('''        </main>

        <section class="chapter-summary">
            <h2>Chapters in Bundle A</h2>
            <div class="chapter-grid">
''')

    # Aggregate chapters
    chapter_slips = {}
    for slip_num, chapters in slip_chapters.items():
        for ch, _, _ in chapters:
            if ch not in chapter_slips:
                chapter_slips[ch] = []
            if slip_num not in chapter_slips[ch]:
                chapter_slips[ch].append(slip_num)

    for ch in sorted(chapter_slips.keys()):
        slips = sorted(chapter_slips[ch])
        theme = chapter_themes.get(ch, "")
        slip_list = ", ".join(str(s) for s in slips)

        html_parts.append(f'''                <div class="chapter-card">
                    <h3>Chapter {ch}</h3>
                    <p class="theme">{theme}</p>
                    <p class="slips">Slips: {slip_list}</p>
                </div>
''')

    # Footer
    html_parts.append('''            </div>
        </section>

        <footer>
            <p>Guodian bamboo slips discovered 1993, Hubei Province, China</p>
            <p>Tomb sealed ~278 BCE | Oldest known Dao De Jing manuscript</p>
            <p>Part of the <a href="/">Our Infinite Reality</a> translation project</p>
        </footer>
    </div>

    <script>
        function scrollToSlip(num) {
            const element = document.getElementById('slip-' + num);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    </script>
</body>
</html>
''')

    return "".join(html_parts)


def main():
    print("Building Guodian Bundle A visualization...")

    # Load data
    transcriptions = load_verified_transcriptions()
    inventory = load_slip_inventory()
    slip_chapters = get_slip_chapter_mapping()

    print(f"  Loaded {len(transcriptions)} chapter transcriptions")
    print(f"  Loaded {len(inventory)} slip inventories")

    # Build character lookup
    char_lookup = build_char_lookup(transcriptions)
    print(f"  Built lookup for {len(char_lookup)} character positions")

    # Generate HTML
    html = generate_html(inventory, char_lookup, slip_chapters)

    # Write output
    output_path = PROJECT_ROOT / "public" / "guodian-bundle-a.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nGenerated: {output_path}")
    print(f"  File size: {len(html):,} bytes")


if __name__ == "__main__":
    main()
