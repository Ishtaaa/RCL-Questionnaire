# Netlify + Netlify DB (Neon) deployment

This app uses **Netlify DB** (powered by Neon) so Netlify can create and wire a Postgres database for you.

## One-time setup

### 1. Enable Netlify DB

**Option A – Let the build create the database (recommended)**

- The repo already has `@netlify/neon` installed.
- Deploy the site (connect the repo to Netlify and push, or run `netlify build`).
- Netlify will create a Neon database and set `NETLIFY_DATABASE_URL` automatically when the build runs.

**Option B – Create the database from your machine**

- Node.js 20.12.2 or later.
- In the project root run:
  ```bash
  npx netlify db init
  ```
- Follow the prompts to create the database and link the project.

### 2. Claim your database (required for production)

- In the Netlify dashboard: **Extensions** → **Neon** (install the Neon extension if needed).
- Click **Connect Neon** and complete the Neon account / authorization steps.
- On the project’s Neon extension page, click **Claim database** so the database stays active beyond the initial period and you can manage it in the Neon console.

### 3. Create tables and seed questions

After the database exists (and is claimed if you want it long-term):

- **Option A – Neon SQL Editor**  
  In the [Neon console](https://console.neon.tech), open the SQL Editor for your project and run the contents of `database/schema.sql`. Then, to load questions from the app, run once locally with the DB URL set:
  ```bash
  NETLIFY_DATABASE_URL="postgresql://..." npm run db:init
  ```
  (Get the connection string from Netlify: Site → Environment variables → `NETLIFY_DATABASE_URL`, or from the Neon dashboard.)

- **Option B – Local one-off (recommended)**  
  Put your Neon URL in a `.env` file in the project root (no spaces around `=`):
  ```
  DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
  ```
  Then run:
  ```bash
  npm run db:init
  ```
  Use `npm run migrate` if you have existing data in `src/lib/responses.json` to import.

- **PowerShell (one-off without .env)**  
  In PowerShell, set the variable then run the script (use one line or run `$env:DATABASE_URL = "..."` first):
  ```powershell
  $env:DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"; npm run db:init
  ```
  Do not use `VAR=value command`; that is bash syntax and will not work in PowerShell.

## How the app uses the database

- **On Netlify**: The app uses `@netlify/neon` and reads `NETLIFY_DATABASE_URL` (set by Netlify DB). No need to set `DATABASE_URL` in the Netlify UI if you use Netlify DB.
- **Locally**: Set `DATABASE_URL` in `.env` (or `NETLIFY_DATABASE_URL` if you prefer) so `npm run dev` / `npm run db:init` use your Neon DB. With `netlify dev`, Netlify can inject `NETLIFY_DATABASE_URL` for you.
- **Fallback**: If no database URL is available, `POST /api/save-response` falls back to writing to a JSON file.

## After deploy

- Home: `/`
- Questionnaire: `/questionnaire`
- API: `POST /api/save-response` (writes to Netlify DB when `NETLIFY_DATABASE_URL` is set).

## Troubleshooting

- **DaisyUI / styling**: Theme is in `src/app.html` (`data-theme="rusks"`) and `tailwind.config.js`. Do not add a root `_redirects` that sends `/*` to `index.html`; the Netlify adapter handles routing.
- **Navigation**: “Begin questionnaire” is an `<a href="/questionnaire">` so it works without JavaScript.
- **DB not found**: Ensure the Neon extension is installed and the database is claimed. Check **Site settings → Environment variables** for `NETLIFY_DATABASE_URL` (or `DATABASE_URL` if you set it manually).
