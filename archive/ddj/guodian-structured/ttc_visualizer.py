#!/usr/bin/env python3
"""
Tao Te Ching Operator Visualizer
Transforms CSV of characters into color-coded HTML grid
"""

import csv
import sys
from pathlib import Path

# ===== COLOR DEFINITIONS =====

COLORS = {
    # Tier 1: Coordinate Axes
    '道': '#B8860B',  # Dark Gold - The Pattern
    '常': '#0047AB',  # Deep Blue - Implicit
    '可': '#87CEEB',  # Light Blue - Explicit
    '無': '#DC143C',  # Deep Red - Nothing
    '有': '#FF69B4',  # Pink - Something
    
    # Tier 2: Origin/Paradox
    '玄': '#FFD700',  # Bright Gold - Paradox
    '一': '#FFD700',  # Bright Gold - Unity
    '沖': '#FFD700',  # Bright Gold - Hollow center
    '中': '#FFD700',  # Bright Gold - Center
    
    # Tier 3: Complementary Poles
    '天': '#9370DB',  # Purple - Heaven/Yang
    '陽': '#9370DB',  # Purple - Yang
    '雄': '#9370DB',  # Purple - Male principle
    '剛': '#9370DB',  # Purple - Rigid
    '上': '#9370DB',  # Purple - Above
    '前': '#9370DB',  # Purple - Front
    
    '地': '#228B22',  # Forest Green - Earth/Yin
    '陰': '#228B22',  # Forest Green - Yin
    '谷': '#228B22',  # Forest Green - Valley
    '牝': '#228B22',  # Forest Green - Female principle
    '柔': '#228B22',  # Forest Green - Soft/yielding
    '雌': '#228B22',  # Forest Green - Female
    '下': '#228B22',  # Forest Green - Below
    '後': '#228B22',  # Forest Green - Behind
    
    # Tier 4: Perception Operators
    '觀': '#00CED1',  # Cyan - Observe
    '欲': '#00CED1',  # Cyan - Orient
    '見': '#00CED1',  # Cyan - See
    '視': '#00CED1',  # Cyan - Look
    '知': '#00CED1',  # Cyan - Know
    
    '妙': '#FF00FF',  # Magenta - Patterns
    '徼': '#8B008B',  # Dark Magenta - Boundaries
    '明': '#FF00FF',  # Magenta - Clarity
    
    # Tier 5: Dynamics Operators
    '反': '#FF8C00',  # Bright Orange - Return/Oscillation
    '生': '#FFA500',  # Orange - Generate
    '動': '#FF8C00',  # Bright Orange - Movement
    '化': '#FFA500',  # Orange - Transform
    '逝': '#FFA500',  # Orange - Extend
    '行': '#FFA500',  # Orange - Travel
    '復': '#FF8C00',  # Bright Orange - Return to origin
    
    '靜': '#8B4513',  # Brown - Stillness
    '久': '#8B4513',  # Brown - Enduring
    '守': '#8B4513',  # Brown - Guard
    '存': '#8B4513',  # Brown - Preserve
    '長': '#8B4513',  # Brown - Long-lasting
    
    # Tier 6: Function/Quality Operators
    '用': '#808080',  # Gray - Function
    '為': '#A9A9A9',  # Light Gray - Act
    '治': '#A9A9A9',  # Light Gray - Govern
    '弱': '#008080',  # Teal - Soft/Indefinite
    '強': '#696969',  # Dim Gray - Rigid
    '大': '#A9A9A9',  # Light Gray - Vast
    '小': '#A9A9A9',  # Light Gray - Small
    '名': '#9370DB',  # Purple - Name/Distinction
    '異': '#9370DB',  # Purple - Different
    '非': '#9370DB',  # Purple - Divergence
    '門': '#A9A9A9',  # Light Gray - Gate
    '德': '#A9A9A9',  # Light Gray - Virtue
}

# ===== LEGEND DEFINITIONS =====

LEGEND = [
    ('■ Dark Gold', '#B8860B', '道 - The Pattern'),
    ('■ Deep Blue', '#0047AB', '常 - Implicit/Frame-independent'),
    ('■ Light Blue', '#87CEEB', '可 - Explicit/Frame-dependent'),
    ('■ Deep Red', '#DC143C', '無 - Nothing/Void/Absence'),
    ('■ Pink', '#FF69B4', '有 - Something/Form/Presence'),
    ('■ Bright Gold', '#FFD700', '玄,一,沖,中 - Origin/Paradox/Center'),
    ('■ Purple', '#9370DB', '天,陽,名 - Yang/Active/Distinction'),
    ('■ Forest Green', '#228B22', '地,陰,谷 - Yin/Receptive/Valley'),
    ('■ Cyan', '#00CED1', '觀,欲,知 - Observation Methods'),
    ('■ Magenta', '#FF00FF', '妙,徼,明 - Observed Qualities'),
    ('■ Bright Orange', '#FF8C00', '反,動,復 - Movement/Oscillation'),
    ('■ Orange', '#FFA500', '生,化,逝 - Generation/Transform'),
    ('■ Brown', '#8B4513', '靜,久,守 - Stillness/Persistence'),
    ('■ Gray/Teal', '#808080', '用,為,治,弱 - Functions/Qualities'),
    ('□ White', '#FFFFFF', 'Content characters'),
]

