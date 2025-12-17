"""
Chu Script Renderer: Rebuild Guodian text using original Chu bamboo slip glyphs.

Uses CHUBS glyph images to render DDJ text in its original script form.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class ChuRenderer:
    """
    Render Chinese text using Chu bamboo slip glyph images from CHUBS.
    """

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.chubs_dir = self.project_root / "data" / "CHUBS_repo"
        self.glyphs_dir = self.chubs_dir / "glyphs"
        self.mappings_path = self.chubs_dir / "twelve_book_glyph_mappings.json"
        self.output_dir = self.project_root / "output" / "chu_renders"

        self._mappings = None

    @property
    def mappings(self) -> Dict:
        """Lazy-load glyph mappings."""
        if self._mappings is None:
            if self.mappings_path.exists():
                with open(self.mappings_path, encoding='utf-8') as f:
                    self._mappings = json.load(f)
            else:
                self._mappings = {}
        return self._mappings

    def get_glyph_path(self, character: str, prefer_laozi: bool = True) -> Optional[Path]:
        """
        Get path to best glyph image for a character.

        Args:
            character: Chinese character
            prefer_laozi: Prefer Guodian Laozi source images

        Returns:
            Path to glyph image or None
        """
        if character not in self.mappings:
            return None

        data = self.mappings[character]
        paths = data.get("paths", [])

        if not paths:
            return None

        # Try to find a Laozi-sourced glyph
        if prefer_laozi and data.get("guodian_laozi"):
            for path in paths:
                if "老子" in path:
                    glyph_dir = Path(path)
                    if glyph_dir.exists():
                        images = list(glyph_dir.glob("*.png")) + list(glyph_dir.glob("*.jpg"))
                        # Find one from Laozi
                        for img in images:
                            if "老子" in img.name:
                                return img
                        # Fall back to first image in Laozi folder
                        if images:
                            return images[0]

        # Fall back to first available path
        for path in paths:
            glyph_dir = Path(path)
            if glyph_dir.exists():
                images = list(glyph_dir.glob("*.png")) + list(glyph_dir.glob("*.jpg"))
                if images:
                    return images[0]

        return None

    def get_coverage(self, text: str) -> Dict[str, Any]:
        """
        Analyze coverage for a text passage.

        Args:
            text: Chinese text

        Returns:
            Coverage statistics
        """
        chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
        unique = set(chars)

        covered = [c for c in unique if c in self.mappings]
        laozi_covered = [c for c in unique if c in self.mappings and self.mappings[c].get("guodian_laozi")]
        missing = [c for c in unique if c not in self.mappings]

        return {
            "total_chars": len(chars),
            "unique_chars": len(unique),
            "covered": len(covered),
            "covered_pct": 100 * len(covered) / len(unique) if unique else 0,
            "laozi_covered": len(laozi_covered),
            "laozi_pct": 100 * len(laozi_covered) / len(unique) if unique else 0,
            "missing": missing,
            "missing_count": len(missing)
        }

    def render_text_info(self, text: str) -> List[Dict[str, Any]]:
        """
        Get rendering info for each character in text.

        Args:
            text: Chinese text

        Returns:
            List of character info dicts
        """
        result = []
        for char in text:
            if not ('\u4e00' <= char <= '\u9fff'):
                result.append({
                    "char": char,
                    "type": "punctuation",
                    "has_glyph": False
                })
                continue

            glyph_path = self.get_glyph_path(char)
            data = self.mappings.get(char, {})

            result.append({
                "char": char,
                "type": "chinese",
                "has_glyph": glyph_path is not None,
                "glyph_path": str(glyph_path) if glyph_path else None,
                "guodian_laozi": data.get("guodian_laozi", False),
                "glyph_count": data.get("glyph_count", 0)
            })

        return result

    def render_to_html(self, text: str, title: str = "Chu Script Render") -> str:
        """
        Render text as HTML with Chu glyph images.

        Args:
            text: Chinese text to render
            title: Page title

        Returns:
            HTML string
        """
        info = self.render_text_info(text)
        coverage = self.get_coverage(text)

        html_parts = [f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Noto Sans SC', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }}
        h1 {{ color: #ffd700; }}
        .stats {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .text-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        .char-box {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 5px;
        }}
        .glyph-img {{
            width: 64px;
            height: 64px;
            object-fit: contain;
            background: #f5f5dc;
            border-radius: 4px;
        }}
        .missing {{
            width: 64px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #333;
            border: 2px dashed #666;
            border-radius: 4px;
            font-size: 32px;
        }}
        .modern {{
            font-size: 14px;
            color: #888;
            margin-top: 4px;
        }}
        .laozi {{
            border: 2px solid #ffd700;
        }}
        .legend {{
            display: flex;
            gap: 20px;
            margin: 10px 0;
            font-size: 14px;
        }}
        .legend span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .legend-box {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }}
        .legend-laozi {{ background: #f5f5dc; border: 2px solid #ffd700; }}
        .legend-other {{ background: #f5f5dc; }}
        .legend-missing {{ background: #333; border: 2px dashed #666; }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="stats">
        <strong>Coverage:</strong> {coverage['covered']}/{coverage['unique_chars']} characters
        ({coverage['covered_pct']:.1f}%)
        | <strong>Guodian Laozi:</strong> {coverage['laozi_covered']}
        ({coverage['laozi_pct']:.1f}%)
        | <strong>Missing:</strong> {''.join(coverage['missing'][:20])}{'...' if len(coverage['missing']) > 20 else ''}
    </div>

    <div class="legend">
        <span><div class="legend-box legend-laozi"></div> Guodian Laozi glyph</span>
        <span><div class="legend-box legend-other"></div> Other Chu glyph</span>
        <span><div class="legend-box legend-missing"></div> No glyph (modern char shown)</span>
    </div>

    <div class="text-row">
"""]

        for item in info:
            if item["type"] == "punctuation":
                html_parts.append(f'<div class="char-box"><div class="missing">{item["char"]}</div></div>')
            elif item["has_glyph"]:
                laozi_class = "laozi" if item["guodian_laozi"] else ""
                # Use relative path from output dir
                rel_path = item["glyph_path"]
                html_parts.append(f'''
                    <div class="char-box">
                        <img class="glyph-img {laozi_class}" src="{rel_path}" alt="{item['char']}" title="{item['char']} ({item['glyph_count']} glyphs)">
                        <span class="modern">{item['char']}</span>
                    </div>
                ''')
            else:
                html_parts.append(f'''
                    <div class="char-box">
                        <div class="missing">{item['char']}</div>
                        <span class="modern">{item['char']}</span>
                    </div>
                ''')

        html_parts.append("""
    </div>
</body>
</html>
""")

        return "".join(html_parts)

    def render_passage(self, text: str, output_name: str = "render") -> Path:
        """
        Render a passage and save to file.

        Args:
            text: Chinese text
            output_name: Output filename (without extension)

        Returns:
            Path to output file
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{output_name}.html"

        html = self.render_to_html(text, title=f"Chu Script: {output_name}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path


def main():
    """Demo the renderer."""
    renderer = ChuRenderer()

    # Chapter 25 opening - the "sphere proof"
    ch25 = "有物混成先天地生寂兮寥兮獨立不改周行而不殆可以為天下母"

    # Check coverage
    print("=== Chu Script Renderer Demo ===")
    print()
    coverage = renderer.get_coverage(ch25)
    print(f"Chapter 25 opening ({len(ch25)} chars):")
    print(f"  Coverage: {coverage['covered']}/{coverage['unique_chars']} ({coverage['covered_pct']:.1f}%)")
    print(f"  Guodian Laozi: {coverage['laozi_covered']} ({coverage['laozi_pct']:.1f}%)")
    print(f"  Missing: {''.join(coverage['missing'])}")

    # Show which chars have glyphs
    print()
    print("Character breakdown:")
    info = renderer.render_text_info(ch25)
    for item in info:
        if item["type"] == "chinese":
            status = "✓ LAOZI" if item["guodian_laozi"] else ("✓" if item["has_glyph"] else "✗")
            print(f"  {item['char']}: {status}")

    # Chapter 40 - the oscillation engine
    ch40 = "反者道之動弱者道之用天下萬物生於有有生於無"

    print()
    print(f"Chapter 40 ({len(ch40)} chars):")
    coverage40 = renderer.get_coverage(ch40)
    print(f"  Coverage: {coverage40['covered']}/{coverage40['unique_chars']} ({coverage40['covered_pct']:.1f}%)")
    print(f"  Guodian Laozi: {coverage40['laozi_covered']} ({coverage40['laozi_pct']:.1f}%)")
    print(f"  Missing: {''.join(coverage40['missing']) or 'None!'}")


if __name__ == "__main__":
    main()
