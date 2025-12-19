"""
Oracle Bone Mapper: Integration with HUST-OBC dataset for DDJ character evolution tracking.

Maps DDJ characters to their oracle bone (甲骨文) forms from the HUST-OBC dataset.
Provides access to glyph images for cross-stage character evolution analysis.

Dataset: https://github.com/Pengjie-W/HUST-OBC
License: CC BY 4.0
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class OracleBoneMapper:
    """Map modern Chinese characters to oracle bone script glyphs."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.obc_root = self.project_root / "data" / "HUST-OBC" / "HUST-OBC"
        self.deciphered_dir = self.obc_root / "deciphered"
        self._char_to_id = None
        self._id_to_char = None

    @property
    def char_to_id(self) -> Dict[str, str]:
        """Lazy-load character to ID mapping."""
        if self._char_to_id is None:
            mapping_file = self.deciphered_dir / "chinese_to_ID.json"
            if mapping_file.exists():
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    self._char_to_id = json.load(f)
            else:
                self._char_to_id = {}
        return self._char_to_id

    @property
    def id_to_char(self) -> Dict[str, str]:
        """Lazy-load ID to character mapping."""
        if self._id_to_char is None:
            mapping_file = self.deciphered_dir / "ID_to_chinese.json"
            if mapping_file.exists():
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    self._id_to_char = json.load(f)
            else:
                self._id_to_char = {}
        return self._id_to_char

    def has_oracle_bone(self, char: str) -> bool:
        """Check if a character has oracle bone forms."""
        return char in self.char_to_id

    def get_oracle_bone_id(self, char: str) -> Optional[str]:
        """Get the oracle bone ID for a character."""
        return self.char_to_id.get(char)

    def get_glyph_folder(self, char: str) -> Optional[Path]:
        """Get the folder containing oracle bone glyphs for a character."""
        ob_id = self.get_oracle_bone_id(char)
        if not ob_id:
            return None

        # Check for combined folder (e.g., "0011_0012_0013")
        for folder in self.deciphered_dir.iterdir():
            if folder.is_dir():
                # Check if this ID is in the folder name (handles combined folders)
                if ob_id in folder.name.split('_'):
                    return folder

        # Direct folder match
        direct_folder = self.deciphered_dir / ob_id
        if direct_folder.exists():
            return direct_folder

        return None

    def get_glyph_images(self, char: str) -> List[Dict]:
        """
        Get all oracle bone glyph images for a character.

        Returns list of dicts with:
        - path: full path to image
        - filename: image filename
        - source: source reference (e.g., "合36544" for Heji collection)
        """
        folder = self.get_glyph_folder(char)
        if not folder:
            return []

        ob_id = self.get_oracle_bone_id(char)
        images = []

        for img in folder.glob("*.png"):
            # Parse source from filename: G_0429_林1.27.8合36544.png
            filename = img.name
            source = ""

            # Extract source reference after the ID prefix
            prefix = f"G_{ob_id}_"
            if filename.startswith(prefix):
                source = filename[len(prefix):].replace('.png', '')

            images.append({
                'path': str(img),
                'filename': filename,
                'source': source,
                'char': char,
                'ob_id': ob_id
            })

        return images

    def get_ddj_coverage(self) -> Dict[str, any]:
        """
        Analyze oracle bone coverage for DDJ characters.

        Returns statistics on which DDJ characters have oracle bone forms.
        """
        # Key DDJ characters (from the 81 chapters)
        ddj_core_chars = set("""
            道德天地無有萬物自然反弱水谷聖人心者之不為
            上下大小長短高低前後左右內外生死始終動靜
            柔強陰陽明暗善惡美醜真偽虛實難易輕重
            常名母子玄妙徼眾門沖用盈似宗挫銳解紛光塵
            湛存象帝先仁芻狗間橐籥守中神根綿若勤久
            能身退私非幾正時持滿揣保富驕咎遂載營魄抱
        """.replace('\n', '').replace(' ', ''))

        found = []
        not_found = []

        for char in ddj_core_chars:
            if self.has_oracle_bone(char):
                images = self.get_glyph_images(char)
                found.append({
                    'char': char,
                    'ob_id': self.get_oracle_bone_id(char),
                    'glyph_count': len(images)
                })
            else:
                not_found.append(char)

        return {
            'total_ddj_chars': len(ddj_core_chars),
            'found': len(found),
            'not_found': len(not_found),
            'coverage_pct': len(found) / len(ddj_core_chars) * 100,
            'found_chars': found,
            'missing_chars': not_found
        }

    def export_for_glossary(self, char: str) -> Optional[Dict]:
        """
        Export oracle bone data for a character in glossary format.

        Returns dict ready for glossary integration:
        {
            "attested": True,
            "ob_id": "0429",
            "glyph_count": 75,
            "image_refs": ["path/to/img1.png", ...],
            "sources": ["合36544", "合22055", ...]
        }
        """
        if not self.has_oracle_bone(char):
            return {
                "attested": False,
                "ob_id": None,
                "glyph_count": 0,
                "image_refs": [],
                "sources": []
            }

        images = self.get_glyph_images(char)
        return {
            "attested": True,
            "ob_id": self.get_oracle_bone_id(char),
            "glyph_count": len(images),
            "image_refs": [img['path'] for img in images[:10]],  # First 10 for glossary
            "sources": list(set(img['source'] for img in images if img['source']))[:10]
        }


def main():
    """Demo oracle bone integration."""
    mapper = OracleBoneMapper()

    print("=" * 60)
    print("ORACLE BONE SCRIPT INTEGRATION")
    print("HUST-OBC Dataset")
    print("=" * 60)

    # Check dataset availability
    if not mapper.deciphered_dir.exists():
        print("\nDataset not found. Please download from:")
        print("https://figshare.com/s/8a9c0420312d94fc01e3")
        return

    print(f"\nTotal oracle bone characters: {len(mapper.char_to_id)}")

    # DDJ coverage analysis
    print("\n" + "-" * 40)
    print("DDJ CHARACTER COVERAGE")
    print("-" * 40)

    coverage = mapper.get_ddj_coverage()
    print(f"DDJ characters analyzed: {coverage['total_ddj_chars']}")
    print(f"Found in oracle bone: {coverage['found']} ({coverage['coverage_pct']:.1f}%)")
    print(f"Not found: {coverage['not_found']}")

    print("\nCharacters with oracle bone forms:")
    for item in sorted(coverage['found_chars'], key=lambda x: -x['glyph_count'])[:15]:
        print(f"  {item['char']} (ID {item['ob_id']}): {item['glyph_count']} glyphs")

    print(f"\nMissing (may be later concepts): {''.join(coverage['missing_chars'][:20])}")

    # Sample detailed view
    print("\n" + "-" * 40)
    print("SAMPLE: 天 (tiān - heaven/sky)")
    print("-" * 40)

    tian_data = mapper.export_for_glossary('天')
    print(f"Attested: {tian_data['attested']}")
    print(f"Oracle Bone ID: {tian_data['ob_id']}")
    print(f"Glyph count: {tian_data['glyph_count']}")
    print(f"Sample sources: {tian_data['sources'][:5]}")

    # Notable absence
    print("\n" + "-" * 40)
    print("NOTABLE: 道 and 德")
    print("-" * 40)
    print("道 (dào) - NOT in oracle bone: May indicate later conceptualization")
    print("德 (dé) - NOT in oracle bone: Core Daoist term, likely evolved form")


if __name__ == "__main__":
    main()
