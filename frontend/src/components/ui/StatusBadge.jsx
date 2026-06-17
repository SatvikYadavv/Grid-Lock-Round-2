import { cn } from '../../utils/cn.js';
import { formatViolationType } from '../../utils/formatters.js';

const statusStyles = {
  pending_review: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-200',
  confirmed: 'bg-teal-100 text-teal-800 dark:bg-teal-900/40 dark:text-teal-200',
  rejected: 'bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
  failed: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-200',
  completed: 'bg-teal-100 text-teal-800 dark:bg-teal-900/40 dark:text-teal-200',
  processing: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-200',
};

export default function StatusBadge({ value }) {
  return (
    <span
      className={cn(
        'inline-flex min-h-7 items-center px-2.5 text-xs font-semibold',
        statusStyles[value] || 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
      )}
    >
      {formatViolationType(value)}
    </span>
  );
}

