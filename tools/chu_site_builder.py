"""
Chu Script Site Builder: Generate a complete browsable site of Guodian DDJ in Chu script.

Creates:
1. Individual chapter pages with Chu glyph renders
2. Index page with navigation and coverage stats
3. Glyph atlas showing all available characters
"""

import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
from datetime import datetime

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from chu_renderer import ChuRenderer
from guodian_glyph_mapper import GuodianGlyphMapper


class ChuSiteBuilder:
    """Build a complete Chu script browsing site."""

    # Guodian confirmed chapters
    GUODIAN_CHAPTERS = [2, 5, 9, 13, 15, 16, 17, 18, 19, 20, 25, 30, 31, 32,
                        35, 37, 40, 41, 44, 45, 46, 48, 52, 54, 56, 57, 63, 64, 66]

    # Pinyin dictionary for DDJ characters
    PINYIN = {
        '道': 'dào', '德': 'dé', '經': 'jīng', '可': 'kě', '名': 'míng', '常': 'cháng',
        '無': 'wú', '有': 'yǒu', '萬': 'wàn', '物': 'wù', '之': 'zhī', '始': 'shǐ',
        '母': 'mǔ', '故': 'gù', '欲': 'yù', '以': 'yǐ', '觀': 'guān', '其': 'qí',
        '妙': 'miào', '徼': 'jiào', '此': 'cǐ', '兩': 'liǎng', '者': 'zhě', '同': 'tóng',
        '出': 'chū', '而': 'ér', '異': 'yì', '謂': 'wèi', '玄': 'xuán', '又': 'yòu',
        '眾': 'zhòng', '門': 'mén', '天': 'tiān', '下': 'xià', '皆': 'jiē', '知': 'zhī',
        '美': 'měi', '為': 'wéi', '斯': 'sī', '惡': 'è', '已': 'yǐ', '善': 'shàn',
        '不': 'bù', '相': 'xiāng', '生': 'shēng', '難': 'nán', '易': 'yì', '成': 'chéng',
        '長': 'cháng', '短': 'duǎn', '形': 'xíng', '高': 'gāo', '傾': 'qīng', '音': 'yīn',
        '聲': 'shēng', '和': 'hé', '前': 'qián', '後': 'hòu', '隨': 'suí', '是': 'shì',
        '聖': 'shèng', '人': 'rén', '處': 'chù', '事': 'shì', '行': 'xíng', '言': 'yán',
        '教': 'jiào', '作': 'zuò', '辭': 'cí', '功': 'gōng', '弗': 'fú', '居': 'jū',
        '夫': 'fū', '唯': 'wéi', '去': 'qù', '賢': 'xián', '使': 'shǐ', '民': 'mín',
        '爭': 'zhēng', '貴': 'guì', '貨': 'huò', '盜': 'dào', '見': 'jiàn', '心': 'xīn',
        '亂': 'luàn', '治': 'zhì', '虛': 'xū', '實': 'shí', '腹': 'fù', '弱': 'ruò',
        '志': 'zhì', '強': 'qiáng', '骨': 'gǔ', '沖': 'chōng', '用': 'yòng', '或': 'huò',
        '盈': 'yíng', '淵': 'yuān', '似': 'sì', '宗': 'zōng', '挫': 'cuò', '銳': 'ruì',
        '解': 'jiě', '紛': 'fēn', '光': 'guāng', '塵': 'chén', '湛': 'zhàn', '存': 'cún',
        '吾': 'wú', '誰': 'shuí', '子': 'zǐ', '象': 'xiàng', '帝': 'dì', '先': 'xiān',
        '地': 'dì', '仁': 'rén', '芻': 'chú', '狗': 'gǒu', '間': 'jiān', '橐': 'tuó',
        '籥': 'yuè', '動': 'dòng', '愈': 'yù', '窮': 'qióng', '數': 'shù', '守': 'shǒu',
        '中': 'zhōng', '谷': 'gǔ', '神': 'shén', '死': 'sǐ', '根': 'gēn', '綿': 'mián',
        '若': 'ruò', '勤': 'qín', '久': 'jiǔ', '能': 'néng', '身': 'shēn', '退': 'tuì',
        '私': 'sī', '非': 'fēi', '上': 'shàng', '水': 'shuǐ', '幾': 'jǐ', '於': 'yú',
        '所': 'suǒ', '正': 'zhèng', '時': 'shí', '持': 'chí', '滿': 'mǎn', '如': 'rú',
        '揣': 'chuǎi', '莫': 'mò', '保': 'bǎo', '富': 'fù', '驕': 'jiāo', '咎': 'jiù',
        '遂': 'suì', '載': 'zài', '營': 'yíng', '魄': 'pò', '抱': 'bào', '一': 'yī',
        '離': 'lí', '專': 'zhuān', '氣': 'qì', '致': 'zhì', '柔': 'róu', '嬰': 'yīng',
        '兒': 'ér', '滌': 'dí', '除': 'chú', '覽': 'lǎn', '疵': 'cī', '愛': 'ài',
        '國': 'guó', '開': 'kāi', '闔': 'hé', '雌': 'cí', '明': 'míng', '白': 'bái',
        '達': 'dá', '四': 'sì', '畜': 'chù', '三': 'sān', '十': 'shí', '輻': 'fú',
        '共': 'gòng', '轂': 'gǔ', '當': 'dāng', '車': 'chē', '埏': 'shān', '埴': 'zhí',
        '器': 'qì', '戶': 'hù', '牖': 'yǒu', '室': 'shì', '利': 'lì', '五': 'wǔ',
        '色': 'sè', '令': 'lìng', '目': 'mù', '盲': 'máng', '馳': 'chí', '騁': 'chěng',
        '田': 'tián', '獵': 'liè', '狂': 'kuáng', '味': 'wèi', '口': 'kǒu', '爽': 'shuǎng',
        '得': 'dé', '稀': 'xī', '腸': 'cháng', '寵': 'chǒng', '辱': 'rǔ', '驚': 'jīng',
        '患': 'huàn', '大': 'dà', '何': 'hé', '貴': 'guì', '寄': 'jì', '託': 'tuō',
        '視': 'shì', '聽': 'tīng', '聞': 'wén', '摶': 'tuán', '希': 'xī', '夷': 'yí',
        '微': 'wēi', '混': 'hùn', '繩': 'shéng', '繹': 'yì', '狀': 'zhuàng', '惚': 'hū',
        '恍': 'huǎng', '迎': 'yíng', '首': 'shǒu', '隨': 'suí', '尾': 'wěi', '執': 'zhí',
        '古': 'gǔ', '御': 'yù', '今': 'jīn', '紀': 'jì', '士': 'shì', '豫': 'yù',
        '冬': 'dōng', '涉': 'shè', '川': 'chuān', '猶': 'yóu', '畏': 'wèi', '鄰': 'lín',
        '儼': 'yǎn', '客': 'kè', '渙': 'huàn', '冰': 'bīng', '釋': 'shì', '敦': 'dūn',
        '樸': 'pǔ', '曠': 'kuàng', '渾': 'hún', '濁': 'zhuó', '靜': 'jìng', '徐': 'xú',
        '清': 'qīng', '安': 'ān', '徐': 'xú', '極': 'jí', '致': 'zhì', '篤': 'dǔ',
        '復': 'fù', '命': 'mìng', '容': 'róng', '公': 'gōng', '王': 'wáng', '殆': 'dài',
        '太': 'tài', '親': 'qīn', '譽': 'yù', '畏': 'wèi', '侮': 'wǔ', '信': 'xìn',
        '猶': 'yóu', '貴': 'guì', '功': 'gōng', '自': 'zì', '然': 'rán', '絕': 'jué',
        '智': 'zhì', '百': 'bǎi', '倍': 'bèi', '棄': 'qì', '巧': 'qiǎo', '孝': 'xiào',
        '慈': 'cí', '素': 'sù', '少': 'shǎo', '私': 'sī', '寡': 'guǎ', '學': 'xué',
        '憂': 'yōu', '唯': 'wéi', '阿': 'ā', '相': 'xiāng', '去': 'qù', '遠': 'yuǎn',
        '畏': 'wèi', '荒': 'huāng', '央': 'yāng', '熙': 'xī', '春': 'chūn', '登': 'dēng',
        '臺': 'tái', '孩': 'hái', '未': 'wèi', '咳': 'hāi', '乘': 'chéng', '歸': 'guī',
        '累': 'lěi', '食': 'shí', '獨': 'dú', '貴': 'guì', '昏': 'hūn', '昭': 'zhāo',
        '察': 'chá', '悶': 'mèn', '望': 'wàng', '海': 'hǎi', '飄': 'piāo', '風': 'fēng',
        '止': 'zhǐ', '孔': 'kǒng', '從': 'cóng', '曲': 'qū', '全': 'quán', '枉': 'wǎng',
        '直': 'zhí', '窪': 'wā', '敝': 'bì', '新': 'xīn', '多': 'duō', '惑': 'huò',
        '抱': 'bào', '式': 'shì', '伐': 'fá', '矜': 'jīn', '希': 'xī', '飄': 'piāo',
        '驟': 'zhòu', '雨': 'yǔ', '終': 'zhōng', '朝': 'zhāo', '孰': 'shú', '企': 'qǐ',
        '立': 'lì', '跨': 'kuà', '餘': 'yú', '贅': 'zhuì', '惡': 'wù', '混': 'hùn',
        '先': 'xiān', '寂': 'jì', '寥': 'liáo', '改': 'gǎi', '周': 'zhōu', '逝': 'shì',
        '反': 'fǎn', '字': 'zì', '強': 'qiáng', '重': 'zhòng', '輕': 'qīng', '躁': 'zào',
        '靜': 'jìng', '君': 'jūn', '師': 'shī', '資': 'zī', '奇': 'qí', '寶': 'bǎo',
        '要': 'yào', '妙': 'miào', '牝': 'pìn', '牡': 'mǔ', '雄': 'xióng', '黑': 'hēi',
        '榮': 'róng', '辱': 'rǔ', '嬰': 'yīng', '樸': 'pǔ', '散': 'sàn', '官': 'guān',
        '長': 'zhǎng', '割': 'gē', '取': 'qǔ', '將': 'jiāng', '輔': 'fǔ', '兵': 'bīng',
        '果': 'guǒ', '已': 'yǐ', '矜': 'jīn', '伐': 'fá', '壯': 'zhuàng', '老': 'lǎo',
        '早': 'zǎo', '夫': 'fū', '佳': 'jiā', '凶': 'xiōng', '左': 'zuǒ', '右': 'yòu',
        '偏': 'piān', '將': 'jiàng', '軍': 'jūn', '喪': 'sāng', '禮': 'lǐ', '哀': 'āi',
        '勝': 'shèng', '樸': 'pǔ', '小': 'xiǎo', '臣': 'chén', '侯': 'hóu', '正': 'zhèng',
        '亦': 'yì', '足': 'zú', '魚': 'yú', '脫': 'tuō', '利': 'lì', '示': 'shì',
        '執': 'zhí', '大': 'dà', '象': 'xiàng', '往': 'wǎng', '害': 'hài', '平': 'píng',
        '過': 'guò', '餌': 'ěr', '樂': 'lè', '淡': 'dàn', '視': 'shì', '足': 'zú',
        '歙': 'xī', '張': 'zhāng', '廢': 'fèi', '興': 'xīng', '奪': 'duó', '予': 'yǔ',
        '魚': 'yú', '脫': 'tuō', '淵': 'yuān', '化': 'huà', '欲': 'yù', '鎮': 'zhèn',
        '羞': 'xiū', '寧': 'níng', '侮': 'wǔ', '哉': 'zāi', '議': 'yì', '江': 'jiāng',
        '王': 'wáng', '海': 'hǎi', '谿': 'xī', '百': 'bǎi', '谷': 'gǔ', '言': 'yán',
        '爭': 'zhēng', '莫': 'mò', '慈': 'cí', '儉': 'jiǎn', '敢': 'gǎn', '先': 'xiān',
        '廣': 'guǎng', '死': 'sǐ', '活': 'huó', '柔': 'róu', '堅': 'jiān', '剛': 'gāng',
        '齒': 'chǐ', '舌': 'shé', '木': 'mù', '強': 'qiáng', '大': 'dà', '處': 'chǔ',
        '正': 'zhèng', '言': 'yán', '若': 'ruò', '反': 'fǎn', '怨': 'yuàn', '報': 'bào',
        '德': 'dé', '司': 'sī', '徹': 'chè', '契': 'qì', '責': 'zé', '小': 'xiǎo',
        '國': 'guó', '寡': 'guǎ', '民': 'mín', '甘': 'gān', '美': 'měi', '樂': 'lè',
        '俗': 'sú', '鄰': 'lín', '雞': 'jī', '犬': 'quǎn', '老': 'lǎo', '往': 'wǎng',
        '來': 'lái', '信': 'xìn', '美': 'měi', '善': 'shàn', '辯': 'biàn', '博': 'bó',
        '積': 'jī', '予': 'yǔ', '損': 'sǔn', '益': 'yì'
    }

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.renderer = ChuRenderer()
        self.glyph_mapper = GuodianGlyphMapper()
        self.output_dir = self.project_root / "output" / "chu_site"
        self.chapters_dir = self.project_root / "translations" / "chapters"

    def get_pinyin(self, char: str) -> str:
        """Get pinyin for a character."""
        return self.PINYIN.get(char, '')

    def find_chapter_file(self, chapter_num: int) -> Optional[Path]:
        """Find the chapter file for a given chapter number."""
        pattern = f"chapter{chapter_num:02d}_*.md"
        files = list(self.chapters_dir.glob(pattern))
        if not files:
            pattern = f"chapter{chapter_num}_*.md"
            files = list(self.chapters_dir.glob(pattern))
        return sorted(files)[-1] if files else None

    def extract_chapter_text(self, chapter_num: int) -> Optional[str]:
        """Extract Chinese text from a chapter file."""
        chapter_file = self.find_chapter_file(chapter_num)
        if not chapter_file:
            return None

        text = chapter_file.read_text()

        # Extract Chinese text blocks - look for lines that are mostly Chinese
        chinese_blocks = []
        for line in text.split('\n'):
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', line)
            # Lower threshold and check ratio of Chinese to total
            if len(chinese_chars) >= 5:
                clean = ''.join(c for c in line if '\u4e00' <= c <= '\u9fff' or c in '，。、；：')
                # Must be mostly Chinese (not just a line with some Chinese words)
                if clean and len(clean) >= len(chinese_chars):
                    chinese_blocks.append(clean)

        # Combine consecutive Chinese blocks (the full chapter text)
        return ''.join(chinese_blocks) if chinese_blocks else None

    def extract_translation_content(self, chapter_num: int) -> Dict[str, Any]:
        """Extract translation content from a chapter file."""
        chapter_file = self.find_chapter_file(chapter_num)
        if not chapter_file:
            return {}

        text = chapter_file.read_text()
        lines = text.split('\n')

        result = {
            'title': '',
            'subtitle': '',
            'chinese_lines': [],
            'line_translations': [],
            'full_content': text
        }

        # Extract title from first lines
        for line in lines[:10]:
            if line.startswith('# CHAPTER') or line.startswith('Chapter'):
                if 'Chapter' in line and ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        result['title'] = parts[1].strip()
            elif line.startswith('Or:'):
                result['subtitle'] = line[3:].strip()

        # Find Chinese text lines and their translations
        # Look for patterns like **Chinese** followed by translation
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check for bold Chinese text (like **反者道之動**)
            bold_match = re.match(r'\*\*([^*]+)\*\*', line)
            if bold_match:
                chinese = bold_match.group(1)
                if re.search(r'[\u4e00-\u9fff]', chinese):
                    # Look for translation in next few lines
                    translation = ''
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line.startswith('"') and next_line.endswith('"'):
                            translation = next_line.strip('"')
                            break
                        elif next_line.startswith('"'):
                            translation = next_line.strip('"').rstrip('"')
                            break
                    if translation:
                        result['line_translations'].append({
                            'chinese': chinese,
                            'translation': translation
                        })
            i += 1

        return result

    def get_all_chapters(self) -> Dict[int, str]:
        """Get Chinese text for all available chapters."""
        chapters = {}
        for ch_num in range(1, 82):
            text = self.extract_chapter_text(ch_num)
            if text:
                chapters[ch_num] = text
        return chapters

    def get_slip_glyphs_for_chapter(self, chapter_num: int, chapter_text: str = "") -> Dict[int, List[Dict]]:
        """Get glyphs organized by slip for a chapter, with punctuation."""
        from transcription_generator import TranscriptionGenerator
        generator = TranscriptionGenerator()

        result = {}
        slips = generator.get_chapter_slips(chapter_num)

        # Parse chapter text into sequence: [(char, punct_after), ...]
        text_sequence = []
        i = 0
        while i < len(chapter_text):
            char = chapter_text[i]
            if '\u4e00' <= char <= '\u9fff':
                # Chinese character - look ahead for punctuation
                punct = ""
                j = i + 1
                while j < len(chapter_text) and chapter_text[j] in '，。、；：':
                    punct += chapter_text[j]
                    j += 1
                text_sequence.append((char, punct))
            i += 1

        # Build all glyph positions across slips in order
        all_positions = []
        for slip_num in slips:
            slip_data = generator.generate_slip_transcription(slip_num)
            for pos in slip_data["positions"]:
                pos["slip"] = slip_num
                all_positions.append(pos)

        # Match glyphs to text sequence by received character
        text_idx = 0
        for pos in all_positions:
            guo_char = pos["guodian_char"]
            rec_char = pos.get("received_char") or guo_char

            # Skip particles (也) - they're in Guodian but not received
            if pos.get("is_particle"):
                pos["punct_after"] = ""
                continue

            # Find matching character in text sequence
            found = False
            search_start = text_idx
            for offset in range(min(5, len(text_sequence) - text_idx)):
                idx = text_idx + offset
                if idx < len(text_sequence) and text_sequence[idx][0] == rec_char:
                    pos["punct_after"] = text_sequence[idx][1]
                    text_idx = idx + 1
                    found = True
                    break

            if not found:
                pos["punct_after"] = ""

        # Re-organize by slip
        for slip_num in slips:
            result[slip_num] = [p for p in all_positions if p["slip"] == slip_num]

        return result

    def render_chapter_page(self, chapter_num: int, text: str,
                           prev_ch: Optional[int], next_ch: Optional[int]) -> str:
        """Render a single chapter page."""
        # Set chapter for glyph overrides
        self.renderer.set_chapter(chapter_num)
        info = self.renderer.render_text_info(text)
        coverage = self.renderer.get_coverage(text)
        is_guodian = chapter_num in self.GUODIAN_CHAPTERS
        translation = self.extract_translation_content(chapter_num)

        # Check for verified transcription
        has_verified = chapter_num in self.glyph_mapper.verified_transcriptions
        verified_data = self.glyph_mapper.verified_transcriptions.get(chapter_num, {})
        verification_status = verified_data.get("verification_status", "none")

        # Get slip-organized glyph data for bamboo strip view
        slip_glyphs = self.get_slip_glyphs_for_chapter(chapter_num, text) if is_guodian else {}

        # Navigation links
        prev_link = f'<a href="chapter{prev_ch:02d}.html">← Ch {prev_ch}</a>' if prev_ch else '<span class="disabled">← Prev</span>'
        next_link = f'<a href="chapter{next_ch:02d}.html">Ch {next_ch} →</a>' if next_ch else '<span class="disabled">Next →</span>'

        guodian_badge = '<span class="guodian-badge">GUODIAN 郭店</span>' if is_guodian else ''
        verified_badge = f'<span class="verified-badge">{len(verified_data.get("slips", []))} slips verified</span>' if has_verified else ''
        title_html = f'<h2 class="chapter-title">{translation.get("title", "")}</h2>' if translation.get("title") else ''
        subtitle_html = f'<p class="chapter-subtitle">{translation.get("subtitle", "")}</p>' if translation.get("subtitle") else ''
        compare_link = f'<a href="compare-chapter{chapter_num:02d}.html" class="compare-link">Compare View 比較</a>' if is_guodian else ''

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chapter {chapter_num} - Chu Script DDJ</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <a href="index.html">Index</a>
        <span class="nav-arrows">{prev_link} | {next_link}</span>
        <a href="atlas.html">Glyph Atlas</a>
    </nav>

    <header>
        <h1>Chapter {chapter_num} {guodian_badge} {verified_badge}</h1>
        {title_html}
        {subtitle_html}
        <div class="stats">
            <span class="coverage">{coverage['covered']}/{coverage['unique_chars']} characters ({coverage['covered_pct']:.0f}%)</span>
            <span class="laozi">Guodian Laozi: {coverage['laozi_covered']} ({coverage['laozi_pct']:.0f}%)</span>
        </div>
    </header>

    <div class="view-toggle">
        <button onclick="setView('horizontal')" id="btn-horiz">Horizontal 橫</button>
        <button onclick="setView('vertical')" id="btn-vert">Vertical 竪</button>
        <button onclick="setView('bamboo')" id="btn-bamboo" class="active">Bamboo Strips 竹簡</button>
        {compare_link}
    </div>

    <main class="text-display bamboo" id="text-display">
