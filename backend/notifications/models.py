from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ('TASK', 'Tâche'),
        ('EVENT', 'Événement'),
        ('FINANCE', 'Finance'),
        ('PROJECT', 'Projet'),
        ('SYSTEM', 'Système'),
        ('DIGEST', 'Bilan journalier'),
        ('ADVISOR', 'Conseiller Expert'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='SYSTEM')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.title}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings')
    email_tasks = models.BooleanField(default=True)
    email_events = models.BooleanField(default=True)
    email_daily_digest = models.BooleanField(default=True)
    email_projects = models.BooleanField(default=True)
    inapp_tasks = models.BooleanField(default=True)
    inapp_events = models.BooleanField(default=True)
    inapp_finance = models.BooleanField(default=True)
    digest_time = models.TimeField(default='08:00')

    def __str__(self):
        return f"Paramètres notifications — {self.user}"
