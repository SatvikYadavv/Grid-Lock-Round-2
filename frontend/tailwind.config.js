/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'sans-serif'],
      },
      colors: {
        civic: {
          ink: '#111827',
          paper: '#f7f8fb',
          line: '#d8dee9',
          authority: '#1f4e79',
          teal: '#0f766e',
          amber: '#b45309',
          alert: '#b91c1c',
        },
      },
      boxShadow: {
        panel: '0 12px 30px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
};

