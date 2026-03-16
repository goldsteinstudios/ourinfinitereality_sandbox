import type {
  DerivationStep,
  StructuralElement,
  Prediction,
  ThreeEquations,
  ParallaxCorrespondence,
} from '../types/rsm';

/**
 * The 14-step entailment chain from RSM v5.5 Core Logic Mapping §1–§9.
 * Each step IS the next (identity, not production).
 */
export const DERIVATION_STEPS: DerivationStep[] = [
  {
    id: '1',
    section: '§1',
    title: 'Starting Point',
    statement:
      'If reality is infinitely divisible, what obtains must be distinguishable.',
    explanation:
      'This is a model, not a proof. Everything derived is conditional on the single premise of infinite divisibility. We do not assert the premise is true — we trace what follows if it is. What obtains must be distinguishable; what is not distinguishable does not obtain. This is not an assumption added to the premise — it is what "obtains" means under infinite divisibility.',
    entailsFrom: null,
    entailsTo: '2.1',
    keyInsight:
      'What obtains must be distinguishable. What is not distinguishable does not obtain.',
    geometricFeature: { type: 'empty' },
  },
  {
    id: '2.1',
    section: '§2.1',
    title: 'P0 incoherent ≡ differentiation obtains',
    statement:
      'P0 (zero distinguishability) is incoherent. Differentiation obtains. These are the same structural fact.',
    explanation:
      'Under infinite divisibility, absolute indistinguishability (P0) cannot obtain — it would violate the premise that what obtains is distinguishable. The incoherence of P0 is not a separate step from differentiation obtaining; they are identical statements. The "≡" is literal: saying "P0 is incoherent" and saying "differentiation obtains" are two descriptions of one fact.',
    entailsFrom: '1',
    entailsTo: '2.2',
    notation: 'P0 incoherent ≡ differentiation obtains',
    keyInsight: 'Incoherence of P0 IS differentiation. One fact, two descriptions.',
    geometricFeature: { type: 'hyperbola', equation: 'xy=1' },
  },
  {
    id: '2.2',
    section: '§2.2',
    title: 'Differentiation ≡ duality',
    statement:
      'Differentiation requires at least two distinguishable aspects. This IS duality.',
    explanation:
      'Differentiation means "not all the same." The minimum content of "not all the same" is two distinguishable modes. This is not differentiation producing duality — differentiation IS duality. One cannot differentiate into fewer than two.',
    entailsFrom: '2.1',
    entailsTo: '2.3',
    notation: 'differentiation ≡ duality (x, y)',
    keyInsight: 'You cannot differentiate into fewer than two.',
    geometricFeature: { type: 'duality' },
  },
  {
    id: '2.3',
    section: '§2.3',
    title: 'Duality + P0 incoherent ≡ conservation',
    statement:
      'Since P0 cannot obtain and the two modes are dual, their product is conserved: xy = 1.',
    explanation:
      'If either mode reached zero, distinguishability would vanish (P0 re-obtained). Since P0 is incoherent, neither mode can vanish. The conserved product xy = 1 is not an added law — it IS the statement that P0 cannot obtain, expressed quantitatively. The product is the minimum conserved quantity: if xy < 1, the system collapses toward P0; if xy could be arbitrary, the constraint has no content.',
    entailsFrom: '2.2',
    entailsTo: '2.4',
    notation: 'xy = 1 (conserved product)',
    keyInsight: 'xy = 1 IS the statement that P0 cannot obtain.',
    geometricFeature: { type: 'conservation' },
  },
  {
    id: '2.4',
    section: '§2.4',
    title: 'Conservation ≡ gradient',
    statement:
      'The constraint xy = 1 defines a gradient: as x increases, y must decrease.',
    explanation:
      'The equation xy = 1 does not sit at a single point — it defines a curve in (x, y) space. Along this curve, increasing one mode requires decreasing the other. This reciprocal variation IS a gradient. The gradient is not imposed on the conservation law; it is what the conservation law looks like when you ask "what are the possible states?"',
    entailsFrom: '2.3',
    entailsTo: '2.5',
    notation: 'y = 1/x → dy/dx = −1/x²',
    keyInsight: 'The conservation law IS a gradient when you examine possible states.',
    geometricFeature: { type: 'gradient' },
  },
  {
    id: '2.5',
    section: '§2.5',
    title: 'Gradient ≡ hyperbola',
    statement:
      'The gradient xy = 1 IS the rectangular hyperbola. The curve is the complete set of distinguishable states.',
    explanation:
      'The set of all (x, y) satisfying xy = 1 with x, y > 0 is the positive branch of the rectangular hyperbola. This is not a metaphor — it is the literal geometry of the conservation constraint. Every point on the curve is a possible configuration; the curve itself is the "space" of what can obtain.',
    entailsFrom: '2.4',
    entailsTo: '3.1',
    notation: 'xy = 1 → rectangular hyperbola in ℝ₊²',
    keyInsight: 'The hyperbola is the geometry of what can obtain.',
    geometricFeature: { type: 'hyperbola', equation: 'xy=1' },
  },
  {
    id: '3.1',
    section: '§3.1',
    title: 'Exponential parameterization',
    statement:
      'The hyperbola xy = 1 can be parameterized as x = eᵘ, y = e⁻ᵘ, compressing the gradient structure into a single parameter u.',
    explanation:
      'Setting x = eᵘ, y = e⁻ᵘ satisfies xy = eᵘ · e⁻ᵘ = e⁰ = 1 for all u ∈ ℝ. The parameter u measures displacement along the curve: u = 0 gives the balance point (1,1); u > 0 gives x-dominant states; u < 0 gives y-dominant states. This is not a choice among many parameterizations — it is the unique parameterization that makes the curve its own derivative (exponential self-similarity). The cost of moving along the curve grows exponentially with displacement, deriving the energy barrier from geometry rather than importing it from physics.',
    entailsFrom: '2.5',
    entailsTo: '4.1',
    notation: 'x = eᵘ, y = e⁻ᵘ, u ∈ ℝ',
    keyInsight:
      'The exponential parameterization is unique: the curve is its own derivative. Energy barriers are geometric, not imported.',
    geometricFeature: { type: 'exponential', parameterization: 'eu_e-u' },
  },
  {
    id: '4.1',
    section: '§4.1',
    title: 'Lorentz correspondence',
    statement:
      'Under X = cosh u, T = sinh u, the hyperbola xy = 1 becomes X² − T² = 1.',
    explanation:
      'The substitution X = (x + y)/2 = cosh u, T = (x − y)/2 = sinh u transforms the reciprocal constraint into the standard Lorentz invariant. This is not an analogy — it is an algebraic identity. The structural constraint (conservation under infinite divisibility) and the relativistic invariant (proper interval) are the same equation in different coordinates. The "speed limit" (|T| < X) follows from the fact that x and y must both remain positive.',
    entailsFrom: '3.1',
    entailsTo: '5.1',
    notation: 'X = cosh u, T = sinh u → X² − T² = 1',
    keyInsight:
      'The Lorentz invariant is the same constraint as xy = 1 in rotated coordinates.',
    geometricFeature: { type: 'lorentz', equation: 'X2-T2=1' },
  },
  {
    id: '5.1',
    section: '§5.1',
    title: 'Balance axis and orthogonality',
    statement:
      'The line x = y bisects the dual modes. At the intersection P = (1,1), the balance line is perpendicular to the hyperbola.',
    explanation:
      'The balance axis x = y (slope +1) divides x-dominant from y-dominant regions. It intersects the hyperbola xy = 1 at exactly one point: (1,1). At this point the slope of the hyperbola is dy/dx = −1/x² = −1 (slope −1). Since (+1)(−1) = −1, the two lines are perpendicular. This orthogonality is not incidental — it is the geometric expression of maximal symmetry between the two modes. P = (1,1) is the unique point where neither mode dominates.',
    entailsFrom: '4.1',
    entailsTo: '5.2',
    notation: 'B: x = y, slope = +1; G at P: slope = −1; (+1)(−1) = −1 → ⊥',
    keyInsight:
      'P = (1,1) is the unique point of maximal symmetry — neither mode dominates, and the curves are perpendicular.',
    geometricFeature: { type: 'balance_line', equation: 'x=y' },
  },
  {
    id: '5.2',
    section: '§5.2',
    title: 'Orthogonality at P',
    statement:
      'The perpendicularity at P = (1,1) means the paradox condition must exist but cannot persist as a static point.',
    explanation:
      'At P = (1,1), the gradient (hyperbola) and balance axis are orthogonal. This means any displacement from P immediately generates asymmetry — one mode begins to dominate. P must exist (it is where xy = 1 intersects x = y), but it cannot be a stable equilibrium because the perpendicularity means the restoring force is zero at P while the gradient pulls away from it. P is the paradox condition: structurally necessary, dynamically unstable.',
    entailsFrom: '5.1',
    entailsTo: '6.1',
    notation: 'Pₙ = Gₙ ∩ Bₙ = (1,1); must exist, cannot persist',
    keyInsight:
      'P must exist and cannot persist — this is the paradox condition.',
    geometricFeature: { type: 'orthogonality', point: [1, 1] },
  },
  {
    id: '6.1',
    section: '§6.1',
    title: 'Non-termination (energy barrier)',
    statement:
      'As u → ±∞, the modes approach but never reach their asymptotes. The cost of compression grows exponentially.',
    explanation:
      'On the hyperbola x = eᵘ, y = e⁻ᵘ: as u → +∞, x → ∞ and y → 0⁺ (but never reaches 0). As u → −∞, y → ∞ and x → 0⁺. The asymptotes (x = 0, y = 0) represent P0 — which is incoherent. The exponential parameterization means that each additional unit of displacement along u costs exponentially more — this IS the energy barrier. It is not imported from physics; it is the geometric cost of approaching the forbidden boundary. This is why there is a "speed of light": the asymptote of the hyperbola X² − T² = 1 can be approached but never reached.',
    entailsFrom: '5.2',
    entailsTo: '7.1',
    notation: 'u → ±∞: cost ~ eᵘ → ∞; asymptotes unreachable',
    keyInsight:
      'The energy barrier is the exponential cost of approaching the forbidden asymptote — derived from geometry, not imported from physics.',
    geometricFeature: { type: 'non_termination' },
  },
  {
    id: '7.1',
    section: '§7.1',
    title: 'Frame recursion (parturition)',
    statement:
      'The gradient Gₙ of frame n becomes the x-axis of frame n+1; the balance Bₙ becomes the y-axis. New frames co-emerge from old.',
    explanation:
      'Since P cannot persist as a point, it must "resolve" — but P0 is incoherent, so resolution cannot be collapse. The only structural option is promotion: P becomes the origin of a new frame. In this new frame, the old gradient becomes one axis and the old balance becomes the other. This is parturition — frame generation. Gₙ → xAxis_(n+1), Bₙ → yAxis_(n+1). The new frame has its own gradient, balance, and paradox point, at a different scale. The product 1ₙ is conserved within each frame.',
    entailsFrom: '6.1',
    entailsTo: '8.1',
    notation: 'Gₙ → x_{n+1}, Bₙ → y_{n+1}; Pₙ → O_{n+1}',
    keyInsight:
      'Frame generation (parturition): old structure becomes the axes of new structure.',
    geometricFeature: { type: 'frame_recursion', from: 'n', to: 'n+1' },
  },
  {
    id: '8.1',
    section: '§8.1',
    title: 'Dimensionality from the two-branch connection problem',
    statement:
      'The hyperbola has two disconnected branches. Connecting them requires a bridge through a new dimension, yielding S² → ℝ³.',
    explanation:
      'The full hyperbola xy = 1 has two branches (x > 0, y > 0 and x < 0, y < 0 — or equivalently, the two branches of X² − T² = 1). These branches are disconnected in the (x,y) plane. To connect them, a path must leave the plane — this requires a third dimension. The minimal closed surface connecting two points that preserves the rotational symmetry is the circle S¹; the minimal surface enclosing a region with no preferred direction is the sphere S². S² can only be embedded in ℝ³. This derives three spatial dimensions from the two-branch connection problem, not by assertion.',
    entailsFrom: '7.1',
    entailsTo: '8.2',
    notation: 'Two branches → S¹ bridge → S² isotropy → ℝ³',
    keyInsight:
      'Three spatial dimensions are derived from the need to connect the two branches of the hyperbola.',
    geometricFeature: { type: 'two_branch', connection: 'bridge' },
  },
  {
    id: '8.2',
    section: '§8.2',
    title: 'Three equations',
    statement:
      'The three fundamental equations — xy = 1, x² + y² = 1, x² + y² + z² = 1 — encode flat constraint, circular bridge, and spherical isotropy.',
    explanation:
      'Equation 1 (xy = 1): the flat reciprocal constraint — one measurement point on the gradient. Equation 2 (x² + y² = 1): the unit circle — rotation around the forbidden center, the bridge between branches. Equation 3 (x² + y² + z² = 1): the unit sphere — no preferred direction, full isotropy. Each equation IS the next level of the structural requirement: constraint → rotation → isotropy.',
    entailsFrom: '8.1',
    entailsTo: '9.1',
    notation: 'xy = 1 → x² + y² = 1 → x² + y² + z² = 1',
    keyInsight:
      'Three equations, three levels: flat constraint, circular bridge, spherical isotropy.',
    geometricFeature: { type: 'circle', equation: 'x2+y2=1' },
  },
  {
    id: '9.1',
    section: '§9.1',
    title: 'Oscillation',
    statement:
      'The system oscillates through the paradox point P — never resting at it, never escaping it.',
    explanation:
      'Since P must exist and cannot persist, the system must continually pass through P without remaining there. This creates oscillation — a back-and-forth traversal across the paradox boundary. The oscillation is not imposed; it follows from the conjunction of structural necessity (P must exist) and dynamic instability (P cannot persist). This is the origin of periodicity, wave behavior, and all cyclic phenomena. The oscillation through P at each frame level is what manifests as time, vibration, and the wave-particle character of physical systems.',
    entailsFrom: '8.2',
    entailsTo: null,
    notation: '... → P → ... → P → ... (oscillation through paradox)',
    keyInsight:
      'Oscillation through P is the origin of all periodicity — the system must pass through what it cannot stay at.',
    geometricFeature: { type: 'oscillation', across: 'P' },
  },
];

