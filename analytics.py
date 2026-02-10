"""
RCL Questionnaire - Complete Survey Analysis (Windows Compatible)
Fetches data from Neon database and performs comprehensive NLP analysis
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Fix Windows console encoding issues
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ============================================================================
# DEPENDENCIES AND SETUP
# ============================================================================

print("=" * 80)
print("RCL SURVEY ANALYSIS - INITIALIZING")
print("=" * 80)

# Check and install required packages
def install_package(package_name, import_name=None):
    """Install a package if it's not already installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name, '--quiet'])
            print(f"[OK] {package_name} installed")
            return True
        except subprocess.CalledProcessError:
            print(f"[ERROR] Failed to install {package_name}")
            return False

# Install required packages
required_packages = [
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
    ('matplotlib', 'matplotlib'),
    ('seaborn', 'seaborn'),
    ('nltk', 'nltk'),
    ('psycopg2-binary', 'psycopg2'),
    ('openpyxl', 'openpyxl'),  # For Excel export
]

print("\nChecking dependencies...")
for package, import_name in required_packages:
    install_package(package, import_name)

# Import all required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# NLTK imports
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

# Database import
import psycopg2
import psycopg2.extras

# Download NLTK data
print("\nDownloading NLTK resources...")
nltk_resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'stopwords', 'vader_lexicon']
for resource in nltk_resources:
    try:
        nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else 
                       f'taggers/{resource}' if 'tagger' in resource else 
                       f'sentiment/{resource}' if resource == 'vader_lexicon' else 
                       f'corpora/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

