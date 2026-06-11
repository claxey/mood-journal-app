from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sentiment_analyzer.models import SentimentAnalysis
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate exercise suggestions based on sentiment analysis'

    def handle(self, *args, **options):
        # Get users with high anxiety or self-hate scores in the last week
        last_week = datetime.now() - timedelta(days=7)
        recent_analyses = SentimentAnalysis.objects.filter(
            entry_date__gte=last_week
        ).select_related('user')

        # Group analyses by user
        user_analyses = {}
        for analysis in recent_analyses:
            if analysis.user not in user_analyses:
                user_analyses[analysis.user] = []
            user_analyses[analysis.user].append(analysis)

        # Generate suggestions for each user
        for user, analyses in user_analyses.items():
            avg_anxiety = sum(a.anxiety_score for a in analyses) / len(analyses)
            avg_self_hate = sum(a.self_hate_score for a in analyses) / len(analyses)
            
            # Get unique suggested exercises
            suggested_exercises = set()
            for analysis in analyses:
                suggested_exercises.update(analysis.suggested_exercises)
            
            if suggested_exercises:
                self.stdout.write(
                    f"\nExercise suggestions for {user.username}:"
                    f"\nAverage anxiety score: {avg_anxiety:.2f}"
                    f"\nAverage self-hate score: {avg_self_hate:.2f}"
                    f"\nSuggested exercises:"
                )
                for exercise in suggested_exercises:
                    self.stdout.write(f"- {exercise}") 