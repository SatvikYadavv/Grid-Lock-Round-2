export default function LoadingState({ label = 'Loading data' }) {
  return (
    <div className="surface flex min-h-48 items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="mb-4 h-4 w-40 animate-pulse bg-slate-200 dark:bg-slate-800" />
        <div className="space-y-3">
          <div className="h-3 w-full animate-pulse bg-slate-200 dark:bg-slate-800" />
          <div className="h-3 w-10/12 animate-pulse bg-slate-200 dark:bg-slate-800" />
          <div className="h-3 w-7/12 animate-pulse bg-slate-200 dark:bg-slate-800" />
        </div>
        <p className="mt-5 text-sm text-slate-500 dark:text-slate-400">{label}</p>
      </div>
    </div>
  );
}

