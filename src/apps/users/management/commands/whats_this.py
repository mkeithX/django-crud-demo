import os
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "What's this?"

    def handle(self, *args, **options):
        os.system("cls" if os.name == "nt" else "clear")
        command_name = "Django CRUD Demo"
        command_description = "\nSimple CRUD application built with Django.\n"
        border_length = len(command_name) * 2 + 2

        print("+" + "-" * (border_length - 2) + "+")
        print("", end=" ")
        for char in command_name:
            print(char, end=" ")
        print("")
        print("+" + "-" * (border_length - 2) + "+")
        self.stdout.write(self.style.SUCCESS(command_description))