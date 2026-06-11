from django import forms
from .models import DailyTask, Goal, DailyTracker, PointedJournal, Vent

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_date', 'category', 'progress']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

class DailyTrackerForm(forms.ModelForm):
    class Meta:
        model = DailyTracker
        fields = ['date', 'completed_tasks', 'pending_tasks', 'productivity_score', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'completed_tasks': forms.NumberInput(attrs={'min': 0}),
            'pending_tasks': forms.NumberInput(attrs={'min': 0}),
            'productivity_score': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PointedJournalForm(forms.ModelForm):
    class Meta:
        model = PointedJournal
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class VentForm(forms.ModelForm):
    class Meta:
        model = Vent
        fields = ['title', 'content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        } 