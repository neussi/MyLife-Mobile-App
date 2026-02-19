from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from planning.models import Task, Event
from finance.models import Transaction
from notes.models import Note
from notifications.emails import send_daily_digest_email
from notifications.models import Notification, NotificationSettings

User = get_user_model()


class Command(BaseCommand):
    help = 'Envoie le bilan journalier par email à tous les utilisateurs actifs'

    def handle(self, *args, **options):
        today = timezone.localdate()
        users = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')

        sent = 0
        for user in users:
            try:
                settings_obj = NotificationSettings.objects.filter(user=user).first()
                if settings_obj and not settings_obj.email_daily_digest:
                    continue

                tasks_today = Task.objects.filter(user=user, due_date__date=today)
                tasks_completed = tasks_today.filter(is_completed=True).count()
                tasks_total = tasks_today.count()

                events_today = Event.objects.filter(user=user, start_time__date=today)
                events_count = events_today.count()

                income = Transaction.objects.filter(
                    user=user, type='INCOME', date__year=today.year, date__month=today.month
                ).aggregate(total=Sum('amount'))['total'] or 0

                expense = Transaction.objects.filter(
                    user=user, type='EXPENSE', date__year=today.year, date__month=today.month
                ).aggregate(total=Sum('amount'))['total'] or 0

                notes_today = Note.objects.filter(user=user, created_at__date=today).count()

                digest_data = {
                    'tasks_completed': tasks_completed,
                    'tasks_total': tasks_total,
                    'events_count': events_count,
                    'events_today': events_today,
                    'tasks_today': tasks_today,
                    'income': income,
                    'expense': expense,
                    'balance': income - expense,
                    'notes_today': notes_today,
                }

                send_daily_digest_email(user, digest_data)

                # Create in-app notification
                Notification.objects.create(
                    user=user,
                    title=f"Bilan du {today.strftime('%d/%m/%Y')}",
                    message=f"{tasks_completed}/{tasks_total} tâches complétées, {events_count} événements, solde mensuel: {income - expense:.2f}€",
                    type='DIGEST',
                    link='/dashboard/',
                )

                sent += 1
                self.stdout.write(f"✓ Bilan envoyé à {user.email}")

            except Exception as e:
                self.stderr.write(f"✗ Erreur pour {user.email}: {e}")

        self.stdout.write(self.style.SUCCESS(f"\n{sent} bilans journaliers envoyés."))
