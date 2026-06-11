from django.apps import AppConfig


class SentimentAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sentiment_analyzer'

    def ready(self):
        import sentiment_analyzer.signals  # Register signals
