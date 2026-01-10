"""
Contact models for Tawi Meridian.

This module defines the ContactSubmission model for contact form submissions.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone


# Project type choices
PROJECT_TYPES = [
    ('engineering', 'Engineering & Energy Systems'),
    ('data_science', 'Data Science & Analytics'),
    ('research', 'Research & Strategic Analysis'),
    ('international', 'International Development'),
    ('capacity_building', 'Capacity Building & Training'),
    ('other', 'Other'),
]

# Budget range choices
BUDGET_RANGES = [
    ('under_50k', 'Under $50,000'),
    ('50k_100k', '$50,000 - $100,000'),
    ('100k_250k', '$100,000 - $250,000'),
    ('250k_500k', '$250,000 - $500,000'),
    ('500k_1m', '$500,000 - $1,000,000'),
    ('over_1m', 'Over $1,000,000'),
    ('not_specified', 'Not Specified'),
]


class ContactSubmission(models.Model):
    """
    Contact form submission.
    
    Stores submissions from the contact form with validation and spam protection.
    """
    # Contact Information
    name = models.CharField(max_length=200, help_text='Contact name')
    email = models.EmailField(help_text='Contact email address')
    organization = models.CharField(
        max_length=200,
        blank=True,
        help_text='Organization name (optional)'
    )
    
    # Project Details
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPES,
        default='other',
        help_text='Type of project or service needed'
    )
    message = models.TextField(help_text='Project details or inquiry message')
    budget_range = models.CharField(
        max_length=50,
        choices=BUDGET_RANGES,
        default='not_specified',
        blank=True,
        help_text='Estimated budget range (optional)'
    )
    
    # Status & Tracking
    is_read = models.BooleanField(
        default=False,
        help_text='Whether submission has been reviewed'
    )
    is_responded = models.BooleanField(
        default=False,
        help_text='Whether response has been sent'
    )
    notes = models.TextField(
        blank=True,
        help_text='Internal notes about this submission'
    )
    
    # Metadata
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text='IP address of submitter (for spam detection)'
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        help_text='User agent string (for spam detection)'
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['is_read', 'submitted_at']),
            models.Index(fields=['is_responded', 'submitted_at']),
            models.Index(fields=['project_type', 'submitted_at']),
        ]

    def __str__(self):
        return f'{self.name} - {self.email} - {self.submitted_at.strftime("%Y-%m-%d")}'

    def get_absolute_url(self):
        """Return URL to view submission in admin."""
        return reverse('admin:contact_contactsubmission_change', args=[self.pk])

    def mark_as_read(self):
        """Mark submission as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def mark_as_responded(self):
        """Mark submission as responded."""
        if not self.is_responded:
            self.is_responded = True
            self.responded_at = timezone.now()
            self.save(update_fields=['is_responded', 'responded_at'])


class CapabilityDownload(models.Model):
    """
    Track capability statement downloads.
    
    Used to track downloads of capability statements for analytics.
    """
    # Document Information
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Capability Statement'),
            ('federal', 'Federal Capability Statement'),
            ('international', 'International Capability Statement'),
        ],
        default='general',
        help_text='Type of capability statement downloaded'
    )
    
    # Tracking Information
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text='IP address of downloader'
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        help_text='User agent string'
    )
    referer = models.URLField(
        blank=True,
        help_text='Referring page URL'
    )
    
    # Timestamp
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Capability Download'
        verbose_name_plural = 'Capability Downloads'
        ordering = ['-downloaded_at']
        indexes = [
            models.Index(fields=['document_type', 'downloaded_at']),
            models.Index(fields=['ip_address', 'downloaded_at']),
        ]

    def __str__(self):
        return f'{self.document_type} - {self.downloaded_at.strftime("%Y-%m-%d %H:%M")}'
