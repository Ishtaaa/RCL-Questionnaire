/**
 * Database initialization script
 * Creates tables and initializes questions in the Neon database
 */

import { neon } from '@neondatabase/serverless';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { db } from '../src/lib/db/index.js';
import { questions } from '../src/lib/questions.js';

const DATABASE_URL = process.env.DATABASE_URL || process.env.NETLIFY_DATABASE_URL;

if (!DATABASE_URL) {
  console.error('Error: DATABASE_URL or NETLIFY_DATABASE_URL environment variable is required');
  process.exit(1);
}

const sql = neon(DATABASE_URL);

async function initDatabase() {
  try {
    console.log('Initializing database...\n');

    // Step 1: Read and execute schema
    console.log('Step 1: Creating database tables...');
    const schemaPath = join(process.cwd(), 'database', 'schema.sql');
    const schema = readFileSync(schemaPath, 'utf-8');
    
    // Execute schema (split by semicolons for individual statements)
    const statements = schema
      .split(';')
      .map(s => s.trim())
      .filter(s => s.length > 0 && !s.startsWith('--'));
    
    for (const statement of statements) {
      try {
        await sql(statement);
      } catch (error: any) {
        // Ignore "already exists" errors
        if (!error.message?.includes('already exists')) {
          console.warn(`Warning executing statement: ${error.message}`);
        }
      }
    }
    console.log('✓ Database tables created\n');

    // Step 2: Initialize questions
    console.log('Step 2: Initializing questions...');
    await db.initializeQuestions(questions);
    console.log('✓ Questions initialized\n');

    // Step 3: Verify setup
    console.log('Step 3: Verifying setup...');
    const questionCount = await sql`SELECT COUNT(*) as count FROM questions`;
    const responseCount = await sql`SELECT COUNT(*) as count FROM responses`;
    
    console.log(`✓ Questions in database: ${questionCount[0].count}`);
    console.log(`✓ Responses in database: ${responseCount[0].count}`);
    console.log('\n✓ Database initialization complete!');

  } catch (error) {
    console.error('Database initialization failed:', error);
    process.exit(1);
  }
}

initDatabase();