# ===== HTML GENERATION =====

def get_char_color(char):
    """Return the background color for a character."""
    return COLORS.get(char, '#FFFFFF')

def generate_html(csv_data, output_file):
    """Generate HTML visualization from CSV data."""
    
    # Start HTML
    html = ['<!DOCTYPE html>']
    html.append('<html lang="zh">')
    html.append('<head>')
    html.append('<meta charset="UTF-8">')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append('<title>Tao Te Ching - Operator Visualization</title>')
    html.append('<style>')
    
    # CSS Styles
    html.append('''
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans CJK SC", sans-serif;
            background: #fafafa;
            padding: 20px;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
            color: #333;
        }
        
        .subtitle {
            text-align: center;
            margin-bottom: 30px;
            color: #666;
            font-size: 14px;
        }
        
        .legend {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 5px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            font-size: 13px;
            color: #333;
        }
        
        .legend-box {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            border: 1px solid #999;
            flex-shrink: 0;
        }
        
        .grid-container {
            overflow-x: auto;
        }
        
        table {
            border-collapse: collapse;
            margin: 0 auto;
            background: white;
        }
        
        th {
            background: #333;
            color: white;
            padding: 12px 8px;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid #222;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        td {
            width: 40px;
            height: 40px;
            text-align: center;
            vertical-align: middle;
            border: 1px solid #ddd;
            font-size: 18px;
            font-weight: 500;
            color: #000;
        }
        
        td.empty {
            background: #f9f9f9;
        }
        
        tr:hover td {
            border-color: #999;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
                padding: 10px;
            }
            th {
                background: #333 !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            td {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
    ''')
    
    html.append('</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<div class="container">')
    
    # Title
    html.append('<h1>道德經 Operator Visualization</h1>')
    html.append('<p class="subtitle">Structural Notation of the Tao Te Ching</p>')
    
    # Legend
    html.append('<div class="legend">')
    for label, color, desc in LEGEND:
        html.append(f'<div class="legend-item">')
        html.append(f'<div class="legend-box" style="background-color: {color};"></div>')
        html.append(f'<span><strong>{label}</strong> — {desc}</span>')
        html.append('</div>')
    html.append('</div>')
    
    # Table
    html.append('<div class="grid-container">')
    html.append('<table>')
    
    # Get headers (chapter numbers)
    headers = csv_data[0]
    
    # Header row
    html.append('<tr>')
    for header in headers:
        html.append(f'<th>{header}</th>')
    html.append('</tr>')
    
    # Data rows
    # Find the maximum number of rows across all columns
    max_rows = max(len(col) for col in zip(*csv_data[1:]))
    
    # Transpose the data for row-by-row processing
    for row_idx in range(max_rows):
        html.append('<tr>')
        for col_idx, header in enumerate(headers):
            # Get the character at this position (if it exists)
            col_data = [row[col_idx] for row in csv_data[1:] if col_idx < len(row)]
            
            if row_idx < len(col_data):
                char = col_data[row_idx].strip()
                if char:
                    color = get_char_color(char)
                    html.append(f'<td style="background-color: {color};">{char}</td>')
                else:
                    html.append('<td class="empty"></td>')
            else:
                html.append('<td class="empty"></td>')
        html.append('</tr>')
    
    html.append('</table>')
    html.append('</div>')
    
    html.append('</div>')
    html.append('</body>')
    html.append('</html>')
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python ttc_visualizer.py <input.csv> [output.html]")
        print("\nExample: python ttc_visualizer.py chapters.csv visualization.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'ttc_visualization.html'
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    print(f"Reading CSV from: {input_file}")
    
    # Read CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        csv_data = list(reader)
    
    if not csv_data:
        print("Error: CSV file is empty.")
        sys.exit(1)
    
    print(f"Found {len(csv_data[0])} chapters")
    print(f"Generating HTML visualization...")
    
    # Generate HTML
    generate_html(csv_data, output_file)
    
    print(f"✓ Visualization saved to: {output_file}")
    print(f"\nOpen the file in any web browser to view.")
    print(f"The file is self-contained and can be shared.")

if __name__ == '__main__':
    main()