/** Structural elements of the RSM vocabulary */
export const STRUCTURAL_ELEMENTS: StructuralElement[] = [
  {
    symbol: 'P0',
    name: 'Pre-frame impossibility',
    role: 'Absolute indistinguishability — incoherent under the premise',
  },
  {
    symbol: 'Oₙ',
    name: 'Origin',
    role: 'Reference point; holds paradox open',
    mathematicalForm: '0ₙ (operational co-presence)',
  },
  {
    symbol: 'Gₙ',
    name: 'Inverse curve / Gradient',
    role: 'Reciprocal constraint between dual modes',
    mathematicalForm: 'xy = 1ₙ',
  },
  {
    symbol: 'Bₙ',
    name: 'Balance axis',
    role: 'Divides modal regions; bisector of dual modes',
    mathematicalForm: 'x = y',
  },
  {
    symbol: 'Pₙ',
    name: 'Paradox-condition',
    role: 'Must exist, cannot persist — intersection of Gₙ and Bₙ',
    mathematicalForm: 'Gₙ ∩ Bₙ = (1,1)',
  },
  {
    symbol: 'Rₙ',
    name: 'Frame',
    role: 'Everything expressible within recursion level n',
  },
  {
    symbol: '1ₙ',
    name: 'Minimum distinction',
    role: 'Conserved product within frame n',
    mathematicalForm: 'xy = 1ₙ',
  },
];

