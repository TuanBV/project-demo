/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
    screens: {
      sp: { max: '768px' },
      md: { min: '769px' },
    },
  },
  plugins: [],
  prefix: 'tw-',
};
