"""
URL configuration for Tawi Meridian project.

This module defines the URL patterns for the entire site.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

# Import sitemaps when created
# from blog.sitemaps import BlogSitemap
# from portfolio.sitemaps import PortfolioSitemap

# sitemaps = {
#     'blog': BlogSitemap,
#     'portfolio': PortfolioSitemap,
# }

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core pages
    path('', include('core.urls')),
    
    # Services
    path('services/', include('services.urls')),
    
    # Portfolio/Case Studies
    path('portfolio/', include('portfolio.urls')),
    
    # Blog/Insights
    path('insights/', include('blog.urls')),
    
    # Contact
    path('contact/', include('contact.urls')),
    
    # Business Plan Tracking
    path('business-plan/', include('business_plan.urls')),
    
    # Sitemap (uncomment when sitemaps are created)
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'Tawi Meridian Administration'
admin.site.site_title = 'Tawi Meridian Admin'
admin.site.index_title = 'Welcome to Tawi Meridian Administration'
