import { ArrowDownRight, ArrowUpRight } from 'lucide-react';
import { cn } from '../../utils/cn.js';

export default function MetricCard({ title, value, detail, trend, tone = 'default', icon: Icon }) {
  const tones = {
    default: 'border-l-civic-authority',
    success: 'border-l-civic-teal',
    warning: 'border-l-civic-amber',
    danger: 'border-l-civic-alert',
  };

  return (
    <div className={cn('surface border-l-4 p-4', tones[tone])}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            {title}
          </p>
          <p className="mt-3 truncate text-2xl font-semibold text-slate-950 dark:text-white">
            {value}
          </p>
        </div>
        {Icon ? (
          <div className="flex h-10 w-10 shrink-0 items-center justify-center bg-slate-100 text-civic-authority dark:bg-slate-900 dark:text-teal-300">
            <Icon size={19} />
          </div>
        ) : null}
      </div>
      <div className="mt-4 flex min-h-5 items-center justify-between gap-3 text-xs text-slate-500 dark:text-slate-400">
        <span className="truncate">{detail}</span>
        {trend ? (
          <span
            className={cn(
              'inline-flex shrink-0 items-center gap-1 font-semibold',
              trend.direction === 'down' ? 'text-teal-700 dark:text-teal-300' : 'text-red-700 dark:text-red-300',
            )}
          >
            {trend.direction === 'down' ? <ArrowDownRight size={14} /> : <ArrowUpRight size={14} />}
            {trend.value}
          </span>
        ) : null}
      </div>
    </div>
  );
}

