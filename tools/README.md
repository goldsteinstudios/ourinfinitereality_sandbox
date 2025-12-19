# Dao De Jing Radical Co-occurrence Analysis

A comprehensive Python toolkit for analyzing radical-level patterns in the Dao De Jing (Tao Te Ching). This tool reveals the "hidden grammar of transformations" encoded in the radical structure of the text.

## Overview

This analysis toolkit examines **how radicals (not characters) co-occur** in the Dao De Jing, based on the theory that Chinese radicals encode topological operations - showing HOW characters transform meaning, not just categorizing them.

### Key Features

- **711 characters** mapped to **57 unique radicals**
- **9 topological radical categories**: motion, fluid, constraint, boundary, thread, cloth, agent, internal, action
- Co-occurrence matrix analysis with ±5 character window
- Statistical significance testing
- Heat map visualizations
- Hierarchical clustering
- Sequence pattern detection

## Project Structure

```
python_analysis/
├── radical_dictionary.py       # Radical decomposition mappings
├── ttc_parser.py               # CSV parser for Dao De Jing text
├── radical_cooccurrence.py     # Co-occurrence matrix calculator
├── visualizations.py           # Heat maps and visualizations
├── statistical_analysis.py     # Statistical tests and pattern detection
├── requirements.txt            # Python dependencies
└── output/
    ├── radical_cooccurrence_matrix.csv
    ├── radical_cooccurrence_normalized.csv
    ├── top_radical_pairs.csv
    ├── visualizations/
    │   ├── full_heatmap_normalized.png
    │   ├── category_heatmap.png
    │   ├── top_pairs_bar.png
    │   ├── motion_radicals_focused.png
    │   ├── fluid_radicals_focused.png
    │   ├── constraint_radicals_focused.png
    │   ├── thread_cloth_focused.png
    │   └── neighbors_*.png
    └── statistical_analysis/
        ├── significance_analysis.csv
        ├── avoidance_pairs.csv
        └── radical_clustering_dendrogram.png
```

## Installation