/** The six falsifiable predictions from v5.5 */
export const FALSIFIABLE_PREDICTIONS: Prediction[] = [
  {
    id: 1,
    claim:
      'No persistent structure without paradoxical center: every stable system must orbit an inaccessible center.',
    falsifier:
      'A persistent structure that is solid through its center with no asymptotic behavior — no void, no singularity, no inaccessible region.',
  },
  {
    id: 2,
    claim:
      'Conservation requires duality: every conserved quantity implies at least two reciprocally constrained modes.',
    falsifier:
      'A conserved quantity that does not decompose into reciprocally varying aspects — a conserved scalar with no dual structure.',
  },
  {
    id: 3,
    claim:
      'Orthogonality at the paradox point: wherever dual modes are balanced, the gradient and balance structures are perpendicular.',
    falsifier:
      'A system where dual modes are perfectly balanced but the gradient and balance axes are not orthogonal.',
  },
  {
    id: 4,
    claim:
      'Exponential cost of extremity: approaching the asymptote of any conserved reciprocal relationship costs exponentially more per unit of progress.',
    falsifier:
      'A system obeying xy = constant where the cost of making x arbitrarily large grows linearly or sub-exponentially.',
  },
  {
    id: 5,
    claim:
      'Frame recursion preserves structure: each new frame level contains the same structural elements (O, G, B, P, 1) at a different scale.',
    falsifier:
      'A recursion level that lacks one of the structural elements — e.g., a frame with a gradient but no balance axis, or a paradox point that does not generate a new frame.',
  },
  {
    id: 6,
    claim:
      'Three dimensions from two branches: any system with two disconnected reciprocal branches requires exactly three embedding dimensions for isotropic closure.',
    falsifier:
      'A two-branch reciprocal system that achieves isotropic closure in fewer than three dimensions, or that requires more than three.',
  },
];

