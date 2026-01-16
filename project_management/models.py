"""
Project Management Models

Models for managing business operations including:
- Organizations (companies, government agencies, universities, etc.)
- Contacts (people associated with organizations)
- Interactions (communications, meetings, notes)
- Opportunities and proposals
- Projects and tasks
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, EmailValidator
from django.urls import reverse
from django.utils import timezone


class OrganizationType(models.Model):
    """
    Types of organizations (e.g., "Farmer Cooperative", "Government Agency", "University")
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Organization Type'
        verbose_name_plural = 'Organization Types'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class ContactCategory(models.Model):
    """
    Categories for organizing contacts (e.g., "TOP PRIORITY", "STRATEGIC PARTNER", "KEY ACADEMIC PARTNER")
    """
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, default='blue', help_text='CSS color for display')
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Contact Category'
        verbose_name_plural = 'Contact Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    Organizations (companies, government agencies, universities, cooperatives, etc.)
    """
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('partner', 'Partner'),
        ('competitor', 'Competitor'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, blank=True, related_name='organizations')
    category = models.ForeignKey(ContactCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='organizations')
    
    # Contact Information
    website = models.URLField(blank=True, validators=[URLValidator()])
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, help_text='City, County, Country')
    
    # Details
    description = models.TextField(blank=True, help_text='Overview and background')
    key_notes = models.TextField(blank=True, help_text='Why contact, key needs, opportunities')
    contact_strategy = models.TextField(blank=True, help_text='Recommended approach for engagement')
    
    # Status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospect')
    
    # Tracking
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_organizations')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags for filtering')
    
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_management:organization_detail', kwargs={'pk': self.pk})
    
    @property
    def primary_contact(self):
        """Get the primary contact for this organization"""
        return self.contacts.filter(is_primary=True).first()
    
    @property
    def contact_count(self):
        """Count of associated contacts"""
        return self.contacts.count()


class Contact(models.Model):
    """
    Individual contacts (people) associated with organizations
    """
    ROLE_CHOICES = [
        ('chairman', 'Chairman'),
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('coordinator', 'Coordinator'),
        ('researcher', 'Researcher'),
        ('officer', 'Officer'),
        ('representative', 'Representative'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True, help_text='Job title or position')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    
    # Organization
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='contacts')
    is_primary = models.BooleanField(default=False, help_text='Primary contact for the organization')
    
    # Contact Information
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    
    # Notes
    notes = models.TextField(blank=True, help_text='Additional information about this contact')
    key_info = models.TextField(blank=True, help_text='Important details, background, connections')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['organization', 'is_primary', 'last_name', 'first_name']
        # Only enforce unique email when email is not empty
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'email'],
                condition=models.Q(email__isnull=False) & ~models.Q(email=''),
                name='unique_contact_email_per_org'
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'email'],
                condition=models.Q(email__isnull=False) & ~models.Q(email=''),
                name='unique_contact_email_per_org'
            ),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.organization.name}"
    
    def get_full_name(self):
        """Get full name of the contact"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_absolute_url(self):
        return reverse('project_management:contact_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Ensure only one primary contact per organization
        if self.is_primary:
            Contact.objects.filter(organization=self.organization, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class ContactInteraction(models.Model):
    """
    Track interactions with contacts (meetings, calls, emails, notes)
    """
    INTERACTION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('proposal', 'Proposal Sent'),
        ('follow_up', 'Follow-up'),
        ('other', 'Other'),
    ]
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='interactions')
    
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPE_CHOICES, default='note')
    subject = models.CharField(max_length=200, blank=True)
    notes = models.TextField(help_text='Details of the interaction')
    
    # Dates
    interaction_date = models.DateTimeField(default=timezone.now)
    next_action = models.CharField(max_length=200, blank=True, help_text='Next step or follow-up action')
    next_action_date = models.DateField(null=True, blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_interactions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contact Interaction'
        verbose_name_plural = 'Contact Interactions'
        ordering = ['-interaction_date', '-created_at']
    
    def __str__(self):
        contact_name = self.contact.get_full_name() if self.contact else 'Organization'
        return f"{self.interaction_type.title()} with {contact_name} - {self.interaction_date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Update last_contacted on organization and contact
        if self.organization:
            Organization.objects.filter(pk=self.organization.pk).update(last_contacted=self.interaction_date)
        if self.contact:
            Contact.objects.filter(pk=self.contact.pk).update(last_contacted=self.interaction_date)
        super().save(*args, **kwargs)
