from django.db import models
from django.conf import settings

class Contact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('FAMILY', 'Famille'),
        ('FRIEND', 'Ami(e)'),
        ('COLLEAGUE', 'Collègue'),
        ('PROFESSIONAL', 'Professionnel'),
        ('OTHER', 'Autre'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='OTHER')
    birthday = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='contacts_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
