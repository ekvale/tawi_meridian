"""
Management command to test email sending.

Usage: python manage.py test_email
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email sending configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default=None,
            help='Email address to send test email to (defaults to DEFAULT_FROM_EMAIL)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing email configuration...'))
        
        # Display current email settings
        self.stdout.write('\nCurrent Email Settings:')
        self.stdout.write(f'  EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'  EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'  EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'  EMAIL_USE_TLS: {getattr(settings, "EMAIL_USE_TLS", "N/A")}')
        self.stdout.write(f'  EMAIL_USE_SSL: {getattr(settings, "EMAIL_USE_SSL", "N/A")}')
        self.stdout.write(f'  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'  CONTACT_EMAIL: {getattr(settings, "CONTACT_EMAIL", "N/A")}')
        
        # Determine recipient
        recipient = options['to'] or settings.DEFAULT_FROM_EMAIL
        
        self.stdout.write(f'\nSending test email to: {recipient}')
        
        try:
            # Send test email
            send_mail(
                subject='Test Email from Tawi Meridian Server',
                message='This is a test email to verify email configuration is working correctly.\n\n'
                       'If you received this email, your email settings are configured properly!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS('\n✓ Email sent successfully!'))
            self.stdout.write(f'Check {recipient} for the test email.')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error sending email: {e}'))
            import traceback
            self.stdout.write(self.style.ERROR('\nFull error traceback:'))
            self.stdout.write(traceback.format_exc())
            return
        
        # Also test the contact form notification function
        self.stdout.write('\n' + '='*50)
        self.stdout.write('Testing contact form notification function...')
        
        try:
            from contact.forms import send_contact_notification
            from contact.models import ContactSubmission
            
            # Create a test submission
            test_submission = ContactSubmission(
                name='Test User',
                email=recipient,
                organization='Test Organization',
                project_type='engineering',
                message='This is a test submission to verify email notifications work.',
                budget_range='not_specified',
            )
            test_submission.save()
            
            self.stdout.write(f'Created test submission (ID: {test_submission.id})')
            
            # Try sending notification
            send_contact_notification(test_submission)
            
            self.stdout.write(self.style.SUCCESS('✓ Contact form notification email sent!'))
            self.stdout.write('Check your configured contact emails for the notification.')
            
            # Clean up test submission (optional)
            cleanup = input('\nDelete test submission? (y/N): ').strip().lower()
            if cleanup == 'y':
                test_submission.delete()
                self.stdout.write('Test submission deleted.')
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'\nWarning: Contact form test failed: {e}'))
            self.stdout.write('The basic email test passed, but contact form notifications may need review.')