'''

        for item in info:
            if item["type"] == "punctuation":
                if item["char"] in '，。、；：':
                    html += f'<span class="punct">{item["char"]}</span>'
            elif item["has_glyph"]:
                laozi_class = "laozi" if item["guodian_laozi"] else ""
                glyph_path = item["glyph_path"]
                pinyin = self.get_pinyin(item['char'])
                # Make path relative
                if glyph_path:
                    rel_path = glyph_path  # Keep absolute for now, browser will handle
                html += f'''
                    <div class="char-box">
                        <img class="glyph-img {laozi_class}" src="{rel_path}"
                             alt="{item['char']}" title="{item['char']} ({item['glyph_count']} glyphs)">
                        <span class="pinyin">{pinyin}</span>
                        <span class="modern">{item['char']}</span>
                    </div>
'''
            else:
                pinyin = self.get_pinyin(item['char'])
                html += f'''
                    <div class="char-box missing">
                        <div class="missing-glyph">{item['char']}</div>
                        <span class="pinyin">{pinyin}</span>
                        <span class="modern">{item['char']}</span>
                    </div>
'''

        html += '''
    </main>
'''

        # Add bamboo strip view for Guodian chapters
        if slip_glyphs:
            html += '''
    <div class="bamboo-strips" id="bamboo-strips">
