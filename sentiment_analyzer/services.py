import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from collections import defaultdict
import json
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.anxiety_words = self._load_word_list('anxiety_words.txt')
        self.self_hate_words = self._load_word_list('self_hate_words.txt')
        self.exercise_suggestions = {
            'high_anxiety': [
                'Deep breathing exercises',
                'Progressive muscle relaxation',
                'Mindful walking',
                'Yoga',
                'Meditation'
            ],
            'high_self_hate': [
                'Positive self-talk exercises',
                'Gratitude journaling',
                'Physical exercise',
                'Art therapy',
                'Social connection activities'
            ]
        }
    
    def _load_word_list(self, filename):
        """Load word lists from the data directory"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        file_path = os.path.join(data_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return set(line.strip().lower() for line in f)
        except FileNotFoundError:
            # Return default word lists if files don't exist
            if filename == 'anxiety_words.txt':
                return {'anxiety', 'worry', 'stress', 'panic', 'fear', 'nervous', 'tense', 'overwhelm'}
            elif filename == 'self_hate_words.txt':
                return {'hate', 'worthless', 'failure', 'stupid', 'ugly', 'useless', 'hopeless', 'pathetic'}
            return set()
    
    def analyze_text(self, text):
        """Analyze text for sentiment, anxiety, and self-hate"""
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Get VADER sentiment scores
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Calculate anxiety score
        anxiety_matches = sum(1 for word in tokens if word in self.anxiety_words)
        anxiety_score = min(1.0, anxiety_matches / 10)  # Normalize to 0-1
        
        # Calculate self-hate score
        self_hate_matches = sum(1 for word in tokens if word in self.self_hate_words)
        self_hate_score = min(1.0, self_hate_matches / 10)  # Normalize to 0-1
        
        # Get trigger words
        trigger_words = list(set(word for word in tokens if word in self.anxiety_words or word in self.self_hate_words))
        
        # Get exercise suggestions based on scores
        suggested_exercises = []
        if anxiety_score > 0.5:
            suggested_exercises.extend(self.exercise_suggestions['high_anxiety'])
        if self_hate_score > 0.5:
            suggested_exercises.extend(self.exercise_suggestions['high_self_hate'])
        
        return {
            'anxiety_score': anxiety_score,
            'self_hate_score': self_hate_score,
            'overall_sentiment': sentiment_scores['compound'],
            'trigger_words': trigger_words,
            'suggested_exercises': list(set(suggested_exercises))  # Remove duplicates
        } 