
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from planning.models import Task
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends email reminders for upcoming tasks'

    def handle(self, *args, **options):
        now = timezone.now()
        # Find tasks starting in the next hour that haven't been reminded
        upcoming_tasks = Task.objects.filter(
            start_time__gt=now,
            start_time__lte=now + timezone.timedelta(hours=1),
            reminder_sent=False
        )
        
        self.stdout.write(f"Found {upcoming_tasks.count()} tasks to remind.")

        for task in upcoming_tasks:
            if task.user.email:
                try:
                    send_mail(
                        f'Rappel MyLife: {task.title}',
                        f'Bonjour {task.user.username},\n\nVotre tâche "{task.title}" commence bientôt ({task.start_time.strftime("%H:%M")}).\n\nPréparez-vous !\n\nL\'équipe MyLife',
                        settings.DEFAULT_FROM_EMAIL,
                        [task.user.email],
                        fail_silently=False,
                    )
                    task.reminder_sent = True
                    task.save()
                    self.stdout.write(self.style.SUCCESS(f'Email sent specifically to {task.user.email} for task "{task.title}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to send email for "{task.title}": {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'User for task "{task.title}" has no email.'))
