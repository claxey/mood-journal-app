from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyTaskForm, GoalForm, DailyTrackerForm
from .models import DailyTask, Goal, DailyTracker, Entry, PointedJournal, Vent, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
from django.http import JsonResponse, HttpResponseRedirect
from textblob import TextBlob
from .forms import VentForm

# Create your views here.

def home(request):
    return render(request, 'journal/base.html')

@login_required
def daily_task(request):
    if request.method == 'POST':
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('daily_task')
    else:
        form = DailyTaskForm()
    
    tasks = DailyTask.objects.filter(user=request.user).order_by('due_date', '-created_at')
    return render(request, 'journal/daily_task.html', {
        'form': form,
        'tasks': tasks
    })

@login_required
def goals(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()
    
    goals = Goal.objects.filter(user=request.user).order_by('target_date', '-created_at')
    return render(request, 'journal/goals.html', {
        'form': form,
        'goals': goals
    })

@login_required
def daily_tracker(request):
    if request.method == 'POST':
        form = DailyTrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.user = request.user
            tracker.save()
            return redirect('daily_tracker')
    else:
        form = DailyTrackerForm()
    
    trackers = DailyTracker.objects.filter(user=request.user).order_by('-date')
    return render(request, 'journal/daily_tracker.html', {
        'form': form,
        'trackers': trackers
    })

def pointed_journal(request):
    return render(request, 'journal/pointed_journal.html')

def vent(request):
    return render(request, 'journal/vent.html')

# Journal Entry Views
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'journal/entry_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('-created_at')

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'journal/entry_detail.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'journal/entry_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('journal:entry_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    template_name = 'journal/entry_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('journal:entry_list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'journal/entry_confirm_delete.html'
    success_url = reverse_lazy('journal:entry_list')

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

# Daily Task Views
class DailyTaskListView(LoginRequiredMixin, ListView):
    model = DailyTask
    template_name = 'journal/daily_task.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        completed_tasks = tasks.filter(completed=True)
        pending_tasks = tasks.filter(completed=False)
        
        context['completed_tasks'] = completed_tasks.count()
        context['pending_tasks'] = pending_tasks.count()
        context['total_tasks'] = tasks.count()
        context['completion_rate'] = int((completed_tasks.count() / tasks.count() * 100) if tasks.count() > 0 else 0)
        return context

class DailyTaskCreateView(LoginRequiredMixin, CreateView):
    model = DailyTask
    template_name = 'journal/daily_task.html'
    fields = ['title', 'description', 'due_date', 'priority']
    success_url = reverse_lazy('journal:daily_task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DailyTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyTask
    template_name = 'journal/daily_task.html'
    fields = ['title', 'description', 'due_date', 'priority']
    success_url = reverse_lazy('journal:daily_task')

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)

class DailyTaskCompleteView(LoginRequiredMixin, UpdateView):
    model = DailyTask
    fields = []
    success_url = reverse_lazy('journal:daily_task')

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_at = timezone.now()
        return super().form_valid(form)

class DailyTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyTask
    success_url = reverse_lazy('journal:daily_task')

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)

# Goal Views
class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'journal/goals.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by('-created_at')

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'journal/goals.html'
    fields = ['title', 'description', 'target_date', 'category']
    success_url = reverse_lazy('journal:goals')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'journal/goals.html'
    fields = ['title', 'description', 'target_date', 'category']
    success_url = reverse_lazy('journal:goals')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalCompleteView(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = []
    success_url = reverse_lazy('journal:goals')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_at = timezone.now()
        return super().form_valid(form)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy('journal:goals')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['progress']
    success_url = reverse_lazy('journal:goals')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

# Pointed Journal Views
class PointedJournalListView(LoginRequiredMixin, ListView):
    model = PointedJournal
    template_name = 'journal/pointed_journal.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return PointedJournal.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = self.get_queryset()
        
        # Get topic distribution
        topics = {}
        for entry in entries:
            for tag in entry.tags.all():
                topics[tag.name] = topics.get(tag.name, 0) + 1
        
        context['topic_labels'] = list(topics.keys())
        context['topic_data'] = list(topics.values())
        
        # Get writing frequency
        frequency = {}
        for entry in entries:
            date = entry.created_at.strftime('%Y-%m-%d')
            frequency[date] = frequency.get(date, 0) + 1
        
        context['frequency_labels'] = list(frequency.keys())
        context['frequency_data'] = list(frequency.values())
        
        return context

class PointedJournalCreateView(LoginRequiredMixin, CreateView):
    model = PointedJournal
    template_name = 'journal/pointed_journal.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('journal:pointed_journal')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Handle tags
        tags_str = self.request.POST.get('tags', '')
        if tags_str:
            # Split tags by comma and clean them
            tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
            
            # Create or get tags
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                form.instance.tags.add(tag)
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = PointedJournal.objects.filter(user=self.request.user).order_by('-created_at')
        context['recent_entries'] = context['entries'][:5]
        
        # Get topic distribution
        topics = {}
        for entry in context['entries']:
            for tag in entry.tags.all():
                topics[tag.name] = topics.get(tag.name, 0) + 1
        
        context['topic_labels'] = list(topics.keys())
        context['topic_data'] = list(topics.values())
        
        # Get writing frequency
        frequency = {}
        for entry in context['entries']:
            date = entry.created_at.strftime('%Y-%m-%d')
            frequency[date] = frequency.get(date, 0) + 1
        
        context['frequency_labels'] = list(frequency.keys())
        context['frequency_data'] = list(frequency.values())
        
        return context

class PointedJournalUpdateView(LoginRequiredMixin, UpdateView):
    model = PointedJournal
    template_name = 'journal/pointed_journal.html'
    fields = ['title', 'content', 'tags', 'category']
    success_url = reverse_lazy('journal:pointed_journal')

    def get_queryset(self):
        return PointedJournal.objects.filter(user=self.request.user)

class PointedJournalDeleteView(LoginRequiredMixin, DeleteView):
    model = PointedJournal
    success_url = reverse_lazy('journal:pointed_journal')

    def get_queryset(self):
        return PointedJournal.objects.filter(user=self.request.user)

# Daily Tracker Views
class DailyTrackerView(LoginRequiredMixin, ListView):
    model = DailyTracker
    template_name = 'journal/daily_tracker.html'
    context_object_name = 'trackers'

    def get_queryset(self):
        return DailyTracker.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trackers = self.get_queryset()
        
        # Get today's stats
        today = timezone.now().date()
        today_tracker = trackers.filter(date=today).first()
        
        context['today_completed'] = today_tracker.completed_tasks if today_tracker else 0
        context['today_pending'] = today_tracker.pending_tasks if today_tracker else 0
        
        # Calculate streak
        streak = 0
        current_date = today
        while trackers.filter(date=current_date).exists():
            streak += 1
            current_date -= timezone.timedelta(days=1)
        context['current_streak'] = streak
        
        # Weekly progress
        week_start = today - timezone.timedelta(days=today.weekday())
        week_trackers = trackers.filter(date__gte=week_start)
        weekly_completed = sum(t.completed_tasks for t in week_trackers)
        weekly_total = sum(t.completed_tasks + t.pending_tasks for t in week_trackers)
        context['weekly_completion_rate'] = int((weekly_completed / weekly_total * 100) if weekly_total > 0 else 0)
        context['weekly_completed'] = weekly_completed
        
        # Chart data
        dates = [t.date.strftime('%Y-%m-%d') for t in trackers[:7]]
        completed_data = [t.completed_tasks for t in trackers[:7]]
        productivity_data = [t.productivity_score for t in trackers[:7]]
        
        context['dates'] = dates
        context['completed_data'] = completed_data
        context['productivity_data'] = productivity_data
        
        return context

class DailyTrackerCreateView(LoginRequiredMixin, CreateView):
    model = DailyTracker
    template_name = 'journal/daily_tracker.html'
    fields = ['date', 'completed_tasks', 'pending_tasks', 'productivity_score', 'notes']
    success_url = reverse_lazy('journal:daily_tracker')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DailyTrackerUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyTracker
    template_name = 'journal/daily_tracker.html'
    fields = ['date', 'completed_tasks', 'pending_tasks', 'productivity_score', 'notes']
    success_url = reverse_lazy('journal:daily_tracker')

    def get_queryset(self):
        return DailyTracker.objects.filter(user=self.request.user)

class DailyTrackerDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyTracker
    success_url = reverse_lazy('journal:daily_tracker')

    def get_queryset(self):
        return DailyTracker.objects.filter(user=self.request.user)

# Vent Views
class VentListView(LoginRequiredMixin, ListView):
    model = Vent
    template_name = 'journal/vent.html'
    context_object_name = 'vents'

    def get_queryset(self):
        return Vent.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get mood distribution data (now using detected_mood)
        mood_data = Vent.objects.filter(user=self.request.user).values('detected_mood').annotate(count=Count('id'))
        mood_labels = [item['detected_mood'].title() for item in mood_data]
        mood_counts = [item['count'] for item in mood_data]
        
        # Get sentiment trend data (last 7 days)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        sentiment_data = Vent.objects.filter(
            user=self.request.user,
            created_at__range=[start_date, end_date]
        ).order_by('created_at')
        
        sentiment_labels = [vent.created_at.strftime('%b %d') for vent in sentiment_data]
        sentiment_scores = [vent.sentiment_score for vent in sentiment_data]
        
        context.update({
            'mood_labels': mood_labels,
            'mood_data': mood_counts,
            'sentiment_labels': sentiment_labels,
            'sentiment_data': sentiment_scores,
        })
        return context

class VentCreateView(LoginRequiredMixin, CreateView):
    model = Vent
    form_class = VentForm
    template_name = 'journal/vent_form.html'
    success_url = reverse_lazy('journal:vent')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class VentUpdateView(LoginRequiredMixin, UpdateView):
    model = Vent
    template_name = 'journal/vent_form.html'
    fields = ['title', 'content', 'is_private']
    success_url = reverse_lazy('journal:vent')

    def get_queryset(self):
        return Vent.objects.filter(user=self.request.user)

class VentDeleteView(LoginRequiredMixin, DeleteView):
    model = Vent
    success_url = reverse_lazy('journal:vent')

    def get_queryset(self):
        return Vent.objects.filter(user=self.request.user)
        
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return HttpResponseRedirect(success_url)
