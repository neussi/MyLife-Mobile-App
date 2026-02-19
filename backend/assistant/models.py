from django.db import models
from django.conf import settings

class AdvisorMood(models.Model):
    MOOD_CHOICES = [
        ('HAPPY', 'Joyeux'),
        ('CONCERNED', 'Inquiet'),
        ('ANGRY', 'Fâché'),
        ('FURIOUS', 'Furieux'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advisor_mood')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='HAPPY')
    anger_level = models.IntegerField(default=0)  # 0 to 100
    last_evaluation = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Humeur du conseiller pour {self.user.username} : {self.get_mood_display()}"

    @property
    def color_class(self):
        map = {
            'HAPPY': 'sky',
            'CONCERNED': 'amber',
            'ANGRY': 'red',
            'FURIOUS': 'red',
        }
        return map.get(self.mood, 'sky')

    @property
    def bg_class(self):
        map = {
            'HAPPY': 'bg-sky-50 dark:bg-sky-900/20 text-sky-500',
            'CONCERNED': 'bg-amber-50 dark:bg-amber-900/20 text-amber-500',
            'ANGRY': 'bg-red-50 dark:bg-red-900/20 text-red-500',
            'FURIOUS': 'bg-red-900 text-white',
        }
        return map.get(self.mood, 'bg-sky-50 text-sky-500')

    @property
    def icon_name(self):
        map = {
            'HAPPY': 'smile',
            'CONCERNED': 'alert-circle',
            'ANGRY': 'frown',
            'FURIOUS': 'zap',
        }
        return map.get(self.mood, 'user')

class AdvisorInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advisor_interactions')
    mood_at_time = models.CharField(max_length=20)
    message_type = models.CharField(max_length=50) # e.g., 'finance_warning', 'habit_shaming'
    sent_at = models.DateTimeField(auto_now_add=True)
    message_content = models.TextField()
    is_email = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Interaction {self.message_type} ({self.sent_at.date()}) - {self.user.username}"