'''
            # Sort slips in reverse order (right to left reading)
            for slip_num in sorted(slip_glyphs.keys(), reverse=True):
                positions = slip_glyphs[slip_num]
                html += f'''
        <div class="bamboo-slip" data-slip="{slip_num}">
            <div class="slip-header">簡{slip_num}</div>
            <div class="slip-chars">
'''
                for pos in positions:
                    guo_char = pos["guodian_char"]
                    rec_char = pos.get("received_char") or ""
                    is_loan = pos.get("is_loan", False)
                    is_corrected = pos.get("is_corrected", False)
                    needs_review = pos.get("needs_review", False)
                    glyph_path = pos.get("path", "")

                    loan_class = "loan" if is_loan else ""
                    corrected_class = "corrected" if is_corrected else ""
                    review_class = "needs-review" if needs_review else ""

                    punct = pos.get("punct_after", "")

                    if glyph_path:
                        html += f'''
                <div class="slip-char {loan_class} {corrected_class} {review_class}"
                     data-pos="{pos['position']}" title="{guo_char} → {rec_char}">
                    <img src="{glyph_path}" alt="{guo_char}">
                    <span class="char-label">{guo_char}</span>
                </div>
'''
                    else:
                        # No glyph image, show character directly
                        html += f'''
                <div class="slip-char no-image {loan_class} {corrected_class} {review_class}"
                     data-pos="{pos['position']}" title="{guo_char}">
                    <span class="char-text">{guo_char}</span>
                    <span class="char-label">{guo_char}</span>
                </div>
