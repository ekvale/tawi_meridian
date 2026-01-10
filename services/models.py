"""
Services models for Tawi Meridian.

This module defines the Service model and related models.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    """
    Service offerings of Tawi Meridian.
    
    Each service represents a core capability area such as:
    - Engineering & Energy Systems
    - Data Science & Analytics
    - Research & Strategic Analysis
    - International Development
    - Capacity Building & Training
    """
    # Basic Information
    title = models.CharField(max_length=200, help_text='Service name (e.g., "Data Science & Analytics")')
    slug = models.SlugField(max_length=200, unique=True, help_text='URL-friendly version of title')
    short_description = models.TextField(
        max_length=500,
        help_text='Brief description for cards and listings (max 500 characters)'
    )
    full_description = models.TextField(
        help_text='Full description for service detail page'
    )
    
    # Visual Elements
    icon = models.CharField(
        max_length=50,
        default='chart-bar',
        help_text='Heroicon name (e.g., "chart-bar", "lightning-bolt", "globe-alt")'
    )
    featured_image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text='Featured image for service page'
    )
    
    # Organization
    display_order = models.IntegerField(
        default=0,
        help_text='Order for display (lower numbers appear first)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this service is currently offered'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Show prominently on homepage'
    )
    
    # SEO & Metadata
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        help_text='SEO title (defaults to title if not set)'
    )
    meta_description = models.TextField(
        max_length=300,
        blank=True,
        help_text='SEO description (defaults to short_description if not set)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['display_order', 'title']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
            models.Index(fields=['display_order', 'is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to service detail page."""
        return reverse('services:service_detail', kwargs={'slug': self.slug})

    @property
    def display_title(self):
        """Return meta_title if set, otherwise title."""
        return self.meta_title or self.title

    @property
    def display_description(self):
        """Return meta_description if set, otherwise short_description."""
        return self.meta_description or self.short_description


class ServiceFeature(models.Model):
    """
    Key features or capabilities within a service.
    
    Used to display bullet points or feature lists on service detail pages.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='features'
    )
    title = models.CharField(max_length=200, help_text='Feature title')
    description = models.TextField(help_text='Feature description')
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Optional icon name'
    )
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Service Feature'
        verbose_name_plural = 'Service Features'
        ordering = ['display_order', 'title']

    def __str__(self):
        return f'{self.service.title}: {self.title}'


class ServiceCaseStudy(models.Model):
    """
    Many-to-many relationship between Services and Case Studies.
    
    This allows case studies to be associated with multiple services
    and services to show related case studies.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_case_studies')
    # Will reference portfolio.CaseStudy when that app is created
    case_study_id = models.IntegerField(help_text='ID of related case study')
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Service Case Study'
        verbose_name_plural = 'Service Case Studies'
        ordering = ['display_order']
        unique_together = ['service', 'case_study_id']

    def __str__(self):
        return f'{self.service.title} - Case Study {self.case_study_id}'
