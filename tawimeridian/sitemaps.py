"""
Sitemap configuration for SEO.

This module defines sitemaps for different sections of the site.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Import models when apps are created
# from services.models import Service
# from portfolio.models import CaseStudy
# from blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'services', 'portfolio', 'blog', 'contact']

    def location(self, item):
        return reverse(item)


# Additional sitemaps will be added in their respective apps
