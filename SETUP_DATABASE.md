# Database Setup Guide for Neon + Netlify

This guide will help you migrate your RCL Questionnaire from JSON file storage to Neon PostgreSQL database on Netlify.

## Overview

The application now supports:
- ✅ Neon PostgreSQL database (production)
- ✅ JSON file fallback (local development)
- ✅ Automatic migration from existing JSON data
- ✅ Backward compatible API endpoints

## Quick Start

### 1. Create Neon Database

1. Sign up at https://neon.tech (free tier available)
2. Create a new project
3. Copy your connection string from the dashboard
   - Format: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`

### 2. Set Environment Variables

#### Local Development

Create a `.env` file in the project root:

```bash
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
```

#### Netlify Deployment

1. Go to Netlify Dashboard → Your Site → Site Settings → Environment Variables
2. Add new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Your Neon connection string
3. Redeploy your site

### 3. Install Dependencies

```bash
npm install
```

This installs `@neondatabase/serverless` and `tsx` for running scripts.

### 4. Initialize Database

```bash
npm run db:init
```

This will:
- Create all database tables
- Insert question definitions from `src/lib/questions.ts`
- Set up the default survey

### 5. Migrate Existing Data (Optional)

If you have existing responses in `src/lib/responses.json`:

```bash
npm run migrate
```

This migrates all existing responses to the database.

## Project Structure

```
├── database/
│   ├── schema.sql          # Database schema
│   └── README.md           # Database documentation
├── scripts/
│   ├── init-db.ts          # Initialize database tables
│   ├── migrate-json-to-db.ts  # Migrate JSON to database
│   └── export-responses-to-json.ts  # Export database to JSON
├── src/
│   ├── lib/
│   │   └── db/
│   │       └── index.ts    # Database service layer
│   └── routes/
│       └── api/
│           └── save-response/
│               └── +server.ts  # Updated API endpoint
└── netlify.toml            # Netlify configuration
```

## Database Schema

### Tables

1. **surveys** - Survey definitions
2. **questions** - Question definitions (from `questions.ts`)
3. **responses** - Each survey submission
4. **answers** - Individual answer values

### Key Features

- Questions are stored with their IDs (e.g., `fullName`, `A_taste`)
- Answers support both simple values (text/number) and complex data (arrays/objects)
- Backward compatible with existing JSON structure

## API Changes

The `/api/save-response` endpoint now:

1. **First tries** to save to Neon database
2. **Falls back** to JSON file if database is unavailable (local dev)
3. **Returns** the same response format for compatibility

No frontend changes required!

## Scripts Reference

| Command | Description |
|---------|-------------|
| `npm run db:init` | Initialize database tables and questions |
| `npm run migrate` | Migrate existing JSON responses to database |
| `npm run db:export` | Export database responses to JSON file |

## Analysis Notebook

Your Jupyter notebook (`src/lib/analysis.ipynb`) can continue using JSON files, or you can:

1. **Option 1**: Export database to JSON before analysis
   ```bash
   npm run db:export
   ```

2. **Option 2**: Update notebook to read directly from database
   - Use the `db.getResponsesAsJSON()` function
   - See `src/lib/db/index.ts` for examples

## Troubleshooting

### "DATABASE_URL is required" Error

- Ensure `.env` file exists (local) or environment variable is set (Netlify)
- Check connection string format
- Verify Neon project is active

### Migration Fails

- Run `npm run db:init` first
- Check that `responses.json` is valid JSON
- Verify database connection

### Connection Timeout

- Check Neon project status
- Verify connection string includes `?sslmode=require`
- Ensure IP allowlist allows connections (if configured)

### Responses Not Saving

- Check browser console for errors
- Verify API endpoint is working
- Check Netlify function logs
- Ensure database has write permissions

## Environment Variables

### Required

- `DATABASE_URL` or `NETLIFY_DATABASE_URL` - Neon connection string

### Optional

- None (application has sensible defaults)

## Deployment Checklist

- [ ] Create Neon database
- [ ] Set `DATABASE_URL` in Netlify environment variables
- [ ] Run `npm run db:init` (or create a one-time setup function)
- [ ] Deploy to Netlify
- [ ] Verify responses are saving correctly
- [ ] (Optional) Migrate existing data

## Security Notes

- ✅ Connection strings use SSL (`sslmode=require`)
- ✅ Database credentials stored in environment variables
- ✅ No credentials in code or version control
- ✅ Prepared statements prevent SQL injection

## Support

For issues:
1. Check Netlify function logs
2. Verify Neon dashboard for connection status
3. Review `database/README.md` for detailed schema info

## Next Steps

- Consider adding response analytics endpoints
- Set up automated backups
- Add response export functionality
- Implement response editing/deletion (if needed)

