import { getImageUrl } from '../../services/api.js';
import { formatDateTime, formatPercent, formatViolationType } from '../../utils/formatters.js';
import StatusBadge from '../ui/StatusBadge.jsx';

export default function EvidencePanel({ violation }) {
  const evidence = violation?.evidence?.[0];
  const imageUrl = getImageUrl(evidence?.annotated_image_url || evidence?.evidence_image_url || violation?.image?.image_url);

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.65fr)]">
      <div className="surface overflow-hidden">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt="Violation evidence"
            className="aspect-video w-full bg-slate-100 object-contain dark:bg-slate-900"
          />
        ) : (
          <div className="flex aspect-video items-center justify-center bg-slate-100 text-sm text-slate-500 dark:bg-slate-900 dark:text-slate-400">
            Evidence image unavailable
          </div>
        )}
      </div>

      <div className="surface p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Evidence Record
            </p>
            <h2 className="mt-2 text-xl font-semibold text-slate-950 dark:text-white">
              {formatViolationType(violation.violation_type)}
            </h2>
          </div>
          <StatusBadge value={violation.status} />
        </div>

        <dl className="mt-5 divide-y divide-slate-200 text-sm dark:divide-slate-800">
          <Detail label="Plate number" value={violation.plate_number || 'Unidentified'} />
          <Detail label="Vehicle type" value={violation.vehicle_type || 'Unknown'} />
          <Detail label="Confidence" value={formatPercent(violation.confidence)} />
          <Detail label="Camera" value={violation.camera?.name || 'Unassigned'} />
          <Detail label="Location" value={violation.camera?.location_name || 'Unknown'} />
          <Detail label="Detected at" value={formatDateTime(violation.detected_at)} />
        </dl>
      </div>
    </div>
  );
}

function Detail({ label, value }) {
  return (
    <div className="grid grid-cols-[120px_1fr] gap-3 py-3">
      <dt className="text-slate-500 dark:text-slate-400">{label}</dt>
      <dd className="font-medium text-slate-950 dark:text-white">{value}</dd>
    </div>
  );
}

