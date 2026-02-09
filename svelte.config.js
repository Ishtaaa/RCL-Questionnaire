import adapter from '@sveltejs/adapter-netlify';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  
  kit: {
    adapter: adapter({
      edge: false,
      split: false
    }),
    
    // Add this to help with function generation
    files: {
      assets: 'static'
    }
  }
};

export default config;