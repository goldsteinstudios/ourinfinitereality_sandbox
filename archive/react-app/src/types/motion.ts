// Motion Decoder Types
// Implements the 8-step Character Motion Analysis wizard

export interface RadicalComponent {
  radical: string;
  meaning: string;
  category?: string;
}

export interface ToolIdentification {
  toolType: string; // e.g., "blade", "agriculture", "construction", "relational operator"
  description: string;
  physicalOrStructural: 'physical' | 'structural' | 'hybrid';
}

export interface MotionDescription {
  action: string; // The primary action/motion
  directionality: string; // Direction of motion
  force: string; // Type/intensity of force
  spatialExtent: string; // Spatial characteristics
  temporalAspect: string; // Time-related characteristics
}

export interface GeometricPattern {
  patternType: string; // e.g., "circle", "spiral", "arc", "wave", "grid", "fractal"
  description: string;
}

export interface MathematicalRelationship {
  relationshipType: string; // e.g., "phi", "pi", "fibonacci", "symmetry", "recursion"
  description: string;
  formula?: string;
}

export interface ContextTest {
  chapter: number;
  position: number;
  character: string;
  context: string;
  interpretation: string;
  fits: boolean;
  notes: string;
}

export interface MotionInsight {
  id: string;
  timestamp: number;
  character: string;

  // Step 1: Character Selection
  characterInfo: {
    pinyin: string;
    occurrences: Array<{ chapter: number; position: number }>;
  };

  // Step 2: Radical Breakdown
  radicals: RadicalComponent[];

  // Step 3: Tool Identification
  tools: ToolIdentification[];

  // Step 4: Motion Imagination
  motion: MotionDescription;

  // Step 5: Geometric Pattern
  geometricPatterns: GeometricPattern[];

  // Step 6: Mathematical Relationships
  mathematicalRelationships: MathematicalRelationship[];

  // Step 7: Context Testing
  contextTests: ContextTest[];

  // Step 8: Insights & Hypothesis
  hypothesis: string;
  confidence: 'low' | 'medium' | 'high';
  notes: string;
  tags: string[];
}

export interface MotionDecoderState {
  currentStep: number;
  workingInsight: Partial<MotionInsight> | null;
  savedInsights: MotionInsight[];
  comparisonMode: boolean;
  comparisonInsights: string[]; // IDs of insights to compare
}
