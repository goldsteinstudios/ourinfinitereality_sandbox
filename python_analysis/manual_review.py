"""
Manual Review Interface for Guodian Laozi Transcription.

Generates HTML review pages for uncertain glyph positions:
- Displays glyph image with surrounding context
- Shows CHUBS annotation and suggested identification
- Provides form for human corrections
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from chubs_reverse_mapper import ChubsReverseMapper
from transcription_generator import TranscriptionGenerator


class ManualReviewGenerator:
    """Generate HTML review pages for uncertain glyph positions."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.mapper = ChubsReverseMapper()
        self.generator = TranscriptionGenerator()
        self.output_dir = self.project_root / "output" / "glyph_review"

    def get_context_glyphs(self, slip_num: int, position: int, window: int = 3) -> List[Dict]:
        """Get surrounding glyphs for context."""
        slip_data = self.mapper.get_slip_transcription(slip_num)

        result = []
        for glyph in slip_data:
            if abs(glyph["position"] - position) <= window:
                glyph["is_target"] = glyph["position"] == position
                result.append(glyph)

        return sorted(result, key=lambda x: x["position"])

    def generate_review_item_html(self, slip_num: int, position: int, glyph: Dict) -> str:
        """Generate HTML for a single review item."""
        context = self.get_context_glyphs(slip_num, position)

        context_html = []
        for g in context:
            cls = "target" if g.get("is_target") else ""
            char = g["guodian_char"]
            context_html.append(f'<span class="context-char {cls}">{char}</span>')

        suggested = glyph.get("received_char", glyph["guodian_char"])
        if glyph["guodian_char"] == "○":
            # Get the standard char from folder name
            suggested = glyph.get("folder", "").split("（")[-1].rstrip("）") if "（" in glyph.get("folder", "") else "?"

        return f'''
        <div class="review-item" data-slip="{slip_num}" data-position="{position}">
            <div class="item-header">
                <span class="slip-pos">Slip {slip_num}, Position {position}</span>
                <span class="chubs-folder">CHUBS: {glyph.get("folder", "?")}</span>
            </div>

            <div class="item-content">
                <div class="glyph-image">
                    <img src="{glyph.get("path", "")}" alt="Glyph at {slip_num}-{position}">
                </div>

                <div class="context">
                    <div class="context-label">Context:</div>
                    <div class="context-chars">
                        {"".join(context_html)}
                    </div>
                </div>

                <div class="identification">
                    <div class="current">
                        <label>CHUBS identifies as:</label>
                        <span class="char-display">{glyph["guodian_char"]}</span>
                        {f'<span class="variant-note">(variant of {suggested})</span>' if glyph["guodian_char"] != suggested else ""}
                    </div>

                    <div class="correction">
                        <label for="correct-{slip_num}-{position}">Your identification:</label>
                        <input type="text"
                               id="correct-{slip_num}-{position}"
                               name="correct-{slip_num}-{position}"
                               value="{suggested}"
                               class="char-input"
                               maxlength="2">
                        <input type="text"
                               id="note-{slip_num}-{position}"
                               name="note-{slip_num}-{position}"
                               placeholder="Notes..."
                               class="note-input">
                    </div>
                </div>
            </div>
        </div>
        '''

    def generate_chapter_review_page(self, chapter_num: int) -> str:
        """Generate HTML review page for a single chapter."""
        transcription = self.generator.generate_chapter_transcription(chapter_num)

        if not transcription["review_needed"]:
            return f'''<!DOCTYPE html>
<html>
<head><title>Chapter {chapter_num} - No Review Needed</title></head>
<body>
    <h1>Chapter {chapter_num}</h1>
    <p>All glyphs auto-identified with high confidence. No manual review needed.</p>
    <a href="index.html">Back to Index</a>
</body>
</html>'''

        review_items_html = []
        for review_item in transcription["review_needed"]:
            slip = review_item["slip"]
            pos = review_item["position"]

            # Get full glyph data
            glyph_index = self.mapper.build_glyph_index()
            matching = [
                g for g in glyph_index.values()
                if g["slip"] == slip and g["position"] == pos
            ]

            if matching:
                glyph = matching[0]
                review_items_html.append(
                    self.generate_review_item_html(slip, pos, glyph)
                )

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Review: Chapter {chapter_num}</title>
    <style>
        :root {{
            --bg-dark: #1a1a1a;
            --bg-card: #252525;
            --text: #e0e0e0;
            --gold: #ffd700;
            --accent: #4a9eff;
            --warning: #ff6b6b;
        }}

        body {{
            font-family: 'Noto Sans SC', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            color: var(--gold);
            border-bottom: 2px solid var(--gold);
            padding-bottom: 10px;
        }}

        .stats {{
            background: var(--bg-card);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .review-item {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .item-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #888;
        }}

        .item-content {{
            display: grid;
            grid-template-columns: 120px 1fr 1fr;
            gap: 20px;
            align-items: start;
        }}

        .glyph-image img {{
            width: 100px;
            height: 100px;
            object-fit: contain;
            background: #f5f5dc;
            border-radius: 8px;
        }}

        .context-chars {{
            font-size: 2em;
            margin-top: 10px;
        }}

        .context-char {{
            padding: 5px;
        }}

        .context-char.target {{
            background: var(--warning);
            color: black;
            border-radius: 4px;
        }}

        .identification {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .char-display {{
            font-size: 2em;
            color: var(--gold);
            margin-left: 10px;
        }}

        .variant-note {{
            font-size: 0.8em;
            color: #888;
            margin-left: 10px;
        }}

        .correction {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .char-input {{
            width: 60px;
            font-size: 1.5em;
            padding: 5px;
            text-align: center;
            border: 2px solid var(--accent);
            border-radius: 4px;
            background: var(--bg-dark);
            color: var(--text);
        }}

        .note-input {{
            width: 200px;
            padding: 8px;
            border: 1px solid #444;
            border-radius: 4px;
            background: var(--bg-dark);
            color: var(--text);
        }}

        .nav {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }}

        .nav a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .save-btn {{
            background: var(--accent);
            color: black;
            border: none;
            padding: 12px 30px;
            font-size: 1.1em;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
        }}

        .save-btn:hover {{
            background: #6ab0ff;
        }}

        #save-status {{
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
            display: none;
        }}

        #save-status.success {{
            display: block;
            background: #2d4a2d;
            color: #90EE90;
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <a href="index.html">&larr; Back to Index</a>
        <span>Chapter {chapter_num}</span>
    </nav>

    <h1>Review: Chapter {chapter_num}</h1>

    <div class="stats">
        <strong>Slips:</strong> {", ".join(str(s) for s in transcription["slips"])} |
        <strong>Total glyphs:</strong> {transcription["stats"]["total_glyphs"]} |
        <strong>Need review:</strong> {len(transcription["review_needed"])}
    </div>

    <form id="review-form">
        {"".join(review_items_html)}

        <button type="button" class="save-btn" onclick="saveCorrections()">
            Save Corrections
        </button>

        <div id="save-status"></div>
    </form>

    <script>
        function saveCorrections() {{
            const form = document.getElementById('review-form');
            const items = document.querySelectorAll('.review-item');
            const corrections = [];

            items.forEach(item => {{
                const slip = item.dataset.slip;
                const position = item.dataset.position;
                const correctedChar = document.getElementById(`correct-${{slip}}-${{position}}`).value;
                const note = document.getElementById(`note-${{slip}}-${{position}}`).value;

                corrections.push({{
                    slip: parseInt(slip),
                    position: parseInt(position),
                    corrected_char: correctedChar,
                    note: note
                }});
            }});

            // Output as JSON for user to save
            const json = JSON.stringify({{
                chapter: {chapter_num},
                corrections: corrections,
                reviewed_at: new Date().toISOString()
            }}, null, 2);

            // Show in console and prompt download
            console.log(json);

            const blob = new Blob([json], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chapter_{chapter_num}_corrections.json`;
            a.click();

            document.getElementById('save-status').className = 'success';
            document.getElementById('save-status').textContent =
                `Saved! Download chapter_{chapter_num}_corrections.json`;
        }}
    </script>
</body>
</html>'''

    def generate_index_page(self) -> str:
        """Generate index page showing all chapters needing review."""
        transcriptions = self.generator.generate_all_transcriptions()

        chapters_html = []
        total_review = 0

        for chapter in sorted(transcriptions.keys()):
            data = transcriptions[chapter]
            review_count = len(data["review_needed"])
            total_review += review_count

            status_class = "complete" if review_count == 0 else "needs-review"
            status_text = "Complete" if review_count == 0 else f"{review_count} to review"

            chapters_html.append(f'''
            <a href="chapter_{chapter}.html" class="chapter-card {status_class}">
                <span class="ch-num">{chapter}</span>
                <span class="ch-status">{status_text}</span>
                <span class="ch-glyphs">{data["stats"]["total_glyphs"]} glyphs</span>
            </a>
            ''')

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Guodian Laozi - Manual Review</title>
    <style>
        :root {{
            --bg-dark: #1a1a1a;
            --bg-card: #252525;
            --text: #e0e0e0;
            --gold: #ffd700;
            --accent: #4a9eff;
            --success: #4caf50;
            --warning: #ff9800;
        }}

        body {{
            font-family: 'Noto Sans SC', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            color: var(--gold);
        }}

        .stats {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }}

        .stat-box {{
            text-align: center;
        }}

        .stat-num {{
            font-size: 2em;
            color: var(--gold);
        }}

        .stat-label {{
            color: #888;
        }}

        .chapters {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }}

        .chapter-card {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--text);
            text-align: center;
            transition: transform 0.2s;
        }}

        .chapter-card:hover {{
            transform: scale(1.05);
        }}

        .chapter-card.complete {{
            border: 2px solid var(--success);
        }}

        .chapter-card.needs-review {{
            border: 2px solid var(--warning);
        }}

        .ch-num {{
            display: block;
            font-size: 2em;
            color: var(--gold);
        }}

        .ch-status {{
            display: block;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .ch-glyphs {{
            display: block;
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }}

        .chapter-card.complete .ch-status {{
            color: var(--success);
        }}

        .chapter-card.needs-review .ch-status {{
            color: var(--warning);
        }}
    </style>
</head>
<body>
    <h1>Guodian Laozi A - Manual Review</h1>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-num">{len(transcriptions)}</div>
            <div class="stat-label">Chapters</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{sum(d["stats"]["total_glyphs"] for d in transcriptions.values())}</div>
            <div class="stat-label">Total Glyphs</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{total_review}</div>
            <div class="stat-label">Need Review</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{sum(1 for d in transcriptions.values() if not d["review_needed"])}</div>
            <div class="stat-label">Complete</div>
        </div>
    </div>

    <h2>Chapters</h2>
    <div class="chapters">
        {"".join(chapters_html)}
    </div>
</body>
</html>'''

    def build_review_site(self) -> Path:
        """Build complete review site."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate index
        index_path = self.output_dir / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_index_page())

        # Generate chapter pages
        transcriptions = self.generator.generate_all_transcriptions()
        for chapter in transcriptions:
            chapter_path = self.output_dir / f"chapter_{chapter}.html"
            with open(chapter_path, 'w', encoding='utf-8') as f:
                f.write(self.generate_chapter_review_page(chapter))

        return self.output_dir


def main():
    """Build manual review site."""
    generator = ManualReviewGenerator()

    print("Building manual review site...")
    output = generator.build_review_site()
    print(f"Review site built at: {output}")
    print(f"Open: {output / 'index.html'}")


if __name__ == "__main__":
    main()
