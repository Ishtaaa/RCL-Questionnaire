# Database Setup Guide

This guide will help you set up Neon PostgreSQL database for the RCL Questionnaire application.

## Prerequisites

1. A Neon account (sign up at https://neon.tech)
2. Node.js and npm installed
3. Access to your Neon project dashboard

## Step 1: Create Neon Database

1. Go to https://console.neon.tech
2. Create a new project (or use an existing one)
3. Copy your connection string from the dashboard
   - It should look like: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`

## Step 2: Set Environment Variables

### Local Development

Create a `.env` file in the project root:

```bash
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
```

### Netlify Deployment

1. Go to your Netlify dashboard
2. Navigate to: Site Settings > Environment Variables
3. Add a new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Your Neon connection string

Alternatively, you can use `NETLIFY_DATABASE_URL` as the variable name.

## Step 3: Install Dependencies

```bash
npm install
```

This will install `@neondatabase/serverless` package.

## Step 4: Initialize Database

Run the initialization script to create tables and set up questions:

```bash
npm run db:init
```

This will:
- Create all necessary database tables
- Insert question definitions from `src/lib/questions.ts`
- Set up the default survey

## Step 5: Migrate Existing Data (Optional)

If you have existing responses in `src/lib/responses.json`, migrate them:

```bash
npm run migrate
```

This will:
- Read all responses from `responses.json`
- Insert them into the Neon database
- Verify the migration was successful

## Step 6: Verify Setup

The application will automatically use the database when `DATABASE_URL` is set. If the database is not available, it will fall back to JSON file storage (for local development).

## Database Schema

The database consists of four main tables:

- **surveys**: Stores survey definitions
- **questions**: Stores question definitions (from `questions.ts`)
- **responses**: Stores each survey submission
- **answers**: Stores individual answer values for each response

See `database/schema.sql` for the complete schema.

## Troubleshooting

### Connection Issues

- Verify your connection string is correct
- Ensure your Neon project is active
- Check that SSL mode is set to `require` in the connection string

### Migration Errors

- Ensure the database is initialized first (`npm run db:init`)
- Check that `responses.json` is valid JSON
- Verify you have write permissions

### Environment Variables Not Working

- For local development: Ensure `.env` file is in the project root
- For Netlify: Verify variables are set in the dashboard and redeploy

## API Endpoints

The application uses the same API endpoint (`/api/save-response`) but now saves to the database instead of JSON files.

## Analysis Notebook

The Jupyter notebook (`src/lib/analysis.ipynb`) can be updated to read from the database instead of JSON. You can use the `db.getResponsesAsJSON()` function to get data in the same format as before.

