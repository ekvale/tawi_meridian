"""
Views for blog app.

This module contains views for listing and displaying blog posts.
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from .models import BlogPost, CATEGORIES


class BlogListView(ListView):
    """
    List view for all published blog posts.
    
    Supports filtering by category, tag, and search.
    """
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter blog posts based on query parameters."""
        queryset = BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).order_by('-published_date', '-created_at')
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        # Filter by featured
        featured = self.request.GET.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        
        # Get filter options
        context['categories'] = CATEGORIES
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Get featured posts for sidebar or header
        context['featured_posts'] = BlogPost.objects.filter(
            is_published=True,
            is_featured=True,
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:3]
        
        # Get recent posts
        context['recent_posts'] = BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:5]
        
        context['page_title'] = 'Insights & Blog'
        context['meta_description'] = (
            'Read insights, analysis, and thought leadership from Tawi Meridian '
            'on engineering, data science, climate solutions, and government contracting.'
        )
        
        return context


class BlogPostDetailView(DetailView):
    """
    Detail view for individual blog posts.
    
    Increments view count and displays related posts.
    """
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Only show published posts."""
        return BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        )
    
    def get_object(self, queryset=None):
        """Get object and increment view count."""
        obj = super().get_object(queryset)
        # Increment view count (could be done asynchronously in production)
        obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        """Add additional context for template."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related images
        context['images'] = post.images.all().order_by('display_order')
        
        # Get related posts (same category or shared tags)
        related_queryset = BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).exclude(id=post.id)
        
        # Prioritize same category, then shared tags
        same_category = related_queryset.filter(category=post.category)
        
        # Get posts with shared tags
        shared_tags = []
        if post.tags:
            for tag in post.tags_list:
                shared_tags.extend(related_queryset.filter(tags__icontains=tag))
        
        # Combine and deduplicate
        related = list(same_category[:2]) + list(shared_tags[:2])
        # Remove duplicates while preserving order
        seen = set()
        unique_related = []
        for item in related:
            if item.id not in seen:
                seen.add(item.id)
                unique_related.append(item)
        
        context['related_posts'] = unique_related[:3]
        
        # Get recent posts for sidebar
        context['recent_posts'] = BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).exclude(id=post.id).order_by('-published_date')[:5]
        
        # SEO metadata
        context['page_title'] = post.display_title
        context['meta_description'] = post.display_description
        
        # Tags for display
        context['tags_list'] = post.tags_list
        
        return context
