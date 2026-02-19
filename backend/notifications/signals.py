from django.db.models.signals import post_save
from django.dispatch import receiver
from planning.models import Task, Event
from .models import Notification, NotificationSettings
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Task)
def task_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="Nouvelle tâche créée",
            message=f"La tâche « {instance.title} » a été ajoutée à votre planning.",
            type='TASK',
            link='/planning/',
        )


@receiver(post_save, sender=Event)
def event_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="Nouvel événement créé",
            message=f"L'événement « {instance.title} » a été ajouté à votre agenda.",
            type='EVENT',
            link='/planning/',
        )


@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.get_or_create(user=instance)
