/**
 * Database service layer for Neon PostgreSQL
 * Handles all database operations for the questionnaire
 */

import { neon } from '@neondatabase/serverless';
import type { Question } from '../types';

// Get database URL from environment (optional - allows fallback to JSON)
function getDatabaseUrl(): string | null {
  return process.env.DATABASE_URL || process.env.NETLIFY_DATABASE_URL || null;
}

// Initialize Neon client lazily (only when needed)
function getSql() {
  const DATABASE_URL = getDatabaseUrl();
  if (!DATABASE_URL) {
    throw new Error('DATABASE_URL or NETLIFY_DATABASE_URL environment variable is required. Database operations are not available.');
  }
  return neon(DATABASE_URL);
}

export interface ResponseData {
  [key: string]: string | number | string[] | null;
}

export interface StoredResponse {
  id: number;
  survey_id: number;
  submitted_at: Date;
  answers: Array<{
    question_id: string;
    answer_value: string | null;
    answer_data: any;
  }>;
}

export const db = {
  /**
   * Initialize questions in database from questions.ts
   */
  async initializeQuestions(questions: Question[], surveyId: number = 1): Promise<void> {
    const sql = getSql();
    try {
      for (let i = 0; i < questions.length; i++) {
        const q = questions[i];
        await sql`
          INSERT INTO questions (
            survey_id, 
            question_id, 
            question_text, 
            question_type, 
            options, 
            required, 
            scale, 
            placeholder, 
            order_index
          )
          VALUES (
            ${surveyId},
            ${q.id},
            ${q.label},
            ${q.type},
            ${q.options ? JSON.stringify(q.options) : null},
            ${q.required ?? false},
            ${q.scale ?? null},
            ${q.placeholder ?? null},
            ${i}
          )
          ON CONFLICT (survey_id, question_id) 
          DO UPDATE SET
            question_text = EXCLUDED.question_text,
            question_type = EXCLUDED.question_type,
            options = EXCLUDED.options,
            required = EXCLUDED.required,
            scale = EXCLUDED.scale,
            placeholder = EXCLUDED.placeholder,
            order_index = EXCLUDED.order_index
        `;
      }
      console.log(`Initialized ${questions.length} questions in database`);
    } catch (error) {
      console.error('Error initializing questions:', error);
      throw error;
    }
  },

  /**
   * Submit a survey response
   */
  async submitResponse(
    responseData: ResponseData,
    surveyId: number = 1
  ): Promise<{ id: number; submitted_at: Date }> {
    const sql = getSql();
    try {
      // Insert response record
      const [response] = await sql`
        INSERT INTO responses (survey_id)
        VALUES (${surveyId})
        RETURNING id, submitted_at
      `;

      // Prepare and insert answers
      const answerEntries = Object.entries(responseData)
        .filter(([key]) => key !== 'timestamp') // Exclude timestamp from answers
        .map(([questionId, value]) => {
          // Determine if value should go in answer_value or answer_data
          const isSimpleValue = 
            typeof value === 'string' || 
            typeof value === 'number' || 
            value === null;
          
          return {
            response_id: response.id,
            question_id: questionId,
            answer_value: isSimpleValue ? String(value ?? '') : null,
            answer_data: !isSimpleValue ? JSON.stringify(value) : null
          };
        });

      // Insert answers (using Promise.all for parallel inserts)
      if (answerEntries.length > 0) {
        await Promise.all(
          answerEntries.map((answer) =>
            sql`
              INSERT INTO answers (response_id, question_id, answer_value, answer_data)
              VALUES (${answer.response_id}, ${answer.question_id}, ${answer.answer_value}, ${answer.answer_data})
            `
          )
        );
      }

      return {
        id: response.id,
        submitted_at: response.submitted_at
      };
    } catch (error) {
      console.error('Error submitting response:', error);
      throw error;
    }
  },

  /**
   * Get all responses for a survey
   */
  async getResponses(surveyId: number = 1): Promise<StoredResponse[]> {
    const sql = getSql();
    try {
      const responses = await sql`
        SELECT 
          r.id,
          r.survey_id,
          r.submitted_at,
          json_agg(
            json_build_object(
              'question_id', a.question_id,
              'answer_value', a.answer_value,
              'answer_data', a.answer_data
            )
          ) as answers
        FROM responses r
        LEFT JOIN answers a ON a.response_id = r.id
        WHERE r.survey_id = ${surveyId}
        GROUP BY r.id, r.survey_id, r.submitted_at
        ORDER BY r.submitted_at DESC
      `;

      return responses.map((r: any) => ({
        id: r.id,
        survey_id: r.survey_id,
        submitted_at: r.submitted_at,
        answers: r.answers || []
      }));
    } catch (error) {
      console.error('Error fetching responses:', error);
      throw error;
    }
  },

  /**
   * Get responses in the original JSON format (for backward compatibility)
   */
  async getResponsesAsJSON(surveyId: number = 1): Promise<ResponseData[]> {
    try {
      const responses = await this.getResponses(surveyId);
      
      return responses.map((response) => {
        const data: ResponseData = {
          timestamp: response.submitted_at.toISOString()
        };

        response.answers.forEach((answer: any) => {
          if (answer.answer_data) {
            // Parse JSON string back to object/array
            try {
              data[answer.question_id] = JSON.parse(answer.answer_data);
            } catch {
              // If parsing fails, use as-is
              data[answer.question_id] = answer.answer_data;
            }
          } else {
            // Try to parse as number if possible
            const numValue = Number(answer.answer_value);
            if (!isNaN(numValue) && answer.answer_value !== '' && answer.answer_value !== null) {
              data[answer.question_id] = numValue;
            } else {
              data[answer.question_id] = answer.answer_value;
            }
          }
        });

        return data;
      });
    } catch (error) {
      console.error('Error fetching responses as JSON:', error);
      throw error;
    }
  },

  /**
   * Get response count for a survey
   */
  async getResponseCount(surveyId: number = 1): Promise<number> {
    const sql = getSql();
    try {
      const [result] = await sql`
        SELECT COUNT(*) as count
        FROM responses
        WHERE survey_id = ${surveyId}
      `;
      return Number(result.count);
    } catch (error) {
      console.error('Error getting response count:', error);
      throw error;
    }
  },

  /**
   * Get all questions for a survey
   */
  async getQuestions(surveyId: number = 1): Promise<Question[]> {
    const sql = getSql();
    try {
      const questions = await sql`
        SELECT 
          question_id as id,
          question_text as label,
          question_type as type,
          options,
          required,
          scale,
          placeholder,
          order_index
        FROM questions
        WHERE survey_id = ${surveyId}
        ORDER BY order_index ASC
      `;

      return questions.map((q: any) => ({
        id: q.id,
        label: q.label,
        type: q.type,
        options: q.options,
        required: q.required,
        scale: q.scale,
        placeholder: q.placeholder
      }));
    } catch (error) {
      console.error('Error fetching questions:', error);
      throw error;
    }
  }
};

