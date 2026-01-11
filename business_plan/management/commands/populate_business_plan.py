"""
Management command to populate business plan data from the outline.

Usage: python manage.py populate_business_plan
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from business_plan.models import MilestonePeriod, Milestone, Task, CertificationTracking
from core.models import Certification

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate business plan milestones and tasks from the business plan outline'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing milestones and tasks before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing milestones and tasks...'))
            Task.objects.all().delete()
            Milestone.objects.all().delete()
            MilestonePeriod.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Populating business plan data...'))
        
        # Get or create admin user (for assignments)
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.WARNING('No admin user found. Creating milestones without assignments.'))
        
        # Create milestone periods
        self.create_milestone_periods()
        
        # Create milestones and tasks
        self.create_milestones_and_tasks(admin_user)
        
        # Create certification tracking
        self.create_certification_tracking(admin_user)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated business plan data.'))

    def create_milestone_periods(self):
        """Create milestone periods from the business plan."""
        today = timezone.now().date()
        year = today.year
        
        periods_data = [
            {
                'name': '90-Day Plan (Months 1-3)',
                'description': 'Foundation and market entry',
                'start_date': datetime(year, 1, 1).date(),
                'end_date': datetime(year, 3, 31).date(),
                'display_order': 1,
            },
            {
                'name': '6-Month Plan (Months 1-6)',
                'description': 'Building foundation and first wins',
                'start_date': datetime(year, 1, 1).date(),
                'end_date': datetime(year, 6, 30).date(),
                'display_order': 2,
            },
            {
                'name': 'Year 1',
                'description': 'First year of operations',
                'start_date': datetime(year, 1, 1).date(),
                'end_date': datetime(year, 12, 31).date(),
                'display_order': 3,
            },
        ]
        
        for data in periods_data:
            period, created = MilestonePeriod.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created period: {period.name}')
            else:
                self.stdout.write(f'Period already exists: {period.name}')

    def create_milestones_and_tasks(self, admin_user):
        """Create milestones and tasks from the business plan outline."""
        period_90_day = MilestonePeriod.objects.get(name='90-Day Plan (Months 1-3)')
        period_6_month = MilestonePeriod.objects.get(name='6-Month Plan (Months 1-6)')
        period_year1 = MilestonePeriod.objects.get(name='Year 1')
        
        today = timezone.now().date()
        
        # Month 1 Milestones (90-Day Plan)
        milestone_data = [
            {
                'period': period_90_day,
                'title': 'Complete Company Formation',
                'description': 'File Delaware LLC, apply for EIN, open business bank account, finalize operating agreement',
                'status': 'not_started',
                'priority': 'critical',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=7),
                'tasks': [
                    {'title': 'File Delaware LLC', 'description': 'Complete LLC filing'},
                    {'title': 'Apply for EIN', 'description': 'Obtain Employer Identification Number'},
                    {'title': 'Open business bank account', 'description': 'Set up business banking'},
                    {'title': 'Finalize operating agreement', 'description': 'Complete operating agreement with lawyer'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Complete SAM.gov Registration',
                'description': 'Register in System for Award Management (required for federal contracting)',
                'status': 'not_started',
                'priority': 'critical',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=14),
                'tasks': [
                    {'title': 'Obtain UEI/DUNS number', 'description': 'Get Unique Entity Identifier'},
                    {'title': 'Complete SAM.gov registration', 'description': 'Submit SAM.gov registration'},
                    {'title': 'Verify registration status', 'description': 'Confirm registration is active'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Submit WOSB Certification Application',
                'description': 'Apply for Women-Owned Small Business certification',
                'status': 'not_started',
                'priority': 'high',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=21),
                'tasks': [
                    {'title': 'Gather required documents', 'description': 'Collect all required WOSB documentation'},
                    {'title': 'Complete WOSB application', 'description': 'Fill out application on certify.sba.gov'},
                    {'title': 'Submit WOSB application', 'description': 'Submit application for review'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Begin 8(a) Application Preparation',
                'description': 'Start gathering documents and preparing 8(a) Business Development Program application',
                'status': 'not_started',
                'priority': 'high',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=30),
                'tasks': [
                    {'title': 'Review 8(a) requirements', 'description': 'Understand all application requirements'},
                    {'title': 'Gather personal financial documents', 'description': 'Collect required financial statements'},
                    {'title': 'Draft capability statement', 'description': 'Create company capability statement'},
                    {'title': 'Identify potential consultant', 'description': 'Research 8(a) application consultants (optional)'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Create Capability Statements',
                'description': 'Develop capability statements for different audiences',
                'status': 'not_started',
                'priority': 'medium',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=30),
                'tasks': [
                    {'title': 'Create general capability statement', 'description': 'General version for broad distribution'},
                    {'title': 'Create federal-focused capability statement', 'description': 'Tailored for federal agencies'},
                    {'title': 'Create USAID-focused capability statement', 'description': 'Tailored for USAID opportunities'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Launch Basic Website',
                'description': 'Get initial website live with core pages',
                'status': 'completed' if today > datetime(today.year, today.month, 1).date() + timedelta(days=21) else 'in_progress',
                'priority': 'high',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=21),
                'tasks': [
                    {'title': 'Launch basic website (v1)', 'description': 'Get initial version live'},
                    {'title': 'Create core pages (Home, About, Services)', 'description': 'Add essential pages'},
                ]
            },
            {
                'period': period_90_day,
                'title': 'Submit First Proposals',
                'description': 'Submit first 5 proposals to begin building pipeline',
                'status': 'not_started',
                'priority': 'high',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=90),
                'tasks': [
                    {'title': 'Identify first 10 target opportunities', 'description': 'Research and select opportunities'},
                    {'title': 'Respond to 2-3 RFIs', 'description': 'Submit responses to sources sought'},
                    {'title': 'Connect with 5 prime contractors', 'description': 'Establish teaming relationships'},
                    {'title': 'Submit first 2-3 proposals', 'description': 'Complete and submit proposals'},
                ]
            },
        ]
        
        # 6-Month Plan Milestones
        milestone_data.extend([
            {
                'period': period_6_month,
                'title': 'Win First Contract',
                'description': 'Secure first contract (subcontract or small prime)',
                'status': 'not_started',
                'priority': 'critical',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=120),
                'tasks': [
                    {'title': 'Deliver first project', 'description': 'Complete first contract successfully'},
                    {'title': 'Obtain first client testimonial', 'description': 'Request and receive testimonial'},
                ]
            },
            {
                'period': period_6_month,
                'title': 'Build Past Performance',
                'description': 'Establish track record with completed projects',
                'status': 'not_started',
                'priority': 'high',
                'target_date': datetime(today.year, today.month, 1).date() + timedelta(days=180),
                'tasks': [
                    {'title': 'Complete 2-3 projects', 'description': 'Successfully deliver multiple projects'},
                    {'title': 'Document case studies', 'description': 'Create case studies for past performance'},
                ]
            },
        ])
        
        # Year 1 Milestones
        milestone_data.extend([
            {
                'period': period_year1,
                'title': '8(a) Certification Approved',
                'description': 'Receive 8(a) Business Development Program certification',
                'status': 'not_started',
                'priority': 'critical',
                'target_date': datetime(today.year, 9, 1).date(),
                'tasks': [
                    {'title': 'Submit 8(a) application', 'description': 'Complete and submit application'},
                    {'title': 'Respond to SBA requests', 'description': 'Address any SBA questions or requests'},
                    {'title': 'Receive 8(a) certification', 'description': 'Obtain approval'},
                ]
            },
            {
                'period': period_year1,
                'title': 'Achieve $175k-$275k Revenue',
                'description': 'Reach Year 1 revenue targets',
                'status': 'not_started',
                'priority': 'critical',
                'target_date': datetime(today.year, 12, 31).date(),
                'tasks': [
                    {'title': 'Win 3-5 active contracts', 'description': 'Maintain active contract portfolio'},
                    {'title': 'Establish 2-3 recurring clients', 'description': 'Build repeat business'},
                ]
            },
        ])
        
        # Create milestones and tasks
        for milestone_info in milestone_data:
            period = milestone_info.pop('period')
            tasks_data = milestone_info.pop('tasks', [])
            
            milestone, created = Milestone.objects.get_or_create(
                period=period,
                title=milestone_info['title'],
                defaults={
                    **milestone_info,
                    'assigned_to': admin_user,
                }
            )
            
            if created:
                self.stdout.write(f'Created milestone: {milestone.title}')
            else:
                self.stdout.write(f'Milestone already exists: {milestone.title}')
            
            # Create tasks for this milestone
            for i, task_info in enumerate(tasks_data):
                task, task_created = Task.objects.get_or_create(
                    milestone=milestone,
                    title=task_info['title'],
                    defaults={
                        'description': task_info.get('description', ''),
                        'display_order': i,
                        'assigned_to': admin_user,
                    }
                )
                if task_created:
                    self.stdout.write(f'  Created task: {task.title}')

    def create_certification_tracking(self, admin_user):
        """Create certification tracking entries."""
        # Link to existing certifications or create tracking entries
        certifications = Certification.objects.all()
        today = timezone.now().date()
        
        cert_tracking_data = [
            {
                'name': '8(a) Business Development Program',
                'priority': 'critical',
                'status': 'application_prep',
                'target_submission_date': datetime(today.year, 2, 1).date(),
            },
            {
                'name': 'WOSB (Women-Owned Small Business)',
                'priority': 'high',
                'status': 'application_submitted',
                'target_submission_date': datetime(today.year, 1, 21).date(),
            },
            {
                'name': 'EDWOSB (Economically Disadvantaged WOSB)',
                'priority': 'high',
                'status': 'application_submitted',
                'target_submission_date': datetime(today.year, 1, 21).date(),
            },
        ]
        
        for data in cert_tracking_data:
            # Try to find matching certification
            cert = certifications.filter(name__icontains=data['name'].split('(')[0].strip()).first()
            
            tracking, created = CertificationTracking.objects.get_or_create(
                certification=cert if cert else None,
                name=data['name'] if not cert else cert.name,
                defaults={
                    **{k: v for k, v in data.items() if k != 'name'},
                    'assigned_to': admin_user,
                }
            )
            if created:
                self.stdout.write(f'Created certification tracking: {tracking.name}')

