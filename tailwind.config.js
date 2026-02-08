import path from 'node:path';
import { fileURLToPath } from 'node:url';
import daisyui from 'daisyui';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(__dirname, 'src');

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    path.join(src, '**', '*.{html,js,svelte,ts}'),
    path.join(src, 'app.html'),
  ],
  theme: {
    extend: {},
  },
  plugins: [forms, typography, daisyui],
  daisyui: {
    themes: [
      {
        rusks: {
          primary: '#0066A1',
          'primary-focus': '#004d7a',
          'primary-content': '#ffffff',
          secondary: '#FDB913',
          'secondary-focus': '#e5a510',
          'secondary-content': '#1a1a1a',
          accent: '#009FD4',
          'accent-focus': '#0085b3',
          'accent-content': '#ffffff',
          neutral: '#3d4451',
          'neutral-focus': '#2a2e37',
          'neutral-content': '#ffffff',
          'base-100': '#ffffff',
          'base-200': '#f3f4f6',
          'base-300': '#e5e7eb',
          'base-content': '#1f2937',
          info: '#3ABFF8',
          'info-content': '#002b3d',
          success: '#36D399',
          'success-content': '#003320',
          warning: '#FBBD23',
          'warning-content': '#382800',
          error: '#F87272',
          'error-content': '#470000',
        },
      },
    ],
    darkTheme: false,
    base: true,
    styled: true,
    utils: true,
    defaultTheme: 'rusks',
  },
  safelist: [
    { pattern: /^(btn|card|input|label|checkbox|radio|stat|loading|divider|form-control|figure)(-|$)/ },
    { pattern: /^(text|bg|border)-(primary|secondary|base-100|base-200|base-300|base-content|success|error|warning)/ },
    'label-text',
    'card-body',
    'card-actions',
    'stat-title',
    'stat-value',
    'loading-spinner',
    'loading-sm',
  ],
};
