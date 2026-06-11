from django.db.models.signals import post_save
from django.dispatch import receiver
from journal.models import Entry
from .models import SentimentAnalysis
from .services import SentimentAnalyzer

analyzer = SentimentAnalyzer()

@receiver(post_save, sender=Entry)
def analyze_vent_entry(sender, instance, created, **kwargs):
    """Analyze vent entries when they are created"""
    if created and instance.title.lower() == 'vent':
        # Analyze the content
        analysis = analyzer.analyze_text(instance.content)
        
        # Create sentiment analysis record
        SentimentAnalysis.objects.create(
            user=instance.user,
            anxiety_score=analysis['anxiety_score'],
            self_hate_score=analysis['self_hate_score'],
            overall_sentiment=analysis['overall_sentiment'],
            trigger_words=analysis['trigger_words'],
            suggested_exercises=analysis['suggested_exercises']
        ) 