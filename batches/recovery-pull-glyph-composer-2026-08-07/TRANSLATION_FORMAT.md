# Translation Format Guide

## File Structure

Each chapter translation should be saved as: `translations/chapters/chapterXX.md`

## Format Template

```markdown
# Chapter XX: [Title/Theme]

## Source Text
[Original Chinese text from bamboo slip version]

## Key Characters & Corrections
| Character | Traditional | Geometric | Structure | Validation |
|-----------|-------------|-----------|-----------|------------|
| 常 | "eternal" | implicit/concealed | 巾+尚 | TEST1 ✓ |
| 欲 | "desire" | directed orientation | 谷+欠 | TEST1 ✓ |

## Geometric Translation
[Line-by-line translation using geometric readings]

Line 1: [Chinese] → [Geometric English]
Line 2: [Chinese] → [Geometric English]
...

## Structural Analysis
### Operators Used
- 道: trajectory/continuous evolution
- 反: reversal/unitarity
- 大: unbounded field

### Radical Families Present
- 氵(water): [list characters with geometric operations]
- 禾 (grain): [list characters with geometric operations]
- 心 (heart): [list characters with geometric operations]

### New Patterns Identified
[Any geometric patterns not yet documented in test_results/]

## Traditional vs Geometric Comparison
**Traditional:** [Standard moral/mystical reading]
**Geometric:** [Our reading with operations and substrates]
**Key Difference:** [What the geometric reading reveals]

## Cross-References
- Related to: [Other chapters with similar patterns]
- Validates: [Which test results this supports]
- Extends: [Which test results this adds to]

## Notes
[Additional insights, open questions, areas needing validation]
```

## Quick Start

For chapters you already have, you can share them in any format and I'll:
1. Parse them into this structure
2. Extract key character usage
3. Cross-reference with our test results (Tests 1-9)
4. Identify new patterns
5. Generate validation reports

## What I'll Build

I'm creating tools to:
- **translation_integrator.py**: Parse your translations and extract insights
- **character_validator.py**: Check which validated characters you're using
- **pattern_detector.py**: Find new geometric patterns in your text
- **bidirectional_sync.py**: Update translations with new validations
- **coverage_report.py**: Show which chapters use which corrections
