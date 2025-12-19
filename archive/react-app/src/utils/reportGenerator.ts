import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import type {
  ContrastHypothesis,
  CoOccurrenceMatrix,
  ContextWindow,
  AnalysisReport,
} from '../types/analysis';
import { formatContextWindow } from './contextExtractor';
import { exportMatrixToCSV } from './coOccurrenceCalculator';

/**
 * Generate markdown report for contrast pair analysis
 */
export function generateContrastMarkdown(hypothesis: ContrastHypothesis): string {
  const { char1, char2, name, description, statistics, instances } = hypothesis;

  const lines: string[] = [];

  // Header
  lines.push(`# Contrast Pair Analysis: ${char1}/${char2}`);
  lines.push('');
  lines.push(`**Hypothesis Name:** ${name}`);
  lines.push('');
  lines.push(`**Description:** ${description}`);
  lines.push('');

  // Statistics
  lines.push('## Statistics');
  lines.push('');
  lines.push(`- **Total Instances:** ${statistics.total}`);
  lines.push(`- **Opposition:** ${statistics.oppose} (${(statistics.oppositionRate * 100).toFixed(1)}%)`);
  lines.push(`- **Alignment:** ${statistics.align} (${(statistics.alignmentRate * 100).toFixed(1)}%)`);
  lines.push(`- **Ambiguous:** ${statistics.ambiguous}`);
  lines.push(`- **Independent:** ${statistics.independent}`);
  lines.push(`- **Unclassified:** ${statistics.unclassified}`);
  lines.push(`- **Confidence Level:** ${statistics.confidenceLevel.toUpperCase()}`);
  lines.push('');

  // Confidence interpretation
  lines.push('## Interpretation');
  lines.push('');
  if (statistics.oppositionRate > 0.7) {
    lines.push('**Strong evidence for systematic opposition.** The characters oppose each other in the majority of co-occurrences.');
  } else if (statistics.oppositionRate > 0.5) {
    lines.push('**Moderate evidence for opposition pattern.** The characters show oppositional tendency but not overwhelmingly.');
  } else if (statistics.alignmentRate > 0.5) {
    lines.push('**Evidence suggests alignment rather than opposition.** The characters tend to support rather than contrast each other.');
  } else {
    lines.push('**Mixed or unclear pattern.** The relationship between these characters requires further investigation.');
  }
  lines.push('');

  // Detailed instances
  lines.push('## Analyzed Instances');
  lines.push('');

  // Group by classification
  const byClass = {
    oppose: instances.filter(i => i.classification === 'oppose'),
    align: instances.filter(i => i.classification === 'align'),
    ambiguous: instances.filter(i => i.classification === 'ambiguous'),
    independent: instances.filter(i => i.classification === 'independent'),
    unclassified: instances.filter(i => i.classification === null),
  };

  for (const [classification, classInstances] of Object.entries(byClass)) {
    if (classInstances.length === 0) continue;

    lines.push(`### ${classification.charAt(0).toUpperCase() + classification.slice(1)} (${classInstances.length})`);
    lines.push('');

    for (const instance of classInstances) {
      const contextStr = formatContextWindow(instance.context, {
        showChapter: true,
        showPosition: true,
        highlightCenter: true,
        separator: ' ',
      });

      lines.push(`- ${contextStr}`);
      if (instance.note) {
        lines.push(`  - *Note:* ${instance.note}`);
      }
    }
    lines.push('');
  }

  // Metadata
  lines.push('---');
  lines.push('');
  lines.push(`*Analysis generated: ${new Date(hypothesis.updatedAt).toLocaleString()}*`);
  lines.push('');
  lines.push('*Generated with Dao De Jing Pattern Analyzer*');

  return lines.join('\n');
}

/**
 * Generate CSV report for contrast pair analysis
 */
export function generateContrastCSV(hypothesis: ContrastHypothesis): string {
  const rows: string[][] = [];

  // Header
  rows.push(['Chapter', 'Position 1', 'Position 2', 'Classification', 'Context', 'Note']);

  // Data rows
  for (const instance of hypothesis.instances) {
    rows.push([
      instance.context.chapter.toString(),
      instance.char1Occurrence.position.toString(),
      instance.char2Occurrence.position.toString(),
      instance.classification || 'unclassified',
      formatContextWindow(instance.context, { highlightCenter: false }),
      instance.note || '',
    ]);
  }

  return rows.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
}

/**
 * Generate PDF report for contrast pair analysis
 */
