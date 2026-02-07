/**
 * Database initialization script
 * Creates tables and initializes questions in the Neon database
 * Loads .env so DATABASE_URL or NETLIFY_DATABASE_URL is available
 */

import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import pg from 'pg';
import { db } from '../src/lib/db/index.js';
import { questions } from '../src/lib/questions.js';

const DATABASE_URL = process.env.DATABASE_URL || process.env.NETLIFY_DATABASE_URL;

if (!DATABASE_URL) {
  console.error('Error: DATABASE_URL or NETLIFY_DATABASE_URL is required.');
  console.error('Set it in .env (no spaces around =) or in PowerShell: $env:DATABASE_URL = "postgresql://..."');
  process.exit(1);
}

async function initDatabase() {
  const client = new pg.Client({ connectionString: DATABASE_URL });
  try {
    await client.connect();
    console.log('Initializing database...\n');

    // Step 1: Run schema (raw SQL)
    console.log('Step 1: Creating database tables...');
    const schemaPath = join(process.cwd(), 'database', 'schema.sql');
    const schema = readFileSync(schemaPath, 'utf-8');
    const statements = schema
      .split(';')
      .map((s) => s.trim())
      .filter((s) => s.length > 0 && !s.startsWith('--'));

    for (const statement of statements) {
      const sql = statement + ';';
      try {
        await client.query(sql);
      } catch (err: any) {
        if (!err.message?.includes('already exists')) {
          console.warn('Warning:', err.message);
        }
      }
    }
    console.log('✓ Database tables created\n');

    // Step 2: Initialize questions (uses app db layer; needs same env)
    console.log('Step 2: Initializing questions...');
    await db.initializeQuestions(questions);
    console.log('✓ Questions initialized\n');

    // Step 3: Verify
    console.log('Step 3: Verifying...');
    const q = await client.query('SELECT COUNT(*)::int as count FROM questions');
    const r = await client.query('SELECT COUNT(*)::int as count FROM responses');
    console.log(`✓ Questions: ${q.rows[0].count}, Responses: ${r.rows[0].count}`);
    console.log('\n✓ Database initialization complete.');
  } catch (error) {
    console.error('Database initialization failed:', error);
    process.exit(1);
  } finally {
    await client.end();
  }
}

initDatabase();
