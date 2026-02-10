# RCL Questionnaire - Survey & Analysis Tool

A complete survey platform with real-time data analysis for comparing products (A/B testing). Collect feedback through an interactive web form and analyze responses with AI-powered insights.

## 🎯 What Does This Do?

This project helps you:
- **Collect Feedback**: Display an interactive web questionnaire where users rate and review two products
- **Store Responses**: Save all answers to a PostgreSQL database (Neon)
- **Analyze Data**: Use Python & machine learning to find patterns in feedback
- **Generate Reports**: Get visualizations and Excel exports with key insights

### Example Use Case
You're testing two versions of a BBQ chicken pocket (Product A vs B). You want to know:
- Which one tastes better?
- What do people like/dislike about each?
- Common themes in feedback (e.g., "too dry", "juicy", "good sauce")?
- Which should you market?

This tool answers all those questions automatically!

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Node.js** installed ([download](https://nodejs.org/))
- **Python 3.8+** installed ([download](https://www.python.org/))
- A code editor like [VS Code](https://code.visualstudio.com/)

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Set Up Database
Create a `.env` file in the project root with:
```
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
```

Get a free PostgreSQL database from [Neon](https://neon.tech/):
1. Sign up at https://neon.tech
2. Create a new project
3. Copy your connection string
4. Paste it as `DATABASE_URL` in `.env`

### Step 3: Initialize Database
```bash
npm run db:init
```

### Step 4: Start the Web App
```bash
npm run dev
```

Open http://localhost:5173 in your browser - the questionnaire will load!

### Step 5: Analyze Results
```bash
jupyter notebook src/lib/analysis.ipynb
```

Run the notebook cells to generate analysis and charts automatically.

---

## 📋 How It Works

### 1️⃣ Web Questionnaire (For Users)
- Users open the web app and fill out a survey
- They rate two products (A & B) on taste, appearance, etc.
- They write what they like/dislike about each
- Their responses are saved to the database

### 2️⃣ Data Storage (Database)
- All responses stored in PostgreSQL (Neon)
- Structured tables for questions, responses, and answers
- Encrypted connection to cloud database

### 3️⃣ Analysis Notebook (For You)
- Connect to database automatically
- Extract key phrases using AI (NLTK)
- Identify sentiment (positive/negative)
- Compare Product A vs B
- Generate charts and Excel reports

---

## 🎨 Features

### Survey Interface
- ✅ Clean, mobile-friendly design
- ✅ Multiple question types (text, ratings, multiple choice)
- ✅ Easy navigation with "Next" button
- ✅ Thank you page after submission

### Analysis Capabilities
- 📊 **Sentiment Analysis**: Understand if feedback is positive or negative
- 🏷️ **Tag Extraction**: Find common themes (e.g., "too salty", "juicy")
- 📈 **Comparisons**: Product A vs B metrics side-by-side
- 🔍 **Text Mining**: Extract adjectives and classify them
- 📉 **Visualizations**: Charts and graphs
- 📄 **Excel Reports**: Export all findings

---

## 📁 Project Structure

```
RCL-Questionnaire/
├── src/
│   ├── routes/               # Web pages
│   │   ├── +page.svelte      # Home page
│   │   └── questionnaire/    # Survey form
│   └── lib/
│       ├── analysis.ipynb    # Data analysis notebook
│       ├── db/               # Database code
│       └── questions.ts      # Survey questions
├── database/
│   └── schema.sql           # Database structure
├── scripts/
│   ├── export-responses-to-json.ts
│   ├── migrate-json-to-db.ts
│   └── init-db.ts
├── package.json             # Project dependencies
├── .env                     # Your database URL (keep secret!)
└── README.md               # This file
```

---

## 🛠️ Commands Reference

| Command | What It Does |
|---------|--------------|
| `npm run dev` | Start development server (http://localhost:5173) |
| `npm run build` | Create production version |
| `npm run db:init` | Set up database tables |
| `npm run db:export` | Export responses to JSON file |
| `npm run migrate` | Move old JSON responses to database |
| `jupyter notebook src/lib/analysis.ipynb` | Open analysis notebook |

---

## 📊 Analysis Notebook Guide

The notebook (`src/lib/analysis.ipynb`) does advanced analysis automatically:

### What It Analyzes
1. **Adjectives**: Extracts descriptive words (good, dry, juicy, etc.)
2. **Sentiment**: Classifies feedback as positive/negative
3. **Tags**: Finds themes like "too salty", "good portion"
4. **Comparisons**: Product A vs B ratings
5. **Cooking Methods**: Impact of different preparation methods

### Output Files
- `adjective_analysis.png` - Top adjectives per product
- `survey_analysis.png` - Rating comparisons
- `tag_sentiment_analysis.png` - Common themes
- `survey_analysis_results.xlsx` - Complete report

### Requirements
```bash
# Install Python dependencies (one time)
pip install pandas numpy matplotlib seaborn nltk psycopg2-binary
```

---

## 🔧 Common Tasks

### Add a New Question
Edit `src/lib/questions.ts` and add a question object to the list.

### Customize the Survey
1. Open `src/routes/questionnaire/+page.svelte`
2. Modify the form layout or styling
3. Changes appear automatically (hot reload)

### Export Responses as JSON
```bash
npm run db:export
```
Creates `src/lib/responses.json` with all responses.

### View Raw Data
```bash
npm run db:export
```
Then open `src/lib/responses.json` in your editor.

---

## 🚨 Troubleshooting

### "Cannot find module 'psycopg2'"
**Solution**: Run `pip install psycopg2-binary`

### "Database connection refused"
**Checks**:
- ✓ Is `.env` file in project root with `DATABASE_URL`?
- ✓ Is the Neon database URL correct?
- ✓ Does it have the right username/password?

### "Port 5173 already in use"
**Solution**: Run `npm run dev -- --port 5174`

### "No responses showing in analysis"
**Checks**:
- ✓ Did you submit responses via the questionnaire?
- ✓ Run `npm run db:export` to check responses are in database
- ✓ Try the fallback: Copy responses to `src/lib/responses.json`

---

## 📚 Documentation

- **Setup Guide**: See `ANALYSIS_SETUP.md` for detailed database info
- **Quick Reference**: See `QUICK_START.md` for analysis notebook
- **API Docs**: Database functions in `src/lib/db/index.ts`

---

## 🔐 Security Notes

⚠️ **Never commit `.env` to Git!** It contains your database password.

`.env` is already in `.gitignore` - it won't be tracked.

---

## 🎓 For Beginners: Concepts Explained

### What is a Database?
A database is like an Excel spreadsheet in the cloud that stores all your survey responses. PostgreSQL is a popular database system, and Neon hosts it for you.

### What is Node.js?
Node.js lets you run JavaScript outside the browser. `npm` is the package manager (like an app store for code libraries).

### What is Python/Jupyter?
Python is a programming language great for data analysis. Jupyter Notebook lets you write and run Python code in your browser, seeing results instantly.

### What is Svelte?
Svelte is a JavaScript framework for building interactive web apps (the questionnaire form you see in your browser).

---

## 📝 Example Workflow

1. **Day 1**: Set up project, initialize database
2. **Days 2-7**: Share questionnaire link with testers, collect 50+ responses
3. **Day 8**: Run analysis notebook
4. **Result**: Get insights on which product is better, why people prefer it, what to improve

---

## 💡 Tips

- Test the questionnaire yourself first before sharing
- Collect at least 20-30 responses for meaningful analysis
- Check the Excel export (`survey_analysis_results.xlsx`) for easy sharing
- Use `npm run dev -- --open` to automatically open the browser

---

## 🤝 Need Help?

Check these files for more details:
- `QUICK_START.md` - Analysis notebook quick guide
- `ANALYSIS_SETUP.md` - Complete setup documentation
- `database/schema.sql` - Database structure
- `src/lib/questions.ts` - Survey questions

---

## 📄 License

This project is open source. Feel free to use it for your own surveys!

---

**Happy surveying! 🎉**
