from textblob import TextBlob
import pandas as pd
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DataPipeline:
    """Base class for data processing pipelines"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour cache timeout

    def process_data(self, data):
        """Process the input data"""
        raise NotImplementedError("Subclasses must implement process_data")

    def validate_data(self, data):
        """Validate the input data"""
        raise NotImplementedError("Subclasses must implement validate_data")

    def store_data(self, processed_data):
        """Store the processed data"""
        raise NotImplementedError("Subclasses must implement store_data")


class JournalEntryPipeline(DataPipeline):
    """Pipeline for processing journal entries"""
    
    def validate_data(self, data):
        if not data.get('content'):
            raise ValueError("Journal entry content cannot be empty")
        return True

    def process_data(self, data):
        try:
            # Perform sentiment analysis
            blob = TextBlob(data['content'])
            sentiment = blob.sentiment.polarity
            
            # Extract key topics (simple implementation)
            words = blob.words
            topics = [word for word in words if len(word) > 4]
            
            processed_data = {
                'content': data['content'],
                'sentiment_score': sentiment,
                'topics': topics,
                'processed_at': datetime.now(),
                'word_count': len(words)
            }
            
            return processed_data
        except Exception as e:
            logger.error(f"Error processing journal entry: {str(e)}")
            raise

    def store_data(self, processed_data):
        cache_key = f"journal_entry_{processed_data.get('id')}"
        cache.set(cache_key, processed_data, self.cache_timeout)


class DailyTaskPipeline(DataPipeline):
    """Pipeline for processing daily tasks"""
    
    def validate_data(self, data):
        required_fields = ['title', 'due_date']
        return all(field in data for field in required_fields)

    def process_data(self, data):
        try:
            processed_data = {
                'title': data['title'],
                'due_date': data['due_date'],
                'status': data.get('status', 'pending'),
                'priority': data.get('priority', 'medium'),
                'processed_at': datetime.now()
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error processing daily task: {str(e)}")
            raise

    def store_data(self, processed_data):
        cache_key = f"daily_task_{processed_data.get('id')}"
        cache.set(cache_key, processed_data, self.cache_timeout)


class GoalPipeline(DataPipeline):
    """Pipeline for processing goals"""
    
    def validate_data(self, data):
        required_fields = ['title', 'target_date']
        return all(field in data for field in required_fields)

    def process_data(self, data):
        try:
            # Calculate progress percentage
            current_progress = data.get('current_progress', 0)
            target_progress = data.get('target_progress', 100)
            progress_percentage = (current_progress / target_progress) * 100

            processed_data = {
                'title': data['title'],
                'target_date': data['target_date'],
                'current_progress': current_progress,
                'target_progress': target_progress,
                'progress_percentage': progress_percentage,
                'processed_at': datetime.now()
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error processing goal: {str(e)}")
            raise

    def store_data(self, processed_data):
        cache_key = f"goal_{processed_data.get('id')}"
        cache.set(cache_key, processed_data, self.cache_timeout)


class VentPipeline(DataPipeline):
    """Pipeline for processing vent entries"""
    
    def validate_data(self, data):
        if not data.get('content'):
            raise ValueError("Vent entry content cannot be empty")
        return True

    def process_data(self, data):
        try:
            # Perform sentiment analysis
            blob = TextBlob(data['content'])
            sentiment = blob.sentiment.polarity
            
            # Extract emotional intensity
            emotional_intensity = abs(sentiment)
            
            processed_data = {
                'content': data['content'],
                'sentiment_score': sentiment,
                'emotional_intensity': emotional_intensity,
                'processed_at': datetime.now(),
                'is_private': data.get('is_private', True)
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error processing vent entry: {str(e)}")
            raise

    def store_data(self, processed_data):
        cache_key = f"vent_{processed_data.get('id')}"
        cache.set(cache_key, processed_data, self.cache_timeout)


class AnalyticsPipeline:
    """Pipeline for generating analytics"""
    
    @staticmethod
    def generate_daily_summary(user_id, date):
        """Generate daily summary of user activities"""
        try:
            # Get data from cache or database
            journal_entries = cache.get(f"journal_entries_{user_id}_{date}")
            tasks = cache.get(f"daily_tasks_{user_id}_{date}")
            goals = cache.get(f"goals_{user_id}_{date}")
            
            summary = {
                'date': date,
                'journal_entries_count': len(journal_entries) if journal_entries else 0,
                'tasks_completed': len([t for t in tasks if t['status'] == 'completed']) if tasks else 0,
                'goals_progress': sum(g['progress_percentage'] for g in goals) / len(goals) if goals else 0,
                'generated_at': datetime.now()
            }
            
            return summary
        except Exception as e:
            logger.error(f"Error generating daily summary: {str(e)}")
            raise 