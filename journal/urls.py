from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    # Journal Entries
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('entry/new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),

    # Daily Tasks
    path('tasks/', views.DailyTaskListView.as_view(), name='daily_task'),
    path('tasks/new/', views.DailyTaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.DailyTaskUpdateView.as_view(), name='edit_task'),
    path('tasks/<int:pk>/complete/', views.DailyTaskCompleteView.as_view(), name='complete_task'),
    path('tasks/<int:pk>/delete/', views.DailyTaskDeleteView.as_view(), name='delete_task'),

    # Goals
    path('goals/', views.GoalListView.as_view(), name='goals'),
    path('goals/new/', views.GoalCreateView.as_view(), name='goal_create'),
    path('goals/<int:pk>/edit/', views.GoalUpdateView.as_view(), name='edit_goal'),
    path('goals/<int:pk>/complete/', views.GoalCompleteView.as_view(), name='complete_goal'),
    path('goals/<int:pk>/delete/', views.GoalDeleteView.as_view(), name='delete_goal'),
    path('goals/<int:pk>/progress/', views.GoalProgressUpdateView.as_view(), name='update_goal_progress'),

    # Pointed Journal
    path('pointed/', views.PointedJournalListView.as_view(), name='pointed_journal'),
    path('pointed/new/', views.PointedJournalCreateView.as_view(), name='pointed_create'),
    path('pointed/<int:pk>/edit/', views.PointedJournalUpdateView.as_view(), name='edit_pointed'),
    path('pointed/<int:pk>/delete/', views.PointedJournalDeleteView.as_view(), name='delete_pointed'),

    # Daily Tracker
    path('tracker/', views.DailyTrackerView.as_view(), name='daily_tracker'),
    path('tracker/new/', views.DailyTrackerCreateView.as_view(), name='tracker_create'),
    path('tracker/<int:pk>/edit/', views.DailyTrackerUpdateView.as_view(), name='edit_tracker'),
    path('tracker/<int:pk>/delete/', views.DailyTrackerDeleteView.as_view(), name='delete_tracker'),

    # Vent
    path('vent/', views.VentListView.as_view(), name='vent'),
    path('vent/new/', views.VentCreateView.as_view(), name='vent_create'),
    path('vent/<int:pk>/edit/', views.VentUpdateView.as_view(), name='edit_vent'),
    path('vent/<int:pk>/delete/', views.VentDeleteView.as_view(), name='delete_vent'),
] 