"""
Views for portfolio app.

This module contains views for listing and displaying case studies.
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import CaseStudy, CLIENT_TYPES


class CaseStudyListView(ListView):
    """
    List view for all published case studies.
    
    Supports filtering by client_type, service, and search.
    """
    model = CaseStudy
    template_name = 'portfolio/list.html'
    context_object_name = 'case_studies'
    paginate_by = 9
    
    def get_queryset(self):
        """Filter case studies based on query parameters."""
        queryset = CaseStudy.objects.filter(published=True).order_by('-published_date', '-created_at')
        
        # Filter by client type
        client_type = self.request.GET.get('client_type')
        if client_type:
            queryset = queryset.filter(client_type=client_type)
        
        # Filter by service
        service_slug = self.request.GET.get('service')
        if service_slug:
            queryset = queryset.filter(service__slug=service_slug)
        
        # Filter by featured
        featured = self.request.GET.get('featured')
        if featured == 'true':
            queryset = queryset.filter(featured=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(challenge__icontains=search_query) |
                Q(solution__icontains=search_query) |
                Q(results__icontains=search_query) |
                Q(technologies__icontains=search_query) |
                Q(client_name__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        
        # Get filter options
        context['client_types'] = CLIENT_TYPES
        context['selected_client_type'] = self.request.GET.get('client_type', '')
        context['selected_service'] = self.request.GET.get('service', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Get featured case studies for sidebar or header
        context['featured_case_studies'] = CaseStudy.objects.filter(
            published=True,
            featured=True
        ).order_by('-published_date')[:3]
        
        context['page_title'] = 'Portfolio & Case Studies'
        context['meta_description'] = (
            'Explore Tawi Meridian\'s portfolio of engineering, data science, '
            'and consulting projects for government agencies and organizations.'
        )
        
        return context


class CaseStudyDetailView(DetailView):
    """
    Detail view for individual case studies.
    
    Displays full case study information, images, testimonials, and related case studies.
    """
    model = CaseStudy
    template_name = 'portfolio/detail.html'
    context_object_name = 'case_study'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Only show published case studies."""
        return CaseStudy.objects.filter(published=True)
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        case_study = self.get_object()
        
        # Get related images
        context['images'] = case_study.images.all().order_by('display_order')
        
        # Get testimonials
        context['testimonials'] = case_study.testimonials.all().order_by('display_order')
        
        # Get related case studies (same service or client type)
        related_queryset = CaseStudy.objects.filter(
            published=True
        ).exclude(id=case_study.id)
        
        # Prioritize same service, then same client type
        same_service = related_queryset.filter(service=case_study.service)
        same_client_type = related_queryset.filter(client_type=case_study.client_type).exclude(
            service=case_study.service
        )
        
        related = list(same_service[:2]) + list(same_client_type[:1])
        context['related_case_studies'] = related[:3]
        
        # SEO metadata
        context['page_title'] = case_study.display_title
        context['meta_description'] = case_study.display_description
        
        return context
