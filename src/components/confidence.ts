export const CONFIDENCE_TIERS = {
  strong: { color: '--color-strong', label: 'strong' },
  plausible: { color: '--color-plausible', label: 'plausible' },
  speculative: { color: '--color-speculative', label: 'speculative' },
} as const;

export type ConfidenceLevel = keyof typeof CONFIDENCE_TIERS;
