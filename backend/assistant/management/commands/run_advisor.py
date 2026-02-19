from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assistant.engine import AdvisorBrain
from assistant.dispatch import AdvisorDispatcher

User = get_user_model()

class Command(BaseCommand):
    help = 'Analyse les performances des utilisateurs et envoie des conseils/réprimandes.'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(self.style.SUCCESS(f"Démarrage de l'analyse pour {users.count()} utilisateurs..."))
        
        for user in users:
            self.stdout.write(f"Analyse de {user.username}...")
            brain = AdvisorBrain(user)
            mood, reports = brain.get_advice()
            
            dispatcher = AdvisorDispatcher(user)
            dispatcher.dispatch(mood, reports)
            
            self.stdout.write(self.style.SUCCESS(f"Terminé pour {user.username} (Humeur: {mood})"))
