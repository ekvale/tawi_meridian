"""
Core models for Tawi Meridian.

This module contains models shared across the application.
"""

from django.db import models
from django.core.validators import RegexValidator


class SiteSetting(models.Model):
    """
    Site-wide settings that can be managed through admin.
    
    This model allows non-technical users to update site settings
    without modifying code.
    """
    key = models.CharField(max_length=100, unique=True, help_text='Setting key (e.g., company_phone)')
    value = models.TextField(help_text='Setting value')
    description = models.TextField(blank=True, help_text='What this setting is used for')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'
        ordering = ['key']

    def __str__(self):
        return f'{self.key}: {self.value[:50]}'


class OfficeLocation(models.Model):
    """
    Office locations for the company.
    
    Used to display contact information and locations on the site.
    """
    name = models.CharField(max_length=200, help_text='Location name (e.g., "Minneapolis Office")')
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False, help_text='Mark as primary location')
    display_order = models.IntegerField(default=0, help_text='Order for display (lower numbers first)')

    class Meta:
        verbose_name = 'Office Location'
        verbose_name_plural = 'Office Locations'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_full_address(self):
        """Return formatted full address."""
        parts = []
        if self.address_line1:
            parts.append(self.address_line1)
        if self.address_line2:
            parts.append(self.address_line2)
        city_state = self.city
        if self.state:
            city_state += f', {self.state}'
        if self.zip_code:
            city_state += f' {self.zip_code}'
        if city_state:
            parts.append(city_state)
        if self.country:
            parts.append(self.country)
        return ', '.join(parts)


class Certification(models.Model):
    """
    Company certifications and credentials.
    
    Examples: 8(a), WOSB, EDWOSB, MBE
    """
    name = models.CharField(max_length=200, help_text='Certification name (e.g., "8(a) Certified")')
    abbreviation = models.CharField(max_length=50, blank=True, help_text='Short form (e.g., "WOSB")')
    description = models.TextField(blank=True, help_text='Brief description of the certification')
    logo = models.ImageField(upload_to='certifications/', blank=True, null=True, help_text='Certification logo/badge')
    certification_number = models.CharField(max_length=100, blank=True, help_text='Certification ID number')
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('active', 'Active'),
            ('expired', 'Expired'),
        ],
        default='pending'
    )
    display_order = models.IntegerField(default=0, help_text='Order for display (lower numbers first)')
    is_featured = models.BooleanField(default=False, help_text='Show prominently on homepage')

    class Meta:
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        ordering = ['display_order', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

    @property
    def is_active(self):
        """Check if certification is currently active."""
        if self.status == 'active':
            return True
        return False
