/**
 * Export responses from database to JSON file
 * Useful for backup or for the analysis notebook
 * Loads .env so DATABASE_URL or NETLIFY_DATABASE_URL is available
 */

import 'dotenv/config';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { db } from '../src/lib/db/index.js';

const OUTPUT_PATH = join(process.cwd(), 'src', 'lib', 'responses.json');

async function exportResponses() {
  try {
    console.log('Exporting responses from database to JSON...\n');

    const responses = await db.getResponsesAsJSON();
    
    console.log(`Found ${responses.length} responses in database`);
    
    await writeFile(OUTPUT_PATH, JSON.stringify(responses, null, 2), 'utf-8');
    
    console.log(`✓ Exported ${responses.length} responses to ${OUTPUT_PATH}`);
    console.log('✓ Export complete!');
    
  } catch (error) {
    console.error('Export failed:', error);
    process.exit(1);
  }
}

exportResponses();

