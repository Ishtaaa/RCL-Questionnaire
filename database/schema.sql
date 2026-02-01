-- Database Schema for RCL Questionnaire
-- Adapted for Neon PostgreSQL on Netlify

-- Surveys table (for future multi-survey support)
CREATE TABLE IF NOT EXISTS surveys (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL DEFAULT 'RCL Questionnaire',
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Questions table (stores question definitions)
CREATE TABLE IF NOT EXISTS questions (
  id SERIAL PRIMARY KEY,
  survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE DEFAULT 1,
  question_id VARCHAR(100) NOT NULL UNIQUE, -- e.g., 'fullName', 'A_taste'
  question_text TEXT NOT NULL,
  question_type VARCHAR(50) NOT NULL, -- 'text', 'number', 'rating', 'radio', 'checkbox'
  options JSONB, -- For multiple choice/checkbox options
  required BOOLEAN DEFAULT false,
  scale INTEGER, -- For rating questions
  placeholder TEXT,
  order_index INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(survey_id, question_id)
);

-- Responses table (stores each submission)
CREATE TABLE IF NOT EXISTS responses (
  id SERIAL PRIMARY KEY,
  survey_id INTEGER REFERENCES surveys(id) ON DELETE CASCADE DEFAULT 1,
  submitted_at TIMESTAMP DEFAULT NOW()
);

-- Answers table (stores individual answer values)
-- Uses JSONB for flexible storage of different answer types
CREATE TABLE IF NOT EXISTS answers (
  id SERIAL PRIMARY KEY,
  response_id INTEGER REFERENCES responses(id) ON DELETE CASCADE,
  question_id VARCHAR(100) NOT NULL, -- References questions.question_id
  answer_value TEXT, -- For simple text/number answers
  answer_data JSONB, -- For complex answers (arrays, objects)
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_questions_survey_id ON questions(survey_id);
CREATE INDEX IF NOT EXISTS idx_questions_question_id ON questions(question_id);
CREATE INDEX IF NOT EXISTS idx_responses_survey_id ON responses(survey_id);
CREATE INDEX IF NOT EXISTS idx_responses_submitted_at ON responses(submitted_at);
CREATE INDEX IF NOT EXISTS idx_answers_response_id ON answers(response_id);
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON answers(question_id);

-- Insert default survey
INSERT INTO surveys (id, title, description) 
VALUES (1, 'RCL Questionnaire', 'BBQ Chicken Pocket Product Survey')
ON CONFLICT (id) DO NOTHING;

