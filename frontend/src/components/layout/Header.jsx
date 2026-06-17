import { Bell, Moon, Search, Sun } from 'lucide-react';

export default function Header({ isDark, onToggleTheme }) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
      <div className="mx-auto flex h-16 max-w-[1560px] items-center gap-4 px-4 sm:px-6 lg:px-8">
        <div className="hidden min-w-0 flex-1 items-center gap-3 border border-slate-200 bg-slate-50 px-3 py-2 md:flex dark:border-slate-800 dark:bg-slate-900">
          <Search size={16} className="text-slate-500" />
          <input
            type="search"
            placeholder="Search violations, plate numbers, locations"
            className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-500 focus:outline-none dark:text-slate-100"
          />
        </div>
        <div className="ml-auto flex items-center gap-2">
          <button
            type="button"
            aria-label="Notifications"
            className="focus-ring inline-flex h-10 w-10 items-center justify-center border border-slate-200 bg-white text-slate-700 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
          >
            <Bell size={18} />
          </button>
          <button
            type="button"
            aria-label="Toggle dark mode"
            onClick={onToggleTheme}
            className="focus-ring inline-flex h-10 w-10 items-center justify-center border border-slate-200 bg-white text-slate-700 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}

