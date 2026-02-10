"""
Helper script to fetch responses directly from Neon database for analysis
Use this if you want to export responses to JSON for backup or offline analysis
"""

import os
import json
import psycopg2
import psycopg2.extras
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent.parent / '.env'
load_dotenv(env_file)

def get_database_url():
    """Get database URL from environment variables"""
    db_url = os.environ.get('NETLIFY_DATABASE_URL')
    if db_url:
        return db_url
    
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        return db_url
    
    raise ValueError(
        "No database URL found. Please set DATABASE_URL or NETLIFY_DATABASE_URL in .env file"
    )

def fetch_responses_from_db(survey_id=1):
    """Fetch all responses from Neon database and convert to JSON format"""
    db_url = get_database_url()
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Fetch all responses with their answers
    cur.execute("""
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
        LEFT JOIN answers a ON r.id = a.response_id
        WHERE r.survey_id = %s
        GROUP BY r.id, r.survey_id, r.submitted_at
        ORDER BY r.submitted_at DESC
    """, (survey_id,))
    
    responses_data = cur.fetchall()
    cur.close()
    conn.close()
    
    # Convert to JSON format
    responses_json = []
    for row in responses_data:
        response_obj = {}
        
        if row['answers']:
            for answer in row['answers']:
                question_id = answer['question_id']
                answer_value = answer['answer_value']
                answer_data = answer['answer_data']
                
                if answer_data:
                    try:
                        response_obj[question_id] = json.loads(answer_data)
                    except json.JSONDecodeError:
                        response_obj[question_id] = answer_data
                else:
                    if answer_value is not None:
                        try:
                            num_value = float(answer_value)
                            if num_value == int(num_value):
                                response_obj[question_id] = int(num_value)
                            else:
                                response_obj[question_id] = num_value
                        except (ValueError, TypeError):
                            response_obj[question_id] = answer_value
                    else:
                        response_obj[question_id] = None
        
        responses_json.append(response_obj)
    
    return responses_json

if __name__ == '__main__':
    try:
        print("Fetching responses from Neon database...")
        responses = fetch_responses_from_db()
        print(f"✓ Retrieved {len(responses)} responses")
        
        # Print summary
        if responses:
            print(f"\nFirst response fields: {list(responses[0].keys())}")
            print(f"Total responses: {len(responses)}")
        else:
            print("No responses found in database")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        raise