'''
                    # Add punctuation after character if present
                    if punct:
                        html += f'''
                <div class="slip-punct">{punct}</div>
'''

                html += '''
            </div>
        </div>
'''
            html += '''
    </div>
'''

        # Add line-by-line translations if available
        if translation.get('line_translations'):
            html += '''
    <section class="translation-section">
        <h3>Line-by-Line Translation</h3>
'''
            for lt in translation['line_translations']:
                html += f'''
        <div class="translation-line">
            <p class="chinese-line">{lt['chinese']}</p>
            <p class="english-line">{lt['translation']}</p>
        </div>
'''
            html += '''
    </section>
'''

        # Add original text at bottom
        html += f'''
    <footer>
        <h3>Original Text</h3>
        <p class="original-text">{text}</p>
        <p class="missing-chars">Missing glyphs: {''.join(coverage['missing']) or 'None'}</p>
    </footer>

    <script>
    function setView(mode) {{
        const display = document.getElementById('text-display');
        const bamboo = document.getElementById('bamboo-strips');
        const btnHoriz = document.getElementById('btn-horiz');
        const btnVert = document.getElementById('btn-vert');
        const btnBamboo = document.getElementById('btn-bamboo');

        // Reset all
        display.classList.remove('vertical', 'bamboo');
        if (bamboo) bamboo.style.display = 'none';
        btnHoriz.classList.remove('active');
        btnVert.classList.remove('active');
        if (btnBamboo) btnBamboo.classList.remove('active');

        if (mode === 'bamboo' && bamboo) {{
            display.style.display = 'none';
            bamboo.style.display = 'flex';
            btnBamboo.classList.add('active');
        }} else if (mode === 'vertical') {{
            display.style.display = 'block';
            display.classList.add('vertical');
            btnVert.classList.add('active');
        }} else {{
            display.style.display = 'flex';
            btnHoriz.classList.add('active');
        }}
        localStorage.setItem('viewMode', mode);
    }}

    // Restore saved preference
    const savedMode = localStorage.getItem('viewMode') || 'bamboo';
    setView(savedMode);
    </script>
