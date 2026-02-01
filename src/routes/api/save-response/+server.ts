import { json } from '@sveltejs/kit';
import { db } from '$lib/db/index.js';

/**
 * API endpoint to save survey responses to Neon database
 * Falls back to JSON file if database is not configured
 */
export async function POST({ request }) {
  try {
    const body = await request.json();

    // Try to save to database first
    try {
      const result = await db.submitResponse(body);
      return json({ 
        success: true, 
        id: result.id,
        submitted_at: result.submitted_at 
      });
    } catch (dbError) {
      // If database is not configured, fall back to JSON file
      console.warn('Database save failed, falling back to JSON file:', dbError);
      
      // Fallback to JSON file storage (for development/local)
      const { existsSync } = await import('node:fs');
      const { readFileSync } = await import('node:fs');
      const { writeFile } = await import('node:fs/promises');
      const path = await import('node:path');
      
      const RESPONSES_PATH = path.join(process.cwd(), 'src', 'lib', 'responses.json');
      
      let existing: unknown = [];
      
      if (existsSync(RESPONSES_PATH)) {
        const raw = readFileSync(RESPONSES_PATH, 'utf-8').trim();
        if (raw.length > 0) {
          try {
            existing = JSON.parse(raw);
          } catch {
            existing = [];
          }
        }
      }
      
      const responses = Array.isArray(existing) ? existing : [];
      responses.push(body);
      
      await writeFile(RESPONSES_PATH, JSON.stringify(responses, null, 2), 'utf-8');
      
      return json({ success: true, fallback: 'json' });
    }
  } catch (error) {
    console.error('Error saving response:', error);
    return json({ 
      success: false, 
      error: 'Failed to save response' 
    }, { status: 500 });
  }
}

