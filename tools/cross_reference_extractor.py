#!/usr/bin/env python3
"""
Cross-Reference Network Extractor for DDJ Structural Translations

Parses all translated chapters, extracts chapter-to-chapter connections
from the "Cross-Reference to Framework" sections, and generates a
network graph visualization.

Author: Will Goldstein, 2025
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Connection type patterns
CONNECTION_TYPES = {
    'same_principle': [
        r'[Ss]ame\s+(?:principle|pattern|structure)',
        r'[Bb]oth\s+(?:describe|document|use)',
        r'[Ss]ame\s+\w+\s+principle',
    ],
    'extends': [
        r'[Ee]xtends?',
        r'[Ee]xpands?',
        r'[Bb]uilds?\s+on',
        r'[Cc]ontinues?',
    ],
    'applies': [
        r'[Aa]pplies?',
        r'[Aa]pplication',
        r'[Uu]ses?\s+the',
        r'[Dd]eploys?',
    ],
    'same_term': [
        r'[Ss]ame\s+(?:term|phrase|character|word)',
        r'[Ss]ame\s+\w+\s+from',
        r'[Ii]dentical',
    ],
    'contrast': [
        r'[Cc]ontrast',
        r'[Ww]hereas',
        r'[Uu]nlike',
        r'[Dd]iffers?',
    ],
    'validates': [
        r'[Vv]alidat',
        r'[Cc]onfirm',
        r'[Pp]roves?',
        r'[Dd]emonstrat',
    ],
    'specifies': [
        r'[Ss]pecifi',
        r'[Dd]ocuments?\s+the',
        r'[Dd]efines?',
        r'[Dd]etails?',
    ],
}


def extract_chapter_number(filename: str) -> int:
    """Extract chapter number from filename like 'chapter01_2025-11-26.md'"""
    match = re.search(r'chapter(\d+)', filename)
    if match:
        return int(match.group(1))
    return 0


def find_chapter_references(text: str, source_chapter: int) -> List[Tuple[int, str, str]]:
    """
    Find all chapter references in text.
    Returns list of (target_chapter, connection_type, context_snippet)
    """
    connections = []

    # Patterns to find chapter references
    chapter_patterns = [
        r'[Cc]hapter\s+(\d+)',
        r'[Cc]h\.?\s*(\d+)',
        r'[Cc]h(\d+)',
    ]

    # Split into lines for context
    lines = text.split('\n')

    for i, line in enumerate(lines):
        for pattern in chapter_patterns:
            for match in re.finditer(pattern, line):
                target_chapter = int(match.group(1))

                # Skip self-references
                if target_chapter == source_chapter:
                    continue

                # Get surrounding context (this line + adjacent if short)
                context = line.strip()
                if len(context) < 50 and i > 0:
                    context = lines[i-1].strip() + ' ' + context

                # Determine connection type
                conn_type = classify_connection(context)

                connections.append((target_chapter, conn_type, context[:200]))

    return connections


def classify_connection(context: str) -> str:
    """Classify the type of connection based on context text."""
    for conn_type, patterns in CONNECTION_TYPES.items():
        for pattern in patterns:
            if re.search(pattern, context):
                return conn_type
    return 'references'  # default type


def extract_cross_reference_section(text: str) -> str:
    """Extract the Cross-Reference to Framework section from a chapter."""
    # Look for the section header
    patterns = [
        r'## Cross-Reference to Framework\s*\n(.*?)(?=\n## |\n---|\Z)',
        r'## Cross-Reference\s*\n(.*?)(?=\n## |\n---|\Z)',
        r'### Connection to .*?\n(.*?)(?=\n## |\n---|\Z)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)

    # If no specific section, search the whole document
    return text


def parse_translation_file(filepath: Path) -> Dict:
    """Parse a single translation file and extract connections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    chapter_num = extract_chapter_number(filepath.name)

    # Extract the cross-reference section specifically
    cross_ref_section = extract_cross_reference_section(text)

    # Find all chapter references in cross-reference section
    connections = find_chapter_references(cross_ref_section, chapter_num)

    # Also scan the full document for any additional references
    full_connections = find_chapter_references(text, chapter_num)

    # Merge, preferring cross-reference section findings
    seen_targets = {c[0] for c in connections}
    for conn in full_connections:
        if conn[0] not in seen_targets:
            connections.append(conn)

    # Extract title
    title_match = re.search(r'^# (.+)$', text, re.MULTILINE)
    title = title_match.group(1) if title_match else f'Chapter {chapter_num}'

    # Extract subtitle
    subtitle_match = re.search(r'^\*(.+)\*$', text, re.MULTILINE)
    subtitle = subtitle_match.group(1) if subtitle_match else ''

    return {
        'chapter': chapter_num,
        'title': title,
        'subtitle': subtitle,
        'connections': connections,
        'filepath': str(filepath),
    }


