import { cn } from '../../utils/cn.js';

const variants = {
  primary: 'bg-civic-authority text-white hover:bg-[#183f61] dark:bg-teal-600 dark:hover:bg-teal-500',
  secondary:
    'border border-slate-200 bg-white text-slate-800 hover:bg-slate-50 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100 dark:hover:bg-slate-900',
  danger: 'bg-civic-alert text-white hover:bg-red-800',
};

export default function Button({
  children,
  className,
  disabled,
  icon: Icon,
  type = 'button',
  variant = 'primary',
  ...props
}) {
  return (
    <button
      type={type}
      disabled={disabled}
      className={cn(
        'focus-ring inline-flex min-h-10 items-center justify-center gap-2 px-4 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60',
        variants[variant],
        className,
      )}
      {...props}
    >
      {Icon ? <Icon size={17} /> : null}
      <span>{children}</span>
    </button>
  );
}