print("[OK] All dependencies ready\n")

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def load_env_file():
    """Load environment variables from .env file"""
    env_paths = [
        Path('.env'),
        Path('../.env'),
        Path('../../.env'),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            print(f"Loading environment from: {env_path}")
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"\'')
            return True
    return False

def get_database_url():
    """Get database URL from environment variables"""
    # Load .env file if it exists
    load_env_file()
    
    # Try NETLIFY_DATABASE_URL first (production/Netlify)
    db_url = os.environ.get('NETLIFY_DATABASE_URL')
    if db_url:
        print("Using NETLIFY_DATABASE_URL")
        return db_url
    
    # Fall back to DATABASE_URL (local development)
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print("Using DATABASE_URL")
        return db_url
    
    return None

def fetch_responses_from_db(survey_id=1):
    """Fetch all responses from Neon database and convert to JSON format"""
    db_url = get_database_url()
    
    if not db_url:
        raise ValueError("No database URL found")
    
    try:
        print(f"Connecting to database...")
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
        
        print(f"[OK] Fetched {len(responses_data)} responses from database")
        
        # Convert to the same JSON format as responses.json
        responses_json = []
        for row in responses_data:
            response_obj = {}
            
            # Process answers
            if row['answers']:
                for answer in row['answers']:
                    question_id = answer['question_id']
                    answer_value = answer['answer_value']
                    answer_data = answer['answer_data']
                    
                    # Determine which field to use
                    if answer_data:
                        try:
                            response_obj[question_id] = json.loads(answer_data)
                        except json.JSONDecodeError:
                            response_obj[question_id] = answer_data
                    else:
                        # Try to parse as number if possible
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
    
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def load_data():
    """Load data from database or fallback to JSON file"""
    print("\n" + "=" * 80)
    print("DATA LOADING")
    print("=" * 80)
    
    # Try database first
    try:
        print("\nAttempting to fetch from Neon database...")
        data = fetch_responses_from_db()
        print(f"[OK] Successfully loaded {len(data)} responses from database")
        return data
    except Exception as e:
        print(f"[ERROR] Database fetch failed: {e}")
        print("\nFalling back to responses.json file...")
        
        # Fallback to responses.json
        possible_paths = [
            Path('responses.json'),
            Path('src/lib/responses.json'),
            Path('../src/lib/responses.json'),
            Path('../../src/lib/responses.json'),
        ]
        
        for p in possible_paths:
            if p.exists():
                with open(p, encoding='utf-8') as f:
                    data = json.load(f)
                print(f"[OK] Loaded {len(data)} responses from {p}")
                return data
        
        raise FileNotFoundError(
            "Could not find responses.json and database connection failed. "
            "Please ensure DATABASE_URL is set in .env or responses.json exists."
        )

# ============================================================================
# TEXT PROCESSING UTILITIES
# ============================================================================

def clean_text(text):
    """Clean and normalize text for analysis"""
    if pd.isna(text) or text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def normalize_text(text):
    """Normalize text input - handle all edge cases consistently"""
    if text is None:
        return ""
    if pd.isna(text):
        return ""
    
    text_str = str(text).strip()
    
    if not text_str or text_str.lower() in ['none', 'null', 'n/a', 'na']:
        return ""
    
    return text_str

# ============================================================================
# NLTK-BASED ADJECTIVE EXTRACTION
# ============================================================================

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

def get_wordnet_pos(treebank_tag):
    """Convert treebank POS tag to wordnet POS tag for lemmatization"""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def extract_adjectives(text):
    """Extract adjectives from text using NLTK POS tagging"""
    normalized_text = normalize_text(text)
    
    if not normalized_text:
        return []
    
    try:
        tokens = word_tokenize(normalized_text)
        
        if not tokens:
            return []
        
        pos_tags = pos_tag(tokens)
        
        adjectives = []
        for word, tag in pos_tags:
            if tag and tag.startswith('JJ'):
                word_lower = word.lower().strip()
                
                if (len(word_lower) > 2 and 
                    word_lower not in stop_words and 
                    any(c.isalpha() for c in word_lower)):
                    
                    try:
                        lemma = lemmatizer.lemmatize(word_lower, pos=wordnet.ADJ)
                        if lemma and any(c.isalpha() for c in lemma):
                            adjectives.append(lemma)
                    except Exception:
                        adjectives.append(word_lower)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_adjectives = []
        for adj in adjectives:
            if adj not in seen:
                seen.add(adj)
                unique_adjectives.append(adj)
        
        return unique_adjectives
        
    except Exception as e:
        print(f"Warning: Error processing text '{text[:50]}...': {str(e)}")
        return []

def classify_adjective_sentiment(adjective):
    """Classify if an adjective is positive or negative using VADER sentiment"""
    if not adjective or not isinstance(adjective, str):
        return 'neutral'
    
    adjective = adjective.lower().strip()
    if not adjective:
        return 'neutral'
    
    try:
        scores = sia.polarity_scores(adjective)
        compound = scores.get('compound', 0.0)
        
        if compound >= 0.1:
            return 'positive'
        elif compound <= -0.1:
            return 'negative'
        else:
            # Domain-specific word lists
            positive_words = {
                'good', 'great', 'nice', 'excellent', 'amazing', 'wonderful',
                'delicious', 'tasty', 'flavorful', 'flavourful', 'juicy', 
                'crispy', 'tender', 'sweet', 'savory', 'savoury', 'appetizing',
                'fresh', 'moist', 'succulent', 'yummy', 'scrumptious', 'delectable',
                'aromatic', 'crunchy', 'satisfying'
            }
            
            negative_words = {
                'bad', 'terrible', 'awful', 'bland', 'dry', 'soggy', 'greasy',
                'burnt', 'overcooked', 'undercooked', 'tough', 'hard', 'stale',
                'sour', 'bitter', 'salty', 'spicy', 'tasteless', 'flavorless',
                'flavourless', 'disgusting', 'unappetizing', 'rubbery', 'chewy',
                'mushy', 'watery', 'oily', 'overdone'
            }
            
            if adjective in positive_words:
                return 'positive'
            elif adjective in negative_words:
                return 'negative'
            else:
                return 'neutral'
                
    except Exception as e:
        print(f"Warning: Error classifying sentiment for '{adjective}': {str(e)}")
        return 'neutral'

def group_similar_adjectives(adjectives):
    """Group similar adjectives using synonym mapping"""
    if not adjectives:
        return {}
    
    synonym_groups = {
        'tasty': ['tasty', 'flavorful', 'flavourful', 'delicious', 'yummy', 
                  'scrumptious', 'delectable', 'appetizing'],
        'bland': ['bland', 'tasteless', 'flavorless', 'flavourless', 'boring'],
        'dry': ['dry', 'dried', 'dehydrated'],
        'juicy': ['juicy', 'moist', 'succulent', 'tender'],
        'crispy': ['crispy', 'crunchy', 'crisp'],
        'soggy': ['soggy', 'soft', 'mushy', 'watery'],
        'greasy': ['greasy', 'oily', 'fatty'],
        'sweet': ['sweet', 'sugary', 'sugared'],
        'salty': ['salty', 'salted', 'over-salted'],
        'spicy': ['spicy', 'hot', 'pungent'],
        'tender': ['tender', 'soft', 'delicate'],
        'tough': ['tough', 'hard', 'chewy', 'rubbery'],
        'fresh': ['fresh', 'crisp', 'new'],
        'stale': ['stale', 'old', 'rancid'],
        'burnt': ['burnt', 'burned', 'charred', 'overcooked'],
        'good': ['good', 'nice', 'fine', 'decent'],
        'great': ['great', 'excellent', 'amazing', 'wonderful'],
        'bad': ['bad', 'terrible', 'awful', 'poor'],
    }
    
    adj_to_group = {}
    for group_name, variants in synonym_groups.items():
        for variant in variants:
            adj_to_group[variant] = group_name
    
    final_groups = defaultdict(list)
    for adj in adjectives:
        if not adj or not isinstance(adj, str):
            continue
        adj_lower = adj.lower().strip()
        group_key = adj_to_group.get(adj_lower, adj_lower)
        final_groups[group_key].append(adj_lower)
    
    return dict(final_groups)

def analyze_adjectives_by_sentiment(adjectives_list, context='likes'):
    """Analyze adjectives and classify them as positive/negative based on context"""
    if not isinstance(adjectives_list, list):
        adjectives_list = []
    
    valid_adjectives = []
    for adj in adjectives_list:
        if adj and isinstance(adj, str) and adj.strip():
            valid_adjectives.append(adj.strip())
    
    positive_adjs = []
    negative_adjs = []
    neutral_adjs = []
    
    for adj in valid_adjectives:
        try:
            sentiment = classify_adjective_sentiment(adj)
            
            if context == 'likes':
                if sentiment in ['positive', 'neutral']:
                    positive_adjs.append(adj)
                else:
                    negative_adjs.append(adj)
            else:  # dislikes context
                if sentiment in ['negative', 'neutral']:
                    negative_adjs.append(adj)
                else:
                    positive_adjs.append(adj)
        except Exception as e:
            print(f"Warning: Error analyzing adjective '{adj}': {str(e)}")
            continue
    
    return {
        'positive': positive_adjs,
        'negative': negative_adjs,
        'neutral': neutral_adjs
    }

def group_and_count_adjectives(adjectives):
    """Group similar adjectives and count frequencies"""
    if not isinstance(adjectives, list):
        adjectives = []
    
    valid_adjectives = []
    for adj in adjectives:
        if adj and isinstance(adj, str) and adj.strip():
            valid_adjectives.append(adj.strip().lower())
    
    if not valid_adjectives:
        return Counter(), Counter()
    
    raw_counts = Counter(valid_adjectives)
    
    try:
        grouped = group_similar_adjectives(valid_adjectives)
    except Exception as e:
        print(f"Warning: Error grouping adjectives: {str(e)}")
        grouped = {}
    
    grouped_counts = Counter()
    for group_name, variants in grouped.items():
        if not variants:
            continue
        count = 0
        for variant in variants:
            count += raw_counts.get(variant, 0)
            count += raw_counts.get(variant.lower(), 0)
        if count > 0:
            grouped_counts[group_name] = count
    
    return raw_counts, grouped_counts

# ============================================================================
# TAG EXTRACTION
# ============================================================================

TAG_KEYWORDS = {
    "smoky": ["smoky"],
    "sweet": ["sweet"],
    "salty": ["salty", "too salty", "too much salt", "heavily salted"],
    "not_enough_salt": ["not enough salt", "needs more salt"],
    "bland": ["bland", "no flavour", "no flavor"],
    "good_flavour": ["nice flavour", "good flavour", "tasty", "flavorful", "flavourful", "good flavor"],
    "needs_more_sauce": ["not enough sauce", "needs more sauce", "more sauce", "could use more sauce"],
    "too_much_sauce": ["too much sauce"],
    "juicy_chicken": ["juicy", "tender chicken", "well cooked"],
    "dry_chicken": ["dry chicken", "chicken felt dry", "chicken a bit dry"],
    "not_filling": ["not filling", "not very filling", "needs more filling"],
    "good_portion": ["good portion", "good size", "filling", "more filling"],
    "crispy_pastry": ["crispy"],
    "dry_pastry": ["dry pastry", "pastry was a bit dry", "slightly dry"],
    "soggy_pastry": ["soggy"],
    "greasy": ["greasy"],
    "kids_liked": ["kids liked"],
    "too_strong_for_kids": ["too smoky for kids", "too strong for kids"],
    "kid_friendly": ["kids preferred", "kid friendly"],
    "would_buy": ["would buy", "buy again", "would buy regularly", "would definitely buy"],
    "would_not_buy": ["wouldn't buy", "would not buy", "skip"],
    "average": ["average", "okay", "fine", "decent", "ok"]
}

def extract_tags(text, tag_keywords):
    """Extract tags from text based on keyword matching"""
    text = clean_text(text)
    found_tags = []
    
    for tag, keywords in tag_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text:
                found_tags.append(tag)
                break
    
    return found_tags

def count_tags(tag_series):
    """Count frequency of all tags"""
    all_tags = []
    for tags in tag_series:
        if isinstance(tags, list):
            all_tags.extend(tags)
    return Counter(all_tags)

def calculate_tag_ratings(df, variant):
    """Calculate average taste ratings for each tag"""
    tag_ratings = defaultdict(list)
    taste_col = f'{variant}_taste'
    
    if taste_col not in df.columns:
        return {}
    
    for idx, row in df.iterrows():
        tags = row.get(f'{variant}_all_tags', [])
        taste_rating = row[taste_col]
        
        try:
            taste_value = float(taste_rating)
        except (TypeError, ValueError):
            continue
        
        for tag in tags:
            tag_ratings[tag].append(taste_value)
    
    tag_avg = {tag: np.mean(ratings) for tag, ratings in tag_ratings.items() if ratings}
    return tag_avg

# ============================================================================
# COOKING METHOD NORMALIZATION
# ============================================================================

def normalize_cooking_method(method):
    """Normalize cooking method variations to standard groups"""
    if pd.isna(method) or method is None:
        return "Unknown"
    
    method_str = str(method).strip().lower()
    
    normalization_map = {
        'air fryer': 'Air Fryer',
        'air fried': 'Air Fryer',
        'air fry': 'Air Fryer',
        'airfryer': 'Air Fryer',
        'air-fryer': 'Air Fryer',
        'air-fried': 'Air Fryer',
        'deep fried': 'Deep Fried',
        'deep fry': 'Deep Fried',
        'deep-fried': 'Deep Fried',
        'deep-fry': 'Deep Fried',
        'fried': 'Deep Fried',
        'oven': 'Oven',
        'baked': 'Oven',
        'bake': 'Oven',
        'oven baked': 'Oven',
        'oven-baked': 'Oven',
        'microwave': 'Microwave',
        'microwaved': 'Microwave',
        'microwave oven': 'Microwave',
        'stovetop': 'Stovetop',
        'stove top': 'Stovetop',
        'pan fried': 'Stovetop',
        'pan-fried': 'Stovetop',
        'pan fry': 'Stovetop',
        'sautéed': 'Stovetop',
        'sauteed': 'Stovetop',
        'grill': 'Grill',
        'grilled': 'Grill',
        'bbq': 'Grill',
        'barbecue': 'Grill',
    }
    
    if method_str in normalization_map:
        return normalization_map[method_str]
    
    for key, normalized in normalization_map.items():
        if key in method_str:
            return normalized
    
    return method_str.title()

# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================

def calculate_sentiment(likes, dislikes):
    """Simple sentiment based on presence of content"""
    likes_len = len(clean_text(likes).split())
    dislikes_len = len(clean_text(dislikes).split())
    
    if likes_len > dislikes_len * 2:
        return "Positive"
    elif dislikes_len > likes_len * 2:
        return "Negative"
    else:
        return "Neutral"

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    """Main analysis function"""
    
    # Load data
    data = load_data()
    df = pd.DataFrame(data)
    
    print("\n" + "=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)
    print(f"Total responses: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Clean text fields
    text_columns = ['A_likes', 'A_dislikes', 'A_Feedback', 'B_likes', 'B_dislikes', 'B_Feedback']
    for col in text_columns:
        if col in df.columns:
            df[f'{col}_clean'] = df[col].apply(clean_text)
    
    # ========================================================================
    # ADJECTIVE EXTRACTION
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("EXTRACTING ADJECTIVES USING NLTK")
    print("=" * 80)
    
    for variant in ['A', 'B']:
        likes_col = f'{variant}_likes'
        dislikes_col = f'{variant}_dislikes'
        
        # Extract adjectives
        if likes_col in df.columns:
            df[f'{variant}_likes_adjectives'] = df[likes_col].apply(extract_adjectives)
        else:
            df[f'{variant}_likes_adjectives'] = [[] for _ in range(len(df))]
        
        if dislikes_col in df.columns:
            df[f'{variant}_dislikes_adjectives'] = df[dislikes_col].apply(extract_adjectives)
        else:
            df[f'{variant}_dislikes_adjectives'] = [[] for _ in range(len(df))]
        
        # Combine adjectives
        def combine_adjectives(row):
            likes_adj = row.get(f'{variant}_likes_adjectives', [])
            dislikes_adj = row.get(f'{variant}_dislikes_adjectives', [])
            if not isinstance(likes_adj, list):
                likes_adj = []
            if not isinstance(dislikes_adj, list):
                dislikes_adj = []
            return likes_adj + dislikes_adj
        
        df[f'{variant}_all_adjectives'] = df.apply(combine_adjectives, axis=1)
        
        # Summary
        total_likes_adj = sum(len(adj_list) for adj_list in df[f'{variant}_likes_adjectives'] if isinstance(adj_list, list))
        total_dislikes_adj = sum(len(adj_list) for adj_list in df[f'{variant}_dislikes_adjectives'] if isinstance(adj_list, list))
        print(f"\n{variant} Summary: {total_likes_adj} adjectives from likes, {total_dislikes_adj} from dislikes")
    
    # ========================================================================
    # ADJECTIVE SENTIMENT ANALYSIS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("ADJECTIVE SENTIMENT ANALYSIS")
    print("=" * 80)
    
    for variant in ['A', 'B']:
        df[f'{variant}_likes_adj_analysis'] = df[f'{variant}_likes_adjectives'].apply(
            lambda x: analyze_adjectives_by_sentiment(x, context='likes')
        )
        
        df[f'{variant}_dislikes_adj_analysis'] = df[f'{variant}_dislikes_adjectives'].apply(
            lambda x: analyze_adjectives_by_sentiment(x, context='dislikes')
        )
        
        df[f'{variant}_positive_adjectives'] = df.apply(
            lambda row: row[f'{variant}_likes_adj_analysis']['positive'] + 
                        row[f'{variant}_dislikes_adj_analysis']['positive'],
            axis=1
        )
        
        df[f'{variant}_negative_adjectives'] = df.apply(
            lambda row: row[f'{variant}_likes_adj_analysis']['negative'] + 
                        row[f'{variant}_dislikes_adj_analysis']['negative'],
            axis=1
        )
    
    # Collect and group adjectives
    all_positive_A = []
    all_negative_A = []
    all_positive_B = []
    all_negative_B = []
    
    for idx, row in df.iterrows():
        try:
            pos_A = row.get('A_positive_adjectives', [])
            if isinstance(pos_A, list):
                all_positive_A.extend(pos_A)
        except Exception:
            pass
        
        try:
            neg_A = row.get('A_negative_adjectives', [])
            if isinstance(neg_A, list):
                all_negative_A.extend(neg_A)
        except Exception:
            pass
        
        try:
            pos_B = row.get('B_positive_adjectives', [])
            if isinstance(pos_B, list):
                all_positive_B.extend(pos_B)
        except Exception:
            pass
        
        try:
            neg_B = row.get('B_negative_adjectives', [])
            if isinstance(neg_B, list):
                all_negative_B.extend(neg_B)
        except Exception:
            pass
    
    # Group and count
    pos_A_raw, pos_A_grouped = group_and_count_adjectives(all_positive_A)
    neg_A_raw, neg_A_grouped = group_and_count_adjectives(all_negative_A)
    pos_B_raw, pos_B_grouped = group_and_count_adjectives(all_positive_B)
    neg_B_raw, neg_B_grouped = group_and_count_adjectives(all_negative_B)
    
    print("\n" + "=" * 80)
    print("PRODUCT A - ADJECTIVE ANALYSIS")
    print("=" * 80)
    print("\nPositive Adjectives (Grouped):")
    for adj, count in pos_A_grouped.most_common(15):
        print(f"  {adj}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\nNegative Adjectives (Grouped):")
    for adj, count in neg_A_grouped.most_common(15):
        print(f"  {adj}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n" + "=" * 80)
    print("PRODUCT B - ADJECTIVE ANALYSIS")
    print("=" * 80)
    print("\nPositive Adjectives (Grouped):")
    for adj, count in pos_B_grouped.most_common(15):
        print(f"  {adj}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\nNegative Adjectives (Grouped):")
    for adj, count in neg_B_grouped.most_common(15):
        print(f"  {adj}: {count} ({count/len(df)*100:.1f}%)")
    
    # ========================================================================
    # TAG EXTRACTION
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("TAG EXTRACTION")
    print("=" * 80)
    
    for variant in ['A', 'B']:
        likes_col = f'{variant}_likes'
        dislikes_col = f'{variant}_dislikes'
        feedback_col = f'{variant}_Feedback'
        
        if likes_col in df.columns:
            df[f'{variant}_likes_tags'] = df[likes_col].apply(lambda x: extract_tags(x, TAG_KEYWORDS))
        else:
            df[f'{variant}_likes_tags'] = [[] for _ in range(len(df))]
        
        if dislikes_col in df.columns:
            df[f'{variant}_dislikes_tags'] = df[dislikes_col].apply(lambda x: extract_tags(x, TAG_KEYWORDS))
        else:
            df[f'{variant}_dislikes_tags'] = [[] for _ in range(len(df))]
        
        if feedback_col in df.columns:
            df[f'{variant}_feedback_tags'] = df[feedback_col].apply(lambda x: extract_tags(x, TAG_KEYWORDS))
        else:
            df[f'{variant}_feedback_tags'] = [[] for _ in range(len(df))]
        
        df[f'{variant}_all_tags'] = df.apply(
            lambda row: list(set(
                row[f'{variant}_likes_tags'] + 
                row[f'{variant}_dislikes_tags'] + 
                row[f'{variant}_feedback_tags']
            )), axis=1
        )
    
    tag_freq_A = count_tags(df['A_all_tags'])
    tag_freq_B = count_tags(df['B_all_tags'])
    
    print("\nProduct A - Top Tags:")
    for tag, count in tag_freq_A.most_common(10):
        print(f"  {tag}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\nProduct B - Top Tags:")
    for tag, count in tag_freq_B.most_common(10):
        print(f"  {tag}: {count} ({count/len(df)*100:.1f}%)")
    
    # ========================================================================
    # TAG-RATING CORRELATION
    # ========================================================================
    
    tag_ratings_A = calculate_tag_ratings(df, 'A')
    tag_ratings_B = calculate_tag_ratings(df, 'B')
    
    print("\n" + "=" * 80)
    print("TAG vs RATING CORRELATION")
    print("=" * 80)
    
    print("\nProduct A - Tags with Highest Taste Ratings:")
    sorted_A = sorted(tag_ratings_A.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, rating in sorted_A:
        print(f"  {tag}: {rating:.2f}")
    
    print("\nProduct B - Tags with Highest Taste Ratings:")
    sorted_B = sorted(tag_ratings_B.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, rating in sorted_B:
        print(f"  {tag}: {rating:.2f}")
    
    # ========================================================================
    # COOKING METHOD ANALYSIS
    # ========================================================================
    
    if 'cookingMethod' in df.columns:
        df['cookingMethod_normalized'] = df['cookingMethod'].apply(normalize_cooking_method)
        
        print("\n" + "=" * 80)
        print("COOKING METHOD ANALYSIS")
        print("=" * 80)
        
        cooking_summary = df.groupby('cookingMethod_normalized').agg({
            'A_taste': 'mean',
            'B_taste': 'mean',
            'fullName': 'count'
        }).round(2)
        cooking_summary.columns = ['A Avg Taste', 'B Avg Taste', 'Count']
        cooking_summary = cooking_summary.sort_values('Count', ascending=False)
        print("\n", cooking_summary)
    
    # ========================================================================
    # SENTIMENT ANALYSIS
    # ========================================================================
    
    df['A_sentiment'] = df.apply(lambda x: calculate_sentiment(x.get('A_likes', ''), x.get('A_dislikes', '')), axis=1)
    df['B_sentiment'] = df.apply(lambda x: calculate_sentiment(x.get('B_likes', ''), x.get('B_dislikes', '')), axis=1)
    
    print("\n" + "=" * 80)
    print("SENTIMENT DISTRIBUTION")
    print("=" * 80)
    print("\nProduct A:")
    print(df['A_sentiment'].value_counts())
    print("\nProduct B:")
    print(df['B_sentiment'].value_counts())
    
    # ========================================================================
    # COMPARISON METRICS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("A vs B COMPARISON")
    print("=" * 80)
    
    comparison_metrics = {
        'Taste': ('A_taste', 'B_taste'),
        'Appearance': ('A_appearance', 'B_appearance'),
        'Self Relevance': ('A_selfRelevance', 'B_selfRelevance'),
        'Met Expectations': ('A_expectation', 'B_expectation'),
    }
    
    comparison_df = pd.DataFrame()
    for metric_name, (col_a, col_b) in comparison_metrics.items():
        if col_a in df.columns and col_b in df.columns:
            comparison_df[metric_name] = [
                df[col_a].mean(),
                df[col_b].mean(),
                df[col_b].mean() - df[col_a].mean()
            ]
    
    if not comparison_df.empty:
        comparison_df.index = ['Product A', 'Product B', 'Difference (B-A)']
        print("\n", comparison_df.round(2))
    
    # ========================================================================
    # VISUALIZATIONS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # Adjective visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    top_pos_A = dict(pos_A_grouped.most_common(10))
    if top_pos_A:
        axes[0, 0].barh(list(top_pos_A.keys()), list(top_pos_A.values()), color='green', alpha=0.7)
        axes[0, 0].set_xlabel('Frequency')
        axes[0, 0].set_title('Product A - Top 10 Positive Adjectives')
        axes[0, 0].invert_yaxis()
        axes[0, 0].grid(axis='x', alpha=0.3)
    
    top_neg_A = dict(neg_A_grouped.most_common(10))
    if top_neg_A:
        axes[0, 1].barh(list(top_neg_A.keys()), list(top_neg_A.values()), color='red', alpha=0.7)
        axes[0, 1].set_xlabel('Frequency')
        axes[0, 1].set_title('Product A - Top 10 Negative Adjectives')
        axes[0, 1].invert_yaxis()
        axes[0, 1].grid(axis='x', alpha=0.3)
    
    top_pos_B = dict(pos_B_grouped.most_common(10))
    if top_pos_B:
        axes[1, 0].barh(list(top_pos_B.keys()), list(top_pos_B.values()), color='green', alpha=0.7)
        axes[1, 0].set_xlabel('Frequency')
        axes[1, 0].set_title('Product B - Top 10 Positive Adjectives')
        axes[1, 0].invert_yaxis()
        axes[1, 0].grid(axis='x', alpha=0.3)
    
    top_neg_B = dict(neg_B_grouped.most_common(10))
    if top_neg_B:
        axes[1, 1].barh(list(top_neg_B.keys()), list(top_neg_B.values()), color='red', alpha=0.7)
        axes[1, 1].set_xlabel('Frequency')
        axes[1, 1].set_title('Product B - Top 10 Negative Adjectives')
        axes[1, 1].invert_yaxis()
        axes[1, 1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('adjective_analysis.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: adjective_analysis.png")
    
    # Tag and rating comparison
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    top_tags_A = dict(tag_freq_A.most_common(10))
    if top_tags_A:
        axes[0, 0].barh(list(top_tags_A.keys()), list(top_tags_A.values()), color='steelblue')
        axes[0, 0].set_xlabel('Frequency')
        axes[0, 0].set_title('Product A - Top 10 Tags')
        axes[0, 0].invert_yaxis()
    
    top_tags_B = dict(tag_freq_B.most_common(10))
    if top_tags_B:
        axes[0, 1].barh(list(top_tags_B.keys()), list(top_tags_B.values()), color='coral')
        axes[0, 1].set_xlabel('Frequency')
        axes[0, 1].set_title('Product B - Top 10 Tags')
        axes[0, 1].invert_yaxis()
    
    if 'A_taste' in df.columns and 'B_taste' in df.columns:
        if not comparison_df.empty:
            metrics = list(comparison_df.columns)
            a_scores = comparison_df.loc['Product A'].values
            b_scores = comparison_df.loc['Product B'].values
            
            x = np.arange(len(metrics))
            width = 0.35
            axes[1, 0].bar(x - width/2, a_scores, width, label='Product A', color='steelblue')
            axes[1, 0].bar(x + width/2, b_scores, width, label='Product B', color='coral')
            axes[1, 0].set_ylabel('Average Rating')
            axes[1, 0].set_title('A vs B - Key Metrics Comparison')
            axes[1, 0].set_xticks(x)
            axes[1, 0].set_xticklabels(metrics, rotation=45, ha='right')
            axes[1, 0].legend()
            axes[1, 0].grid(axis='y', alpha=0.3)
        
        axes[1, 1].hist([df['A_taste'], df['B_taste']], bins=9, label=['Product A', 'Product B'], 
                        color=['steelblue', 'coral'], alpha=0.7)
        axes[1, 1].set_xlabel('Taste Rating')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Taste Rating Distribution')
        axes[1, 1].legend()
        axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('survey_analysis.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: survey_analysis.png")
    
    # ========================================================================
    # EXPORT TO EXCEL
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)
    
    summary_results = {
        'Tag_Frequency_A': pd.DataFrame(tag_freq_A.most_common(), columns=['Tag', 'Count_A']),
        'Tag_Frequency_B': pd.DataFrame(tag_freq_B.most_common(), columns=['Tag', 'Count_B']),
        'Tag_Ratings_A': pd.DataFrame(sorted_A, columns=['Tag', 'Avg_Rating_A']),
        'Tag_Ratings_B': pd.DataFrame(sorted_B, columns=['Tag', 'Avg_Rating_B']),
        'Positive_Adj_A': pd.DataFrame(pos_A_grouped.most_common(), columns=['Adjective', 'Count']),
        'Negative_Adj_A': pd.DataFrame(neg_A_grouped.most_common(), columns=['Adjective', 'Count']),
        'Positive_Adj_B': pd.DataFrame(pos_B_grouped.most_common(), columns=['Adjective', 'Count']),
        'Negative_Adj_B': pd.DataFrame(neg_B_grouped.most_common(), columns=['Adjective', 'Count']),
    }
    
    if not comparison_df.empty:
        summary_results['Metrics_Comparison'] = comparison_df
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_filename = f'survey_analysis_results_{timestamp}.xlsx'
    
    with pd.ExcelWriter(excel_filename) as writer:
        for sheet_name, data in summary_results.items():
            if isinstance(data, pd.DataFrame) and not data.empty:
                data.to_excel(writer, sheet_name=sheet_name, 
                             index=True if sheet_name == 'Metrics_Comparison' else False)
        
        # Add raw data
        df.to_excel(writer, sheet_name='Raw_Data', index=False)
    
    print(f"[OK] Saved: {excel_filename}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nFiles generated:")
    print("  - adjective_analysis.png")
    print("  - survey_analysis.png")
    print(f"  - {excel_filename}")
    
    if 'A_taste' in df.columns and 'B_taste' in df.columns:
        print("\nKey Findings:")
        print(f"  - Product A average taste: {df['A_taste'].mean():.2f}")
        print(f"  - Product B average taste: {df['B_taste'].mean():.2f}")
        winner = "B" if df['B_taste'].mean() > df['A_taste'].mean() else "A"
        print(f"  - Winner: Product {winner}")
        
        if tag_freq_A:
            print(f"  - Most common tag for A: {tag_freq_A.most_common(1)[0][0]}")
        if tag_freq_B:
            print(f"  - Most common tag for B: {tag_freq_B.most_common(1)[0][0]}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)