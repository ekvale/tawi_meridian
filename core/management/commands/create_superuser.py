"""
Management command to create a superuser.

Usage: python manage.py create_superuser
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass


class Command(BaseCommand):
    help = 'Create a superuser account'

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write(self.style.SUCCESS('Creating superuser...'))
        
        username = input('Username: ')
        email = input('Email: ')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists.'))
            return
        
        password = getpass.getpass('Password: ')
        password_confirm = getpass.getpass('Password (again): ')
        
        if password != password_confirm:
            self.stdout.write(self.style.ERROR('Passwords do not match.'))
            return
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}".'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
