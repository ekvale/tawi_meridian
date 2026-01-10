"""
Admin configuration for core models.
"""

from django.contrib import admin
from .models import SiteSetting, OfficeLocation, Certification


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    """Admin interface for site settings."""
    list_display = ['key', 'value_short', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['updated_at']
    
    def value_short(self, obj):
        """Display truncated value in list view."""
        return obj.value[:100] + '...' if len(obj.value) > 100 else obj.value
    value_short.short_description = 'Value'


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    """Admin interface for office locations."""
    list_display = ['name', 'city', 'state', 'phone', 'is_primary', 'display_order']
    list_filter = ['state', 'country', 'is_primary']
    search_fields = ['name', 'city', 'address_line1']
    list_editable = ['display_order', 'is_primary']
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'is_primary', 'display_order')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """Admin interface for certifications."""
    list_display = ['name', 'abbreviation', 'status', 'issue_date', 'expiry_date', 'is_featured', 'display_order']
    list_filter = ['status', 'is_featured']
    search_fields = ['name', 'abbreviation', 'certification_number']
    list_editable = ['display_order', 'is_featured']
    date_hierarchy = 'issue_date'
    fieldsets = (
        ('Certification Information', {
            'fields': ('name', 'abbreviation', 'description', 'logo')
        }),
        ('Details', {
            'fields': ('certification_number', 'status', 'issue_date', 'expiry_date')
        }),
        ('Display', {
            'fields': ('is_featured', 'display_order')
        }),
    )
