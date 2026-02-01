# DaisyUI + Tailwind v4 Compatibility Fix

## The Real Problem

DaisyUI v5 may not fully support Tailwind CSS v4's new `@plugin` syntax. Tailwind v4 uses a completely different plugin system than v3.

## Current Setup

- **Tailwind CSS**: v4.1.17 (uses `@tailwindcss/vite` plugin)
- **DaisyUI**: v5.5.14
- **Configuration**: Mix of CSS-based (`@plugin`) and JS config file

## Solution Options

### Option 1: Use tailwind.config.js (Recommended for DaisyUI)

Tailwind v4 can still read from `tailwind.config.js` for plugin compatibility. The config file approach should work better with DaisyUI.

**Current status**: 
- ✅ `tailwind.config.js` exists with DaisyUI plugin configured
- ✅ Custom "rusks" theme is defined
- ⚠️ CSS file uses `@plugin` syntax which might conflict

### Option 2: Import DaisyUI CSS Directly

If the plugin approach doesn't work, we can import DaisyUI's compiled CSS:

```css
@import 'daisyui/dist/full.css';
```

But this won't generate Tailwind utility classes - it only provides component styles.

### Option 3: Downgrade to Tailwind v3

If DaisyUI doesn't work with v4, we might need to use Tailwind v3:

```bash
npm install -D tailwindcss@^3 postcss autoprefixer
npm uninstall @tailwindcss/vite @tailwindcss/forms @tailwindcss/typography
```

## Recommended Fix

1. **Keep using `tailwind.config.js`** - Tailwind v4 should still read it for plugins
2. **Remove `@plugin 'daisyui'` from CSS** - Use the config file instead
3. **Keep theme definitions in CSS** - For Tailwind v4's CSS variables

## Testing

After changes, test locally:
```bash
npm run build
npm run preview
```

Check if DaisyUI classes work in the built output.

## If Still Not Working

Consider:
1. Check DaisyUI GitHub issues for Tailwind v4 compatibility
2. Use Tailwind v3 instead (more stable with DaisyUI)
3. Import DaisyUI CSS directly as fallback

