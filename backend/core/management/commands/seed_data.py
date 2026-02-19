import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from faker import Faker
from planning.models import Event, Task
from finance.models import Category, Transaction
from notes.models import Note
from contacts.models import Contact
from projects.models import Project

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with mock data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Get or create a mock user
        user, created = User.objects.get_or_create(
            username='mock@example.com',
            defaults={
                'email': 'mock@example.com', 
                'firebase_uid': 'mock_uid'
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
            self.stdout.write(f'Created user: {user.email}')
        else:
            self.stdout.write(f'Using existing user: {user.email}')

        # 1. Planning: Events (200 items)
        self.stdout.write('Creating Events...')
        events = []
        for _ in range(200):
            start_time = timezone.now() + timedelta(days=random.randint(-30, 90), hours=random.randint(8, 18))
            end_time = start_time + timedelta(hours=random.randint(1, 4))
            events.append(Event(
                user=user,
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(),
                start_time=start_time,
                end_time=end_time,
                location=fake.address(),
                is_all_day=random.choice([True, False])
            ))
        Event.objects.bulk_create(events)

        # 2. Planning: Tasks (200 items)
        self.stdout.write('Creating Tasks...')
        tasks = []
        priorities = ['LOW', 'MEDIUM', 'HIGH']
        for _ in range(200):
            tasks.append(Task(
                user=user,
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(),
                due_date=timezone.now() + timedelta(days=random.randint(-10, 60)),
                is_completed=random.choice([True, False]),
                priority=random.choice(priorities)
            ))
        Task.objects.bulk_create(tasks)

        # 3. Finance: Categories & Transactions (50 Categories, 200 Transactions)
        self.stdout.write('Creating Finance Data...')
        # Create default categories if they don't exist
        income_cats = ['Salary', 'Freelance', 'Investments', 'Gifts']
        expense_cats = ['Food', 'Rent', 'Transport', 'Utilities', 'Entertainment', 'Health', 'Shopping']
        
        categories = []
        for cat_name in income_cats:
            cat, _ = Category.objects.get_or_create(user=user, name=cat_name, type='INCOME')
            categories.append(cat)
        for cat_name in expense_cats:
            cat, _ = Category.objects.get_or_create(user=user, name=cat_name, type='EXPENSE')
            categories.append(cat)
            
        transactions = []
        for _ in range(200):
            cat = random.choice(categories)
            transactions.append(Transaction(
                user=user,
                category=cat,
                amount=round(random.uniform(10.0, 5000.0), 2),
                description=fake.sentence(),
                date=fake.date_between(start_date='-1y', end_date='today')
            ))
        Transaction.objects.bulk_create(transactions)

        # 4. Notes (150 items)
        self.stdout.write('Creating Notes...')
        notes = []
        for _ in range(150):
            notes.append(Note(
                user=user,
                title=fake.sentence(nb_words=3),
                content=fake.text(max_nb_chars=1000)
            ))
        Note.objects.bulk_create(notes)

        # 5. Contacts (100 items)
        self.stdout.write('Creating Contacts...')
        contacts = []
        for _ in range(100):
            contacts.append(Contact(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:20], 
                email=fake.email(),
                address=fake.address()
            ))
        Contact.objects.bulk_create(contacts)

        # 6. Projects (50 items)
        self.stdout.write('Creating Projects...')
        projects = []
        statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD']
        for _ in range(50):
            start_date = fake.date_between(start_date='-6m', end_date='today')
            end_date = start_date + timedelta(days=random.randint(14, 180))
            projects.append(Project(
                user=user,
                name=fake.catch_phrase(),
                description=fake.paragraph(),
                start_date=start_date,
                end_date=end_date,
                status=random.choice(statuses)
            ))
        Project.objects.bulk_create(projects)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with large dataset!'))
