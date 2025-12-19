"""
Quick test to verify Chinese character rendering in matplotlib
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Configure Chinese fonts
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'Heiti SC', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# Create a test figure with various Chinese radicals
fig, ax = plt.subplots(figsize=(10, 8))

# Test radicals from our analysis
radicals = [
    '辶 (walking)', '水 (water)', '氵 (water radical)',
    '心 (heart)', '忄 (heart radical)', '口 (mouth)',
    '人 (person)', '亻 (person radical)', '手 (hand)',
    '扌 (hand radical)', '火 (fire)', '大 (great)',
    '糸 (thread)', '巾 (cloth)', '宀 (roof)',
    '尸 (corpse)', '門 (gate)', '足 (foot)'
]

# Plot radicals as text
y_pos = 0.95
for radical in radicals:
    ax.text(0.1, y_pos, radical, fontsize=14, transform=ax.transAxes)
    y_pos -= 0.05

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Chinese Radical Font Test - 中文字体测试', fontsize=16, pad=20)

# Show which font is being used
current_font = matplotlib.rcParams['font.sans-serif'][0]
ax.text(0.5, 0.02, f'Using font: {current_font}',
        fontsize=10, ha='center', transform=ax.transAxes,
        style='italic', color='gray')

plt.tight_layout()
plt.savefig('output/font_test.png', dpi=150, bbox_inches='tight')
print(f"Font test saved to output/font_test.png")
print(f"Active font: {current_font}")
print("\nAvailable Chinese fonts on system:")
chinese_fonts = [f.name for f in fm.fontManager.ttflist
                 if any(x in f.name.lower() for x in ['chinese', 'heiti', 'pingfang', 'songti', 'arial unicode', 'simhei'])]
for font in sorted(set(chinese_fonts)):
    print(f"  - {font}")

plt.close()
print("\n✓ Test complete! Check output/font_test.png to verify Chinese characters are rendering.")
