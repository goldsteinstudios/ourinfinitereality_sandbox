#!/bin/bash
# Complete Radical Co-occurrence Analysis Pipeline
# Run this script to generate all outputs

echo "=============================================="
echo "Dao De Jing Radical Co-occurrence Analysis"
echo "=============================================="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "Step 1/3: Running co-occurrence matrix calculation..."
python radical_cooccurrence.py 2>&1 | grep -v "UserWarning"

echo ""
echo "Step 2/3: Generating visualizations..."
python visualizations.py 2>&1 | grep -v "UserWarning"

echo ""
echo "Step 3/3: Running statistical analysis..."
python statistical_analysis.py 2>&1 | grep -v "UserWarning"

echo ""
echo "=============================================="
echo "Analysis Complete!"
echo "=============================================="
echo ""
echo "Output files generated:"
echo ""
echo "CSV Files:"
find output -name "*.csv" -type f | sort
echo ""
echo "Visualizations:"
find output -name "*.png" -type f | sort
echo ""
echo "View the README.md for detailed findings and interpretation."
