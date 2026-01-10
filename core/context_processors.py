"""
Custom context processors for global template variables.
"""

from django.conf import settings
from .models import OfficeLocation, Certification, SiteSetting


def site_settings(request):
    """
    Add site-wide settings to template context.
    
    This makes commonly used data available in all templates,
    reducing the need to pass it explicitly in every view.
    """
    context = {
        'site_name': settings.SITE_NAME,
        'site_description': settings.SITE_DESCRIPTION,
        'google_analytics_id': settings.GOOGLE_ANALYTICS_ID,
        'social_links': settings.SOCIAL_LINKS,
        'impact_metrics': settings.IMPACT_METRICS,
    }
    
    # Add office locations
    try:
        context['office_locations'] = OfficeLocation.objects.all().order_by('display_order')
        context['primary_location'] = OfficeLocation.objects.filter(is_primary=True).first()
    except Exception:
        # Handle case when database tables don't exist yet
        context['office_locations'] = []
        context['primary_location'] = None
    
    # Add featured certifications
    try:
        context['featured_certifications'] = Certification.objects.filter(
            is_featured=True,
            status='active'
        ).order_by('display_order')
    except Exception:
        context['featured_certifications'] = []
    
    # Add site settings as a dictionary for easy access
    try:
        site_settings_dict = {}
        for setting in SiteSetting.objects.all():
            site_settings_dict[setting.key] = setting.value
        context['site_settings'] = site_settings_dict
    except Exception:
        context['site_settings'] = {}
    
    # Add active services for navigation
    try:
        from services.models import Service
        context['services'] = Service.objects.filter(is_active=True).order_by('display_order')[:10]
    except Exception:
        context['services'] = []
    
    return context
