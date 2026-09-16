/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      colors: {
        engine: {
          dark: '#0d1117',
          card: '#161b22',
          border: '#30363d',
          accent: '#238636',
          danger: '#da3633',
          warning: '#d29922',
          cyan: '#38bdf8'
        }
      }
    },
  },
  plugins: [],
}
