from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Notification, NotificationSettings


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    # Mark all as read when viewing list
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notification_list')


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notification_list')


@login_required
def notification_settings(request):
    settings_obj, _ = NotificationSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        settings_obj.email_tasks = 'email_tasks' in request.POST
        settings_obj.email_events = 'email_events' in request.POST
        settings_obj.email_daily_digest = 'email_daily_digest' in request.POST
        settings_obj.email_projects = 'email_projects' in request.POST
        settings_obj.inapp_tasks = 'inapp_tasks' in request.POST
        settings_obj.inapp_events = 'inapp_events' in request.POST
        settings_obj.inapp_finance = 'inapp_finance' in request.POST
        settings_obj.save()
        messages.success(request, "Paramètres de notifications sauvegardés.")
        return redirect('notification_settings')
    return render(request, 'notifications/settings.html', {'settings': settings_obj})


@login_required
def unread_count_api(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})
