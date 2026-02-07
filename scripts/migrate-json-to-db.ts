/**
 * Migration script to migrate existing JSON responses to Neon database
 * Run this once to migrate your existing data
 * Loads .env so DATABASE_URL or NETLIFY_DATABASE_URL is available
 */

import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { db } from '../src/lib/db/index.js';
import { questions } from '../src/lib/questions.js';

const RESPONSES_JSON_PATH = join(process.cwd(), 'src', 'lib', 'responses.json');

async function migrate() {
  try {
    console.log('Starting migration from JSON to Neon database...\n');

    // Step 1: Initialize questions in database
    console.log('Step 1: Initializing questions in database...');
    await db.initializeQuestions(questions);
    console.log('✓ Questions initialized\n');

    // Step 2: Read existing JSON responses
    console.log('Step 2: Reading existing JSON responses...');
    let jsonResponses: any[] = [];
    
    try {
      const jsonData = readFileSync(RESPONSES_JSON_PATH, 'utf-8');
      jsonResponses = JSON.parse(jsonData);
      console.log(`✓ Found ${jsonResponses.length} responses in JSON file\n`);
    } catch (error) {
      console.log('⚠ No existing JSON file found or file is empty. Skipping migration of responses.\n');
      console.log('Migration complete!');
      return;
    }

    // Step 3: Migrate responses
    console.log('Step 3: Migrating responses to database...');
    let successCount = 0;
    let errorCount = 0;

    for (let i = 0; i < jsonResponses.length; i++) {
      const response = jsonResponses[i];
      try {
        await db.submitResponse(response);
        successCount++;
        if ((i + 1) % 10 === 0) {
          console.log(`  Migrated ${i + 1}/${jsonResponses.length} responses...`);
        }
      } catch (error) {
        errorCount++;
        console.error(`  Error migrating response ${i + 1}:`, error);
      }
    }

    console.log(`\n✓ Migration complete!`);
    console.log(`  Successfully migrated: ${successCount} responses`);
    if (errorCount > 0) {
      console.log(`  Errors: ${errorCount} responses`);
    }

    // Step 4: Verify migration
    console.log('\nStep 4: Verifying migration...');
    const dbCount = await db.getResponseCount();
    console.log(`✓ Database now contains ${dbCount} responses`);
    
    if (dbCount === jsonResponses.length) {
      console.log('✓ All responses migrated successfully!');
    } else {
      console.log(`⚠ Warning: Expected ${jsonResponses.length} responses, found ${dbCount}`);
    }

  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

// Run migration
migrate();

