export default function EmptyState({ title = 'No records found', message }) {
  return (
    <div className="surface-muted flex min-h-40 flex-col items-center justify-center p-6 text-center">
      <h2 className="text-base font-semibold text-slate-950 dark:text-white">{title}</h2>
      <p className="mt-2 max-w-md text-sm leading-6 text-slate-600 dark:text-slate-400">
        {message || 'New records will appear here when the backend has data.'}
      </p>
    </div>
  );
}