def build_network(chapters_data: List[Dict]) -> Dict:
    """Build the network structure from parsed chapter data."""
    nodes = []
    edges = []

    # Track all chapters (translated and referenced)
    all_chapters = set()
    translated_chapters = set()

    for data in chapters_data:
        chapter = data['chapter']
        translated_chapters.add(chapter)
        all_chapters.add(chapter)

        nodes.append({
            'id': chapter,
            'title': data['title'],
            'subtitle': data['subtitle'],
            'translated': True,
        })

        for target, conn_type, context in data['connections']:
            all_chapters.add(target)
            edges.append({
                'source': chapter,
                'target': target,
                'type': conn_type,
                'context': context,
            })

    # Add nodes for referenced but untranslated chapters
    for chapter in all_chapters - translated_chapters:
        nodes.append({
            'id': chapter,
            'title': f'Chapter {chapter}',
            'subtitle': '(not yet translated)',
            'translated': False,
        })

    return {
        'nodes': nodes,
        'edges': edges,
        'translated_chapters': sorted(translated_chapters),
        'referenced_untranslated': sorted(all_chapters - translated_chapters),
    }


def compute_network_statistics(network: Dict) -> Dict:
    """Compute network statistics and identify hubs."""
    nodes = {n['id']: n for n in network['nodes']}
    edges = network['edges']

    # Count incoming and outgoing edges for each node
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for edge in edges:
        out_degree[edge['source']] += 1
        in_degree[edge['target']] += 1

    # Compute statistics
    stats = {
        'total_nodes': len(nodes),
        'total_edges': len(edges),
        'translated_count': len(network['translated_chapters']),
        'referenced_untranslated_count': len(network['referenced_untranslated']),
    }

    # Identify hubs (most referenced chapters)
    hubs = sorted(
        [(ch, in_degree[ch]) for ch in nodes.keys()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    stats['top_hubs'] = [
        {
            'chapter': ch,
            'in_degree': deg,
            'title': nodes[ch]['title'],
            'translated': nodes[ch]['translated'],
        }
        for ch, deg in hubs if deg > 0
    ]

    # Identify most-referenced untranslated chapters (priority gaps)
    untranslated_refs = sorted(
        [(ch, in_degree[ch]) for ch in network['referenced_untranslated']],
        key=lambda x: x[1],
        reverse=True
    )
    stats['priority_gaps'] = [
        {'chapter': ch, 'references': deg}
        for ch, deg in untranslated_refs if deg > 0
    ]

    # Connection type distribution
    type_counts = defaultdict(int)
    for edge in edges:
        type_counts[edge['type']] += 1
    stats['connection_types'] = dict(type_counts)

    # Identify leaf nodes (referenced but don't reference others)
    leaves = [
        ch for ch in nodes.keys()
        if in_degree[ch] > 0 and out_degree[ch] == 0
    ]
    stats['leaf_nodes'] = leaves

    # Chapters with most outgoing references
    most_referencing = sorted(
        [(ch, out_degree[ch]) for ch in nodes.keys()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    stats['most_referencing'] = [
        {'chapter': ch, 'out_degree': deg, 'translated': nodes[ch]['translated']}
        for ch, deg in most_referencing if deg > 0
    ]

    return stats


def generate_html_visualization(network: Dict, stats: Dict, output_path: Path):
    """Generate an interactive HTML visualization using D3.js."""

    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dao De Jing Cross-Reference Network</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            overflow: hidden;
        }
        #container {
            display: flex;
            height: 100vh;
        }
        #graph {
            flex: 1;
            position: relative;
        }
        #sidebar {
            width: 350px;
            background: #1a1a1a;
            padding: 20px;
            overflow-y: auto;
            border-left: 1px solid #333;
        }
        h1 {
            font-size: 1.4em;
            margin-bottom: 10px;
            color: #fff;
        }
        h2 {
            font-size: 1.1em;
            margin: 20px 0 10px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat {
            margin: 5px 0;
            font-size: 0.9em;
        }
        .stat-value {
            color: #4ecdc4;
            font-weight: bold;
        }
        .hub-item, .gap-item {
            background: #252525;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #4ecdc4;
        }
        .gap-item {
            border-left-color: #ff6b6b;
        }
        .hub-chapter {
            font-weight: bold;
            color: #fff;
        }
        .hub-refs {
            font-size: 0.8em;
            color: #888;
        }
        .untranslated {
            opacity: 0.7;
            font-style: italic;
        }
        #tooltip {
            position: absolute;
            background: #2a2a2a;
            border: 1px solid #444;
            padding: 12px;
            border-radius: 6px;
            pointer-events: none;
            opacity: 0;
            max-width: 300px;
            font-size: 0.85em;
            z-index: 1000;
        }
        .tooltip-title {
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 5px;
        }
        .tooltip-subtitle {
            color: #888;
            font-style: italic;
            margin-bottom: 8px;
        }
        .tooltip-connections {
            font-size: 0.85em;
        }
        .legend {
            margin-top: 20px;
            padding: 10px;
            background: #252525;
            border-radius: 4px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 0.85em;
        }
        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .legend-line {
            width: 30px;
            height: 2px;
            margin-right: 8px;
        }
        svg {
            width: 100%;
            height: 100%;
        }
        .node circle {
            stroke: #fff;
            stroke-width: 1.5px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .node circle:hover {
            stroke-width: 3px;
        }
        .node text {
            font-size: 11px;
            fill: #fff;
            pointer-events: none;
            text-anchor: middle;
        }
        .link {
            fill: none;
            stroke-opacity: 0.4;
            transition: stroke-opacity 0.2s;
        }
        .link:hover {
            stroke-opacity: 1;
        }
        .node.highlighted circle {
            stroke-width: 3px;
            stroke: #fff;
        }
        .link.highlighted {
            stroke-opacity: 1;
            stroke-width: 2px;
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="graph">
            <div id="tooltip"></div>
        </div>
        <div id="sidebar">
            <h1>道德經 Cross-Reference Network</h1>
            <p style="color: #888; font-size: 0.9em; margin-bottom: 15px;">
                Structural connections between translated chapters
            </p>

            <h2>Statistics</h2>
            <div class="stat">Translated Chapters: <span class="stat-value">''' + str(stats['translated_count']) + '''</span></div>
            <div class="stat">Total Connections: <span class="stat-value">''' + str(stats['total_edges']) + '''</span></div>
            <div class="stat">Referenced (Untranslated): <span class="stat-value">''' + str(stats['referenced_untranslated_count']) + '''</span></div>

            <h2>Hub Chapters (Most Referenced)</h2>
            <div id="hubs"></div>

            <h2>Priority Gaps (Untranslated but Referenced)</h2>
            <div id="gaps"></div>

            <div class="legend">
                <h2 style="margin-top: 0;">Legend</h2>
                <div class="legend-item">
                    <div class="legend-dot" style="background: #4ecdc4;"></div>
                    <span>Translated chapter</span>
                </div>
                <div class="legend-item">
                    <div class="legend-dot" style="background: #ff6b6b;"></div>
                    <span>Untranslated (referenced)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-line" style="background: #666;"></div>
                    <span>Connection</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const networkData = ''' + json.dumps(network) + ''';
        const stats = ''' + json.dumps(stats) + ''';

        // Populate sidebar
        const hubsDiv = document.getElementById('hubs');
        stats.top_hubs.forEach(hub => {
            const div = document.createElement('div');
            div.className = 'hub-item' + (hub.translated ? '' : ' untranslated');
            div.innerHTML = `
                <div class="hub-chapter">Chapter ${hub.chapter}</div>
                <div class="hub-refs">${hub.in_degree} incoming references</div>
            `;
            hubsDiv.appendChild(div);
        });

        const gapsDiv = document.getElementById('gaps');
        stats.priority_gaps.slice(0, 10).forEach(gap => {
            const div = document.createElement('div');
            div.className = 'gap-item';
            div.innerHTML = `
                <div class="hub-chapter">Chapter ${gap.chapter}</div>
                <div class="hub-refs">${gap.references} references from translated chapters</div>
            `;
            gapsDiv.appendChild(div);
        });

        // D3 visualization
        const width = document.getElementById('graph').clientWidth;
        const height = document.getElementById('graph').clientHeight;

        const svg = d3.select('#graph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        // Add zoom behavior
        const g = svg.append('g');

        svg.call(d3.zoom()
            .extent([[0, 0], [width, height]])
            .scaleExtent([0.2, 4])
            .on('zoom', (event) => {
                g.attr('transform', event.transform);
            }));

        // Arrow marker for directed edges
        svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .append('path')
            .attr('d', 'M 0,-5 L 10,0 L 0,5')
            .attr('fill', '#666');

        // Connection type colors
        const typeColors = {
            'same_principle': '#4ecdc4',
            'extends': '#45b7d1',
            'applies': '#96ceb4',
            'same_term': '#ffeaa7',
            'contrast': '#ff6b6b',
            'validates': '#a29bfe',
            'specifies': '#fd79a8',
            'references': '#666',
        };

        // Process data for D3
        const nodes = networkData.nodes.map(n => ({...n}));
        const links = networkData.edges.map(e => ({
            source: e.source,
            target: e.target,
            type: e.type,
            context: e.context
        }));

        // Create force simulation
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links)
                .id(d => d.id)
                .distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(30));

        // Draw links
        const link = g.append('g')
            .selectAll('path')
            .data(links)
            .join('path')
            .attr('class', 'link')
            .attr('stroke', d => typeColors[d.type] || '#666')
            .attr('stroke-width', 1.5)
            .attr('marker-end', 'url(#arrowhead)');

        // Draw nodes
        const node = g.append('g')
            .selectAll('g')
            .data(nodes)
            .join('g')
            .attr('class', 'node')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));

        // Node circles
        node.append('circle')
            .attr('r', d => {
                // Size based on connections
                const inDegree = links.filter(l => l.target.id === d.id || l.target === d.id).length;
                return Math.max(8, Math.min(25, 8 + inDegree * 2));
            })
            .attr('fill', d => d.translated ? '#4ecdc4' : '#ff6b6b');

        // Node labels
        node.append('text')
            .attr('dy', 4)
            .text(d => d.id);

        // Tooltip
        const tooltip = d3.select('#tooltip');

        node.on('mouseover', function(event, d) {
            const incoming = links.filter(l => (l.target.id || l.target) === d.id);
            const outgoing = links.filter(l => (l.source.id || l.source) === d.id);

            tooltip
                .style('opacity', 1)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 10) + 'px')
                .html(`
                    <div class="tooltip-title">${d.title}</div>
                    ${d.subtitle ? `<div class="tooltip-subtitle">${d.subtitle}</div>` : ''}
                    <div class="tooltip-connections">
                        <div>← ${incoming.length} incoming</div>
                        <div>→ ${outgoing.length} outgoing</div>
                        ${!d.translated ? '<div style="color: #ff6b6b;">Not yet translated</div>' : ''}
                    </div>
                `);

            // Highlight connected nodes and edges
            d3.selectAll('.node').classed('highlighted', n =>
                n.id === d.id ||
                incoming.some(l => (l.source.id || l.source) === n.id) ||
                outgoing.some(l => (l.target.id || l.target) === n.id)
            );
            d3.selectAll('.link').classed('highlighted', l =>
                (l.source.id || l.source) === d.id ||
                (l.target.id || l.target) === d.id
            );
        })
        .on('mouseout', function() {
            tooltip.style('opacity', 0);
            d3.selectAll('.node').classed('highlighted', false);
            d3.selectAll('.link').classed('highlighted', false);
        });

        // Update positions on tick
        simulation.on('tick', () => {
            link.attr('d', d => {
                const dx = d.target.x - d.source.x;
                const dy = d.target.y - d.source.y;
                return `M${d.source.x},${d.source.y}L${d.target.x},${d.target.y}`;
            });

            node.attr('transform', d => `translate(${d.x},${d.y})`);
        });

        // Drag functions
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    </script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    """Main entry point."""
    # Find all translation files
    translations_dir = Path(__file__).parent.parent / 'translations' / 'chapters'

    if not translations_dir.exists():
        print(f"Error: Translations directory not found at {translations_dir}")
        return

    # Parse all translation files
    chapters_data = []
    for filepath in sorted(translations_dir.glob('chapter*_2025*.md')):
        # Skip the direct/teaching versions
        if '_direct_' in filepath.name:
            continue

        print(f"Parsing: {filepath.name}")
        data = parse_translation_file(filepath)
        chapters_data.append(data)
        print(f"  Found {len(data['connections'])} connections")

    print(f"\nParsed {len(chapters_data)} chapters")

    # Build network
    network = build_network(chapters_data)
    print(f"Network has {len(network['nodes'])} nodes and {len(network['edges'])} edges")

    # Compute statistics
    stats = compute_network_statistics(network)

    # Output directory
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)

    # Save JSON data
    json_path = output_dir / 'cross_reference_network.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'network': network,
            'statistics': stats,
            'chapters': chapters_data,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nSaved network data to: {json_path}")

    # Generate HTML visualization
    html_path = output_dir / 'cross_reference_network.html'
    generate_html_visualization(network, stats, html_path)
    print(f"Generated visualization at: {html_path}")

    # Print summary
    print("\n" + "="*60)
    print("NETWORK ANALYSIS SUMMARY")
    print("="*60)

    print(f"\nTotal translated chapters: {stats['translated_count']}")
    print(f"Total connections: {stats['total_edges']}")
    print(f"Referenced but untranslated: {stats['referenced_untranslated_count']}")

    print("\n--- TOP HUB CHAPTERS (Most Referenced) ---")
    for hub in stats['top_hubs']:
        status = "✓" if hub['translated'] else "✗ UNTRANSLATED"
        print(f"  Chapter {hub['chapter']:2d}: {hub['in_degree']:2d} references {status}")

    print("\n--- PRIORITY GAPS (Untranslated but Referenced) ---")
    for gap in stats['priority_gaps'][:10]:
        print(f"  Chapter {gap['chapter']:2d}: {gap['references']:2d} references from translated chapters")

    print("\n--- CONNECTION TYPE DISTRIBUTION ---")
    for conn_type, count in sorted(stats['connection_types'].items(), key=lambda x: -x[1]):
        print(f"  {conn_type:20s}: {count:3d}")

    print("\n--- MOST REFERENCING CHAPTERS (Most Outgoing) ---")
    for ref in stats['most_referencing'][:5]:
        print(f"  Chapter {ref['chapter']:2d}: {ref['out_degree']:2d} outgoing references")


if __name__ == '__main__':
    main()
