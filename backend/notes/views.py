from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    notes = Note.objects.filter(user=request.user)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__icontains=query))
    if category:
        notes = notes.filter(category=category)
    pinned = notes.filter(is_pinned=True)
    regular = notes.filter(is_pinned=False)
    return render(request, 'notes/list.html', {
        'pinned_notes': pinned,
        'notes': regular,
        'query': query,
        'category': category,
        'categories': Note.CATEGORY_CHOICES,
    })


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note créée avec succès.")
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Nouvelle Note'})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note modifiée avec succès.")
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Modifier la note'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, "Note supprimée.")
        return redirect('note_list')
    return render(request, 'includes/confirm_delete.html', {
        'object': note.title,
        'type': 'note',
        'cancel_url': reverse('note_list')
    })


@login_required
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('note_list')
