from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Sum
from finance.models import Transaction, Budget
from lifestyle.models import Habit, HabitLog, MoodEntry
from planning.models import Task, Event
from .models import AdvisorMood, AdvisorInteraction

class AdvisorBrain:
    def __init__(self, user):
        self.user = user
        self.mood_obj, _ = AdvisorMood.objects.get_or_create(user=user)
        self.today = timezone.localdate()
        self.reports = []
        self.anger_delta = 0

    def evaluate_finance(self):
        """Analyze financial state."""
        # Check current month transactions
        transactions = Transaction.objects.filter(user=self.user, date__month=self.today.month, date__year=self.today.year)
        income = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        expense = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
        balance = income - expense

        if balance < 0:
            self.anger_delta += 20
            self.reports.append({
                'category': 'FINANCE',
                'severity': 'HIGH',
                'message': f"Tu es dans le rouge de {abs(balance)} FCFA ce mois-ci ! Tu comptes vivre de quoi, d'amour et d'eau fraîche ?"
            })
        elif balance < 100:
            self.anger_delta += 5
            self.reports.append({
                'category': 'FINANCE',
                'severity': 'MEDIUM',
                'message': "Ton solde est dangereusement bas. Un peu de discipline ne te ferait pas de mal."
            })

    def evaluate_lifestyle(self):
        """Analyze habits and mood."""
        # Check missed habits in the last 3 days
        three_days_ago = self.today - timedelta(days=3)
        habits = Habit.objects.filter(user=self.user, is_active=True)
        for habit in habits:
            missed_count = HabitLog.objects.filter(habit=habit, date__range=[three_days_ago, self.today], completed=False).count()
            if missed_count >= 2:
                self.anger_delta += 15
                self.reports.append({
                    'category': 'LIFESTYLE',
                    'severity': 'HIGH',
                    'message': f"Tu as encore raté ton habitude '{habit.name}'... La procrastination est le voleur du temps, et tu es en train de te faire cambrioler."
                })

        # Check recent mood
        recent_mood = MoodEntry.objects.filter(user=self.user).order_by('-created_at').first()
        if recent_mood and recent_mood.score <= 2:
            self.anger_delta -= 10 # Empathy: don't get too angry if they are feeling down
            self.reports.append({
                'category': 'LIFESTYLE',
                'severity': 'LOW',
                'message': "Je vois que ça ne va pas fort. Je vais essayer d'être plus indulgent aujourd'hui, mais ne te laisse pas aller."
            })

    def evaluate_planning(self):
        """Analyze tasks and events."""
        overdue_tasks = Task.objects.filter(user=self.user, is_completed=False, due_date__lt=timezone.now()).count()
        if overdue_tasks > 0:
            self.anger_delta += 10 * overdue_tasks
            self.reports.append({
                'category': 'PLANNING',
                'severity': 'HIGH',
                'message': f"Tu as {overdue_tasks} tâches en retard ! Tu attends quoi pour t'y mettre ? Un miracle ?"
            })

    def update_mood(self):
        """Calculate final mood based on evaluation."""
        self.mood_obj.anger_level = max(0, min(100, self.mood_obj.anger_level + self.anger_delta))
        
        if self.mood_obj.anger_level > 80:
            self.mood_obj.mood = 'FURIOUS'
        elif self.mood_obj.anger_level > 50:
            self.mood_obj.mood = 'ANGRY'
        elif self.mood_obj.anger_level > 20:
            self.mood_obj.mood = 'CONCERNED'
        else:
            self.mood_obj.mood = 'HAPPY'
            
        self.mood_obj.save()

    def get_advice(self):
        """Run all evaluations and return mood + messages."""
        self.anger_delta = -5 # Natural cooling down over time
        self.evaluate_finance()
        self.evaluate_lifestyle()
        self.evaluate_planning()
        self.update_mood()
        return self.mood_obj.mood, self.reports
