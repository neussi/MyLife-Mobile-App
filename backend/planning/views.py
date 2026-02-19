from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import date, timedelta
from .models import Event, Task, DailyDigest
from .forms import EventForm, TaskForm
from finance.models import Transaction
from notes.models import Note


@login_required
def planning_index(request):
    today = timezone.localdate()
    tasks = Task.objects.filter(user=request.user)
    today_tasks = tasks.filter(due_date__date=today)
    upcoming_tasks = tasks.filter(is_completed=False, due_date__date__gt=today).order_by('due_date')[:5]
    today_events = Event.objects.filter(user=request.user, start_time__date=today).order_by('start_time')
    return render(request, 'planning/index.html', {
        'tasks': tasks,
        'today_tasks': today_tasks,
        'upcoming_tasks': upcoming_tasks,
        'today_events': today_events,
        'today': today,
    })


@login_required
def calendar_events_api(request):
    """API JSON pour FullCalendar."""
    events = Event.objects.filter(user=request.user)
    data = []
    for e in events:
        data.append({
            'id': e.id,
            'title': e.title,
            'start': e.start_time.isoformat(),
            'end': e.end_time.isoformat(),
            'color': e.color,
            'description': e.description or '',
            'location': e.location or '',
            'allDay': e.is_all_day,
        })
    return JsonResponse(data, safe=False)


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Événement créé avec succès.")
            return redirect('planning_index')
    else:
        form = EventForm()
    return render(request, 'planning/event_form.html', {'form': form, 'title': 'Nouvel événement'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié avec succès.")
            return redirect('planning_index')
    else:
        form = EventForm(instance=event)
    return render(request, 'planning/event_form.html', {'form': form, 'title': 'Modifier l\'événement'})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Événement supprimé.")
        return redirect('planning_index')
    return render(request, 'includes/confirm_delete.html', {
        'object': event.title,
        'type': 'événement',
        'cancel_url': reverse('planning_index')
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Tâche créée avec succès.")
            return redirect('planning_index')
    else:
        form = TaskForm()
    return render(request, 'planning/task_form.html', {'form': form, 'title': 'Nouvelle tâche'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Tâche modifiée.")
            return redirect('planning_index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'planning/task_form.html', {'form': form, 'title': 'Modifier la tâche'})


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'is_completed': task.is_completed})
    return redirect('planning_index')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Tâche supprimée.")
        return redirect('planning_index')
    return render(request, 'includes/confirm_delete.html', {
        'object': task.title,
        'type': 'tâche',
        'cancel_url': reverse('planning_index')
    })