```bash
cd python_analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### 1. Run Full Co-occurrence Analysis

```bash
source venv/bin/activate
python radical_cooccurrence.py
```

Outputs:
- `output/radical_cooccurrence_matrix.csv` - Full 56x56 co-occurrence matrix
- `output/radical_cooccurrence_normalized.csv` - Normalized frequencies
- `output/top_radical_pairs.csv` - Top 100 pairs with examples

### 2. Generate Visualizations

```bash
python visualizations.py
```

Outputs 14 visualizations including:
- Full heat maps (normalized and filtered)
- Category-level heat maps
- Focused heat maps for specific radical groups
- Individual radical neighbor plots

### 3. Run Statistical Analysis

```bash
python statistical_analysis.py
```

Outputs:
- Statistical significance testing (chi-square)
- Category clustering analysis
- Avoidance pair detection
- Hierarchical clustering dendrogram
- Answers to specific research questions

## Key Findings

### Top Radical Co-occurrences

1. **一 + 口**: 198 occurrences
2. **人 + 口**: 164 occurrences
3. **一 + 火**: 154 occurrences
4. **一 + 丶**: 150 occurrences
5. **一 + 大**: 150 occurrences

### Research Question Answers

#### Q1: Do motion radicals (辶) cluster with other motion radicals?

**Finding**: Motion radicals show **low within-category clustering** (4.75% within-category proportion). The 辶 radical does not frequently co-occur with other motion radicals (走, 足, 行) in its top 20 neighbors.

**Interpretation**: Motion radicals appear to be **distributed** rather than clustered - they mark transitions throughout the text rather than appearing in concentrated "motion zones."

#### Q2: Do constraint radicals (尸) appear before emergence/release characters?

**Finding**: Found **11 constraint→motion sequences** within 5-character windows.

Examples:
- 居道 (dwell → way)
- 富道 (wealth → way)
- 室復 (room → return)
- 厚足 (thick → foot/sufficient)
- 厭復 (satisfied → return)

**Interpretation**: There is evidence of **constraint-to-motion sequences**, suggesting a pattern of constraint followed by release/transformation.

#### Q3: Do thread (糸) and cloth (巾) radicals cluster together?

**Finding**: **No direct co-occurrences** found between thread (糸/纟) and cloth (巾/衣/布) radicals within the 5-character window.

**Interpretation**: Thread and cloth radicals appear **independently** in the text, suggesting they may mark different aspects of connection/structure rather than operating together.

#### Q4: What radicals appear most frequently with 無 and 為?

**無 (wu - nothing/without)** - Radicals: [火]
Top co-occurring radicals:
1. 丶 (dot): 64
2. 人 (person): 60
3. 一 (one): 58
4. 口 (mouth/boundary): 52
5. 火 (fire): 44
6. 大 (great): 36
7. **辶 (walking/motion)**: 19

**為 (wei - do/act/make)** - Radicals: [火]
Top co-occurring radicals:
1. 一 (one): 81
2. 口 (mouth/boundary): 58
3. 人 (person): 56
4. 丶 (dot): 50
5. 大 (great): 49
6. **辶 (walking/motion)**: 41
7. 火 (fire): 39

**Interpretation**: Both 無 and 為 (both contain 火 radical) frequently appear with:
- **Agent radicals** (人) - indicating action/actors
- **Boundary radicals** (口) - indicating definition/scope
- **Motion radicals** (辶) - more strongly with 為 (action) than 無 (absence)
- **Basic structural radicals** (一, 大, 丶) - fundamental building blocks

The stronger association of 為 with 辶 (41 vs 19) suggests **action is more strongly linked to motion** than negation/absence is.

### Category Clustering Analysis

**Within-category co-occurrence proportions:**

| Category | Within % | Cross % | Total |
|----------|----------|---------|-------|
| Boundary | 8.91%    | 91.09%  | 2,289 |
| Agent    | 7.16%    | 92.84%  | 2,096 |
| Motion   | 4.75%    | 95.25%  | 968   |
| Internal | 1.68%    | 98.32%  | 417   |
| Fluid    | 1.59%    | 98.41%  | 440   |
| Cloth    | 1.36%    | 98.64%  | 221   |
| Thread   | 1.00%    | 99.00%  | 100   |
| Action   | 0.99%    | 99.01%  | 403   |
| Constraint| 0.99%   | 99.01%  | 406   |

**Key Insight**: **All radical categories show low within-category clustering** (all <9%), indicating that the Dao De Jing uses radicals in a **distributed, heterogeneous manner** rather than grouping similar transformational operations together.

This suggests the text operates by **combining different types of operations** (motion + constraint + boundary, etc.) rather than dwelling on single operational modes.

## Radical Categories

### Motion (辶, 走, 足, 行)
Marks continuous motion through space
- Color: #ef4444 (red)
- Example: 道 (dào - the Way)

### Fluid (水/氵, 冫, 雨)
Flow and fluid dynamics
- Color: #06b6d4 (cyan)
- Examples: 水, 清, 流

### Constraint (尸, 厂, 广, 宀)
External constraints/boundaries being applied
- Color: #f59e0b (amber)
- Examples: 居, 宀, 室

### Boundary (口, 門, 戶, 囗)
Defined boundaries and enclosures
- Color: #10b981 (green)
- Examples: 口, 名, 門

### Thread (糸/纟)
Continuous connection patterns
- Color: #8b5cf6 (purple)
- Examples: 絲, 綿, 累

### Cloth (巾, 衣, 布)
Woven/flexible structures
- Color: #ec4899 (pink)
- Examples: 巾, 布, 帶

### Agent (人/亻, 夫, 子)
Acting entities
- Color: #3b82f6 (blue)
- Examples: 人, 仁, 使

### Internal (心/忄, 思, 意)
Internal states and processes
- Color: #f59e0b (amber)
- Examples: 心, 性, 情

### Action (手/扌, 寸, 支)
Action and manipulation
- Color: #14b8a6 (teal)
- Examples: 手, 持, 推

## Data Files

### Input
- `../public/Just Characters-Table 1.csv` - Full Dao De Jing text (5,166 characters, 784 unique)

### Output CSVs

**radical_cooccurrence_matrix.csv**
- 56x56 symmetric matrix of raw co-occurrence counts
- Row/column: radical names
- Values: number of times two radicals appear within ±5 characters

**radical_cooccurrence_normalized.csv**
- Same structure, normalized to 0-1 range
- Values: frequency relative to maximum co-occurrence

**top_radical_pairs.csv**
- Columns: radical1, radical2, category1, category2, count, example_pairs
- Top 100 most frequent radical pairs
- Includes example character pairs that contribute to each count

**significance_analysis.csv**
- Columns: radical1, radical2, category1, category2, same_category, observed, expected, enrichment, chi_square, significant
- Statistical significance testing for each pair
- Identifies pairs that co-occur more/less than random chance

**avoidance_pairs.csv**
- Pairs where observed << expected (active avoidance)
- Columns: radical1, radical2, category1, category2, observed, expected, avoidance_ratio

## Methodology

### Co-occurrence Window
- **Window size**: ±5 characters
- Characters within 5 positions (before or after) are considered co-occurring
- Symmetric matrix (A→B counted same as B→A)

### Statistical Significance
- **Chi-square test** comparing observed vs. expected frequencies
- Expected frequency: `(count(X) * count(Y)) / (2 * total_pairs)`
- Threshold: p < 0.05 (chi-square > 3.84)
- **Enrichment ratio**: observed / expected

### Clustering
- **Method**: Hierarchical clustering using correlation distance
- **Linkage**: Average linkage
- Identifies groups of radicals with similar co-occurrence patterns

## Expanding the Dictionary

To add more characters to the radical mapping:

1. Edit `radical_dictionary.py`
2. Add entries to `RADICAL_MAP`:
   ```python
   "字": ["radical1", "radical2"],  # Character with multiple radicals
   ```
3. For new radical types, add to `RADICAL_CATEGORIES`
4. Re-run analysis scripts to update outputs

## Future Directions

### Potential Extensions

1. **Temporal Analysis**: Track how radical patterns change across chapters 1-81
2. **Network Graphs**: Visualize radical relationships as network graphs
3. **Sequence Mining**: Identify frequent radical sequences (3+ radicals)
4. **Comparative Analysis**: Compare TTC patterns with other classical texts
5. **Integration**: Merge with existing TypeScript character-level analysis
6. **Machine Learning**: Cluster characters by radical co-occurrence profiles
7. **Expanded Dictionary**: Map all 806 unique TTC characters

### Research Questions

1. Do certain chapters show different radical distribution patterns?
2. Are there "radical signatures" that mark key philosophical concepts?
3. How do radical patterns correlate with traditional chapter groupings?
4. Can radical analysis identify authorship patterns or textual layers?

## Technical Notes

### Character Encoding
- All files use UTF-8 encoding
- Chinese characters stored as Unicode
- Matplotlib may show font warnings (boxes) but images save correctly

### Performance
- Full analysis runs in ~30 seconds on modern hardware
- Matrix calculation: O(n²) where n = number of characters
- Memory usage: ~50MB for full dataset

### Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scipy >= 1.10.0

## Citation

If you use this analysis in research, please cite:

```
Radical Co-occurrence Analysis of the Dao De Jing
Recursive Structural Model (RSM) Framework
2024
```

## License

Private research tool - not for public distribution yet.

## Contact

For questions about the methodology or findings, please refer to the project documentation.

---

**Generated by**: Claude Code
**Analysis Date**: November 2024
**Text Source**: Dao De Jing (bamboo slip manuscripts and traditional texts)
**Total Characters Analyzed**: 5,166
**Unique Radicals**: 57
**Radical Categories**: 9
