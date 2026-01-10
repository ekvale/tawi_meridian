"""
Admin configuration for services app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Service, ServiceFeature, ServiceCaseStudy


class ServiceFeatureInline(admin.TabularInline):
    """Inline admin for service features."""
    model = ServiceFeature
    extra = 1
    fields = ['title', 'description', 'icon', 'display_order']
    ordering = ['display_order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for services."""
    list_display = [
        'title',
        'slug',
        'icon',
        'is_active',
        'is_featured',
        'display_order',
        'created_at',
        'updated_at'
    ]
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'short_description', 'full_description']
    list_editable = ['is_active', 'is_featured', 'display_order']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'preview_image']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'full_description')
        }),
        ('Visual Elements', {
            'fields': ('icon', 'featured_image', 'preview_image')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active', 'is_featured')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ServiceFeatureInline]
    
    def preview_image(self, obj):
        """Display image preview in admin."""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.featured_image.url
            )
        return 'No image'
    preview_image.short_description = 'Image Preview'


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    """Admin interface for service features."""
    list_display = ['title', 'service', 'icon', 'display_order']
    list_filter = ['service']
    search_fields = ['title', 'description', 'service__title']
    list_editable = ['display_order']
    raw_id_fields = ['service']


@admin.register(ServiceCaseStudy)
class ServiceCaseStudyAdmin(admin.ModelAdmin):
    """Admin interface for service-case study relationships."""
    list_display = ['service', 'case_study_id', 'display_order']
    list_filter = ['service']
    search_fields = ['service__title']
    list_editable = ['display_order']
    raw_id_fields = ['service']
