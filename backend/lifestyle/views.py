from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Habit, HabitLog, MoodEntry
from .forms import HabitForm, MoodForm

@login_required
def lifestyle_dashboard(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user, is_active=True)
    
    # Pre-populate logs for today if they don't exist
    for habit in habits:
        HabitLog.objects.get_or_create(habit=habit, date=today)
    
    habit_logs = HabitLog.objects.filter(habit__user=request.user, date=today)
    recent_moods = MoodEntry.objects.filter(user=request.user).order_by('-created_at')[:7]
    
    return render(request, 'lifestyle/index.html', {
        'habit_logs': habit_logs,
        'recent_moods': recent_moods,
        'today': today,
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('lifestyle_dashboard')
    else:
        form = HabitForm()
    return render(request, 'lifestyle/habit_form.html', {'form': form, 'title': 'Nouvelle Habitude'})

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('lifestyle_dashboard')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'lifestyle/habit_form.html', {'form': form, 'title': 'Modifier l\'habitude'})

@login_required
def habit_toggle(request, pk):
    if request.method == 'POST':
        log = get_object_or_404(HabitLog, pk=pk, habit__user=request.user)
        log.completed = not log.completed
        log.save()
        return JsonResponse({'status': 'ok', 'completed': log.completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('lifestyle_dashboard')
    return render(request, 'includes/confirm_delete.html', {
        'object': habit.name,
        'type': 'habitude',
        'cancel_url': reverse('lifestyle_dashboard')
    })

@login_required
def mood_log(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('lifestyle_dashboard')
    else:
        form = MoodForm()
    return render(request, 'lifestyle/mood_form.html', {'form': form, 'title': 'Comment ça va ?'})

@login_required
def mood_edit(request, pk):
    mood = get_object_or_404(MoodEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            return redirect('lifestyle_dashboard')
    else:
        form = MoodForm(instance=mood)
    return render(request, 'lifestyle/mood_form.html', {'form': form, 'title': 'Modifier l\'humeur'})

@login_required
def mood_delete(request, pk):
    mood = get_object_or_404(MoodEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        mood.delete()
        return redirect('lifestyle_dashboard')
    return render(request, 'includes/confirm_delete.html', {
        'object': f"Humeur du {mood.created_at|date:'d/m/Y'}",
        'type': 'humeur',
        'cancel_url': reverse('lifestyle_dashboard')
    })
