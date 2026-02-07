// tailwind.config.js – Tailwind only (no DaisyUI)
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './src/app.html'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0066A1',
          hover: '#004d7a',
          light: '#e6f2f9',
        },
        secondary: {
          DEFAULT: '#FDB913',
          hover: '#e5a510',
        },
      },
    },
  },
  plugins: [forms, typography],
};
