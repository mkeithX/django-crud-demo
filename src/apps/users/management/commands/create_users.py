import random
import os
from datetime import date
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **options):
        total = options['total']
        created_users = 0
        
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
                    password='password',  # Change this to a more secure password in production
                    email=email,
                    date_of_birth=dob
                )
                created_users += 1
                self.stdout.write(self.style.SUCCESS(f"Successfully created user: {first_name} {last_name} @{username}"))
            except (ValidationError, IntegrityError) as e:
                self.stderr.write(f"Error creating user: {str(e)}")
                continue

        self.stdout.write(self.style.SUCCESS(f"Total users created: {created_users}"))

    def generate_full_name(self):
        return self._get_random_line('first_name.txt')

    def generate_last_name(self):
        return self._get_random_line('last_name.txt')

    def generate_username(self):
        prefix = self._get_random_line('prefixes.txt')
        suffix = self._get_random_line('suffixes.txt')
        return f"{prefix}{suffix}"

    def generate_date_of_birth(self):
        today = date.today()
        start_date = today.replace(year=today.year - 80)
        end_date = today.replace(year=today.year - 18)
        random_dob = date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
        return random_dob

    def generate_email(self, username):
        domains = ['example.com']  # You can add more domains here
        domain = random.choice(domains)
        return f'{username}@{domain}'

    def _get_random_line(self, file_name):
        file_path = os.path.join(settings.BASE_DIR, 'src', 'apps', 'users', 'management', 'lists', file_name)
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:  # Ensure the list is not empty
                return random.choice(lines)
            else:
                self.stderr.write(f"Warning: {file_path} is empty.")
                return "default"  # Fallback value
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return "default"  # Fallback value
