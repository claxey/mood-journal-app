from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import spacy
from textblob import TextBlob

# Load the English language model
nlp = spacy.load("en_core_web_sm")

class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class DailyTask(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('career', 'Career'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    target_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PointedJournal(models.Model):
    CATEGORY_CHOICES = [
        ('reflection', 'Reflection'),
        ('idea', 'Idea'),
        ('quote', 'Quote'),
        ('memory', 'Memory'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='reflection')
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class DailyTracker(models.Model):
    date = models.DateField(default=timezone.now)
    completed_tasks = models.IntegerField(default=0)
    pending_tasks = models.IntegerField(default=0)
    productivity_score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'user']

    def __str__(self):
        return f"Tracker for {self.date}"

class Vent(models.Model):
    SENTIMENT_CHOICES = [
        ('very_positive', 'Very Positive'),
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
        ('very_negative', 'Very Negative'),
    ]

    MOOD_CHOICES = [
        ('joy', 'Joy'),
        ('sadness', 'Sadness'),
        ('anger', 'Anger'),
        ('fear', 'Fear'),
        ('anxiety', 'Anxiety'),
        ('calm', 'Calm'),
        ('neutral', 'Neutral'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Sentiment Analysis Fields
    sentiment_score = models.FloatField(default=0.0)  # Range: -1.0 to 1.0
    sentiment_category = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='neutral')
    subjectivity_score = models.FloatField(default=0.0)  # Range: 0.0 to 1.0
    key_phrases = models.JSONField(default=list, blank=True)  # Store important phrases
    detected_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def analyze_sentiment(self):
        """Analyze the sentiment and mood of the vent content using TextBlob."""
        # Analyze sentiment
        blob = TextBlob(self.content)
        self.sentiment_score = blob.sentiment.polarity
        self.subjectivity_score = blob.sentiment.subjectivity
        
        # Set sentiment category
        if self.sentiment_score >= 0.5:
            self.sentiment_category = 'very_positive'
        elif self.sentiment_score > 0:
            self.sentiment_category = 'positive'
        elif self.sentiment_score == 0:
            self.sentiment_category = 'neutral'
        elif self.sentiment_score > -0.5:
            self.sentiment_category = 'negative'
        else:
            self.sentiment_category = 'very_negative'
            
        # Detect mood based on sentiment
        if self.sentiment_score >= 0.5:
            self.detected_mood = 'joy'
        elif self.sentiment_score > 0:
            self.detected_mood = 'calm'
        elif self.sentiment_score == 0:
            self.detected_mood = 'neutral'
        elif self.sentiment_score > -0.5:
            self.detected_mood = 'sadness'
        else:
            self.detected_mood = 'anger'
            
        # Extract key phrases
        self.key_phrases = [phrase for phrase in blob.noun_phrases]

    def save(self, *args, **kwargs):
        """Override save to automatically analyze sentiment."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or 'content' in kwargs.get('update_fields', []):
            self.analyze_sentiment()
            super().save(update_fields=['sentiment_score', 'sentiment_category', 'subjectivity_score', 'key_phrases', 'detected_mood'])    