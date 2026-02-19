from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Project, Milestone
from .forms import ProjectForm, MilestoneForm


@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'status_filter': status_filter,
        'status_choices': Project.STATUS_CHOICES,
    })


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    milestones = project.milestones.all()
    return render(request, 'projects/detail.html', {'project': project, 'milestones': milestones})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, "Projet créé avec succès.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Nouveau Projet'})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet modifié avec succès.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Modifier le projet'})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Projet supprimé.")
        return redirect('project_list')
    return render(request, 'includes/confirm_delete.html', {
        'object': project.name,
        'type': 'projet',
        'cancel_url': reverse('project_list')
    })


@login_required
def milestone_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            project.update_progress()
            messages.success(request, "Jalon ajouté.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = MilestoneForm()
    return render(request, 'projects/milestone_form.html', {'form': form, 'project': project, 'title': 'Nouveau Jalon'})


@login_required
def milestone_toggle(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk, project__user=request.user)
    milestone.is_completed = not milestone.is_completed
    milestone.completed_at = timezone.now() if milestone.is_completed else None
    milestone.save()
    milestone.project.update_progress()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'is_completed': milestone.is_completed, 'progress': milestone.project.progress})
    return redirect('project_detail', pk=milestone.project.pk)


@login_required
def milestone_edit(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk, project__user=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            milestone.project.update_progress()
            messages.success(request, "Jalon modifié.")
            return redirect('project_detail', pk=milestone.project.pk)
    else:
        form = MilestoneForm(instance=milestone)
    return render(request, 'projects/milestone_form.html', {'form': form, 'project': milestone.project, 'title': 'Modifier le Jalon'})


@login_required
def milestone_delete(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk, project__user=request.user)
    project_pk = milestone.project.pk
    if request.method == 'POST':
        milestone.delete()
        milestone.project.update_progress()
        messages.success(request, "Jalon supprimé.")
        return redirect('project_detail', pk=project_pk)
    return render(request, 'includes/confirm_delete.html', {
        'object': milestone.title,
        'type': 'jalon',
        'cancel_url': reverse('project_detail', kwargs={'pk': project_pk})
    })
