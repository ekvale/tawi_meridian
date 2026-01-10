"""
Views for contact app.

This module contains views for the contact form and capability statement downloads.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from .forms import ContactForm, send_contact_notification
from .models import ContactSubmission, CapabilityDownload


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["GET", "POST"])
@csrf_protect
@never_cache
@ratelimit(key='ip', rate='5/h', method='POST')
def contact(request):
    """
    Contact form view.
    
    Handles both GET (display form) and POST (submit form) requests.
    Includes rate limiting (5 submissions per hour per IP) and spam protection.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Save submission
            submission = form.save(commit=False)
            
            # Add metadata for tracking
            submission.ip_address = get_client_ip(request)
            submission.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            submission.save()
            
            # Send email notification
            try:
                send_contact_notification(submission)
            except Exception as e:
                # Log error but don't fail the submission
                import logging
                logger = logging.getLogger('contact')
                logger.error(f'Failed to send notification email: {e}')
                messages.warning(
                    request,
                    'Your message was received, but we encountered an issue sending the confirmation email. '
                    'Please contact us directly if needed.'
                )
            
            # Success message
            messages.success(
                request,
                'Thank you for contacting us! We have received your message and will respond within 2-3 business days.'
            )
            
            # Redirect to prevent duplicate submissions
            return redirect('contact:contact_success')
    
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us',
        'meta_description': (
            'Get in touch with Tawi Meridian for engineering, data science, '
            'and consulting services. We\'d love to discuss your project.'
        ),
    }
    
    return render(request, 'contact/contact.html', context)


def contact_success(request):
    """Contact form success page."""
    context = {
        'page_title': 'Message Received',
        'meta_description': 'Thank you for contacting Tawi Meridian.',
    }
    return render(request, 'contact/success.html', context)


def capability_download(request, doc_type='general'):
    """
    Handle capability statement downloads.
    
    Tracks downloads for analytics and serves the appropriate PDF.
    
    Args:
        doc_type: Type of capability statement ('general', 'federal', 'international')
    """
    # Validate document type
    valid_types = ['general', 'federal', 'international']
    if doc_type not in valid_types:
        raise Http404('Invalid document type')
    
    # Track download
    try:
        CapabilityDownload.objects.create(
            document_type=doc_type,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            referer=request.META.get('HTTP_REFERER', '')[:200]
        )
    except Exception as e:
        # Log error but don't fail the download
        import logging
        logger = logging.getLogger('contact')
        logger.error(f'Failed to track capability download: {e}')
    
    # Determine file path
    # In production, this would likely be stored in S3 or similar
    file_path = settings.BASE_DIR / 'static' / 'capabilities' / f'{doc_type}_capability_statement.pdf'
    
    # Check if file exists
    if not file_path.exists():
        # In production, this could fetch from S3
        raise Http404('Capability statement not found')
    
    # Serve file
    try:
        return FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf',
            filename=f'tawi_meridian_{doc_type}_capability_statement.pdf',
            as_attachment=True
        )
    except FileNotFoundError:
        raise Http404('Capability statement not found')
