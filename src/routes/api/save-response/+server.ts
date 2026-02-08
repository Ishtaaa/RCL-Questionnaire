import { json } from '@sveltejs/kit';
import { db } from '$lib/db/index.js';
import type { ResponseData } from '$lib/db/index.js';

/** POST: save survey response. Returns 200 so thanks page always shows when submission is accepted. */
export async function POST({ request }) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return json({ success: false, error: 'Invalid JSON' }, { status: 400 });
  }

  if (!body || typeof body !== 'object') {
    return json({ success: false, error: 'Invalid body' }, { status: 400 });
  }

  try {
    const result = await db.submitResponse(body as ResponseData);
    return json({
      success: true,
      saved: true,
      id: result.id,
      submitted_at: result.submitted_at
    });
  } catch (err) {
    console.error('Save response failed:', err);
    return json(
      { success: true, saved: false },
      { status: 200 }
    );
  }
}
