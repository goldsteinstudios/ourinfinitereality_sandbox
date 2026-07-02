---
title: "RSM Dependency Graph"
filename: "dependency_graph.md"
version: "0.993"
set: "meta"
type: "meta"
tier: "meta"
dependencies: []
last_updated: "2026-01-01"
authors:
  - "Will Goldstein"
  - "Claude"
description: "Visual dependency structure showing what derives from what in RSM"
keywords:
  - "dependency"
  - "derivation"
  - "modularity"
reading_time_minutes: 5
---

# RSM Dependency Graph

## What Derives from What

---

```
RSM v0.993 Alignment
────────────────────
Status: Meta-documentation
Purpose: Trace any claim back to its foundations
```

---

## The Graph

```
FOUNDATIONS
═══════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────┐
                    │     AXIOM: CLOSURE          │
                    │  "System must be           │
                    │   self-contained"           │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │   POSTULATE 1: CONTRAST     │
                    │  "Distinguishability        │
                    │   requires opposition"      │
                    └─────────────┬───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ THEOREM 0.1   │     │  META-THEOREM 0.2 │     │  [POSTULATE 2]    │
│ V₀ Unspecifi- │     │  Contrast is      │     │  Continuity       │
│ able          │     │  Necessary        │     │  (optional)       │
└───────┬───────┘     └─────────┬─────────┘     └─────────┬─────────┘
        │                       │                         │
        │                       │                         │
        └───────────┬───────────┘                         │
                    │                                     │
                    ▼                                     │
        ┌───────────────────────┐                         │
        │     THEOREM 0.3       │                         │
        │  O₁ as Generative     │                         │
        │  Center               │◄────────────────────────┘
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│   THEOREM 0.5     │   │  [POSTULATE 3]    │
│   Infinite        │   │  Frame Invariance │
│   Divisibility    │   │  (optional)       │
└───────────┬───────┘   └─────────┬─────────┘
            │                     │
            │     ┌───────────────┘
            │     │
            ▼     ▼
    ┌───────────────────────┐
    │     THEOREM 2.1       │
    │  Measurement Crisis / │
    │  Rotation Necessary   │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │   THREE REQUIREMENTS  │
    │                       │
    │  • Contrast           │
    │  • Rotation           │
    │  • Closure            │
    └───────────┬───────────┘
                │
    ════════════╧════════════════════════════════════════════════════

POSTULATE-DEPENDENT BRANCHES
═══════════════════════════════════════════════════════════════════════

From POSTULATE 2 (Continuity):
        │
        ▼
┌───────────────────┐     ┌───────────────────┐
│   THEOREM 3.1     │────▶│  e as continuous  │
│   e derivation    │     │  generation rate  │
└───────────────────┘     └───────────────────┘

From POSTULATE 3 (Frame Invariance):
        │
        ▼
┌───────────────────┐     ┌───────────────────┐
│   THEOREM 4.1     │────▶│  π as closure of  │
│   π derivation    │     │  curvature        │
└───────────────────┘     └───────────────────┘

From POSTULATE 4 (Reciprocal Constraint):
        │
        ▼
┌───────────────────┐     ┌───────────────────┐
│   X · Y = k       │────▶│  P₁ = 1 at        │
│   constraint      │     │  balance point    │
└───────────────────┘     └───────────────────┘

From POSTULATE 1T (Temporal Continuity):
        │
        ▼
┌───────────────────┐     ┌───────────────────┐
│   THEOREM 0.3T    │────▶│  Present moment   │
│   Temporal O₁     │     │  as temporal O₁   │
└───────────────────┘     └───────────────────┘

═══════════════════════════════════════════════════════════════════════

EMPIRICAL VALIDATION (Independent of Derivation Chain)
═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Plant QC Geometry ──────┐                                         │
│                           │                                         │
│   Kleiber's Law ──────────┼──────▶  EMPIRICAL TEST OF O₁ PATTERN   │
│                           │                                         │
│   Atomic Orbitals ────────┘                                         │
│                                                                     │
│   (These test predictions, not premises)                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Reading the Graph

**Solid arrows (│ ▼ ▶):** Derivation dependency. The conclusion requires the premise.

**Bracketed items [POSTULATE N]:** Optional modeling choices. Can be accepted or rejected without affecting what comes before them.

**Double lines (═══):** Section boundaries in the document.

---

## Modularity Check

| If you reject... | What breaks | What survives |
|-----------------|-------------|---------------|
| Postulate 2 (Continuity) | e derivation, continuous-field claims | V₀, O₁, rotation, three requirements |
| Postulate 3 (Frame Invariance) | π derivation, scale-invariance claims | V₀, O₁, rotation (but closure might take different form) |
| Postulate 4 (Reciprocal Constraint) | P₁ = 1 specifically | V₀, O₁, rotation, P₁ ≠ 0, three requirements |
| Postulate 1T (Temporal) | Present-moment O₁, temporal extension | All spatial claims intact |
| Any Tier 3/4 claim | That specific mapping/analogy | All Tier 1 and 2 claims |

---

## Core Chain

**The core chain (V₀ prohibition → Contrast necessity → O₁ construction → Rotation necessity → Three Requirements) depends only on the Closure axiom and Contrast postulate.**

---

*Extracted from RSM v0.993 Appendix G*
*Classification: Meta-documentation*
