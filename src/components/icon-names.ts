export const ICON_NAMES = [
  'atom',
  'bellows',
  'origin',
  'room',
  'tree',
  'valley',
  'wheel',
] as const;

export type IconName = (typeof ICON_NAMES)[number];
