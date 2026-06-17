import { Menu } from 'lucide-react';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import useDarkMode from '../../hooks/useDarkMode.js';
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { isDark, toggleTheme } = useDarkMode();

  return (
    <div className="min-h-screen bg-civic-paper text-slate-950 dark:bg-[#0c111d] dark:text-slate-100">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="lg:pl-72">
        <Header isDark={isDark} onToggleTheme={toggleTheme} onOpenSidebar={() => setSidebarOpen(true)} />
        <main className="mx-auto w-full max-w-[1560px] px-4 py-5 sm:px-6 lg:px-8">
          <button
            type="button"
            aria-label="Open navigation"
            onClick={() => setSidebarOpen(true)}
            className="focus-ring mb-4 inline-flex h-10 w-10 items-center justify-center border border-slate-200 bg-white text-slate-700 shadow-sm lg:hidden dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
          >
            <Menu size={18} />
          </button>
          <Outlet />
        </main>
      </div>
    </div>
  );
}

