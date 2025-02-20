/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme'

export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    screens: {
      pc: '970px',
      tablet: '768px',
      sm: '640px',
    },
    extend: {
      fontFamily: ['Open Sans', ...defaultTheme.fontFamily.sans],
      colors: {
        'brand-gray-1': '#dadce0',
        'brand-blue-1': '#1967d2',
        'brand-blue-2': '#4285f4',
        'brand-green-1': '#137333',
      },
      boxShadow: {
        blue: '0 0 3px 3px #4285f4',
      },
      animation: {
        spin: 'spin 2s linear infinite',
      },
      keyframes: {
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
    },
  },
  plugins: [],
}
