from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


def send_welcome_email(user):
    """Email de bienvenue à l'inscription."""
    subject = "Bienvenue sur MyLife ! 🎉"
    html_message = render_to_string('emails/welcome.html', {'user': user})
    send_mail(
        subject=subject,
        message=f"Bonjour {user.get_full_name() or user.username}, bienvenue sur MyLife !",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_task_reminder_email(user, task):
    """Rappel d'une tâche par email."""
    subject = f"⏰ Rappel : {task.title}"
    html_message = render_to_string('emails/task_reminder.html', {'user': user, 'task': task})
    send_mail(
        subject=subject,
        message=f"Rappel : votre tâche '{task.title}' est due le {task.due_date}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_event_reminder_email(user, event):
    """Rappel d'un événement par email."""
    subject = f"📅 Rappel : {event.title}"
    html_message = render_to_string('emails/event_reminder.html', {'user': user, 'event': event})
    send_mail(
        subject=subject,
        message=f"Rappel : votre événement '{event.title}' commence le {event.start_time}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_daily_digest_email(user, digest_data):
    """Bilan journalier par email."""
    today = timezone.localdate()
    subject = f"📊 Votre bilan du {today.strftime('%d %B %Y')}"
    html_message = render_to_string('emails/daily_digest.html', {
        'user': user,
        'today': today,
        **digest_data,
    })
    send_mail(
        subject=subject,
        message=f"Votre bilan journalier MyLife du {today}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,
    )
