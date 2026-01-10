"""
Core views for Tawi Meridian.

This module contains views for the main pages (home, about, etc.).
"""

from django.shortcuts import render
from django.conf import settings
from portfolio.models import CaseStudy
from services.models import Service


def home(request):
    """
    Home page view.
    
    Displays:
    - Hero section with mission statement
    - Impact metrics (animated counters)
    - Service pillars
    - Featured case studies
    - Certifications badges
    """
    # Get featured case studies
    featured_case_studies = CaseStudy.objects.filter(
        featured=True,
        published=True
    ).order_by('-published_date')[:3]
    
    # Get active services for service pillars
    services = Service.objects.filter(is_active=True).order_by('display_order')[:3]
    
    # Get impact metrics from settings (can be moved to database later)
    impact_metrics = settings.IMPACT_METRICS
    
    context = {
        'featured_case_studies': featured_case_studies,
        'services': services,
        'impact_metrics': impact_metrics,
        'page_title': 'Home',
        'meta_description': (
            'Tawi Meridian delivers engineering and data science excellence '
            'for government missions. From renewable energy solutions to '
            'advanced analytics, we build sustainable impact.'
        ),
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page view.
    
    Displays company story, mission, founders, and values.
    """
    context = {
        'page_title': 'About Us',
        'meta_description': (
            'Learn about Tawi Meridian\'s mission, founders, and commitment '
            'to engineering excellence and community impact.'
        ),
    }
    
    return render(request, 'core/about.html', context)
