export const CONFIDENCE_TIERS = {
  locked: { color: '--color-locked', label: 'locked' },
  strong: { color: '--color-strong', label: 'strong' },
  plausible: { color: '--color-plausible', label: 'plausible' },
  speculative: { color: '--color-speculative', label: 'speculative' },
} as const;

export type ConfidenceLevel = keyof typeof CONFIDENCE_TIERS;
