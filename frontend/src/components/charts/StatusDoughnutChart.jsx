import { ArcElement, Chart, DoughnutController, Tooltip } from 'chart.js';
import { useEffect, useRef } from 'react';
import { formatViolationType } from '../../utils/formatters.js';

Chart.register(DoughnutController, ArcElement, Tooltip);

export default function StatusDoughnutChart({ data = [] }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) {
      return undefined;
    }

    const chart = new Chart(canvasRef.current, {
      type: 'doughnut',
      data: {
        labels: data.map((item) => formatViolationType(item.status)),
        datasets: [
          {
            data: data.map((item) => item.count),
            backgroundColor: ['#b45309', '#0f766e', '#64748b'],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: { display: false },
        },
      },
    });

    return () => chart.destroy();
  }, [data]);

  return <canvas ref={canvasRef} aria-label="Violation status chart" role="img" />;
}

