from django.db import models
from django.conf import settings

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Quotidien'),
        ('WEEKLY', 'Hebdomadaire'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='star')  # Lucide icon name
    color = models.CharField(max_length=20, default='#38bdf8') # Default sky color
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='DAILY')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, 'Très mal'),
        (2, 'Pas bien'),
        (3, 'Neutre'),
        (4, 'Bien'),
        (5, 'Excellent'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_entries')
    score = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Humeur {self.score} - {self.user.username} - {self.created_at.date()}"
