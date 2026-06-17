import { RefreshCcw } from 'lucide-react';
import { useParams } from 'react-router-dom';
import EmptyState from '../components/states/EmptyState.jsx';
import ErrorState from '../components/states/ErrorState.jsx';
import LoadingState from '../components/states/LoadingState.jsx';
import Button from '../components/ui/Button.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import EvidencePanel from '../components/violations/EvidencePanel.jsx';
import ViolationTable from '../components/violations/ViolationTable.jsx';
import useAsyncData from '../hooks/useAsyncData.js';
import { getViolation, getViolations } from '../services/api.js';
import { formatNumber } from '../utils/formatters.js';

export default function Evidence() {
  const { id } = useParams();
  const { data, error, loading, reload } = useAsyncData(async () => {
    const [violations, selected] = await Promise.all([
      getViolations({ limit: 20, offset: 0 }),
      id ? getViolation(id) : Promise.resolve(null),
    ]);
    return { violations, selected };
  }, [id]);

  if (loading) {
    return <LoadingState label="Loading evidence queue" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={reload} />;
  }

  const items = data.violations?.items || [];

  return (
    <>
      <PageHeader
        eyebrow="Evidence Review"
        title="Violation Evidence"
        description="Review AI-detected traffic violations with image evidence, OCR output, camera metadata, and confidence scoring."
        actions={
          <Button icon={RefreshCcw} variant="secondary" onClick={reload}>
            Refresh
          </Button>
        }
      />

      {data.selected ? (
        <section className="mb-5">
          <EvidencePanel violation={data.selected} />
        </section>
      ) : null}

      <section>
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="text-base font-semibold text-slate-950 dark:text-white">Review Queue</h2>
          <span className="text-sm text-slate-500 dark:text-slate-400">{formatNumber(data.violations?.total)} records</span>
        </div>
        {items.length ? (
          <ViolationTable violations={items} />
        ) : (
          <EmptyState title="No evidence records" message="Violation evidence will appear after uploads produce detections." />
        )}
      </section>
    </>
  );
}

