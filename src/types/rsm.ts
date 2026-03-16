// RSM v5.5 Logic Mapping Type System
// Defines the structural vocabulary for the Recursive Structural Model derivation chain

/** Structural elements within a frame */
export interface StructuralElement {
  symbol: string;       // e.g. "P0", "On", "Gn", "Bn", "Pn", "Rn", "1n"
  name: string;         // e.g. "Pre-frame impossibility"
  role: string;         // e.g. "Absolute indistinguishability"
  mathematicalForm?: string; // e.g. "xy = 1n"
}

/** Geometric features for canvas visualization */
export type GeometricFeature =
  | { type: 'empty' }
  | { type: 'hyperbola'; equation: 'xy=1' }
  | { type: 'balance_line'; equation: 'x=y' }
  | { type: 'orthogonality'; point: [number, number] }
  | { type: 'exponential'; parameterization: 'eu_e-u' }
  | { type: 'lorentz'; equation: 'X2-T2=1' }
  | { type: 'circle'; equation: 'x2+y2=1' }
  | { type: 'sphere'; equation: 'x2+y2+z2=1' }
  | { type: 'frame_recursion'; from: string; to: string }
  | { type: 'oscillation'; across: 'P' }
  | { type: 'two_branch'; connection: 'bridge' }
  | { type: 'duality' }
  | { type: 'conservation' }
  | { type: 'gradient' }
  | { type: 'non_termination' };

/** A single step in the derivation chain */
export interface DerivationStep {
  id: string;           // e.g. "2.1", "2.2", "3.1"
  section: string;      // e.g. "§2.1"
  title: string;        // e.g. "P0 incoherent = differentiation obtains"
  statement: string;    // The core claim in one sentence
  explanation: string;  // The full argument (paragraph)
  entailsFrom: string | null; // Previous step id (null for §1)
  entailsTo: string | null;   // Next step id
  geometricFeature?: GeometricFeature; // What to draw on canvas
  notation?: string;    // Formal notation if any
  keyInsight?: string;  // Bold-text key insight
}

/** The three fundamental equations */
export interface ThreeEquations {
  flat: 'xy = 1';           // one measurement point
  circle: 'x² + y² = 1';   // rotation around forbidden center
  sphere: 'x² + y² + z² = 1'; // no preferred direction
}

/** Parallax correspondence (:: operator) */
export interface ParallaxCorrespondence {
  structuralFeature: string;  // e.g. "inverse constraint"
  mathematics: string;
  physics?: string;
  biology?: string;
  ddj?: string;              // Daodejing correspondence
  euler?: string;            // Euler identity correspondence
}

/** Frame at recursion level n */
export interface Frame {
  n: number;
  origin: string;     // On
  gradient: string;   // Gn (xy = 1n)
  balance: string;    // Bn (x = y)
  paradox: string;    // Pn (Gn ∩ Bn)
  conserved: string;  // 1n
}

/** Falsifiable prediction */
export interface Prediction {
  id: number;
  claim: string;
  falsifier: string;  // what would falsify it
}
