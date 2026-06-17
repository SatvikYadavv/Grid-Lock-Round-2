import {
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  LinearScale,
  Tooltip,
} from 'chart.js';
import { useEffect, useRef } from 'react';
import { formatViolationType } from '../../utils/formatters.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip);

export default function ViolationTypeChart({ data = [] }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) {
      return undefined;
    }

    const labels = data.map((item) => formatViolationType(item.violation_type));
    const values = data.map((item) => item.count);

    const chart = new Chart(canvasRef.current, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Violations',
            data: values,
            backgroundColor: ['#1f4e79', '#0f766e', '#b45309', '#b91c1c'],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: (items) => items[0]?.label || '',
            },
          },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: '#64748b', maxRotation: 0, autoSkip: false },
          },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(148, 163, 184, 0.2)' },
            ticks: { precision: 0, color: '#64748b' },
          },
        },
      },
    });

    return () => chart.destroy();
  }, [data]);

  return <canvas ref={canvasRef} aria-label="Violation type chart" role="img" />;
}

