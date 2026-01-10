"""
Management command to load initial data.

Usage: python manage.py load_initial_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from services.models import Service
from portfolio.models import CaseStudy
from blog.models import BlogPost
from core.models import Certification, OfficeLocation


class Command(BaseCommand):
    help = 'Load initial data for the site'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading initial data...'))
        
        # Create services
        self.create_services()
        
        # Create certifications
        self.create_certifications()
        
        # Create office locations
        self.create_office_locations()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data.'))

    def create_services(self):
        """Create initial services."""
        services_data = [
            {
                'title': 'Engineering & Energy Systems',
                'slug': 'engineering-energy-systems',
                'short_description': 'Renewable energy systems, HVAC optimization, and building performance solutions that reduce costs and environmental impact.',
                'full_description': (
                    'Tawi Meridian provides comprehensive engineering and energy systems services, including renewable energy design, '
                    'HVAC/MEP systems, building performance optimization, and energy audits. Our solutions reduce costs and environmental impact '
                    'while improving operational efficiency.'
                ),
                'icon': 'lightning-bolt',
                'display_order': 1,
                'is_featured': True,
            },
            {
                'title': 'Data Science & Analytics',
                'slug': 'data-science-analytics',
                'short_description': 'Transform complex data into actionable insights through predictive modeling, automated dashboards, and spatial analysis.',
                'full_description': (
                    'Our data science and analytics services help organizations transform complex data into actionable insights. '
                    'We provide predictive modeling, database automation, GIS/spatial analysis, and dashboard development to support '
                    'data-driven decision making.'
                ),
                'icon': 'chart-bar',
                'display_order': 2,
                'is_featured': True,
            },
            {
                'title': 'Research & Strategic Analysis',
                'slug': 'research-strategic-analysis',
                'short_description': 'Evidence-based feasibility studies, market analysis, and grant research to inform critical decisions.',
                'full_description': (
                    'Tawi Meridian conducts evidence-based research and strategic analysis, including feasibility studies, market analysis, '
                    'SBIR/STTR research, and grant research projects. Our research informs critical decisions and supports successful proposals.'
                ),
                'icon': 'academic-cap',
                'display_order': 3,
                'is_featured': True,
            },
            {
                'title': 'International Development',
                'slug': 'international-development',
                'short_description': 'Climate-smart agricultural technology and community-based renewable energy solutions for sustainable development.',
                'full_description': (
                    'Our international development services focus on climate-smart agricultural technology, post-harvest systems, '
                    'community-based renewable energy, and technology transfer. We design solutions that are sustainable, culturally appropriate, '
                    'and community-driven.'
                ),
                'icon': 'globe-alt',
                'display_order': 4,
                'is_featured': False,
            },
            {
                'title': 'Capacity Building & Training',
                'slug': 'capacity-building-training',
                'short_description': 'Training programs and technical assistance that empower organizations and communities to drive their own progress.',
                'full_description': (
                    'Tawi Meridian provides capacity building and training services, including training program design, climate education, '
                    'and technical assistance. We empower organizations and communities to drive their own progress through knowledge transfer '
                    'and skill development.'
                ),
                'icon': 'user-group',
                'display_order': 5,
                'is_featured': False,
            },
        ]
        
        for data in services_data:
            service, created = Service.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created service: {service.title}')
            else:
                self.stdout.write(f'Service already exists: {service.title}')

    def create_certifications(self):
        """Create initial certifications."""
        certifications_data = [
            {
                'name': '8(a) Business Development Program',
                'abbreviation': '8(a)',
                'description': 'Small Business Administration 8(a) Business Development Program',
                'status': 'pending',
                'display_order': 1,
                'is_featured': True,
            },
            {
                'name': 'Women-Owned Small Business',
                'abbreviation': 'WOSB',
                'description': 'Women-Owned Small Business certification',
                'status': 'pending',
                'display_order': 2,
                'is_featured': True,
            },
            {
                'name': 'Economically Disadvantaged Women-Owned Small Business',
                'abbreviation': 'EDWOSB',
                'description': 'Economically Disadvantaged Women-Owned Small Business certification',
                'status': 'pending',
                'display_order': 3,
                'is_featured': True,
            },
            {
                'name': 'Minority Business Enterprise',
                'abbreviation': 'MBE',
                'description': 'Minority Business Enterprise certification',
                'status': 'pending',
                'display_order': 4,
                'is_featured': False,
            },
        ]
        
        for data in certifications_data:
            cert, created = Certification.objects.get_or_create(
                abbreviation=data['abbreviation'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created certification: {cert.name}')
            else:
                self.stdout.write(f'Certification already exists: {cert.name}')

    def create_office_locations(self):
        """Create initial office locations."""
        locations_data = [
            {
                'name': 'Minneapolis Office',
                'address_line1': '',  # Street address can be added later
                'city': 'Minneapolis',
                'state': 'Minnesota',
                'zip_code': '',
                'country': 'United States',
                'is_primary': True,
                'display_order': 1,
            },
            {
                'name': 'Texas Office',
                'address_line1': '',  # Street address can be added later
                'city': 'Austin',
                'state': 'Texas',
                'zip_code': '',
                'country': 'United States',
                'is_primary': False,
                'display_order': 2,
            },
        ]
        
        for data in locations_data:
            location, created = OfficeLocation.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created location: {location.name}')
            else:
                self.stdout.write(f'Location already exists: {location.name}')
