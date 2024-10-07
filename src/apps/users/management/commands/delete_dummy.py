from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Delete users whose usernames start with @dummy_'

    def handle(self, *args, **kwargs):
        User = get_user_model()  # Get the custom user model
        users_to_delete = User.objects.filter(username__startswith='dummy_')

        count = users_to_delete.count()

        if count > 0:
            users_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} user(s) whose usernames start with @dummy_.'))
        else:
            self.stdout.write(self.style.WARNING('No users found with usernames starting with @dummy_.'))
