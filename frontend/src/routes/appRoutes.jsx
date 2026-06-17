import Analytics from '../pages/Analytics.jsx';
import Dashboard from '../pages/Dashboard.jsx';
import Evidence from '../pages/Evidence.jsx';
import Heatmap from '../pages/Heatmap.jsx';
import Recommendations from '../pages/Recommendations.jsx';
import Upload from '../pages/Upload.jsx';

export const appRoutes = [
  { path: '/dashboard', element: <Dashboard /> },
  { path: '/upload', element: <Upload /> },
  { path: '/evidence', element: <Evidence /> },
  { path: '/evidence/:id', element: <Evidence /> },
  { path: '/analytics', element: <Analytics /> },
  { path: '/heatmap', element: <Heatmap /> },
  { path: '/recommendations', element: <Recommendations /> },
];

