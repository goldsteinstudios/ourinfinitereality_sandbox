import { useState, useMemo, useRef, useEffect, useCallback } from "react";

// ============================================================
//  GLYPH COMPOSER v3.1
//  - ASCII quotes fixed
//  - no layout-reset race when loading saved compounds
//  - T subtype counts derived from paletteGlyphs (no extra rescan)
//  - compact T subtype display codes
//  - localStorage persistence for library
// ============================================================

// ------------------------------------------------------------
// PERSISTENCE
// ------------------------------------------------------------

const STORAGE_KEY = "glyph-composer-library";

function loadLibrary(): Compound[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw) as Compound[];
  } catch { /* ignore corrupt data */ }
  return [];
}

function saveLibrary(compounds: Compound[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(compounds));
  } catch { /* storage full or unavailable */ }
}

function exportLibrary(compounds: Compound[]) {
  const blob = new Blob([JSON.stringify(compounds, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `glyph-library-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function importLibrary(file: File): Promise<Compound[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result as string) as Compound[];
        if (!Array.isArray(data)) throw new Error("Invalid format");
        resolve(data);
      } catch (e) { reject(e); }
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file);
  });
}

// ------------------------------------------------------------
// TYPES
// ------------------------------------------------------------

interface Edge {
  type: string;
  r: number;
  c: number;
  r2: number;
  c2: number;
}

interface Classification {
  category: string;
  label: string;
  strokeCount: number;
  nodeCount?: number;
  degreeProfile?: Record<number, number>;
  components?: number;
  tInfo?: TJunctionInfo;
  tSubtype?: string;
}

interface TJunctionInfo {
  isT: boolean;
  isY?: boolean;
  axisDirection?: number[];
  lateralDirection?: number[];
  axisLength?: number;
  axisLen1?: number;
  axisLen2?: number;
  lateralLength?: number;
  axisOrientation?: string;
  symmetry?: string;
  lateralClass?: string;
}

interface PaletteGlyph {
  id: number;
  bits: number[];
  classification: Classification;
}

interface GlyphData {
  bits?: number[];
  isCompound?: boolean;
  compound?: Compound;
  rotation: number;
}

interface Definition {
  text: string;
  source?: string; // e.g. "39017.com", "Shuowen Jiezi"
}

interface Compound {
  id: string;
  layout: string;
  slots: (string | number | null)[];
  glyphData: Record<string, GlyphData>;
  label: string;
  timestamp: number;
  promoted: boolean;
  // Metadata fields (all optional for backwards compat)
  definitions?: Definition[];
  activeDefinitionIndex?: number;
  images?: { url: string; label: string }[];
  guodianLocation?: string;
  locked?: boolean;
}

interface LayoutDef {
  label: string;
  name: string;
  slots: number;
  positions: (w: number, h: number) => { x: number; y: number; w: number; h: number }[];
}

interface PerimeterInfo {
  perimeterTotal: number;
  perimeterActive: number;
  ratio: number;
  interiorActive: number;
}

// ------------------------------------------------------------
// EDGE GENERATION
// ------------------------------------------------------------

function getEdges(cols: number, rows: number, includeDiagonals: boolean): Edge[] {
  const edges: Edge[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (c < cols - 1) edges.push({ type: "h", r, c, r2: r, c2: c + 1 });
      if (r < rows - 1) edges.push({ type: "v", r, c, r2: r + 1, c2: c });
      if (includeDiagonals && c < cols - 1 && r < rows - 1) {
        edges.push({ type: "d1", r, c, r2: r + 1, c2: c + 1 });
        edges.push({ type: "d2", r, c: c + 1, r2: r + 1, c2: c });
      }
    }
  }
  return edges;
}

function indexToEdges(index: number, numEdges: number): number[] {
  const bits: number[] = [];
  for (let i = 0; i < numEdges; i++) bits.push((index >> i) & 1);
  return bits;
}

// ------------------------------------------------------------
// GRAPH CONSTRUCTION
// ------------------------------------------------------------

function nk(r: number, c: number): string {
  return `${r},${c}`;
}

function parseNk(key: string): [number, number] {
  const parts = key.split(",");
  return [parseInt(parts[0], 10), parseInt(parts[1], 10)];
}

function buildGraph(bits: number[], edges: Edge[]): Map<string, string[]> {
  const nodes = new Map<string, string[]>();
  for (let i = 0; i < edges.length; i++) {
    if (!bits[i]) continue;
    const e = edges[i];
    const a = nk(e.r, e.c);
    const b = nk(e.r2, e.c2);
    if (!nodes.has(a)) nodes.set(a, []);
    if (!nodes.has(b)) nodes.set(b, []);
    nodes.get(a)!.push(b);
    nodes.get(b)!.push(a);
  }
  return nodes;
}

// ------------------------------------------------------------
// GRAPH ANALYSIS
// ------------------------------------------------------------

function getComponents(graph: Map<string, string[]>): string[][] {
  const visited = new Set<string>();
  const components: string[][] = [];

  for (const startNode of graph.keys()) {
    if (visited.has(startNode)) continue;

    const comp: string[] = [];
    const stack = [startNode];

    while (stack.length > 0) {
      const n = stack.pop()!;
      if (visited.has(n)) continue;
      visited.add(n);
      comp.push(n);

      const neighbors = graph.get(n) || [];
      for (let j = 0; j < neighbors.length; j++) {
        if (!visited.has(neighbors[j])) stack.push(neighbors[j]);
      }
    }

    components.push(comp);
  }

  return components;
}

function hasCycle(graph: Map<string, string[]>): boolean {
  const visited = new Set<string>();

  for (const start of graph.keys()) {
    if (visited.has(start)) continue;

    const stack: { node: string; parent: string | null }[] = [{ node: start, parent: null }];
    visited.add(start);

    while (stack.length > 0) {
      const item = stack.pop()!;
      const node = item.node;
      const parent = item.parent;
      const nbrs = graph.get(node) || [];

      for (let k = 0; k < nbrs.length; k++) {
        const nb = nbrs[k];
        if (!visited.has(nb)) {
          visited.add(nb);
          stack.push({ node: nb, parent: node });
        } else if (nb !== parent) {
          return true;
        }
      }
    }
  }

  return false;
}

function getDegreeProfile(graph: Map<string, string[]>): Record<number, number> {
  const profile: Record<number, number> = {};
  for (const entry of graph) {
    const d = entry[1].length;
    profile[d] = (profile[d] || 0) + 1;
  }
  return profile;
}

// ------------------------------------------------------------
// PATH DIRECTION ANALYSIS
// ------------------------------------------------------------

function edgeDirection(aKey: string, bKey: string): [number, number] {
  const a = parseNk(aKey);
  const b = parseNk(bKey);
  return [b[0] - a[0], b[1] - a[1]];
}

function isCollinear(d1: [number, number], d2: [number, number]): boolean {
  return d1[0] === -d2[0] && d1[1] === -d2[1];
}

function pathHasTurn(graph: Map<string, string[]>): boolean {
  for (const entry of graph) {
    const node = entry[0];
    const neighbors = entry[1];
    if (neighbors.length !== 2) continue;

    const d1 = edgeDirection(node, neighbors[0]);
    const d2 = edgeDirection(node, neighbors[1]);
    if (!isCollinear(d1, d2)) return true;
  }
  return false;
}

// ------------------------------------------------------------
// T-JUNCTION ANALYSIS
// ------------------------------------------------------------

function walkBranchLength(graph: Map<string, string[]>, from: string, firstStep: string): number {
  let length = 1;
  let prev = from;
  let curr = firstStep;

  while (true) {
    const nbrs = graph.get(curr) || [];
    if (nbrs.length !== 2) break;
    const next = nbrs[0] === prev ? nbrs[1] : nbrs[0];
    prev = curr;
    curr = next;
    length++;
  }

  return length;
}

function analyzeTJunction(graph: Map<string, string[]>): TJunctionInfo {
  let junctionNode: string | null = null;

  for (const entry of graph) {
    if (entry[1].length === 3) {
      junctionNode = entry[0];
      break;
    }
  }

  if (!junctionNode) return { isT: false };

  const neighbors = graph.get(junctionNode)!;

  for (let i = 0; i < 3; i++) {
    const d1 = edgeDirection(junctionNode, neighbors[i]);

    for (let j = i + 1; j < 3; j++) {
      const d2 = edgeDirection(junctionNode, neighbors[j]);

      if (isCollinear(d1, d2)) {
        const lateralIdx = [0, 1, 2].filter((idx) => idx !== i && idx !== j)[0];
        const lateral = edgeDirection(junctionNode, neighbors[lateralIdx]);

        const axisLen1 = walkBranchLength(graph, junctionNode, neighbors[i]);
        const axisLen2 = walkBranchLength(graph, junctionNode, neighbors[j]);
        const lateralLen = walkBranchLength(graph, junctionNode, neighbors[lateralIdx]);

        let axisOrientation = "diagonal";
        if (d1[0] === 0) axisOrientation = "horizontal";
        else if (d1[1] === 0) axisOrientation = "vertical";

        const symmetry = axisLen1 === axisLen2 ? "centered" : "off-center";

        const totalLen = axisLen1 + axisLen2 + lateralLen;
        const lateralProportion = lateralLen / totalLen;
        const lateralClass =
          lateralLen <= 1 ? "stub" : lateralProportion < 0.35 ? "short" : "long";

        return {
          isT: true,
          axisDirection: d1,
          lateralDirection: lateral,
          axisLength: axisLen1 + axisLen2,
          axisLen1,
          axisLen2,
          lateralLength: lateralLen,
          axisOrientation,
          symmetry,
          lateralClass,
        };
      }
    }
  }

  return { isT: false, isY: true };
}

// ------------------------------------------------------------
// PERIMETER ANALYSIS
// ------------------------------------------------------------

function getPerimeterInfo(bits: number[], edges: Edge[], cols: number, rows: number): PerimeterInfo {
  let perimeterTotal = 0;
  let perimeterActive = 0;
  let interiorActive = 0;

  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    const onPerimeter =
      (e.type === "h" && (e.r === 0 || e.r === rows - 1)) ||
      (e.type === "v" && (e.c === 0 || e.c === cols - 1));

    if (onPerimeter) {
      perimeterTotal++;
      if (bits[i]) perimeterActive++;
    } else if (bits[i]) {
      interiorActive++;
    }
  }

  return {
    perimeterTotal,
    perimeterActive,
    ratio: perimeterTotal > 0 ? perimeterActive / perimeterTotal : 0,
    interiorActive,
  };
}

// ------------------------------------------------------------
// CLASSIFIER
// ------------------------------------------------------------

const TOPO_CATEGORIES = [
  { id: "all", label: "All", icon: "*" },
  { id: "line", label: "Line", icon: "\u2500" },
  { id: "bend", label: "Bend", icon: "\u2514" },
  { id: "sideways-t", label: "Sideways T", icon: "\u22A3" },
  { id: "y-fork", label: "Y Fork", icon: "\u2534" },
  { id: "cross", label: "Cross", icon: "\u253C" },
  { id: "fork", label: "Multi-fork", icon: "\u2533" },
  { id: "loop", label: "Loop", icon: "\u25CB" },
  { id: "enclosure", label: "Enclosure", icon: "\u53E3" },
  { id: "bisected", label: "Bisected", icon: "\u65E5" },
  { id: "partitioned", label: "Partitioned", icon: "\u7530" },
  { id: "multi", label: "Multi-part", icon: "\u2016" },
  { id: "complex", label: "Complex", icon: "\u2042" },
  { id: "promoted", label: "Promoted", icon: "\u2192" },
];

function classifyGlyph(bits: number[], edges: Edge[], cols: number, rows: number): Classification {
  let strokeCount = 0;
  for (let i = 0; i < bits.length; i++) strokeCount += bits[i];
  if (strokeCount === 0) return { category: "void", label: "\u7121", strokeCount: 0 };

  const graph = buildGraph(bits, edges);
  const components = getComponents(graph);
  const degreeProfile = getDegreeProfile(graph);
  const deg3 = degreeProfile[3] || 0;
  const deg4 = degreeProfile[4] || 0;
  const cycle = hasCycle(graph);
  const perim = getPerimeterInfo(bits, edges, cols, rows);
  const nodeCount = graph.size;

  const base = { strokeCount, nodeCount, degreeProfile };

  if (components.length > 1) {
    return { category: "multi", label: "\u2016", components: components.length, ...base };
  }

  if (!cycle) {
    if (strokeCount === 1) {
      return { category: "line", label: "\u2500", ...base };
    }

    if (deg3 === 0 && deg4 === 0) {
      if (pathHasTurn(graph)) {
        return { category: "bend", label: "\u2514", ...base };
      }
      return { category: "line", label: "\u2500", ...base };
    }

    if (deg4 === 1 && deg3 === 0) {
      let validCross = true;
      for (const dk in degreeProfile) {
        const d = parseInt(dk, 10);
        if (d !== 1 && d !== 2 && d !== 4) {
          validCross = false;
          break;
        }
      }
      if (validCross) {
        return { category: "cross", label: "\u253C", ...base };
      }
    }

    if (deg4 >= 2) {
      return { category: "complex", label: "\u2042", ...base };
    }

    if (deg3 === 1 && deg4 === 0) {
      const tInfo = analyzeTJunction(graph);

      if (tInfo.isT) {
        let tLabel = "\u22A3";
        if (tInfo.axisOrientation === "horizontal") tLabel = "\u22A4";
        else if (tInfo.axisOrientation === "vertical") tLabel = "\u22A3";
        else tLabel = "\u2E17";

        return {
          category: "sideways-t",
          label: tLabel,
          tInfo,
          tSubtype: `${tInfo.axisOrientation}/${tInfo.symmetry}/${tInfo.lateralClass}`,
          ...base,
        };
      }

      if (tInfo.isY) {
        return { category: "y-fork", label: "\u2534", ...base };
      }

      return { category: "sideways-t", label: "\u22A3", ...base };
    }

    if (deg3 >= 2 || (deg3 >= 1 && deg4 >= 1)) {
      return { category: "fork", label: "\u2533", ...base };
    }

    return { category: "complex", label: "\u2042", ...base };
  }

  if (deg3 === 0 && deg4 === 0) {
    if (perim.ratio >= 0.95) {
      return { category: "enclosure", label: "\u53E3", ...base };
    }
    return { category: "loop", label: "\u25CB", ...base };
  }

  if (perim.ratio >= 0.7) {
    if (perim.interiorActive >= 3) {
      return { category: "partitioned", label: "\u7530", ...base };
    }
    if (perim.interiorActive >= 1) {
      return { category: "bisected", label: "\u65E5", ...base };
    }
    return { category: "enclosure", label: "\u53E3", ...base };
  }

  if (perim.interiorActive > 0) {
    return { category: "bisected", label: "\u65E5", ...base };
  }

  return { category: "loop", label: "\u25CB", ...base };
}

// ------------------------------------------------------------
// DRAWING
// ------------------------------------------------------------

function drawGlyphToCtx(
  ctx: CanvasRenderingContext2D,
  bits: number[],
  edges: Edge[],
  cols: number,
  rows: number,
  x: number,
  y: number,
  w: number,
  h: number,
  rotation: number,
  color: string,
  lineWidth: number
) {
  const pad = Math.min(w, h) * 0.12;
  const iw = w - pad * 2;
  const ih = h - pad * 2;
  const cellW = cols > 1 ? iw / (cols - 1) : iw;
  const cellH = rows > 1 ? ih / (rows - 1) : ih;

  ctx.save();
  ctx.translate(x + w / 2, y + h / 2);
  ctx.rotate((rotation * Math.PI) / 180);
  ctx.translate(-w / 2, -h / 2);
  ctx.strokeStyle = color;
  ctx.lineWidth = lineWidth;
  ctx.lineCap = "round";

  for (let i = 0; i < edges.length; i++) {
    if (!bits[i]) continue;
    const e = edges[i];
    ctx.beginPath();
    ctx.moveTo(pad + e.c * cellW, pad + e.r * cellH);
    ctx.lineTo(pad + e.c2 * cellW, pad + e.r2 * cellH);
    ctx.stroke();
  }

  ctx.restore();
}

function drawCompoundToCtx(
  ctx: CanvasRenderingContext2D,
  compound: Compound,
  edges: Edge[],
  cols: number,
  rows: number,
  x: number,
  y: number,
  w: number,
  h: number,
  depth: number
) {
  if (!compound || !compound.layout || !LAYOUTS[compound.layout]) return;
  if (depth > 6) return;

  const positions = LAYOUTS[compound.layout].positions(w, h);

  for (let i = 0; i < positions.length; i++) {
    const pos = positions[i];
    const slotId = compound.slots[i];
    if (slotId == null) continue;

    const glyph = compound.glyphData[String(slotId)];
    if (!glyph) continue;

    if (glyph.isCompound && glyph.compound) {
      drawCompoundToCtx(
        ctx,
        glyph.compound,
        edges,
        cols,
        rows,
        x + pos.x,
        y + pos.y,
        pos.w,
        pos.h,
        depth + 1
      );
    } else if (glyph.bits) {
      drawGlyphToCtx(
        ctx,
        glyph.bits,
        edges,
        cols,
        rows,
        x + pos.x,
        y + pos.y,
        pos.w,
        pos.h,
        glyph.rotation || 0,
        "#e8e4df",
        Math.max(1.2, Math.min(pos.w, pos.h) * 0.045)
      );
    }
  }
}

// ------------------------------------------------------------
// LAYOUTS
// ------------------------------------------------------------

const LAYOUTS: Record<string, LayoutDef> = {
  single: {
    label: "\u25A1",
    name: "Single",
    slots: 1,
    positions: (w, h) => [{ x: 0, y: 0, w, h }],
  },
  "left-right": {
    label: "\u2FF0",
    name: "Side by side",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: 0, w: w * 0.48, h },
      { x: w * 0.52, y: 0, w: w * 0.48, h },
    ],
  },
  "top-bottom": {
    label: "\u2FF1",
    name: "Stacked",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: 0, w, h: h * 0.48 },
      { x: 0, y: h * 0.52, w, h: h * 0.48 },
    ],
  },
  surround: {
    label: "\u2FF4",
    name: "Full surround",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: 0, w, h },
      { x: w * 0.2, y: h * 0.2, w: w * 0.6, h: h * 0.6 },
    ],
  },
  "surround-left": {
    label: "\u2FF7",
    name: "Left surround",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: 0, w: w * 0.55, h },
      { x: w * 0.35, y: h * 0.15, w: w * 0.6, h: h * 0.7 },
    ],
  },
  "surround-top": {
    label: "\u2FF5",
    name: "Top surround",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: 0, w, h: h * 0.55 },
      { x: w * 0.15, y: h * 0.35, w: w * 0.7, h: h * 0.6 },
    ],
  },
  "surround-bottom": {
    label: "\u2FF6",
    name: "Open top",
    slots: 2,
    positions: (w, h) => [
      { x: 0, y: h * 0.35, w, h: h * 0.65 },
      { x: w * 0.15, y: 0, w: w * 0.7, h: h * 0.7 },
    ],
  },
  "three-across": {
    label: "\u2FF2",
    name: "Three across",
    slots: 3,
    positions: (w, h) => [
      { x: 0, y: 0, w: w * 0.31, h },
      { x: w * 0.345, y: 0, w: w * 0.31, h },
      { x: w * 0.69, y: 0, w: w * 0.31, h },
    ],
  },
  "three-stacked": {
    label: "\u2FF3",
    name: "Three stacked",
    slots: 3,
    positions: (w, h) => [
      { x: 0, y: 0, w, h: h * 0.31 },
      { x: 0, y: h * 0.345, w, h: h * 0.31 },
      { x: 0, y: h * 0.69, w, h: h * 0.31 },
    ],
  },
  "top-lr": {
    label: "\u2FF1\u2FF0",
    name: "Top + split bottom",
    slots: 3,
    positions: (w, h) => [
      { x: 0, y: 0, w, h: h * 0.48 },
      { x: 0, y: h * 0.52, w: w * 0.48, h: h * 0.48 },
      { x: w * 0.52, y: h * 0.52, w: w * 0.48, h: h * 0.48 },
    ],
  },
  "lr-bottom": {
    label: "\u2FF0\u2FF1",
    name: "Split top + bottom",
    slots: 3,
    positions: (w, h) => [
      { x: 0, y: 0, w: w * 0.48, h: h * 0.48 },
      { x: w * 0.52, y: 0, w: w * 0.48, h: h * 0.48 },
      { x: 0, y: h * 0.52, w, h: h * 0.48 },
    ],
  },
  quad: {
    label: "\u56DB",
    name: "Four quadrants",
    slots: 4,
    positions: (w, h) => [
      { x: 0, y: 0, w: w * 0.48, h: h * 0.48 },
      { x: w * 0.52, y: 0, w: w * 0.48, h: h * 0.48 },
      { x: 0, y: h * 0.52, w: w * 0.48, h: h * 0.48 },
      { x: w * 0.52, y: h * 0.52, w: w * 0.48, h: h * 0.48 },
    ],
  },
};

// ------------------------------------------------------------
// UI HELPERS
// ------------------------------------------------------------

function compactTSubtype(code: string): string {
  if (!code) return "";
  const [axis, symmetry, lateral] = code.split("/");
  const a = axis ? axis.charAt(0) : "?";
  const s = symmetry ? symmetry.charAt(0) : "?";
  let l = "?";
  if (lateral === "stub") l = "st";
  else if (lateral === "short") l = "sh";
  else if (lateral === "long") l = "lg";
  return `${a}/${s}/${l}`;
}

interface BtnProps {
  active?: boolean;
  onClick: () => void;
  title?: string;
  dimColor?: string;
  pad?: string;
  fontSize?: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}

function Btn(props: BtnProps) {
  const active = props.active;
  return (
    <button
      onClick={props.onClick}
      title={props.title || ""}
      style={{
        background: active ? "#a0845c" : "#1a1714",
        color: active ? "#0f0d0a" : props.dimColor || "#8a7e70",
        border: `1px solid ${active ? "#c4a46c" : "#2a251f"}`,
        borderRadius: 4,
        padding: props.pad || "3px 10px",
        fontSize: props.fontSize || 12,
        cursor: "pointer",
        fontFamily: "JetBrains Mono, monospace",
        transition: "all 0.12s",
        ...(props.style || {}),
      }}
    >
      {props.children}
    </button>
  );
}

interface MiniGlyphProps {
  bits: number[];
  edges: Edge[];
  cols: number;
  rows: number;
  size: number;
  rotation?: number;
  color?: string;
  selected?: boolean;
  onClick: () => void;
  classification?: Classification;
}

function MiniGlyph(props: MiniGlyphProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const bits = props.bits;
  const edg = props.edges;
  const cs = props.cols;
  const rs = props.rows;
  const sz = props.size;
  const rot = props.rotation || 0;
  const clr = props.color || "#c4b8a8";
  const cls = props.classification;

  useEffect(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    cv.width = sz * 2;
    cv.height = sz * 2;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    ctx.scale(2, 2);
    ctx.clearRect(0, 0, sz, sz);
    drawGlyphToCtx(ctx, bits, edg, cs, rs, 0, 0, sz, sz, rot, clr, Math.max(1, sz * 0.05));
  }, [bits, edg, cs, rs, sz, rot, clr]);

  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      <canvas
        ref={canvasRef}
        width={sz * 2}
        height={sz * 2}
        onClick={props.onClick}
        title={cls?.tSubtype || cls?.category || ""}
        style={{
          width: sz,
          height: sz,
          cursor: "pointer",
          border: props.selected ? "2px solid #c4a46c" : "1px solid #2a251f",
          borderRadius: 4,
          background: props.selected ? "#1f1a14" : "transparent",
          transition: "border-color 0.15s",
          display: "block",
        }}
      />
      {cls && (
        <div
          style={{
            position: "absolute",
            bottom: 1,
            right: 2,
            fontSize: 8,
            color: cls.tSubtype ? "#8b6c3e" : "#4a4238",
            fontFamily: "JetBrains Mono, monospace",
            pointerEvents: "none",
          }}
        >
          {cls.label}
          {cls.tSubtype && (
            <span style={{ fontSize: 6, display: "block", color: "#5a4a38" }}>
              {compactTSubtype(cls.tSubtype)}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

interface PromotedMiniProps {
  compound: Compound;
  edges: Edge[];
  cols: number;
  rows: number;
  size: number;
  selected?: boolean;
  onClick: () => void;
  badge?: string;
  badgeColor?: string;
}

function PromotedMini(props: PromotedMiniProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const comp = props.compound;
  const edg = props.edges;
  const cs = props.cols;
  const rs = props.rows;
  const sz = props.size;

  useEffect(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    cv.width = sz * 2;
    cv.height = sz * 2;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    ctx.scale(2, 2);
    ctx.clearRect(0, 0, sz, sz);
    drawCompoundToCtx(ctx, comp, edg, cs, rs, 0, 0, sz, sz, 0);
  }, [comp, edg, cs, rs, sz]);

  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      <canvas
        ref={canvasRef}
        width={sz * 2}
        height={sz * 2}
        onClick={props.onClick}
        style={{
          width: sz,
          height: sz,
          cursor: "pointer",
          border: props.selected ? "2px solid #8b6c3e" : "1px solid #3d2e1a",
          borderRadius: 4,
          background: props.selected ? "#1c1510" : "#0f0d0a",
          transition: "border-color 0.15s",
          display: "block",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 1,
          left: 2,
          fontSize: 7,
          color: props.badgeColor || "#8b6c3e",
          fontFamily: "JetBrains Mono, monospace",
          pointerEvents: "none",
        }}
      >
        {props.badge ?? "P\u2192O"}
      </div>
    </div>
  );
}

interface GlyphDetailPanelProps {
  compound: Compound;
  allCompounds: Compound[];
  edges: Edge[];
  cols: number;
  rows: number;
  onUpdate: (updates: Partial<Compound>) => void;
  onClose: () => void;
  onDelete: () => void;
}

function GlyphDetailPanel(props: GlyphDetailPanelProps) {
  const { compound, allCompounds, edges, cols, rows, onUpdate, onClose, onDelete } = props;
  const [newDefText, setNewDefText] = useState("");
  const [newDefSource, setNewDefSource] = useState("");
  const [bulkText, setBulkText] = useState("");
  const [bulkMode, setBulkMode] = useState(false);
  const [newImgUrl, setNewImgUrl] = useState("");
  const [newImgLabel, setNewImgLabel] = useState("");
  const [confirmDelete, setConfirmDelete] = useState(false);

  const locked = compound.locked ?? false;

  const activeDef = compound.definitions?.[compound.activeDefinitionIndex ?? -1] ?? null;

  // Find compounds that reference this glyph in their slots
  const usedIn = useMemo(() => {
    return allCompounds.filter(
      (c) => c.id !== compound.id && c.slots.some((s) => String(s) === compound.id)
    );
  }, [allCompounds, compound.id]);

  const addDefinition = () => {
    const text = newDefText.trim();
    if (!text) return;
    const defs = (compound.definitions || []).concat({
      text,
      source: newDefSource.trim() || undefined,
    });
    const updates: Partial<Compound> = { definitions: defs };
    if (compound.activeDefinitionIndex == null) updates.activeDefinitionIndex = 0;
    onUpdate(updates);
    setNewDefText("");
    setNewDefSource("");
  };

  const bulkAddDefinitions = () => {
    const lines = bulkText.split("\n").map((l) => l.trim()).filter(Boolean);
    if (lines.length === 0) return;
    const newDefs: Definition[] = lines.map((line) => {
      // Support "text | source" or "text [source]" or just "text"
      const pipeMatch = line.match(/^(.+?)\s*\|\s*(.+)$/);
      if (pipeMatch) return { text: pipeMatch[1].trim(), source: pipeMatch[2].trim() };
      const bracketMatch = line.match(/^(.+?)\s*\[(.+?)\]\s*$/);
      if (bracketMatch) return { text: bracketMatch[1].trim(), source: bracketMatch[2].trim() };
      // Strip leading number+period patterns like "1. " or "　1. "
      const stripped = line.replace(/^[\s\u3000]*\d+\.\s*/, "");
      return { text: stripped || line };
    });
    const defs = (compound.definitions || []).concat(newDefs);
    const updates: Partial<Compound> = { definitions: defs };
    if (compound.activeDefinitionIndex == null) updates.activeDefinitionIndex = 0;
    onUpdate(updates);
    setBulkText("");
    setBulkMode(false);
  };

  const removeDefinition = (idx: number) => {
    const defs = (compound.definitions || []).filter((_, i) => i !== idx);
    let activeIdx = compound.activeDefinitionIndex ?? 0;
    if (idx === activeIdx) activeIdx = defs.length > 0 ? 0 : -1;
    else if (idx < activeIdx) activeIdx = activeIdx - 1;
    onUpdate({
      definitions: defs,
      activeDefinitionIndex: defs.length > 0 ? Math.max(0, activeIdx) : undefined,
    });
  };

  const addImage = () => {
    const url = newImgUrl.trim();
    if (!url) return;
    const images = (compound.images || []).concat({
      url,
      label: newImgLabel.trim() || "Variant",
    });
    onUpdate({ images });
    setNewImgUrl("");
    setNewImgLabel("");
  };

  const removeImage = (idx: number) => {
    const images = (compound.images || []).filter((_, i) => i !== idx);
    onUpdate({ images });
  };

  const sectionStyle: React.CSSProperties = {
    borderTop: "1px solid #1f1c17",
    padding: "10px 0",
  };

  const labelStyle: React.CSSProperties = {
    fontSize: 9,
    color: "#6b6157",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 6,
  };

  const inputStyle: React.CSSProperties = {
    background: "#0f0d0a",
    border: "1px solid #2a251f",
    color: "#c4b8a8",
    borderRadius: 4,
    padding: "4px 8px",
    fontSize: 11,
    fontFamily: "Crimson Pro, serif",
    outline: "none",
  };

  const smallBtnStyle: React.CSSProperties = {
    background: "#2a251f",
    color: "#c4b8a8",
    border: "1px solid #3d362e",
    borderRadius: 3,
    padding: "3px 8px",
    fontSize: 10,
    cursor: "pointer",
    fontFamily: "JetBrains Mono, monospace",
  };

  return (
    <div
      style={{
        background: "#14110d",
        borderLeft: "1px solid #3d2e1a",
        padding: "16px 16px",
        minHeight: "100vh",
        boxSizing: "border-box",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
        <PromotedMini
          compound={compound}
          edges={edges}
          cols={cols}
          rows={rows}
          size={80}
          onClick={() => {}}
          badge={compound.promoted ? "P\u2192O" : "\u2605"}
          badgeColor={compound.promoted ? "#8b6c3e" : "#6b8b3e"}
        />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 16, color: "#c4a46c", fontWeight: 600 }}>{compound.label}</div>
          {activeDef && (
            <div style={{ fontSize: 12, color: "#6b8b3e", fontStyle: "italic", marginTop: 2 }}>
              {activeDef.text}
            </div>
          )}
        </div>
        <div style={{ display: "flex", gap: 4, flexDirection: "column", alignItems: "flex-end" }}>
          <button
            onClick={onClose}
            style={{
              background: "transparent",
              color: "#5a3d1a",
              border: "1px solid #2a1f14",
              borderRadius: 4,
              padding: "4px 10px",
              fontSize: 14,
              cursor: "pointer",
              lineHeight: 1,
            }}
          >
            {"\u2715"}
          </button>
          <button
            onClick={() => onUpdate({ locked: !locked })}
            style={{
              background: "transparent",
              color: locked ? "#6b8b3e" : "#5a4a38",
              border: `1px solid ${locked ? "#3d5a1a" : "#2a1f14"}`,
              borderRadius: 4,
              padding: "2px 8px",
              fontSize: 9,
              cursor: "pointer",
              fontFamily: "JetBrains Mono, monospace",
            }}
            title={locked ? "Unlock editing" : "Lock editing"}
          >
            {locked ? "\uD83D\uDD12 Locked" : "\uD83D\uDD13 Unlocked"}
          </button>
        </div>
      </div>

      {/* Definitions */}
      <div style={sectionStyle}>
        <div style={labelStyle}>Definitions</div>
        {(compound.definitions || []).map((def, idx) => {
          const isActive = idx === (compound.activeDefinitionIndex ?? -1);
          return (
            <div
              key={idx}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                padding: "4px 6px",
                marginBottom: 4,
                border: isActive ? "1px solid #c4a46c" : "1px solid #1f1c17",
                borderRadius: 4,
                background: isActive ? "#1c1a12" : "transparent",
              }}
            >
              <input
                type="radio"
                name={`def-${compound.id}`}
                checked={isActive}
                onChange={() => onUpdate({ activeDefinitionIndex: idx })}
                style={{ accentColor: "#c4a46c" }}
              />
              <div style={{ flex: 1, fontSize: 12, color: "#c4b8a8" }}>
                {def.text}
                {def.source && (
                  <span style={{ fontSize: 9, color: "#5a4a38", marginLeft: 6 }}>
                    [{def.source}]
                  </span>
                )}
              </div>
              {!locked && (
                <button
                  onClick={() => removeDefinition(idx)}
                  style={{
                    background: "transparent",
                    color: "#5a3d1a",
                    border: "none",
                    cursor: "pointer",
                    fontSize: 14,
                    lineHeight: 1,
                    padding: "0 4px",
                  }}
                >
                  {"\u00D7"}
                </button>
              )}
            </div>
          );
        })}
        {!locked && (
          <>
            <div style={{ display: "flex", gap: 6, marginTop: 6, marginBottom: 4 }}>
              <button
                onClick={() => setBulkMode(false)}
                style={{
                  ...smallBtnStyle,
                  background: !bulkMode ? "#3d2e1a" : "#1a1714",
                  color: !bulkMode ? "#c4a46c" : "#5a4a38",
                }}
              >
                + Single
              </button>
              <button
                onClick={() => setBulkMode(true)}
                style={{
                  ...smallBtnStyle,
                  background: bulkMode ? "#3d2e1a" : "#1a1714",
                  color: bulkMode ? "#c4a46c" : "#5a4a38",
                }}
              >
                Paste bulk
              </button>
            </div>
            {!bulkMode ? (
              <div style={{ display: "flex", gap: 4 }}>
                <textarea
                  value={newDefText}
                  onChange={(e) => setNewDefText(e.target.value)}
                  placeholder="New definition..."
                  rows={2}
                  style={{ ...inputStyle, flex: 2, resize: "vertical" }}
                />
                <input
                  type="text"
                  value={newDefSource}
                  onChange={(e) => setNewDefSource(e.target.value)}
                  placeholder="Source"
                  style={{ ...inputStyle, flex: 1 }}
                />
                <button onClick={addDefinition} style={smallBtnStyle}>
                  Add
                </button>
              </div>
            ) : (
              <div>
                <textarea
                  value={bulkText}
                  onChange={(e) => setBulkText(e.target.value)}
                  placeholder={"Paste definitions, one per line:\nway/path\nvirtue/power | Shuowen\nunity [39017.com]"}
                  rows={6}
                  style={{ ...inputStyle, width: "100%", resize: "vertical", boxSizing: "border-box", marginBottom: 4 }}
                />
                <button onClick={bulkAddDefinitions} style={smallBtnStyle}>
                  Add all ({bulkText.split("\n").filter((l) => l.trim()).length} lines)
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* Paleographic Images */}
      <div style={sectionStyle}>
        <div style={labelStyle}>Paleographic Variants</div>
        {(compound.images || []).length === 0 && (
          <div style={{ fontSize: 11, color: "#3d362e", marginBottom: 6 }}>No images added yet</div>
        )}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 6 }}>
          {(compound.images || []).map((img, idx) => (
            <div key={idx} style={{ textAlign: "center", position: "relative" }}>
              <img
                src={img.url}
                alt={img.label}
                style={{
                  width: 64,
                  height: 64,
                  objectFit: "contain",
                  border: "1px solid #2a251f",
                  borderRadius: 4,
                  background: "#0f0d0a",
                }}
              />
              <div style={{ fontSize: 8, color: "#5a4a38", marginTop: 2 }}>{img.label}</div>
              {!locked && (
                <button
                  onClick={() => removeImage(idx)}
                  style={{
                    position: "absolute",
                    top: -4,
                    right: -4,
                    background: "#1a1714",
                    color: "#5a3d1a",
                    border: "1px solid #2a1f14",
                    borderRadius: "50%",
                    width: 16,
                    height: 16,
                    fontSize: 10,
                    cursor: "pointer",
                    lineHeight: 1,
                    padding: 0,
                  }}
                >
                  {"\u00D7"}
                </button>
              )}
            </div>
          ))}
        </div>
        {!locked && (
          <div style={{ display: "flex", gap: 4 }}>
            <input
              type="text"
              value={newImgUrl}
              onChange={(e) => setNewImgUrl(e.target.value)}
              placeholder="Image URL"
              style={{ ...inputStyle, flex: 2 }}
            />
            <input
              type="text"
              value={newImgLabel}
              onChange={(e) => setNewImgLabel(e.target.value)}
              placeholder="Label (e.g. Oracle Bone)"
              style={{ ...inputStyle, flex: 1 }}
            />
            <button onClick={addImage} style={smallBtnStyle}>
              Add
            </button>
          </div>
        )}
      </div>

      {/* Guodian Location */}
      <div style={sectionStyle}>
        <div style={labelStyle}>Guodian Location</div>
        <input
          type="text"
          value={compound.guodianLocation || ""}
          onChange={(e) => !locked && onUpdate({ guodianLocation: e.target.value })}
          onBlur={(e) => !locked && onUpdate({ guodianLocation: e.target.value })}
          placeholder="e.g. Slip 1, Chapter 19"
          readOnly={locked}
          style={{ ...inputStyle, width: "100%", boxSizing: "border-box", opacity: locked ? 0.6 : 1 }}
        />
      </div>

      {/* Percolation Preview */}
      <div style={sectionStyle}>
        <div style={labelStyle}>Percolation</div>
        {activeDef ? (
          <div style={{ fontSize: 12, color: "#6b8b3e", marginBottom: 6 }}>
            Active: <em>{activeDef.text}</em>
            {activeDef.source && (
              <span style={{ fontSize: 9, color: "#5a4a38", marginLeft: 4 }}>
                [{activeDef.source}]
              </span>
            )}
          </div>
        ) : (
          <div style={{ fontSize: 11, color: "#3d362e", marginBottom: 6 }}>
            No active definition set
          </div>
        )}
        {usedIn.length > 0 && (
          <div>
            <div style={{ fontSize: 9, color: "#5a4a38", marginBottom: 4 }}>
              Used in {usedIn.length} compound{usedIn.length !== 1 ? "s" : ""}:
            </div>
            {usedIn.map((uc) => (
              <div
                key={uc.id}
                style={{
                  fontSize: 11,
                  color: "#8a7e70",
                  padding: "2px 0",
                  display: "flex",
                  gap: 6,
                  alignItems: "baseline",
                }}
              >
                <span style={{ color: "#c4a46c" }}>{uc.label}</span>
                {activeDef && (
                  <span style={{ fontSize: 9, color: "#6b8b3e", fontStyle: "italic" }}>
                    ({activeDef.text})
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
        {usedIn.length === 0 && (
          <div style={{ fontSize: 11, color: "#3d362e" }}>Not used in any other compounds</div>
        )}
      </div>

      {/* Delete section */}
      {!locked && (
        <div style={sectionStyle}>
          {!confirmDelete ? (
            <button
              onClick={() => setConfirmDelete(true)}
              style={{
                background: "transparent",
                color: "#8b2020",
                border: "1px solid #3d1a1a",
                borderRadius: 4,
                padding: "4px 12px",
                fontSize: 10,
                cursor: "pointer",
                fontFamily: "JetBrains Mono, monospace",
              }}
            >
              Delete this glyph
            </button>
          ) : (
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <span style={{ fontSize: 11, color: "#8b2020" }}>Delete permanently?</span>
              <button
                onClick={onDelete}
                style={{
                  background: "#3d1a1a",
                  color: "#e8c4c4",
                  border: "1px solid #8b2020",
                  borderRadius: 4,
                  padding: "4px 12px",
                  fontSize: 10,
                  cursor: "pointer",
                  fontFamily: "JetBrains Mono, monospace",
                  fontWeight: 600,
                }}
              >
                Yes, delete
              </button>
              <button
                onClick={() => setConfirmDelete(false)}
                style={{
                  background: "transparent",
                  color: "#5a4a38",
                  border: "1px solid #2a1f14",
                  borderRadius: 4,
                  padding: "4px 12px",
                  fontSize: 10,
                  cursor: "pointer",
                  fontFamily: "JetBrains Mono, monospace",
                }}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

interface CompositionCanvasProps {
  slots: (string | number | null)[];
  layout: string;
  allGlyphs: Record<string, GlyphData>;
  edges: Edge[];
  cols: number;
  rows: number;
  canvasSize: number;
  activeSlot: number;
}

function CompositionCanvas(props: CompositionCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sz = props.canvasSize;

  useEffect(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    cv.width = sz * 2;
    cv.height = sz * 2;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    ctx.scale(2, 2);

    ctx.fillStyle = "#0f0d0a";
    ctx.fillRect(0, 0, sz, sz);
    ctx.strokeStyle = "#1f1c17";
    ctx.lineWidth = 1;
    ctx.strokeRect(4, 4, sz - 8, sz - 8);

    const lay = props.layout;
    if (!lay || !LAYOUTS[lay]) return;

    const positions = LAYOUTS[lay].positions(sz - 16, sz - 16);

    for (let i = 0; i < positions.length; i++) {
      const pos = positions[i];
      const isActive = i === props.activeSlot;

      ctx.strokeStyle = isActive ? "#3d362e" : "#1a1714";
      ctx.lineWidth = isActive ? 1 : 0.5;
      ctx.setLineDash([3, 3]);
      ctx.strokeRect(8 + pos.x, 8 + pos.y, pos.w, pos.h);
      ctx.setLineDash([]);

      if (isActive && props.slots[i] == null) {
        ctx.fillStyle = "#1f1a14";
        ctx.fillRect(8 + pos.x + 1, 8 + pos.y + 1, pos.w - 2, pos.h - 2);
        ctx.fillStyle = "#3d362e";
        ctx.font = "11px JetBrains Mono, monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(i + 1), 8 + pos.x + pos.w / 2, 8 + pos.y + pos.h / 2);
      }

      const slotId = props.slots[i];
      if (slotId == null) continue;
      const g = props.allGlyphs[String(slotId)];
      if (!g) continue;

      if (g.isCompound && g.compound) {
        drawCompoundToCtx(
          ctx,
          g.compound,
          props.edges,
          props.cols,
          props.rows,
          8 + pos.x,
          8 + pos.y,
          pos.w,
          pos.h,
          0
        );
      } else if (g.bits) {
        drawGlyphToCtx(
          ctx,
          g.bits,
          props.edges,
          props.cols,
          props.rows,
          8 + pos.x,
          8 + pos.y,
          pos.w,
          pos.h,
          g.rotation || 0,
          "#e8e4df",
          Math.max(1.5, Math.min(pos.w, pos.h) * 0.045)
        );
      }
    }
  }, [
    props.slots,
    props.layout,
    props.allGlyphs,
    props.edges,
    props.cols,
    props.rows,
    sz,
    props.activeSlot,
  ]);

  return <canvas ref={canvasRef} style={{ width: sz, height: sz, border: "1px solid #3d362e", borderRadius: 8 }} />;
}

// ------------------------------------------------------------
// MAIN COMPONENT
// ------------------------------------------------------------

const MAX_PALETTE = 600;

type SlotValue = string | number | null;

export default function GlyphComposer() {
  const [gridSize, setGridSize] = useState(3);
  const [diagonals, setDiagonals] = useState(false);
  const [paletteRotation, setPaletteRotation] = useState(0);
  const [minStrokes, setMinStrokes] = useState(1);
  const [maxStrokes, setMaxStrokes] = useState(20);
  const [layout, setLayout] = useState("single");
  const [selGlyph, setSelGlyph] = useState<SlotValue>(null);
  const [activeSlot, setActiveSlot] = useState(0);
  const [slots, setSlots] = useState<SlotValue[]>([null, null, null, null]);
  const [glyphBank, setGlyphBank] = useState<Record<string, GlyphData>>({});
  const [compounds, setCompounds] = useState<Compound[]>(() => loadLibrary());
  const [compoundLabel, setCompoundLabel] = useState("");
  const [filterCat, setFilterCat] = useState("all");
  const [tSubFilter, setTSubFilter] = useState("all");
  const [detailCompoundId, setDetailCompoundId] = useState<string | null>(null);
  const [showTopoLegend, setShowTopoLegend] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const updateCompoundMeta = useCallback((compId: string, updates: Partial<Compound>) => {
    setCompounds((prev) =>
      prev.map((c) => (c.id === compId ? { ...c, ...updates } : c))
    );
  }, []);

  const deleteCompound = useCallback((compId: string) => {
    setCompounds((prev) => prev.filter((c) => c.id !== compId));
    setGlyphBank((prev) => {
      const bank = { ...prev };
      delete bank[compId];
      return bank;
    });
    if (detailCompoundId === compId) setDetailCompoundId(null);
  }, [detailCompoundId]);

  const detailCompound = detailCompoundId
    ? compounds.find((c) => c.id === detailCompoundId) ?? null
    : null;

  // Auto-save library to localStorage
  useEffect(() => {
    saveLibrary(compounds);
  }, [compounds]);

  // Hydrate glyphBank from saved compounds on mount
  useEffect(() => {
    const loaded = loadLibrary();
    if (loaded.length > 0) {
      setGlyphBank((prev) => {
        const bank = { ...prev };
        for (const comp of loaded) {
          bank[comp.id] = { isCompound: true, compound: comp, rotation: 0 };
        }
        return bank;
      });
    }
  }, []);

  const cols = gridSize;
  const rows = gridSize;
  const edges = useMemo(() => getEdges(cols, rows, diagonals), [cols, rows, diagonals]);
  const numEdges = edges.length;

  const paletteGlyphs = useMemo(() => {
    const total = Math.pow(2, numEdges);
    const result: PaletteGlyph[] = [];
    const limit = Math.min(total, numEdges <= 16 ? total : 50000);

    for (let i = 1; i < limit && result.length < MAX_PALETTE; i++) {
      const bits = indexToEdges(i, numEdges);

      let sc = 0;
      for (let b = 0; b < bits.length; b++) sc += bits[b];
      if (sc < minStrokes || sc > Math.min(maxStrokes, numEdges)) continue;

      const cls = classifyGlyph(bits, edges, cols, rows);
      if (filterCat !== "all" && filterCat !== "promoted" && cls.category !== filterCat) continue;
      if (filterCat === "sideways-t" && tSubFilter !== "all" && cls.tSubtype !== tSubFilter) continue;

      result.push({ id: i, bits, classification: cls });
    }

    return result;
  }, [numEdges, edges, cols, rows, minStrokes, maxStrokes, filterCat, tSubFilter]);

  const promotedItems = compounds.filter((c) => c.promoted);

  const sidewaysTSubtypeCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    if (filterCat !== "sideways-t") return counts;

    paletteGlyphs.forEach((g) => {
      if (g.classification.category === "sideways-t" && g.classification.tSubtype) {
        counts[g.classification.tSubtype] = (counts[g.classification.tSubtype] || 0) + 1;
      }
    });

    return counts;
  }, [paletteGlyphs, filterCat]);

  const clearCanvas = useCallback(() => {
    setSlots([null, null, null, null]);
    setActiveSlot(0);
    setSelGlyph(null);
  }, []);

  const selectLayoutAndClear = useCallback((key: string) => {
    setLayout(key);
    setSlots([null, null, null, null]);
    setActiveSlot(0);
    setSelGlyph(null);
  }, []);

  const placeGlyph = useCallback(
    (glyphId: SlotValue, bits: number[] | null, isCompound: boolean, compound: Compound | null) => {
      if (glyphId == null) return;
      const key = String(glyphId);
      const newBank = { ...glyphBank };

      if (isCompound && compound) {
        newBank[key] = { isCompound: true, compound, rotation: 0 };
      } else if (bits) {
        newBank[key] = { bits, rotation: paletteRotation };
      }

      setGlyphBank(newBank);

      const newSlots = slots.slice();
      newSlots[activeSlot] = glyphId;
      setSlots(newSlots);
      setSelGlyph(glyphId);

      const layoutDef = LAYOUTS[layout];
      if (layoutDef) {
        for (let j = 1; j <= layoutDef.slots; j++) {
          const next = (activeSlot + j) % layoutDef.slots;
          if (newSlots[next] == null) {
            setActiveSlot(next);
            break;
          }
        }
      }
    },
    [glyphBank, slots, activeSlot, layout, paletteRotation]
  );

  function collectGlyphRecursive(
    glyphId: string,
    bank: Record<string, GlyphData>,
    collected: Record<string, GlyphData>
  ) {
    if (collected[glyphId]) return;
    const glyph = bank[glyphId];
    if (!glyph) return;

    collected[glyphId] = JSON.parse(JSON.stringify(glyph));

    if (glyph.isCompound && glyph.compound && glyph.compound.slots) {
      const innerBank = glyph.compound.glyphData || {};
      for (let j = 0; j < glyph.compound.slots.length; j++) {
        const innerSlotId = glyph.compound.slots[j];
        if (innerSlotId != null && innerBank[String(innerSlotId)]) {
          collectGlyphRecursive(String(innerSlotId), innerBank, collected);
        }
      }
    }
  }

  function buildRecursiveSnapshot(): Record<string, GlyphData> {
    const snapshot: Record<string, GlyphData> = {};
    for (let i = 0; i < slots.length; i++) {
      if (slots[i] != null) {
        collectGlyphRecursive(String(slots[i]), glyphBank, snapshot);
      }
    }
    return snapshot;
  }

  const saveCompound = useCallback(() => {
    const hasContent = slots.some((s) => s != null);
    if (!hasContent) return null;

    const snapshot = buildRecursiveSnapshot();

    const comp: Compound = {
      id: `saved_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
      layout,
      slots: slots.slice(),
      glyphData: snapshot,
      label: compoundLabel || `compound ${compounds.length + 1}`,
      timestamp: Date.now(),
      promoted: false,
    };

    setCompounds((prev) => prev.concat([comp]));

    const newBank = { ...glyphBank };
    newBank[comp.id] = { isCompound: true, compound: comp, rotation: 0 };
    setGlyphBank(newBank);

    setCompoundLabel("");
    return comp;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layout, slots, glyphBank, compoundLabel, compounds]);

  const promoteCompound = useCallback(() => {
    const hasContent = slots.some((s) => s != null);
    if (!hasContent) return;

    const snapshot = buildRecursiveSnapshot();

    const comp: Compound = {
      id: `promoted_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
      layout,
      slots: slots.slice(),
      glyphData: snapshot,
      label: compoundLabel || `P\u2192O ${compounds.length + 1}`,
      timestamp: Date.now(),
      promoted: true,
    };

    setCompounds((prev) => prev.concat([comp]));

    const newBank = { ...glyphBank };
    newBank[comp.id] = { isCompound: true, compound: comp, rotation: 0 };
    setGlyphBank(newBank);

    setSlots([null, null, null, null]);
    setActiveSlot(0);
    setSelGlyph(null);
    setCompoundLabel("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layout, slots, glyphBank, compoundLabel, compounds]);

  const numSlots = LAYOUTS[layout] ? LAYOUTS[layout].slots : 2;

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f0d0a",
        color: "#e8e4df",
        fontFamily: "Crimson Pro, Georgia, serif",
      }}
    >
      <link
        href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap"
        rel="stylesheet"
      />

      <div style={{ borderBottom: "1px solid #1f1c17", padding: "16px 20px" }}>
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "baseline",
            flexWrap: "wrap",
            gap: 8,
          }}
        >
          <div>
            <h1 style={{ fontSize: 24, fontWeight: 300, color: "#c4a46c", margin: 0, letterSpacing: 2 }}>
              {"\u9053\u751F\u4E00"} Glyph Composer v3.1
            </h1>
            <p
              style={{
                color: "#4a4238",
                fontSize: 12,
                margin: "4px 0 0",
                fontFamily: "JetBrains Mono, monospace",
              }}
            >
              topology {"\u2192"} classification {"\u2192"} composition {"\u2192"} promotion
            </p>
          </div>
          <div
            style={{
              color: "#3d362e",
              fontSize: 11,
              fontFamily: "JetBrains Mono, monospace",
              textAlign: "right",
            }}
          >
            {numEdges} edges {"\u00B7"} 2^{numEdges} = {Math.pow(2, numEdges).toLocaleString()} forms
            {compounds.length > 0 && (
              <span style={{ color: "#8b6c3e" }}>
                {" \u00B7 "}{compounds.length} saved
                {promotedItems.length > 0 && ` (${promotedItems.length} promoted)`}
              </span>
            )}
          </div>
        </div>
      </div>

      <div
        style={{
          maxWidth: 1200,
          margin: "0 auto",
          padding: "16px 20px",
          display: "flex",
          gap: 20,
          flexWrap: "wrap",
        }}
      >
        <div style={{ flex: "1 1 460px", minWidth: 340 }}>
          {compounds.length > 0 && (
            <div
              style={{
                background: "#14110d",
                border: "1px solid #3d2e1a",
                borderRadius: 8,
                marginBottom: 12,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  padding: "10px 16px",
                  borderBottom: "1px solid #2a1f14",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span style={{ fontSize: 11, color: "#8b6c3e", textTransform: "uppercase", letterSpacing: 1 }}>
                  Glyph Library
                </span>
                <span style={{ fontSize: 10, color: "#5a4a38", fontFamily: "JetBrains Mono, monospace" }}>
                  {compounds.length} items
                </span>
              </div>
              <div style={{ padding: 10, display: "flex", flexWrap: "wrap", gap: 6 }}>
                {compounds.map((comp) => (
                  <div key={comp.id} style={{ textAlign: "center" }}>
                    <PromotedMini
                      compound={comp}
                      edges={edges}
                      cols={cols}
                      rows={rows}
                      size={44}
                      selected={selGlyph === comp.id}
                      onClick={() => placeGlyph(comp.id, null, true, comp)}
                      badge={comp.promoted ? "P\u2192O" : "\u2605"}
                      badgeColor={comp.promoted ? "#8b6c3e" : "#6b8b3e"}
                    />
                    <div
                      style={{
                        fontSize: 8,
                        color: "#5a4a38",
                        marginTop: 2,
                        maxWidth: 44,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {comp.label}
                    </div>
                    {comp.definitions?.[comp.activeDefinitionIndex ?? -1] && (
                      <div style={{ fontSize: 7, color: "#6b8b3e", maxWidth: 44, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                        {comp.definitions[comp.activeDefinitionIndex!].text}
                      </div>
                    )}
                    <button
                      onClick={(e) => { e.stopPropagation(); setDetailCompoundId(comp.id); }}
                      style={{
                        fontSize: 8,
                        color: "#c4a46c",
                        background: "#1a1714",
                        border: "1px solid #3d2e1a",
                        borderRadius: 3,
                        padding: "1px 6px",
                        cursor: "pointer",
                        marginTop: 2,
                        fontFamily: "JetBrains Mono, monospace",
                      }}
                      title="Edit details"
                    >
                      Detail
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div
            style={{
              background: "#141210",
              border: "1px solid #1f1c17",
              borderRadius: 8,
              overflow: "hidden",
            }}
          >
            <div style={{ padding: "12px 16px", borderBottom: "1px solid #1f1c17" }}>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center", marginBottom: 10 }}>
                <span style={{ fontSize: 10, color: "#6b6157", textTransform: "uppercase", letterSpacing: 1 }}>Grid</span>
                {[2, 3, 4, 5].map((n) => (
                  <Btn key={n} active={gridSize === n} onClick={() => setGridSize(n)}>
                    {`${n}\u00D7${n}`}
                  </Btn>
                ))}
                <span style={{ width: 1, height: 18, background: "#1f1c17", display: "inline-block" }} />
                <Btn active={diagonals} onClick={() => setDiagonals(!diagonals)}>
                  {diagonals ? "\u2197 Diag" : "\u2197 Off"}
                </Btn>
              </div>

              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center", marginBottom: 10 }}>
                <span style={{ fontSize: 10, color: "#6b6157", textTransform: "uppercase", letterSpacing: 1 }}>Strokes</span>
                <input
                  type="range"
                  min={1}
                  max={numEdges}
                  value={minStrokes}
                  onChange={(e) => setMinStrokes(+e.target.value)}
                  style={{ width: 80, accentColor: "#a0845c" }}
                />
                <span style={{ fontSize: 11, color: "#8a7e70", fontFamily: "JetBrains Mono, monospace" }}>
                  {minStrokes}{"\u2013"}
                  {Math.min(maxStrokes, numEdges)}
                </span>
                <input
                  type="range"
                  min={1}
                  max={numEdges}
                  value={Math.min(maxStrokes, numEdges)}
                  onChange={(e) => setMaxStrokes(+e.target.value)}
                  style={{ width: 80, accentColor: "#a0845c" }}
                />
              </div>

              <div style={{ display: "flex", gap: 4, flexWrap: "wrap", alignItems: "center", marginBottom: 10 }}>
                <span style={{ fontSize: 10, color: "#6b6157", textTransform: "uppercase", letterSpacing: 1 }}>Rot</span>
                {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => (
                  <Btn key={deg} active={paletteRotation === deg} pad="2px 5px" fontSize={10} onClick={() => setPaletteRotation(deg)}>
                    {`${deg}\u00B0`}
                  </Btn>
                ))}
              </div>

              <div style={{ display: "flex", gap: 3, flexWrap: "wrap" }}>
                {TOPO_CATEGORIES.map((cat) => {
                  if (cat.id === "promoted") return null;
                  const active = filterCat === cat.id;
                  return (
                    <button
                      key={cat.id}
                      onClick={() => {
                        setFilterCat(cat.id);
                        setTSubFilter("all");
                      }}
                      style={{
                        background: active ? "#1f1a14" : "transparent",
                        color: active ? "#c4a46c" : "#5a5247",
                        border: `1px solid ${active ? "#3d362e" : "transparent"}`,
                        borderRadius: 4,
                        padding: "2px 7px",
                        fontSize: 10,
                        cursor: "pointer",
                        fontFamily: "JetBrains Mono, monospace",
                      }}
                    >
                      {cat.icon} {cat.label}
                    </button>
                  );
                })}
              </div>

              {filterCat === "sideways-t" && Object.keys(sidewaysTSubtypeCounts).length > 0 && (
                <div
                  style={{
                    display: "flex",
                    gap: 3,
                    flexWrap: "wrap",
                    marginTop: 6,
                    paddingTop: 6,
                    borderTop: "1px solid #1f1c17",
                  }}
                >
                  <span
                    style={{
                      fontSize: 9,
                      color: "#8b6c3e",
                      textTransform: "uppercase",
                      letterSpacing: 1,
                      alignSelf: "center",
                    }}
                  >
                    Subtype
                  </span>
                  <button
                    onClick={() => setTSubFilter("all")}
                    style={{
                      background: tSubFilter === "all" ? "#1c1510" : "transparent",
                      color: tSubFilter === "all" ? "#c4a46c" : "#5a4a38",
                      border: `1px solid ${tSubFilter === "all" ? "#3d2e1a" : "transparent"}`,
                      borderRadius: 3,
                      padding: "1px 6px",
                      fontSize: 9,
                      cursor: "pointer",
                      fontFamily: "JetBrains Mono, monospace",
                    }}
                  >
                    all
                  </button>
                  {Object.keys(sidewaysTSubtypeCounts)
                    .sort()
                    .map((sk) => {
                      const isActive = tSubFilter === sk;
                      return (
                        <button
                          key={sk}
                          onClick={() => setTSubFilter(sk)}
                          style={{
                            background: isActive ? "#1c1510" : "transparent",
                            color: isActive ? "#c4a46c" : "#5a4a38",
                            border: `1px solid ${isActive ? "#3d2e1a" : "transparent"}`,
                            borderRadius: 3,
                            padding: "1px 6px",
                            fontSize: 9,
                            cursor: "pointer",
                            fontFamily: "JetBrains Mono, monospace",
                          }}
                        >
                          {sk} <span style={{ color: "#3d362e" }}>({sidewaysTSubtypeCounts[sk]})</span>
                        </button>
                      );
                    })}
                </div>
              )}
            </div>

            <div
              style={{
                padding: 10,
                maxHeight: 420,
                overflowY: "auto",
                display: "flex",
                flexWrap: "wrap",
                gap: 4,
                alignContent: "flex-start",
              }}
            >
              {paletteGlyphs.length === 0 && (
                <div style={{ color: "#3d362e", fontSize: 13, padding: 20, textAlign: "center", width: "100%" }}>
                  No glyphs match. Adjust filters.
                </div>
              )}
              {paletteGlyphs.map((g) => (
                <MiniGlyph
                  key={g.id}
                  bits={g.bits}
                  edges={edges}
                  cols={cols}
                  rows={rows}
                  size={40}
                  rotation={paletteRotation}
                  selected={selGlyph === g.id}
                  onClick={() => placeGlyph(g.id, g.bits, false, null)}
                  color="#c4b8a8"
                  classification={g.classification}
                />
              ))}
            </div>

            <div
              style={{
                padding: "8px 16px",
                borderTop: "1px solid #1f1c17",
                fontSize: 11,
                color: "#3d362e",
                fontFamily: "JetBrains Mono, monospace",
              }}
            >
              {paletteGlyphs.length} glyphs {"\u00B7"} click to place in slot {activeSlot + 1}
            </div>
          </div>
        </div>

        <div style={{ flex: "1 1 380px", minWidth: 320 }}>
          <div
            style={{
              background: "#141210",
              border: "1px solid #1f1c17",
              borderRadius: 8,
              padding: "8px 12px",
              marginBottom: 8,
            }}
          >
            <div style={{ display: "flex", gap: 3, flexWrap: "wrap", marginBottom: 6 }}>
              {Object.keys(LAYOUTS).map((key) => {
                const L = LAYOUTS[key];
                return (
                  <button
                    key={key}
                    onClick={() => selectLayoutAndClear(key)}
                    title={L.name}
                    style={{
                      background: layout === key ? "#a0845c" : "#1a1714",
                      color: layout === key ? "#0f0d0a" : "#8a7e70",
                      border: `1px solid ${layout === key ? "#c4a46c" : "#2a251f"}`,
                      borderRadius: 4,
                      padding: "2px 5px",
                      fontSize: 13,
                      cursor: "pointer",
                      lineHeight: 1,
                    }}
                  >
                    {L.label}
                  </button>
                );
              })}
            </div>
            <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
              <span style={{ fontSize: 9, color: "#6b6157", textTransform: "uppercase", letterSpacing: 1 }}>Slot</span>
              {Array.from({ length: numSlots }, (_, i) => (
                <button
                  key={i}
                  onClick={() => setActiveSlot(i)}
                  style={{
                    background: activeSlot === i ? "#a0845c" : "#1a1714",
                    color: activeSlot === i ? "#0f0d0a" : "#8a7e70",
                    border: `1px solid ${activeSlot === i ? "#c4a46c" : "#2a251f"}`,
                    borderRadius: 4,
                    width: 24,
                    height: 24,
                    fontSize: 11,
                    cursor: "pointer",
                    fontFamily: "JetBrains Mono, monospace",
                    fontWeight: 600,
                    position: "relative",
                  }}
                >
                  {i + 1}
                  {slots[i] != null && (
                    <div
                      style={{
                        position: "absolute",
                        top: -2,
                        right: -2,
                        width: 5,
                        height: 5,
                        borderRadius: "50%",
                        background: "#c4a46c",
                      }}
                    />
                  )}
                </button>
              ))}
              <span style={{ flex: 1 }} />
              <button
                onClick={clearCanvas}
                style={{
                  background: "transparent",
                  color: "#5a3d1a",
                  border: "1px solid #2a1f14",
                  borderRadius: 4,
                  padding: "2px 8px",
                  fontSize: 10,
                  cursor: "pointer",
                }}
              >
                Clear
              </button>
            </div>
          </div>

          <div
            style={{
              background: "#141210",
              border: "1px solid #1f1c17",
              borderRadius: 8,
              padding: 10,
              marginBottom: 8,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <CompositionCanvas
              slots={slots}
              layout={layout}
              allGlyphs={glyphBank}
              edges={edges}
              cols={cols}
              rows={rows}
              canvasSize={200}
              activeSlot={activeSlot}
            />
            {/* Percolation: slot definitions below canvas */}
            {(() => {
              const slotDefs: { idx: number; text: string }[] = [];
              for (let i = 0; i < slots.length; i++) {
                const slotId = slots[i];
                if (slotId == null) continue;
                const bankEntry = glyphBank[String(slotId)];
                if (!bankEntry?.isCompound) continue;
                const def = bankEntry.compound?.definitions?.[bankEntry.compound?.activeDefinitionIndex ?? -1];
                if (!def) continue;
                slotDefs.push({ idx: i, text: def.text });
              }
              if (slotDefs.length === 0) return null;
              const combined = slotDefs.map((d) => d.text).join(" + ");
              return (
                <div style={{ marginTop: 6, width: "100%", maxWidth: 200 }}>
                  <div style={{ fontSize: 10, color: "#8a7e70" }}>
                    {slotDefs.map((d) => (
                      <div key={d.idx}>
                        <span style={{ color: "#5a4a38" }}>Slot {d.idx + 1}:</span> {d.text}
                      </div>
                    ))}
                  </div>
                  <div style={{ fontSize: 11, color: "#6b8b3e", marginTop: 4, fontStyle: "italic" }}>
                    {combined}
                  </div>
                </div>
              );
            })()}
          </div>

          <div
            style={{
              background: "#141210",
              border: "1px solid #1f1c17",
              borderRadius: 8,
              padding: "6px 10px",
              marginBottom: 8,
              display: "flex",
              gap: 6,
              alignItems: "center",
            }}
          >
            <input
              type="text"
              value={compoundLabel}
              onChange={(e) => setCompoundLabel(e.target.value)}
              placeholder="Name..."
              style={{
                flex: 1,
                background: "#0f0d0a",
                border: "1px solid #2a251f",
                color: "#c4b8a8",
                borderRadius: 4,
                padding: "4px 8px",
                fontSize: 12,
                fontFamily: "Crimson Pro, serif",
                outline: "none",
              }}
            />
            <button
              onClick={saveCompound}
              style={{
                background: "#2a251f",
                color: "#c4b8a8",
                border: "1px solid #3d362e",
                borderRadius: 4,
                padding: "4px 10px",
                fontSize: 11,
                cursor: "pointer",
              }}
            >
              Save
            </button>
            <button
              onClick={promoteCompound}
              title="Save and promote to reusable glyph"
              style={{
                background: "#a0845c",
                color: "#0f0d0a",
                border: "none",
                borderRadius: 4,
                padding: "4px 10px",
                fontSize: 11,
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              P{"\u2192"}O
            </button>
          </div>

          <div
            style={{
              background: "#141210",
              border: "1px solid #1f1c17",
              borderRadius: 8,
              padding: "4px 10px",
              marginBottom: 8,
            }}
          >
            <button
              onClick={() => setShowTopoLegend(!showTopoLegend)}
              style={{
                background: "none",
                border: "none",
                color: "#4a4238",
                fontSize: 9,
                textTransform: "uppercase",
                letterSpacing: 1,
                cursor: "pointer",
                padding: "2px 0",
                fontFamily: "JetBrains Mono, monospace",
                width: "100%",
                textAlign: "left",
              }}
            >
              {showTopoLegend ? "\u25BE" : "\u25B8"} Topology Legend
            </button>
            {showTopoLegend && (
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", fontSize: 9, fontFamily: "JetBrains Mono, monospace", paddingBottom: 4 }}>
                {[
                  { i: "\u2500", d: "line" },
                  { i: "\u2514", d: "bend" },
                  { i: "\u22A3", d: "T" },
                  { i: "\u2534", d: "Y" },
                  { i: "\u253C", d: "cross" },
                  { i: "\u2533", d: "fork" },
                  { i: "\u25CB", d: "loop" },
                  { i: "\u53E3", d: "encl" },
                  { i: "\u65E5", d: "bisect" },
                  { i: "\u7530", d: "part" },
                  { i: "\u2016", d: "multi" },
                ].map((item) => (
                  <span key={item.i} style={{ color: "#6b6157" }}>
                    <span style={{ color: "#8a7e70" }}>{item.i}</span>{item.d}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div
              style={{
                background: "#141210",
                border: "1px solid #1f1c17",
                borderRadius: 8,
                padding: "8px 10px",
              }}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".json"
                style={{ display: "none" }}
                onChange={async (e) => {
                  const file = e.target.files?.[0];
                  if (!file) return;
                  try {
                    const imported = await importLibrary(file);
                    setCompounds((prev) => prev.concat(imported));
                    setGlyphBank((prev) => {
                      const bank = { ...prev };
                      for (const comp of imported) {
                        bank[comp.id] = { isCompound: true, compound: comp, rotation: 0 };
                      }
                      return bank;
                    });
                  } catch { /* ignore bad files */ }
                  e.target.value = "";
                }}
              />
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <span style={{ fontSize: 10, color: "#6b6157", textTransform: "uppercase", letterSpacing: 1 }}>
                  Library ({compounds.length})
                </span>
                <div style={{ display: "flex", gap: 4 }}>
                  <Btn pad="2px 8px" fontSize={9} onClick={() => exportLibrary(compounds)} title="Export library to JSON">
                    Export
                  </Btn>
                  <Btn pad="2px 8px" fontSize={9} onClick={() => fileInputRef.current?.click()} title="Import library from JSON">
                    Import
                  </Btn>
                </div>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {compounds.map((comp) => (
                  <div key={comp.id} style={{ textAlign: "center" }}>
                    <PromotedMini
                      compound={comp}
                      edges={edges}
                      cols={cols}
                      rows={rows}
                      size={52}
                      selected={selGlyph === comp.id}
                      onClick={() => placeGlyph(comp.id, null, true, comp)}
                      badge={comp.promoted ? "P\u2192O" : "\u2605"}
                      badgeColor={comp.promoted ? "#8b6c3e" : "#6b8b3e"}
                    />
                    <div
                      style={{
                        fontSize: 9,
                        color: comp.promoted ? "#8b6c3e" : "#5a5247",
                        marginTop: 2,
                        maxWidth: 52,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {comp.label}
                    </div>
                    {comp.definitions?.[comp.activeDefinitionIndex ?? -1] && (
                      <div style={{ fontSize: 7, color: "#6b8b3e", maxWidth: 52, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                        {comp.definitions[comp.activeDefinitionIndex!].text}
                      </div>
                    )}
                    <button
                      onClick={(e) => { e.stopPropagation(); setDetailCompoundId(comp.id); }}
                      style={{
                        fontSize: 8,
                        color: "#c4a46c",
                        background: "#1a1714",
                        border: "1px solid #3d2e1a",
                        borderRadius: 3,
                        padding: "1px 6px",
                        cursor: "pointer",
                        marginTop: 2,
                        fontFamily: "JetBrains Mono, monospace",
                      }}
                      title="Edit details"
                    >
                      Detail
                    </button>
                    <button
                      onClick={() => {
                        setLayout(comp.layout);
                        setSlots(comp.slots.slice());
                        setGlyphBank({ ...comp.glyphData });
                        setActiveSlot(0);
                        setSelGlyph(null);
                      }}
                      style={{
                        fontSize: 8,
                        color: "#6b6157",
                        background: "none",
                        border: "1px solid #2a2520",
                        borderRadius: 3,
                        padding: "1px 5px",
                        cursor: "pointer",
                        marginTop: 2,
                        fontFamily: "JetBrains Mono, monospace",
                      }}
                    >
                      Restore
                    </button>
                  </div>
                ))}
              </div>
            </div>
        </div>
      </div>

      <div
        style={{
          maxWidth: 1200,
          margin: "20px auto 0",
          padding: "16px 20px",
          borderTop: "1px solid #1f1c17",
          color: "#2a251f",
          fontSize: 11,
          fontFamily: "JetBrains Mono, monospace",
          textAlign: "center",
        }}
      >
        {"\u4E00"} stroke {"\u00B7"} {"\u4E8C"} topology {"\u00B7"} {"\u4E09"} composition {"\u00B7"} {"\u842C\u7269"} recursion {"\u00B7"} placement IS meaning
      </div>

      {/* Detail panel as fixed right-side overlay */}
      {detailCompound && (
        <>
          <div
            onClick={() => setDetailCompoundId(null)}
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(0,0,0,0.4)",
              zIndex: 99,
            }}
          />
          <div
            style={{
              position: "fixed",
              top: 0,
              right: 0,
              width: 360,
              maxWidth: "90vw",
              height: "100vh",
              overflowY: "auto",
              zIndex: 100,
              padding: 0,
            }}
          >
            <GlyphDetailPanel
              compound={detailCompound}
              allCompounds={compounds}
              edges={edges}
              cols={cols}
              rows={rows}
              onUpdate={(updates) => updateCompoundMeta(detailCompound.id, updates)}
              onClose={() => setDetailCompoundId(null)}
              onDelete={() => deleteCompound(detailCompound.id)}
            />
          </div>
        </>
      )}
    </div>
  );
}