export function generateContrastPDF(hypothesis: ContrastHypothesis): jsPDF {
  const pdf = new jsPDF();
  const { char1, char2, name, description, statistics, instances } = hypothesis;

  let yPos = 20;

  // Title
  pdf.setFontSize(18);
  pdf.text(`Contrast Pair Analysis: ${char1}/${char2}`, 20, yPos);
  yPos += 15;

  // Hypothesis details
  pdf.setFontSize(12);
  pdf.text(`Hypothesis: ${name}`, 20, yPos);
  yPos += 10;

  pdf.setFontSize(10);
  const descLines = pdf.splitTextToSize(description, 170);
  pdf.text(descLines, 20, yPos);
  yPos += descLines.length * 7 + 10;

  // Statistics table
  pdf.setFontSize(14);
  pdf.text('Statistics', 20, yPos);
  yPos += 10;

  autoTable(pdf, {
    startY: yPos,
    head: [['Metric', 'Count', 'Percentage']],
    body: [
      ['Total Instances', statistics.total.toString(), '100%'],
      ['Opposition', statistics.oppose.toString(), `${(statistics.oppositionRate * 100).toFixed(1)}%`],
      ['Alignment', statistics.align.toString(), `${(statistics.alignmentRate * 100).toFixed(1)}%`],
      ['Ambiguous', statistics.ambiguous.toString(), `${((statistics.ambiguous / statistics.total) * 100).toFixed(1)}%`],
      ['Confidence Level', statistics.confidenceLevel.toUpperCase(), ''],
    ],
    theme: 'grid',
  });

  yPos = (pdf as any).lastAutoTable.finalY + 15;

  // Sample instances (first 10)
  if (instances.length > 0) {
    if (yPos > 250) {
      pdf.addPage();
      yPos = 20;
    }

    pdf.setFontSize(14);
    pdf.text('Sample Instances', 20, yPos);
    yPos += 10;

    const sampleInstances = instances.slice(0, 10);
    const tableData = sampleInstances.map(instance => [
      `Ch ${instance.context.chapter}`,
      formatContextWindow(instance.context, { highlightCenter: true }),
      instance.classification || 'unclassified',
      instance.note || '',
    ]);

    autoTable(pdf, {
      startY: yPos,
      head: [['Location', 'Context', 'Classification', 'Note']],
      body: tableData,
      theme: 'striped',
      columnStyles: {
        1: { cellWidth: 70 },
        3: { cellWidth: 50 },
      },
    });
  }

  // Metadata
  pdf.setFontSize(8);
  pdf.text(
    `Generated: ${new Date(hypothesis.updatedAt).toLocaleString()}`,
    20,
    pdf.internal.pageSize.height - 10
  );

  return pdf;
}

/**
 * Download analysis report
 */
export function downloadReport(
  filename: string,
  content: string | Blob,
  type: 'text' | 'pdf' = 'text'
) {
  const blob = type === 'pdf'
    ? content as Blob
    : new Blob([content as string], { type: 'text/plain;charset=utf-8' });

  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Export contrast hypothesis in chosen format
 */
export function exportContrastHypothesis(
  hypothesis: ContrastHypothesis,
  format: 'markdown' | 'csv' | 'pdf' | 'json'
) {
  const timestamp = new Date().toISOString().split('T')[0];
  const basename = `contrast_${hypothesis.char1}_${hypothesis.char2}_${timestamp}`;

  switch (format) {
    case 'markdown': {
      const markdown = generateContrastMarkdown(hypothesis);
      downloadReport(`${basename}.md`, markdown);
      break;
    }
    case 'csv': {
      const csv = generateContrastCSV(hypothesis);
      downloadReport(`${basename}.csv`, csv);
      break;
    }
    case 'pdf': {
      const pdf = generateContrastPDF(hypothesis);
      downloadReport(`${basename}.pdf`, pdf.output('blob'), 'pdf');
      break;
    }
    case 'json': {
      const json = JSON.stringify(hypothesis, null, 2);
      downloadReport(`${basename}.json`, json);
      break;
    }
  }
}

/**
 * Export co-occurrence matrix
 */
export function exportCoOccurrenceMatrix(
  matrix: CoOccurrenceMatrix,
  format: 'csv' | 'json'
) {
  const timestamp = new Date().toISOString().split('T')[0];
  const basename = `cooccurrence_matrix_${timestamp}`;

  if (format === 'csv') {
    const csv = exportMatrixToCSV(matrix);
    downloadReport(`${basename}.csv`, csv);
  } else {
    const json = JSON.stringify(
      {
        characters: matrix.characters,
        proximityThreshold: matrix.proximityThreshold,
        minFrequency: matrix.minFrequency,
        pairCount: Array.from(matrix.matrix.values()).reduce(
          (sum, inner) => sum + inner.size,
          0
        ),
      },
      null,
      2
    );
    downloadReport(`${basename}.json`, json);
  }
}