/** The three fundamental equations */
export const THREE_EQUATIONS: ThreeEquations = {
  flat: 'xy = 1',
  circle: 'x² + y² = 1',
  sphere: 'x² + y² + z² = 1',
};

/** Parallax correspondences (:: operator) — cross-framework mappings */
export const PARALLAX_TABLE: ParallaxCorrespondence[] = [
  {
    structuralFeature: 'Inverse constraint (xy = 1)',
    mathematics: 'Rectangular hyperbola',
    physics: 'Lorentz invariant X² − T² = 1',
    biology: 'Metabolic rate × lifespan ≈ constant',
    ddj: '天地 (Tiān Dì) — Heaven–Earth gradient',
    euler: 'e (continuous growth preserving product)',
  },
  {
    structuralFeature: 'Balance axis (x = y)',
    mathematics: 'Identity line, bisector',
    physics: 'Rest frame (v = 0, u = 0)',
    biology: 'Homeostatic set-point',
    ddj: '中 (Zhōng) — the center, the mean',
    euler: '1 (unity, identity element)',
  },
  {
    structuralFeature: 'Orthogonality at P = (1,1)',
    mathematics: 'Perpendicular tangent and bisector',
    physics: 'Proper time τ at rest',
    biology: 'Equilibrium point of competing drives',
    ddj: '玄 (Xuán) — the dark/mysterious pivot',
    euler: 'i (90° rotation, orthogonal dimension)',
  },
  {
    structuralFeature: 'Paradox-condition (must exist, cannot persist)',
    mathematics: 'Saddle point, unstable equilibrium',
    physics: 'Virtual particle, measurement event',
    biology: 'Cell division moment, action potential peak',
    ddj: '無 (Wú) — the functional void',
    euler: '0 (paradox center, additive identity)',
  },
  {
    structuralFeature: 'Exponential cost of asymptote',
    mathematics: 'eᵘ diverges as u → ∞',
    physics: 'Relativistic mass increase, c as speed limit',
    biology: 'Diminishing returns at metabolic extremes',
    ddj: '不可 (Bù Kě) — cannot be reached/named',
    euler: 'e^(iπ) — full traversal returns to origin',
  },
  {
    structuralFeature: 'Frame recursion (parturition)',
    mathematics: 'Nested coordinate systems, self-similar fractals',
    physics: 'Scale hierarchy (quark → nucleon → atom → molecule)',
    biology: 'Cell → tissue → organ → organism',
    ddj: '道生一，一生二，二生三，三生萬物',
    euler: 'Iterated exponentiation (e^(e^(...)))',
  },
  {
    structuralFeature: 'Oscillation through P',
    mathematics: 'Periodic orbit through saddle',
    physics: 'Wave function, EM oscillation',
    biology: 'Heartbeat, circadian rhythm, breath',
    ddj: '反者道之動 — reversal is the movement of Dao',
    euler: 'e^(iθ) = cos θ + i sin θ — circular oscillation',
  },
  {
    structuralFeature: 'Three equations / dimensionality',
    mathematics: 'Hyperbola → circle → sphere (S⁰ → S¹ → S²)',
    physics: 'Three spatial dimensions + time',
    biology: 'Bilateral symmetry → radial organization → spherical embryo',
    ddj: '三生萬物 — three generates the ten thousand things',
    euler: 'π (closure, curvature completing the circle)',
  },
];
