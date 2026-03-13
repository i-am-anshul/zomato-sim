/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        rider: '#2563EB',
        restaurant: '#DC2626',
        nudge: '#F59E0B',
        ui: '#6B7280',
      },
    },
  },
  plugins: [],
};
