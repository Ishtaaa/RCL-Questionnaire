import adapter from '@sveltejs/adapter-netlify';
import { neon } from '@netlify/neon';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: { adapter: adapter() }
};
const DATABASE_URL = neon(process.env.DATABASE_URL || process.env.NEON_DATABASE_URL);
	if (!DATABASE_URL) {
		throw new Error('DATABASE_URL is not set');
	}
	const db = neon(DATABASE_URL);
	export async function submitResponse(response) {
		const result = await db.submitResponse(response);
		return result;
	}

export default config;
