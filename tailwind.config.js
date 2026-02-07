// tailwind.config.js
import daisyui from 'daisyui';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './src/app.html'],
  theme: {
    extend: {},
  },
  plugins: [forms, typography, daisyui],
  daisyui: {
    themes: [
      {
        rusks: {
          // Primary: Deep Blue
          "primary": "#0066A1",
          "primary-focus": "#004d7a",
          "primary-content": "#ffffff",
          
          // Secondary: Gold/Yellow
          "secondary": "#FDB913",
          "secondary-focus": "#e5a510",
          "secondary-content": "#1a1a1a",
          
          // Accent: Teal/Cyan
          "accent": "#009FD4",
          "accent-focus": "#0085b3",
          "accent-content": "#ffffff",
          
          // Neutral: Dark Gray
          "neutral": "#3d4451",
          "neutral-focus": "#2a2e37",
          "neutral-content": "#ffffff",
          
          // Base colors (backgrounds)
          "base-100": "#ffffff",
          "base-200": "#f3f4f6",
          "base-300": "#e5e7eb",
          "base-content": "#1f2937",
          
          // State colors
          "info": "#3ABFF8",
          "info-content": "#002b3d",
          
          "success": "#36D399",
          "success-content": "#003320",
          
          "warning": "#FBBD23",
          "warning-content": "#382800",
          
          "error": "#F87272",
          "error-content": "#470000",
        },
      },
    ],
    darkTheme: false,
    base: true,
    styled: true,
    utils: true,
  },
};