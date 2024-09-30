import random
from datetime import date
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **options):
        total = options['total']
        for _ in range(total):
            first_name = self.generate_full_name()
            last_name = self.generate_last_name()
            username = self.generate_username()
            dob = self.generate_date_of_birth()
            email = self.generate_email(username)

            try:
                User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password='password',
                    email=email,
                    date_of_birth=dob
                )
            except ValidationError as e:
                self.stderr.write(str(e))
                continue

            self.stdout.write(self.style.SUCCESS(f"Successfully created user: {first_name} {last_name} @{username}"))

    def generate_full_name(self):
        with open('src/apps/users/management/lists/first_name.txt', 'r') as f:
            first_names = [word.strip() for word in f.readlines()]
        return random.choice(first_names)

    def generate_last_name(self):
        with open('src/apps/users/management/lists/last_name.txt', 'r') as f:
            last_names = [word.strip() for word in f.readlines()]
        return random.choice(last_names)

    def generate_username(self):
        with open('src/apps/users/management/lists/prefixes.txt', 'r') as f:
            prefixes = [word.strip() for word in f.readlines()]
        with open('src/apps/users/management/lists/suffixes.txt', 'r') as f:
            suffixes = [word.strip() for word in f.readlines()]
        return random.choice(prefixes) + random.choice(suffixes)

    def generate_date_of_birth(self):
        today = date.today()
        start_date = today.replace(year=today.year - 80)
        end_date = today.replace(year=today.year - 18)
        random_dob = date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
        return random_dob

    def generate_email(self, username):
        domains = ['example.com']
        domain = random.choice(domains)
        return f'{username}@{domain}'