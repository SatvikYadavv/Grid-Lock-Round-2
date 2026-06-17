import { CalendarClock, Camera, UploadCloud } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { uploadImage } from '../../services/api.js';
import Button from '../ui/Button.jsx';
import StatusBadge from '../ui/StatusBadge.jsx';

export default function UploadPanel() {
  const [file, setFile] = useState(null);
  const [cameraId, setCameraId] = useState('');
  const [capturedAt, setCapturedAt] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const preview = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!file) {
      setError(new Error('Select a traffic camera image before upload.'));
      return;
    }

    setSubmitting(true);
    setError(null);
    setResult(null);
    try {
      const uploaded = await uploadImage({
        file,
        cameraId: cameraId.trim(),
        capturedAt: capturedAt ? new Date(capturedAt).toISOString() : '',
      });
      setResult(uploaded);
    } catch (err) {
      setError(err);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_380px]" onSubmit={handleSubmit}>
      <div className="surface p-5">
        <label
          htmlFor="image-upload"
          className="focus-ring flex min-h-[320px] cursor-pointer flex-col items-center justify-center border-2 border-dashed border-slate-300 bg-slate-50 p-6 text-center transition hover:border-civic-authority dark:border-slate-700 dark:bg-slate-900 dark:hover:border-teal-400"
        >
          {preview ? (
            <img src={preview} alt="Selected traffic upload" className="max-h-[300px] w-full object-contain" />
          ) : (
            <>
              <UploadCloud size={42} className="text-civic-authority dark:text-teal-300" />
              <span className="mt-4 text-base font-semibold text-slate-950 dark:text-white">
                Select traffic camera image
              </span>
              <span className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                JPEG, PNG, or WebP up to the configured backend limit
              </span>
            </>
          )}
        </label>
        <input
          id="image-upload"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="sr-only"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />
      </div>

      <div className="space-y-5">
        <div className="surface p-5">
          <h2 className="text-base font-semibold text-slate-950 dark:text-white">Upload Metadata</h2>
          <div className="mt-5 space-y-4">
            <label className="block">
              <span className="mb-1.5 flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                <Camera size={16} />
                Camera ID
              </span>
              <input
                value={cameraId}
                onChange={(event) => setCameraId(event.target.value)}
                placeholder="Optional UUID"
                className="focus-ring w-full border border-slate-200 bg-white px-3 py-2 text-sm text-slate-950 dark:border-slate-800 dark:bg-slate-950 dark:text-white"
              />
            </label>
            <label className="block">
              <span className="mb-1.5 flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                <CalendarClock size={16} />
                Captured at
              </span>
              <input
                type="datetime-local"
                value={capturedAt}
                onChange={(event) => setCapturedAt(event.target.value)}
                className="focus-ring w-full border border-slate-200 bg-white px-3 py-2 text-sm text-slate-950 dark:border-slate-800 dark:bg-slate-950 dark:text-white"
              />
            </label>
          </div>
          <Button type="submit" icon={UploadCloud} disabled={submitting} className="mt-5 w-full">
            {submitting ? 'Uploading' : 'Upload and Analyze'}
          </Button>
        </div>

        {error ? (
          <div className="border-l-4 border-l-civic-alert bg-red-50 p-4 text-sm text-red-800 dark:bg-red-950/30 dark:text-red-200">
            {error.message}
          </div>
        ) : null}

        {result ? (
          <div className="surface p-5">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-base font-semibold text-slate-950 dark:text-white">Upload Result</h2>
              <StatusBadge value={result.processing_status} />
            </div>
            <dl className="mt-4 space-y-3 text-sm">
              <Row label="File" value={result.original_filename} />
              <Row label="Size" value={`${Math.round(result.file_size_bytes / 1024)} KB`} />
              <Row label="Violations" value={result.detected_violations} />
            </dl>
          </div>
        ) : null}
      </div>
    </form>
  );
}

function Row({ label, value }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-slate-500 dark:text-slate-400">{label}</dt>
      <dd className="text-right font-medium text-slate-950 dark:text-white">{value}</dd>
    </div>
  );
}
