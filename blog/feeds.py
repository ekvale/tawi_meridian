"""
RSS feed for blog posts.

This module provides RSS feed functionality for blog posts.
"""

from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import BlogPost
from django.utils import timezone


class LatestBlogPostsFeed(Feed):
    """
    RSS feed for latest blog posts.
    
    Provides RSS feed of published blog posts for subscribers and aggregators.
    """
    title = 'Tawi Meridian Insights & Blog'
    link = '/insights/'
    description = 'Latest insights, analysis, and thought leadership from Tawi Meridian.'
    
    def items(self):
        """Return published blog posts."""
        return BlogPost.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:20]
    
    def item_title(self, item):
        """Return post title."""
        return item.title
    
    def item_description(self, item):
        """Return post excerpt."""
        return item.excerpt
    
    def item_pubdate(self, item):
        """Return publication date."""
        return item.published_date
    
    def item_author_name(self, item):
        """Return author name."""
        return item.author
    
    def item_link(self, item):
        """Return absolute URL to post."""
        return item.get_absolute_url()
    
    def item_categories(self, item):
        """Return post category as a list."""
        return [item.get_category_display()]
