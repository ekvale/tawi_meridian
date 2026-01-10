"""
Portfolio models for Tawi Meridian.

This module defines the CaseStudy model for showcasing projects and client work.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


# Client type choices
CLIENT_TYPES = [
    ('federal', 'Federal Agency'),
    ('state', 'State/Local Government'),
    ('international', 'International Organization'),
    ('corporate', 'Corporate'),
    ('foundation', 'Foundation/NGO'),
    ('other', 'Other'),
]


class CaseStudy(models.Model):
    """
    Case study / portfolio project.
    
    Represents a completed project or client engagement.
    Used to showcase Tawi Meridian's work and capabilities.
    """
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text='Project title (e.g., "Hybrid Solar-Biomass Mango Drier")'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='URL-friendly version of title'
    )
    
    # Client & Project Details
    client_type = models.CharField(
        max_length=50,
        choices=CLIENT_TYPES,
        help_text='Type of client organization'
    )
    client_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Client name (optional, may be confidential)'
    )
    
    # Service Relationship
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_case_studies',
        help_text='Primary service category for this project'
    )
    
    # Project Content
    challenge = models.TextField(
        help_text='Problem statement or challenge addressed'
    )
    solution = models.TextField(
        help_text='Approach and solution implemented'
    )
    results = models.TextField(
        help_text='Results and impact achieved'
    )
    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text='Technologies, tools, or methodologies used (comma-separated)'
    )
    
    # Metrics & Impact
    impact_metrics = models.JSONField(
        blank=True,
        null=True,
        help_text='Key metrics as JSON (e.g., {"energy_saved": "45%", "cost_reduction": "$50k"})'
    )
    
    # Visual Elements
    hero_image = models.ImageField(
        upload_to='case_studies/',
        help_text='Main featured image for case study'
    )
    
    # Status & Display
    featured = models.BooleanField(
        default=False,
        help_text='Show prominently on homepage'
    )
    published = models.BooleanField(
        default=False,
        help_text='Make visible on public site'
    )
    published_date = models.DateField(
        help_text='Date project was completed or published'
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
        help_text='SEO description'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['slug', 'published']),
            models.Index(fields=['featured', 'published']),
            models.Index(fields=['client_type', 'published']),
            models.Index(fields=['service', 'published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to case study detail page."""
        return reverse('portfolio:case_study_detail', kwargs={'slug': self.slug})

    @property
    def display_title(self):
        """Return meta_title if set, otherwise title."""
        return self.meta_title or self.title

    @property
    def display_description(self):
        """Return meta_description if set, otherwise excerpt from challenge."""
        if self.meta_description:
            return self.meta_description
        return self.challenge[:200] + '...' if len(self.challenge) > 200 else self.challenge

    @property
    def technologies_list(self):
        """Return technologies as a list."""
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',')]
        return []


class CaseStudyImage(models.Model):
    """
    Additional images for case studies.
    
    Allows multiple images per case study for galleries or detailed views.
    """
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='case_studies/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for accessibility (auto-generated if blank)'
    )
    display_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(
        default=False,
        help_text='Use as primary image if hero_image is not set'
    )

    class Meta:
        verbose_name = 'Case Study Image'
        verbose_name_plural = 'Case Study Images'
        ordering = ['display_order']
        indexes = [
            models.Index(fields=['case_study', 'display_order']),
        ]

    def __str__(self):
        return f'{self.case_study.title} - Image {self.display_order}'

    def save(self, *args, **kwargs):
        """Auto-generate alt text if not provided."""
        if not self.alt_text and self.caption:
            self.alt_text = self.caption
        elif not self.alt_text:
            self.alt_text = f'{self.case_study.title} - Image {self.display_order}'
        super().save(*args, **kwargs)


class CaseStudyTestimonial(models.Model):
    """
    Client testimonials for case studies.
    
    Optional client feedback or quotes about the project.
    """
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name='testimonials'
    )
    quote = models.TextField(help_text='Testimonial text')
    author_name = models.CharField(max_length=200, help_text='Testimonial author name')
    author_title = models.CharField(
        max_length=200,
        blank=True,
        help_text='Author job title or role'
    )
    author_organization = models.CharField(
        max_length=200,
        blank=True,
        help_text='Author organization'
    )
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Case Study Testimonial'
        verbose_name_plural = 'Case Study Testimonials'
        ordering = ['display_order']
        indexes = [
            models.Index(fields=['case_study', 'display_order']),
        ]

    def __str__(self):
        return f'{self.case_study.title} - {self.author_name}'
