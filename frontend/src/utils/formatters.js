export function formatNumber(value) {
  return new Intl.NumberFormat('en-IN').format(value || 0);
}

export function formatDateTime(value) {
  if (!value) {
    return 'Not available';
  }
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

export function formatViolationType(value) {
  if (!value) {
    return 'Unknown';
  }
  return value
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

export function formatPercent(value) {
  return `${Math.round((value || 0) * 100)}%`;
}

export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

