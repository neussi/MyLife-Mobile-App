from django.db import models
from django.conf import settings

class Note(models.Model):
    CATEGORY_CHOICES = [
        ('PERSONAL', 'Personnel'),
        ('WORK', 'Travail'),
        ('IDEA', 'Idée'),
        ('REMINDER', 'Rappel'),
        ('OTHER', 'Autre'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PERSONAL')
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Tags séparés par des virgules")
    color = models.CharField(max_length=20, default='#FFFFFF')
    is_pinned = models.BooleanField(default=False)
    image = models.ImageField(upload_to='notes_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

    def get_tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []
