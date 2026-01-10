"""
Admin configuration for portfolio app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import CaseStudy, CaseStudyImage, CaseStudyTestimonial


class CaseStudyImageInline(admin.TabularInline):
    """Inline admin for case study images."""
    model = CaseStudyImage
    extra = 1
    fields = ['image', 'caption', 'alt_text', 'display_order', 'is_primary']
    ordering = ['display_order']


class CaseStudyTestimonialInline(admin.TabularInline):
    """Inline admin for case study testimonials."""
    model = CaseStudyTestimonial
    extra = 0
    fields = ['quote', 'author_name', 'author_title', 'author_organization', 'display_order']
    ordering = ['display_order']


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    """Admin interface for case studies."""
    list_display = [
        'title',
        'client_type',
        'client_name',
        'service',
        'featured',
        'published',
        'published_date',
        'created_at'
    ]
    list_filter = [
        'client_type',
        'featured',
        'published',
        'published_date',
        'service',
        'created_at'
    ]
    search_fields = [
        'title',
        'client_name',
        'challenge',
        'solution',
        'results',
        'technologies'
    ]
    list_editable = ['featured', 'published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'preview_image']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'client_type', 'client_name', 'service')
        }),
        ('Project Content', {
            'fields': ('challenge', 'solution', 'results', 'technologies', 'impact_metrics')
        }),
        ('Visual Elements', {
            'fields': ('hero_image', 'preview_image')
        }),
        ('Status & Display', {
            'fields': ('featured', 'published', 'published_date')
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
    
    inlines = [CaseStudyImageInline, CaseStudyTestimonialInline]
    
    def preview_image(self, obj):
        """Display image preview in admin."""
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.hero_image.url
            )
        return 'No image'
    preview_image.short_description = 'Image Preview'


@admin.register(CaseStudyImage)
class CaseStudyImageAdmin(admin.ModelAdmin):
    """Admin interface for case study images."""
    list_display = ['case_study', 'caption', 'display_order', 'is_primary', 'image_preview']
    list_filter = ['case_study', 'is_primary']
    search_fields = ['case_study__title', 'caption', 'alt_text']
    list_editable = ['display_order', 'is_primary']
    raw_id_fields = ['case_study']
    
    def image_preview(self, obj):
        """Display image preview in admin list."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 75px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(CaseStudyTestimonial)
class CaseStudyTestimonialAdmin(admin.ModelAdmin):
    """Admin interface for case study testimonials."""
    list_display = ['case_study', 'author_name', 'author_organization', 'display_order', 'quote_short']
    list_filter = ['case_study']
    search_fields = ['case_study__title', 'author_name', 'quote']
    list_editable = ['display_order']
    raw_id_fields = ['case_study']
    
    def quote_short(self, obj):
        """Display truncated quote in list view."""
        return obj.quote[:100] + '...' if len(obj.quote) > 100 else obj.quote
    quote_short.short_description = 'Quote'
