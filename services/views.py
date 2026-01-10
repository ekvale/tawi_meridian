"""
Views for services app.

This module contains views for listing and displaying services.
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service


class ServiceListView(ListView):
    """
    List view for all active services.
    
    Displays all active services in a grid layout.
    Can be filtered by featured status via query parameter.
    """
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        """Filter services based on query parameters."""
        queryset = Service.objects.filter(is_active=True).order_by('display_order', 'title')
        
        # Filter by featured if requested
        featured = self.request.GET.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(full_description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Our Services'
        context['meta_description'] = (
            'Explore Tawi Meridian\'s comprehensive engineering, data science, '
            'and consulting services for government agencies and organizations.'
        )
        context['featured_services'] = Service.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('display_order')[:3]
        return context


class ServiceDetailView(DetailView):
    """
    Detail view for individual service pages.
    
    Displays full service information, features, and related case studies.
    """
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Only show active services."""
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        
        # Get service features
        context['features'] = service.features.all().order_by('display_order')
        
        # Get related case studies (will be implemented when portfolio app is ready)
        # context['related_case_studies'] = service.case_studies.all()[:3]
        
        # SEO metadata
        context['page_title'] = service.display_title
        context['meta_description'] = service.display_description
        
        # Get other services for navigation
        context['other_services'] = Service.objects.filter(
            is_active=True
        ).exclude(id=service.id).order_by('display_order')[:3]
        
        return context
