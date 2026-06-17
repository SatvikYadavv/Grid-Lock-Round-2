import { Eye } from 'lucide-react';
import { Link } from 'react-router-dom';
import { formatDateTime, formatPercent, formatViolationType } from '../../utils/formatters.js';
import StatusBadge from '../ui/StatusBadge.jsx';

export default function ViolationTable({ violations = [], compact = false }) {
  return (
    <div className="surface overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left dark:divide-slate-800">
          <thead className="bg-slate-50 dark:bg-slate-900">
            <tr>
              <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Violation</th>
              <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Plate</th>
              {!compact ? (
                <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Camera</th>
              ) : null}
              <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Status</th>
              <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Confidence</th>
              <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Detected</th>
              <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">
                Review
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white dark:divide-slate-800 dark:bg-slate-950">
            {violations.map((violation) => (
              <tr key={violation.id} className="hover:bg-slate-50 dark:hover:bg-slate-900">
                <td className="px-4 py-3 text-sm font-medium text-slate-950 dark:text-white">
                  {formatViolationType(violation.violation_type)}
                </td>
                <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                  {violation.plate_number || 'Unidentified'}
                </td>
                {!compact ? (
                  <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                    {violation.camera?.name || 'Unassigned'}
                  </td>
                ) : null}
                <td className="px-4 py-3">
                  <StatusBadge value={violation.status} />
                </td>
                <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                  {formatPercent(violation.confidence)}
                </td>
                <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
                  {formatDateTime(violation.detected_at)}
                </td>
                <td className="px-4 py-3 text-right">
                  <Link
                    to={`/evidence/${violation.id}`}
                    aria-label={`Open evidence for ${formatViolationType(violation.violation_type)}`}
                    className="focus-ring inline-flex h-9 w-9 items-center justify-center border border-slate-200 text-slate-700 hover:bg-slate-100 dark:border-slate-800 dark:text-slate-200 dark:hover:bg-slate-900"
                  >
                    <Eye size={17} />
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

