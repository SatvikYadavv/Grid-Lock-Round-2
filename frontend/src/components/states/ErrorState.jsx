import { RefreshCcw } from 'lucide-react';
import Button from '../ui/Button.jsx';

export default function ErrorState({ title = 'Unable to load data', message, onRetry }) {
  return (
    <div className="surface border-l-4 border-l-civic-alert p-6">
      <h2 className="text-base font-semibold text-slate-950 dark:text-white">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
        {message || 'The service did not return a usable response.'}
      </p>
      {onRetry ? (
        <Button icon={RefreshCcw} variant="secondary" className="mt-4" onClick={onRetry}>
          Retry
        </Button>
      ) : null}
    </div>
  );
}