</body>
</html>
'''
        return html

    def render_index_page(self, chapters: Dict[int, str]) -> str:
        """Render the index/home page."""
        # Calculate stats
        total_chars = set()
        total_covered = set()
        total_laozi = set()

        chapter_stats = []
        for ch_num in sorted(chapters.keys()):
            text = chapters[ch_num]
            coverage = self.renderer.get_coverage(text)
            is_guodian = ch_num in self.GUODIAN_CHAPTERS

            chars = set(c for c in text if '\u4e00' <= c <= '\u9fff')
            total_chars.update(chars)

            for c in chars:
                if c in self.renderer.mappings:
                    total_covered.add(c)
                    if self.renderer.mappings[c].get('guodian_laozi'):
                        total_laozi.add(c)

            chapter_stats.append({
                'num': ch_num,
                'guodian': is_guodian,
                'chars': len(coverage['unique_chars']) if isinstance(coverage['unique_chars'], str) else coverage['unique_chars'],
                'covered_pct': coverage['covered_pct'],
                'laozi_pct': coverage['laozi_pct']
            })

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chu Script Dao De Jing - 楚簡道德經</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="site-header">
        <h1>楚簡道德經</h1>
        <h2>Chu Script Dao De Jing</h2>
        <p class="subtitle">The Guodian manuscripts rendered in original Chu bamboo slip script</p>
    </header>

    <section class="overall-stats">
        <h3>Coverage Statistics</h3>
        <div class="stat-grid">
            <div class="stat-box">
                <span class="stat-num">{len(chapters)}</span>
                <span class="stat-label">Chapters</span>
            </div>
            <div class="stat-box">
                <span class="stat-num">{len(total_chars)}</span>
                <span class="stat-label">Unique Characters</span>
            </div>
            <div class="stat-box">
                <span class="stat-num">{len(total_covered)}</span>
                <span class="stat-label">With Chu Glyphs</span>
            </div>
            <div class="stat-box highlight">
                <span class="stat-num">{len(total_laozi)}</span>
                <span class="stat-label">Guodian Laozi</span>
            </div>
        </div>
    </section>

    <nav class="chapter-nav">
        <a href="atlas.html" class="atlas-link">📜 Glyph Atlas</a>
    </nav>

    <section class="chapter-grid">
        <h3>Chapters</h3>
        <div class="chapters">
'''

        for stat in chapter_stats:
            guodian_class = "guodian" if stat['guodian'] else ""
            coverage_class = "high" if stat['laozi_pct'] > 80 else ("medium" if stat['laozi_pct'] > 50 else "low")

            html += f'''
            <a href="chapter{stat['num']:02d}.html" class="chapter-card {guodian_class} {coverage_class}">
                <span class="ch-num">{stat['num']}</span>
                <div class="ch-bar" style="width: {stat['laozi_pct']}%"></div>
                <span class="ch-pct">{stat['laozi_pct']:.0f}%</span>
            </a>
'''

        html += '''
        </div>
    </section>

    <section class="legend">
        <h3>Legend</h3>
        <div class="legend-items">
            <span><div class="legend-box guodian"></div> Confirmed in Guodian manuscripts</span>
            <span><div class="legend-box high"></div> >80% Guodian Laozi glyphs</span>
            <span><div class="legend-box medium"></div> 50-80% coverage</span>
            <span><div class="legend-box low"></div> <50% coverage</span>
        </div>
    </section>

    <footer class="site-footer">
        <p>Built from the <a href="https://huggingface.co/datasets/chen-yingfa/CHUBS">CHUBS Dataset</a></p>
        <p>Generated: ''' + datetime.now().strftime('%Y-%m-%d') + '''</p>
    </footer>
</body>
</html>
'''
        return html

    def render_glyph_atlas(self) -> str:
        """Render a glyph atlas page showing ALL variants per character with provenance."""
        import re

        # Characters with known visual ambiguity
        AMBIGUOUS_PAIRS = {
            '天': {'confusable_with': '而', 'note': 'Single bar may be merged 而'},
            '而': {'confusable_with': '天', 'note': 'Double bar often merges to single'},
        }

        # Collect all Laozi A variants per character
        char_variants = {}

        for char, data in self.renderer.mappings.items():
            if not data.get('guodian_laozi'):
                continue

            paths = data.get('paths', [])
            variants = []
            seen_files = set()  # Deduplicate by filename

            # Search each glyph folder for Laozi A images
            for folder_path in paths:
                folder = Path(folder_path)
                if not folder.exists():
                    continue

                for img in folder.glob("*.png"):
                    # Only Laozi A (老子甲)
                    if "老子甲" not in img.name:
                        continue

                    # Skip if we've already seen this file
                    if img.name in seen_files:
                        continue
                    seen_files.add(img.name)

                    # Parse slip and position: 郭店簡_01A-老子甲_37_01A-37-05.png
                    match = re.search(r'老子甲_(\d+)_01A-\d+-(\d+)', img.name)
                    if match:
                        slip = int(match.group(1))
                        pos = int(match.group(2))
                        variants.append({
                            'path': str(img),
                            'slip': slip,
                            'pos': pos,
                            'label': f"{slip}-{pos:02d}"
                        })

            if variants:
                # Sort by slip, then position
                variants.sort(key=lambda x: (x['slip'], x['pos']))
                sources = data.get('sources', {})
                laozi_count = sum(v for k, v in sources.items() if '老子' in k)
                char_variants[char] = {
                    'char': char,
                    'variants': variants,
                    'count': len(variants),
                    'laozi_total': laozi_count
                }

        # Sort characters by number of Laozi instances
        sorted_chars = sorted(char_variants.values(), key=lambda x: -x['laozi_total'])

        total_variants = sum(c['count'] for c in sorted_chars)

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Glyph Atlas - Chu Script DDJ</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <a href="index.html">← Back to Index</a>
    </nav>

    <header>
        <h1>Glyph Atlas 字形圖譜</h1>
        <p class="subtitle">{len(sorted_chars)} characters, {total_variants} glyph instances from Guodian Laozi A</p>
    </header>

    <main class="atlas-grouped">
'''

        for item in sorted_chars:
            char = item['char']
            ambig_info = AMBIGUOUS_PAIRS.get(char)
            ambig_badge = ''
            if ambig_info:
                ambig_badge = f'<span class="ambig-warning" title="{ambig_info["note"]}">⚠️ ≈ {ambig_info["confusable_with"]}</span>'

            html += f'''
        <div class="char-group{' has-ambiguity' if ambig_info else ''}">
            <div class="char-header">
                <span class="char-main">{char}</span>
                {ambig_badge}
                <span class="char-stats">{item['count']} variants</span>
            </div>
            <div class="variant-row">
'''
            for v in item['variants']:
                html += f'''
                <div class="variant-item">
                    <img src="{v['path']}" alt="{item['char']}" class="variant-glyph">
                    <span class="variant-label">{v['label']}</span>
                </div>
'''
            html += '''
            </div>
        </div>
'''

        html += '''
    </main>
</body>
</html>
'''
        return html

    def write_stylesheet(self) -> None:
        """Write the CSS stylesheet."""
        css = '''
/* Chu Script Site Styles */
:root {
    --bg-dark: #0d0d0d;
    --bg-card: #1a1a1a;
    --bg-hover: #252525;
    --gold: #ffd700;
    --gold-dim: #b8960f;
    --text: #e0e0e0;
    --text-dim: #888;
    --glyph-bg: #f5f5dc;
    --guodian: #2d4a2d;
    --high: #1a4a1a;
    --medium: #4a4a1a;
    --low: #4a1a1a;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Noto Sans SC', 'Helvetica Neue', sans-serif;
    background: var(--bg-dark);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background: var(--bg-card);
    border-bottom: 1px solid #333;
}

nav a {
    color: var(--gold);
    text-decoration: none;
}

nav a:hover { text-decoration: underline; }

.nav-arrows { color: var(--text-dim); }
.nav-arrows a { margin: 0 10px; }
.disabled { color: #444; }

header {
    text-align: center;
    padding: 40px 20px;
}

.site-header h1 {
    font-size: 3em;
    color: var(--gold);
    margin-bottom: 10px;
}

.site-header h2 {
    font-size: 1.5em;
    color: var(--text);
    font-weight: normal;
}

.subtitle {
    color: var(--text-dim);
    margin-top: 10px;
}

h1 { color: var(--gold); font-size: 2em; }

.guodian-badge {
    background: var(--guodian);
    color: var(--gold);
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 0.5em;
    vertical-align: middle;
    margin-left: 10px;
}

.verified-badge {
    background: #1a4a4a;
    color: #4fc3f7;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 0.5em;
    vertical-align: middle;
    margin-left: 10px;
}

.stats {
    margin-top: 15px;
    color: var(--text-dim);
}

.stats span {
    margin: 0 15px;
}

.laozi { color: var(--gold); }

/* Chapter grid on index */
.chapter-grid {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.chapters {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 10px;
    margin-top: 20px;
}

.chapter-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px 10px;
    background: var(--bg-card);
    border-radius: 8px;
    text-decoration: none;
    color: var(--text);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}

.chapter-card:hover {
    transform: scale(1.05);
    background: var(--bg-hover);
}

.chapter-card.guodian {
    border: 2px solid var(--gold-dim);
}

.ch-num {
    font-size: 1.5em;
    font-weight: bold;
    z-index: 1;
}

.ch-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 4px;
    background: var(--gold);
}

