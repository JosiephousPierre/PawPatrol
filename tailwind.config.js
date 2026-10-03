/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Arctic Reflection Color Palette
        primary: '#5289AD',
        'dark-blue': '#243C4C',
        'muted-blue': '#698696',
        'light-blue': '#ACBCBF',
        background: '#F4FCFB',
        // Status Colors
        'risk-safe': '#22c55e',
        'risk-low': '#eab308',
        'risk-moderate': '#f97316',
        'risk-high': '#ef4444',
        'risk-critical': '#991b1b'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'card': '12px',
        'card-lg': '16px'
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'card': '0 4px 12px rgba(0, 0, 0, 0.1)'
      }
    },
  },
  plugins: [],
}