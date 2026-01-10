"""
Admin configuration for contact app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import ContactSubmission, CapabilityDownload


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for contact submissions."""
    list_display = [
        'name',
        'email',
        'organization',
        'project_type',
        'is_read',
        'is_responded',
        'submitted_at',
        'action_buttons'
    ]
    list_filter = [
        'is_read',
        'is_responded',
        'project_type',
        'budget_range',
        'submitted_at'
    ]
    search_fields = [
        'name',
        'email',
        'organization',
        'message',
        'notes'
    ]
    list_editable = ['is_read', 'is_responded']
    readonly_fields = [
        'submitted_at',
        'read_at',
        'responded_at',
        'updated_at',
        'ip_address',
        'user_agent'
    ]
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'organization')
        }),
        ('Project Details', {
            'fields': ('project_type', 'budget_range', 'message')
        }),
        ('Status & Tracking', {
            'fields': ('is_read', 'read_at', 'is_responded', 'responded_at', 'notes')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_responded', 'mark_as_unread', 'mark_as_unresponded']
    
    def action_buttons(self, obj):
        """Display action buttons in list view."""
        buttons = []
        if not obj.is_read:
            buttons.append(
                f'<a class="button" href="{reverse("admin:contact_contactsubmission_change", args=[obj.pk])}?mark_read=1">Mark as Read</a>'
            )
        if not obj.is_responded:
            buttons.append(
                f'<a class="button" href="{reverse("admin:contact_contactsubmission_change", args=[obj.pk])}?mark_responded=1">Mark as Responded</a>'
            )
        return format_html(' '.join(buttons)) if buttons else '-'
    action_buttons.short_description = 'Quick Actions'
    
    def mark_as_read(self, request, queryset):
        """Mark selected submissions as read."""
        for submission in queryset:
            submission.mark_as_read()
        self.message_user(request, f'{queryset.count()} submissions marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_responded(self, request, queryset):
        """Mark selected submissions as responded."""
        for submission in queryset:
            submission.mark_as_responded()
        self.message_user(request, f'{queryset.count()} submissions marked as responded.')
    mark_as_responded.short_description = 'Mark selected as responded'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected submissions as unread."""
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{queryset.count()} submissions marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'
    
    def mark_as_unresponded(self, request, queryset):
        """Mark selected submissions as unresponded."""
        queryset.update(is_responded=False, responded_at=None)
        self.message_user(request, f'{queryset.count()} submissions marked as unresponded.')
    mark_as_unresponded.short_description = 'Mark selected as unresponded'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related()


@admin.register(CapabilityDownload)
class CapabilityDownloadAdmin(admin.ModelAdmin):
    """Admin interface for capability downloads."""
    list_display = [
        'document_type',
        'ip_address',
        'downloaded_at',
        'referer_short'
    ]
    list_filter = [
        'document_type',
        'downloaded_at'
    ]
    search_fields = [
        'ip_address',
        'user_agent',
        'referer'
    ]
    readonly_fields = [
        'document_type',
        'ip_address',
        'user_agent',
        'referer',
        'downloaded_at'
    ]
    date_hierarchy = 'downloaded_at'
    
    fieldsets = (
        ('Download Information', {
            'fields': ('document_type', 'downloaded_at')
        }),
        ('Tracking Information', {
            'fields': ('ip_address', 'user_agent', 'referer'),
            'classes': ('collapse',)
        }),
    )
    
    def referer_short(self, obj):
        """Display truncated referer URL."""
        if obj.referer:
            return obj.referer[:50] + '...' if len(obj.referer) > 50 else obj.referer
        return '-'
    referer_short.short_description = 'Referer'
    
    def has_add_permission(self, request):
        """Prevent manual creation of download records."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of download records."""
        return False