.ch-pct {
    font-size: 0.8em;
    color: var(--text-dim);
    z-index: 1;
}

.chapter-card.high .ch-bar { background: #4caf50; }
.chapter-card.medium .ch-bar { background: #ff9800; }
.chapter-card.low .ch-bar { background: #f44336; }

/* Stats section */
.overall-stats {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-top: 15px;
}

.stat-box {
    background: var(--bg-card);
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}

.stat-box.highlight {
    border: 2px solid var(--gold);
}

.stat-num {
    display: block;
    font-size: 2em;
    font-weight: bold;
    color: var(--gold);
}

.stat-label {
    color: var(--text-dim);
    font-size: 0.9em;
}

/* Text display - horizontal (default) */
.text-display {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 30px;
    max-width: 1200px;
    margin: 0 auto;
    justify-content: center;
}

/* Text display - vertical (bamboo strip style) */
.text-display.vertical {
    writing-mode: vertical-rl;
    display: block;
    overflow-x: auto;
    padding: 20px;
    white-space: nowrap;
}

.text-display.vertical .char-box {
    display: inline-block;
    writing-mode: horizontal-tb;
    margin: 4px 8px;
}

.text-display.vertical .glyph-img {
    width: 56px;
    height: 56px;
}

.text-display.vertical .punct {
    writing-mode: horizontal-tb;
    display: inline-block;
    font-size: 24px;
    margin: 4px;
}

/* View toggle */
.view-toggle {
    text-align: center;
    margin: 20px 0;
}

.view-toggle button {
    background: var(--bg-card);
    color: var(--gold);
    border: 1px solid var(--gold-dim);
    padding: 8px 16px;
    margin: 0 5px;
    border-radius: 4px;
    cursor: pointer;
}

.view-toggle button:hover {
    background: var(--bg-hover);
}

.view-toggle button.active {
    background: var(--gold-dim);
    color: var(--bg-dark);
}

.view-toggle .compare-link {
    background: #1a4a4a;
    color: #4fc3f7;
    border: 1px solid #4fc3f7;
    padding: 8px 16px;
    margin-left: 15px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 0.9em;
}

.view-toggle .compare-link:hover {
    background: #2a5a5a;
}

.char-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
}

.glyph-img {
    width: 64px;
    height: 64px;
    object-fit: contain;
    background: var(--glyph-bg);
    border-radius: 4px;
}

.glyph-img.laozi {
    border: 3px solid var(--gold);
}

.missing-glyph {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #222;
    border: 2px dashed #444;
    border-radius: 4px;
    font-size: 32px;
    color: #666;
}

.pinyin {
    font-size: 11px;
    color: var(--gold-dim);
    margin-top: 2px;
    font-style: italic;
}

.modern {
    font-size: 14px;
    color: var(--text-dim);
    margin-top: 2px;
}

.chapter-title {
    color: var(--text);
    font-size: 1.3em;
    font-weight: normal;
    margin-top: 10px;
}

.chapter-subtitle {
    color: var(--text-dim);
    font-style: italic;
    margin-top: 5px;
}

/* Translation section */
.translation-section {
    max-width: 800px;
    margin: 30px auto;
    padding: 20px 30px;
    background: var(--bg-card);
    border-radius: 8px;
}

.translation-section h3 {
    color: var(--gold);
    margin-bottom: 20px;
}

.translation-line {
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #333;
}

.translation-line:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.chinese-line {
    font-size: 1.3em;
    color: var(--text);
    margin-bottom: 8px;
}

.english-line {
    color: var(--text-dim);
    font-style: italic;
    line-height: 1.6;
}

.punct {
    font-size: 32px;
    color: var(--text-dim);
    align-self: center;
    margin: 0 5px;
}

/* Footer */
footer {
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px 30px;
    background: var(--bg-card);
    border-radius: 8px;
}

footer h3 {
    color: var(--gold);
    margin-bottom: 10px;
}

.original-text {
    font-size: 1.2em;
    line-height: 2;
    color: var(--text);
}

.missing-chars {
    color: var(--text-dim);
    margin-top: 10px;
}

.site-footer {
    text-align: center;
    padding: 30px;
    color: var(--text-dim);
}

.site-footer a {
    color: var(--gold);
}

/* Legend */
.legend {
    max-width: 800px;
    margin: 30px auto;
    padding: 20px;
}

.legend h3 {
    color: var(--gold);
    margin-bottom: 15px;
}

.legend-items {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.legend-items span {
    display: flex;
    align-items: center;
    gap: 8px;
}

.legend-box {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}

.legend-box.guodian { border: 2px solid var(--gold-dim); background: var(--bg-card); }
.legend-box.high { background: #4caf50; }
.legend-box.medium { background: #ff9800; }
.legend-box.low { background: #f44336; }

/* Atlas - Grouped variants with provenance */
.atlas-grouped {
    padding: 20px;
}

.char-group {
    margin-bottom: 24px;
    background: var(--bg-card);
    border-radius: 8px;
    padding: 12px 16px;
}

.char-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 10px;
    border-bottom: 1px solid #333;
    padding-bottom: 8px;
}

.char-main {
    font-size: 2em;
    color: var(--gold);
}

.char-stats {
    font-size: 0.9em;
    color: var(--text-dim);
}

/* Ambiguity warnings */
.char-group.has-ambiguity {
    border: 1px solid #f44336;
}

.ambig-warning {
    background: rgba(244, 67, 54, 0.2);
    color: #f44336;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    cursor: help;
}

.variant-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: flex-start;
}

.variant-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 72px;
}

.variant-glyph {
    width: 64px;
    height: 64px;
    object-fit: contain;
    background: var(--glyph-bg);
    border-radius: 4px;
}

.variant-label {
    font-size: 0.7em;
    color: var(--text-dim);
    margin-top: 4px;
    font-family: monospace;
}

.atlas-link {
    display: inline-block;
    background: var(--bg-card);
    padding: 10px 20px;
    border-radius: 8px;
    color: var(--gold);
    text-decoration: none;
    margin: 20px auto;
}

.chapter-nav {
    text-align: center;
}

/* Bamboo Strip Styles */
.bamboo-strips {
    display: flex;
    flex-direction: row-reverse;  /* Right to left reading */
    gap: 8px;
    padding: 30px;
    overflow-x: auto;
    justify-content: flex-start;
    min-height: 500px;
}

.bamboo-slip {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(to right, #8B7355 0%, #D4B896 15%, #D4B896 85%, #8B7355 100%);
    border-radius: 8px;
    padding: 10px 8px;
    min-width: 72px;
    box-shadow: 2px 4px 8px rgba(0,0,0,0.4);
    position: relative;
}

.bamboo-slip::before,
.bamboo-slip::after {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 4px;
    background: #5C4033;
    border-radius: 2px;
}

.bamboo-slip::before { top: 20px; }
.bamboo-slip::after { bottom: 20px; }

.slip-header {
    font-size: 0.7em;
    color: #5C4033;
    margin-bottom: 8px;
    padding-bottom: 5px;
    writing-mode: horizontal-tb;
    font-weight: bold;
}

.slip-chars {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 30px 0;
}

.slip-char {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4px;
    cursor: pointer;
    transition: background 0.2s;
    border-radius: 4px;
}

.slip-char:hover {
    background: rgba(0,0,0,0.1);
}

.slip-char img {
    width: 48px;
    height: 48px;
    object-fit: contain;
    background: var(--glyph-bg);
    border-radius: 4px;
}

.slip-char .char-text {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: #333;
    background: var(--glyph-bg);
    border-radius: 4px;
}

.slip-char .char-label {
    font-size: 12px;
    color: #5C4033;
    margin-top: 2px;
}

.slip-punct {
    font-size: 24px;
    color: #5C4033;
    padding: 4px 0;
    text-align: center;
}

/* Phonetic loan indicator */
.slip-char.loan {
    position: relative;
}

.slip-char.loan::after {
    content: '→';
    position: absolute;
    top: 0;
    right: -2px;
    font-size: 10px;
    color: var(--gold);
    background: var(--bg-dark);
    border-radius: 50%;
    width: 14px;
    height: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Corrected glyph indicator */
.slip-char.corrected img,
.slip-char.corrected .char-text {
    border: 2px solid #4caf50;
}

/* Needs review indicator */
.slip-char.needs-review img,
.slip-char.needs-review .char-text {
    border: 2px dashed #ff9800;
}

/* Hide bamboo strips by default (shown via JS) */
.bamboo-strips {
    display: none;
}
'''

        css_path = self.output_dir / "style.css"
        with open(css_path, 'w') as f:
            f.write(css)

    def load_strip_photo_mapping(self) -> Dict:
        """Load strip photo to slip mapping."""
        mapping_file = self.project_root / "data" / "ddj" / "strip_photo_mapping.json"
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"photos": {}, "slip_to_photos": {}}

    def get_photos_for_slip(self, slip_num: int) -> List[Dict]:
        """Get all photos containing a specific slip."""
        mapping = self.load_strip_photo_mapping()
        photos = []
        for img_name, data in mapping.get("photos", {}).items():
            if slip_num in data.get("slips", []):
                photos.append({
                    "filename": img_name,
                    "path": str(self.project_root / "data" / "ddj" / "guodian_strips_full" / f"{img_name}.jpeg"),
                    "type": data.get("type", "unknown"),
                    "notes": data.get("notes", "")
                })
        return photos

    def render_comparison_page(self, chapter_num: int) -> str:
        """Render a comparison page showing full strip photos + extracted glyphs."""
        from transcription_generator import TranscriptionGenerator

        generator = TranscriptionGenerator()
        slips = generator.get_chapter_slips(chapter_num)

        # Collect all photos and glyphs for this chapter
        chapter_photos = set()
        slip_data = {}

        for slip_num in slips:
            # Get photos for this slip
            photos = self.get_photos_for_slip(slip_num)
            for p in photos:
                chapter_photos.add((p["filename"], p["path"], p["type"]))

            # Get glyph data
            transcription = generator.generate_slip_transcription(slip_num)
            slip_data[slip_num] = transcription

        chapter_photos = sorted(chapter_photos)

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Compare: Chapter {chapter_num} - Guodian Strip Verification</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .compare-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        .photos-section {{
            margin-bottom: 30px;
        }}
        .photos-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }}
        .photo-card {{
            background: var(--bg-card);
            border-radius: 8px;
            overflow: hidden;
            max-width: 400px;
        }}
        .photo-card img {{
            width: 100%;
            height: auto;
            cursor: pointer;
        }}
        .photo-card .photo-info {{
            padding: 10px;
            font-size: 0.9em;
            color: var(--text-dim);
        }}
        .slips-section {{
            margin-top: 30px;
        }}
        .slip-row {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .slip-header {{
            color: var(--gold);
            font-size: 1.2em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }}
        .glyphs-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .glyph-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 8px;
            background: var(--bg-hover);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}
        .glyph-item:hover {{
            background: #333;
            transform: scale(1.05);
        }}
        .glyph-item img {{
            width: 56px;
            height: 56px;
            object-fit: contain;
            background: var(--glyph-bg);
            border-radius: 4px;
        }}
        .glyph-item .pos-num {{
            font-size: 0.7em;
            color: var(--text-dim);
            margin-top: 4px;
        }}
        .glyph-item .char-info {{
            font-size: 0.9em;
            margin-top: 2px;
        }}
        .glyph-item.loan {{
            border: 2px solid var(--gold);
        }}
        .glyph-item.needs-review {{
            border: 2px dashed #ff9800;
        }}
        .glyph-item.corrected {{
            border: 2px solid #4caf50;
        }}

        /* Modal for corrections */
        .correction-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}
        .correction-modal.active {{
            display: flex;
        }}
        .modal-content {{
            background: var(--bg-card);
            padding: 30px;
            border-radius: 12px;
            max-width: 600px;
            width: 90%;
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .modal-header h3 {{
            color: var(--gold);
        }}
        .close-btn {{
            background: none;
            border: none;
            color: var(--text);
            font-size: 24px;
            cursor: pointer;
        }}
        .modal-glyph {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .modal-glyph img {{
            width: 120px;
            height: 120px;
            object-fit: contain;
            background: var(--glyph-bg);
            border-radius: 8px;
        }}
        .modal-info {{
            margin-bottom: 20px;
        }}
        .modal-info p {{
            margin: 8px 0;
        }}
        .correction-form {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        .correction-form input {{
            padding: 10px;
            font-size: 1.2em;
            border: 2px solid var(--gold);
            border-radius: 6px;
            background: var(--bg-dark);
            color: var(--text);
            text-align: center;
        }}
        .correction-form button {{
            padding: 12px;
            background: var(--gold);
            color: var(--bg-dark);
            border: none;
            border-radius: 6px;
            font-size: 1em;
            cursor: pointer;
        }}
        .correction-form button:hover {{
            background: var(--gold-dim);
        }}

        /* Photo modal */
        .photo-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 999;
            cursor: pointer;
        }}
        .photo-modal.active {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .photo-modal img {{
            max-width: 95%;
            max-height: 95%;
        }}
    </style>
</head>
<body>
    <nav>
        <a href="chapter{chapter_num:02d}.html">← Back to Chapter {chapter_num}</a>
        <span>Strip Comparison View</span>
        <a href="index.html">Index</a>
    </nav>

    <div class="compare-container">
        <header>
            <h1>Chapter {chapter_num} - Strip Comparison</h1>
            <p class="subtitle">Compare full strip photos with extracted glyphs to verify mappings</p>
        </header>

        <section class="photos-section">
            <h2>Full Strip Photos</h2>
            <div class="photos-grid">
'''

        for filename, path, photo_type in chapter_photos:
            type_badge = "Color" if photo_type == "color" else "Annotated"
            html += f'''
                <div class="photo-card">
                    <img src="{path}" alt="{filename}" onclick="openPhotoModal(this.src)">
                    <div class="photo-info">{filename} ({type_badge})</div>
                </div>
'''

        html += '''
            </div>
        </section>

        <section class="slips-section">
            <h2>Extracted Glyphs by Slip</h2>
'''

        for slip_num in sorted(slip_data.keys()):
            data = slip_data[slip_num]
            html += f'''
            <div class="slip-row">
                <div class="slip-header">
                    Slip {slip_num} - {len(data["positions"])} glyphs
                    <span style="color: var(--text-dim); font-size: 0.8em; margin-left: 15px;">
                        Loans: {data["loan_count"]} | Review: {len(data["review_needed"])}
                    </span>
                </div>
                <div class="glyphs-row">
'''

            for pos in data["positions"]:
                guo_char = pos["guodian_char"]
                rec_char = pos.get("received_char") or ""
                is_loan = pos.get("is_loan", False)
                needs_review = pos.get("needs_review", False)
                is_corrected = pos.get("is_corrected", False)
                glyph_path = pos.get("path", "")

                classes = []
                if is_loan:
                    classes.append("loan")
                if needs_review:
                    classes.append("needs-review")
                if is_corrected:
                    classes.append("corrected")

                class_str = " ".join(classes)

                html += f'''
                    <div class="glyph-item {class_str}"
                         onclick="openCorrectionModal({slip_num}, {pos['position']}, '{guo_char}', '{rec_char}', '{glyph_path}')"
                         title="Click to correct">
                        <img src="{glyph_path}" alt="{guo_char}">
                        <span class="pos-num">#{pos['position']}</span>
                        <span class="char-info">{guo_char} → {rec_char}</span>
                    </div>
'''

            html += '''
                </div>
            </div>
'''

        html += f'''
        </section>
    </div>

    <!-- Photo Modal -->
    <div class="photo-modal" id="photoModal" onclick="closePhotoModal()">
        <img src="" id="photoModalImg">
    </div>

    <!-- Correction Modal -->
    <div class="correction-modal" id="correctionModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Correct Glyph Mapping</h3>
                <button class="close-btn" onclick="closeCorrectionModal()">&times;</button>
            </div>
            <div class="modal-glyph">
                <img src="" id="modalGlyphImg">
            </div>
            <div class="modal-info">
                <p><strong>Slip:</strong> <span id="modalSlip"></span>, <strong>Position:</strong> <span id="modalPos"></span></p>
                <p><strong>Current mapping:</strong> <span id="modalCurrentMapping"></span></p>
            </div>
            <div class="correction-form">
                <label>Correct Guodian character:</label>
                <input type="text" id="correctedChar" maxlength="2" placeholder="Enter character">
                <label>Received form (optional):</label>
                <input type="text" id="receivedChar" maxlength="2" placeholder="Standard form">
                <label>Note:</label>
                <input type="text" id="correctionNote" placeholder="Optional note">
                <button onclick="saveCorrection()">Save Correction</button>
            </div>
        </div>
    </div>

    <script>
        let currentSlip = null;
        let currentPos = null;

        function openPhotoModal(src) {{
            document.getElementById('photoModalImg').src = src;
            document.getElementById('photoModal').classList.add('active');
        }}

        function closePhotoModal() {{
            document.getElementById('photoModal').classList.remove('active');
        }}

        function openCorrectionModal(slip, pos, guoChar, recChar, imgPath) {{
            currentSlip = slip;
            currentPos = pos;
            document.getElementById('modalGlyphImg').src = imgPath;
            document.getElementById('modalSlip').textContent = slip;
            document.getElementById('modalPos').textContent = pos;
            document.getElementById('modalCurrentMapping').textContent = guoChar + ' → ' + (recChar || '(particle)');
            document.getElementById('correctedChar').value = guoChar;
            document.getElementById('receivedChar').value = recChar || '';
            document.getElementById('correctionNote').value = '';
            document.getElementById('correctionModal').classList.add('active');
        }}

        function closeCorrectionModal() {{
            document.getElementById('correctionModal').classList.remove('active');
        }}

        function saveCorrection() {{
            const guoChar = document.getElementById('correctedChar').value;
            const recChar = document.getElementById('receivedChar').value;
            const note = document.getElementById('correctionNote').value;

            if (!guoChar) {{
                alert('Please enter the correct Guodian character');
                return;
            }}

            // Build CLI command
            const recArg = recChar ? recChar : '""';
            const noteArg = note ? '"' + note + '"' : '""';
            const cmd = `python3 corrections_manager.py add ${{currentSlip}} ${{currentPos}} ${{guoChar}} ${{recArg}} ${{noteArg}}`;

            // Copy to clipboard
            navigator.clipboard.writeText(cmd).then(() => {{
                alert('Command copied to clipboard!\\n\\n' + cmd + '\\n\\nPaste in terminal to save correction.');
            }}).catch(() => {{
                // Fallback if clipboard fails
                prompt('Copy this command:', cmd);
            }});

            closeCorrectionModal();
        }}

        // Close modals on Escape key
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                closePhotoModal();
                closeCorrectionModal();
            }}
        }});
    </script>
</body>
</html>
'''
        return html

    def build_site(self) -> Dict[str, Any]:
        """Build the complete site."""
        print("Building Chu Script site...")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Get all chapters
        chapters = self.get_all_chapters()
        print(f"Found {len(chapters)} chapters")

        # Write stylesheet
        self.write_stylesheet()
        print("Wrote stylesheet")

        # Render index
        index_html = self.render_index_page(chapters)
        (self.output_dir / "index.html").write_text(index_html)
        print("Rendered index page")

        # Render each chapter
        sorted_chapters = sorted(chapters.keys())
        for i, ch_num in enumerate(sorted_chapters):
            prev_ch = sorted_chapters[i-1] if i > 0 else None
            next_ch = sorted_chapters[i+1] if i < len(sorted_chapters)-1 else None

            html = self.render_chapter_page(ch_num, chapters[ch_num], prev_ch, next_ch)
            (self.output_dir / f"chapter{ch_num:02d}.html").write_text(html)
        print(f"Rendered {len(chapters)} chapter pages")

        # Render glyph atlas
        atlas_html = self.render_glyph_atlas()
        (self.output_dir / "atlas.html").write_text(atlas_html)
        print("Rendered glyph atlas")

        # Render comparison pages for Guodian chapters
        compare_count = 0
        for ch_num in self.GUODIAN_CHAPTERS:
            if ch_num in chapters:
                try:
                    compare_html = self.render_comparison_page(ch_num)
                    (self.output_dir / f"compare-chapter{ch_num:02d}.html").write_text(compare_html)
                    compare_count += 1
                except Exception as e:
                    print(f"  Warning: Could not render comparison page for chapter {ch_num}: {e}")
        print(f"Rendered {compare_count} comparison pages")

        return {
            "output_dir": str(self.output_dir),
            "chapters": len(chapters),
            "compare_pages": compare_count,
            "index": str(self.output_dir / "index.html")
        }


def main():
    builder = ChuSiteBuilder()
    result = builder.build_site()
    print(f"\nSite built at: {result['output_dir']}")
    print(f"Open: {result['index']}")


if __name__ == "__main__":
    main()
