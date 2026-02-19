from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from planning.models import Task, Event
from notes.models import Note
from finance.models import Transaction
from projects.models import Project
from notifications.models import Notification
from lifestyle.models import Habit, HabitLog


@login_required
def dashboard(request):
    today = timezone.localdate()
    now = timezone.now()

    # Habits for today (pre-populate logs if needed)
    habits = Habit.objects.filter(user=request.user, is_active=True)
    for habit in habits:
        HabitLog.objects.get_or_create(habit=habit, date=today)
    habit_logs_today = HabitLog.objects.filter(habit__user=request.user, date=today)
    habits_completed_today = habit_logs_today.filter(completed=True).count()

    # Tasks
    tasks_today = Task.objects.filter(user=request.user, due_date__date=today)
    tasks_pending = Task.objects.filter(user=request.user, is_completed=False).count()
    tasks_completed_today = tasks_today.filter(is_completed=True).count()

    # Events
    events_today = Event.objects.filter(user=request.user, start_time__date=today).order_by('start_time')
    upcoming_events = Event.objects.filter(user=request.user, start_time__gte=now).order_by('start_time')[:5]

    # Finance (current month)
    income_month = Transaction.objects.filter(
        user=request.user, type='INCOME', date__year=today.year, date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    expense_month = Transaction.objects.filter(
        user=request.user, type='EXPENSE', date__year=today.year, date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    balance = income_month - expense_month

    # Recent notes
    recent_notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:4]

    # Projects
    active_projects = Project.objects.filter(user=request.user, status='IN_PROGRESS')[:3]

    # Recent transactions
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')[:5]

    return render(request, 'dashboard/index.html', {
        'today': today,
        'tasks_today': tasks_today,
        'tasks_pending': tasks_pending,
        'tasks_completed_today': tasks_completed_today,
        'events_today': events_today,
        'upcoming_events': upcoming_events,
        'income_month': income_month,
        'expense_month': expense_month,
        'balance': balance,
        'recent_notes': recent_notes,
        'active_projects': active_projects,
        'recent_transactions': recent_transactions,
        'habit_logs_today': habit_logs_today,
        'habits_completed_today': habits_completed_today,
    })

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
