"""
Management command to check CSRF settings.
Usage: python manage.py check_csrf
"""

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Check CSRF configuration settings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== CSRF Configuration Check ===\n'))
        
        # Check CSRF_TRUSTED_ORIGINS
        self.stdout.write(f'CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}')
        self.stdout.write(f'  Type: {type(settings.CSRF_TRUSTED_ORIGINS)}')
        self.stdout.write(f'  Count: {len(settings.CSRF_TRUSTED_ORIGINS)}')
        
        if settings.CSRF_TRUSTED_ORIGINS:
            for origin in settings.CSRF_TRUSTED_ORIGINS:
                self.stdout.write(f'  - {origin}')
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  CSRF_TRUSTED_ORIGINS is empty!'))
        
        # Check other CSRF settings
        self.stdout.write(f'\nCSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}')
        self.stdout.write(f'CSRF_COOKIE_SAMESITE: {getattr(settings, "CSRF_COOKIE_SAMESITE", "Not set")}')
        self.stdout.write(f'SECURE_PROXY_SSL_HEADER: {getattr(settings, "SECURE_PROXY_SSL_HEADER", "Not set")}')
        
        # Check environment
        self.stdout.write(f'\nDEBUG: {settings.DEBUG}')
        self.stdout.write(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        # Check .env file location
        from pathlib import Path
        env_path = Path(settings.BASE_DIR) / '.env'
        self.stdout.write(f'\n.env file path: {env_path}')
        if env_path.exists():
            self.stdout.write(self.style.SUCCESS('  ✓ .env file exists'))
            # Try to read CSRF_TRUSTED_ORIGINS from file
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        if 'CSRF_TRUSTED_ORIGINS' in line:
                            self.stdout.write(f'  Found in .env: {line.strip()}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Error reading .env: {e}'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  .env file not found at this location!'))
        
        self.stdout.write(self.style.SUCCESS('\n=== End of CSRF Check ===\n'))
