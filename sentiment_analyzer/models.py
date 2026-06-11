from django.db import models
from django.contrib.auth.models import User

class SentimentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    anxiety_score = models.FloatField(default=0.0)  # 0-1 scale
    self_hate_score = models.FloatField(default=0.0)  # 0-1 scale
    overall_sentiment = models.FloatField(default=0.0)  # -1 to 1 scale
    trigger_words = models.JSONField(default=list)  # Store detected trigger words
    suggested_exercises = models.JSONField(default=list)  # Store suggested exercises
    
    class Meta:
        ordering = ['-entry_date']
        verbose_name = 'Sentiment Analysis'
        verbose_name_plural = 'Sentiment Analyses'
    
    def __str__(self):
        return f"{self.user.username}'s Analysis - {self.entry_date}"
