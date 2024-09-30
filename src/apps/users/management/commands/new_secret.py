import os
import sys
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = "Secret Key Generator"

    def handle(self, *args, **options):
        os.system("cls" if os.name == "nt" else "clear")
        command_name = 'SECRET KEY GENERATOR - Django'
        print(f'{"-" * 48}')
        print(f'{" " * 12}{command_name}{" " * 12}')
        print(f'{"-" * 48}')
        print("Your new Django secret key:\n")
        self.stdout.write(self.style.ERROR(f"{get_random_secret_key()}"))

        while True:
            response = input(self.style.WARNING('\nGenerate another? (Y/N) '))
            if response == 'y' or response == 'Y':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.stdout.write(self.style.SUCCESS('Generating a new Django secret key...\n'))
                self.stdout.write(self.style.ERROR(f"mkxX{get_random_secret_key()}"))
                
            elif response == 'n' or response == 'N':
                self.stdout.write(self.style.SUCCESS("\nThank you and happy coding.\n"))
                sys.exit()
            else:
                self.stderr.write(self.style.ERROR('\nError: Please select Y or N.\n'))
                continue