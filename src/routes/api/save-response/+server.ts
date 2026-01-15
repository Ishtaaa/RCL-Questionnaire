import { json } from '@sveltejs/kit';
import { existsSync } from 'node:fs';
import { readFileSync } from 'node:fs';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';

const RESPONSES_PATH = path.join(process.cwd(), 'src', 'lib', 'responses.json');

export async function POST({ request }) {
  try {
    const body = await request.json();

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

    return json({ success: true });
  } catch (error) {
    console.error('Error saving response:', error);
    return json({ success: false, error: 'Failed to save response' }, { status: 500 });
  }
}

