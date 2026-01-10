"""
Contact forms for Tawi Meridian.

This module defines forms for contact submissions with spam protection.
"""

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import ContactSubmission, PROJECT_TYPES, BUDGET_RANGES

# Note: Honeypot protection is handled via middleware and template tag
# No need to add HoneypotField directly to form if using honeypot app's middleware


class ContactForm(forms.ModelForm):
    """
    Contact form with spam protection.
    
    Uses honeypot field for spam prevention and rate limiting
    (rate limiting handled in view).
    """
    
    class Meta:
        model = ContactSubmission
        fields = [
            'name',
            'email',
            'organization',
            'project_type',
            'message',
            'budget_range'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization (Optional)'
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us about your project or inquiry...',
                'required': True
            }),
            'budget_range': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Name *',
            'email': 'Email *',
            'organization': 'Organization',
            'project_type': 'Project Type *',
            'message': 'Message *',
            'budget_range': 'Budget Range (Optional)',
        }
        help_texts = {
            'project_type': 'What type of service are you interested in?',
            'budget_range': 'Optional: Estimated budget range for your project',
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form with custom attributes."""
        super().__init__(*args, **kwargs)
        # Make organization and budget_range optional
        self.fields['organization'].required = False
        self.fields['budget_range'].required = False
        
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
    
    def clean_message(self):
        """Validate message field."""
        message = self.cleaned_data.get('message')
        if message:
            # Check for minimum length
            if len(message.strip()) < 10:
                raise forms.ValidationError('Please provide more details about your inquiry (at least 10 characters).')
            # Check for maximum length
            if len(message) > 5000:
                raise forms.ValidationError('Message is too long (maximum 5000 characters).')
        return message
    
    def clean_email(self):
        """Validate email field."""
        email = self.cleaned_data.get('email')
        if email:
            # Basic email validation (Django's EmailField already does this)
            # Could add additional checks here (e.g., disposable email detection)
            pass
        return email


def send_contact_notification(submission):
    """
    Send email notification when contact form is submitted.
    
    Sends notification to both co-founders: Eric Kvale and Sharon Memoi.
    """
    try:
        # Contact email recipients (both co-founders)
        contact_emails = [
            'ekvale@gmail.com',
            'memoi.e.sharon@gmail.com'
        ]
        
        # Also check if there's a CONTACT_EMAIL in settings for additional recipients
        additional_email = getattr(settings, 'CONTACT_EMAIL', None)
        if additional_email and additional_email not in contact_emails:
            contact_emails.append(additional_email)
        
        # Prepare email content
        subject = f'New Contact Form Submission from {submission.name}'
        
        # Create email body (plain text)
        message = f"""
New contact form submission received:

Name: {submission.name}
Email: {submission.email}
Organization: {submission.organization or 'Not provided'}
Project Type: {submission.get_project_type_display()}
Budget Range: {submission.get_budget_range_display()}

Message:
{submission.message}

---
Submitted: {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}
IP Address: {submission.ip_address or 'Not available'}

View in admin: https://{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/admin/contact/contactsubmission/{submission.id}/
"""
        
        # Send email to all recipients
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=contact_emails,
            fail_silently=False,
        )
        
        # Optional: Send auto-reply to submitter
        send_contact_auto_reply(submission)
        
    except Exception as e:
        # Log error but don't fail the form submission
        import logging
        logger = logging.getLogger('contact')
        logger.error(f'Failed to send contact notification: {e}')


def send_contact_auto_reply(submission):
    """
    Send auto-reply email to contact form submitter.
    
    Provides acknowledgment and sets expectations for response time.
    """
    try:
        subject = 'Thank you for contacting Tawi Meridian'
        
        message = f"""
Dear {submission.name},

Thank you for reaching out to Tawi Meridian. We have received your inquiry and will review it shortly.

Your submission details:
- Project Type: {submission.get_project_type_display()}
- Submitted: {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}

Our team will respond to your inquiry within 2-3 business days. If your inquiry is urgent, please call us directly.

Best regards,
Tawi Meridian Team

---
Tawi Meridian LLC
Engineering Climate Solutions, Building Community Resilience
Website: https://tawimeridian.com
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[submission.email],
            fail_silently=False,
        )
        
    except Exception as e:
        # Log error but don't fail the form submission
        import logging
        logger = logging.getLogger('contact')
        logger.error(f'Failed to send auto-reply: {e}')
