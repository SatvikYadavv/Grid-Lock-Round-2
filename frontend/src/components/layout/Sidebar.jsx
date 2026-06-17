import { X } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { cn } from '../../utils/cn.js';
import { navigationItems } from './navigation.js';

export default function Sidebar({ open, onClose }) {
  return (
    <>
      <div
        className={cn(
          'fixed inset-0 z-40 bg-slate-950/50 transition-opacity lg:hidden',
          open ? 'opacity-100' : 'pointer-events-none opacity-0',
        )}
        onClick={onClose}
      />
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-slate-200 bg-white transition-transform lg:translate-x-0 dark:border-slate-800 dark:bg-slate-950',
          open ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div className="min-w-0">
            <div className="text-sm font-semibold uppercase tracking-wide text-civic-authority dark:text-teal-300">
              TraffiSense AI
            </div>
            <div className="truncate text-xs text-slate-500 dark:text-slate-400">
              Intelligent Traffic Enforcement
            </div>
          </div>
          <button
            type="button"
            aria-label="Close navigation"
            onClick={onClose}
            className="focus-ring inline-flex h-9 w-9 items-center justify-center border border-slate-200 text-slate-600 lg:hidden dark:border-slate-800 dark:text-slate-300"
          >
            <X size={18} />
          </button>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  cn(
                    'focus-ring flex min-h-11 items-center gap-3 px-3 text-sm font-medium transition',
                    isActive
                      ? 'bg-civic-authority text-white dark:bg-teal-600'
                      : 'text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-900',
                  )
                }
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-slate-200 p-4 dark:border-slate-800">
          <div className="surface-muted px-3 py-3">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              System Status
            </div>
            <div className="mt-2 flex items-center gap-2 text-sm font-medium">
              <span className="h-2.5 w-2.5 bg-teal-500" />
              Monitoring active
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

