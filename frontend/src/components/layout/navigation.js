import {
  BarChart3,
  FileSearch,
  Gauge,
  Map,
  ShieldCheck,
  UploadCloud,
} from 'lucide-react';

export const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: Gauge },
  { name: 'Upload', path: '/upload', icon: UploadCloud },
  { name: 'Evidence', path: '/evidence', icon: FileSearch },
  { name: 'Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Heatmap', path: '/heatmap', icon: Map },
  { name: 'Recommendations', path: '/recommendations', icon: ShieldCheck },
];

