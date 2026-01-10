"""
Admin configuration for blog app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import BlogPost, BlogImage


class BlogImageInline(admin.TabularInline):
    """Inline admin for blog images."""
    model = BlogImage
    extra = 1
    fields = ['image', 'caption', 'alt_text', 'display_order']
    ordering = ['display_order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for blog posts."""
    list_display = [
        'title',
        'author',
        'category',
        'is_featured',
        'is_published',
        'published_date',
        'view_count',
        'created_at'
    ]
    list_filter = [
        'category',
        'is_featured',
        'is_published',
        'published_date',
        'created_at',
        'author'
    ]
    search_fields = [
        'title',
        'excerpt',
        'content',
        'tags',
        'author'
    ]
    list_editable = ['is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'preview_image']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Author Information', {
            'fields': ('author', 'author_bio', 'author_email')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Visual Elements', {
            'fields': ('featured_image', 'preview_image')
        }),
        ('Status & Display', {
            'fields': ('is_featured', 'is_published', 'published_date')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Engagement', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [BlogImageInline]
    
    def preview_image(self, obj):
        """Display image preview in admin."""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.featured_image.url
            )
        return 'No image'
    preview_image.short_description = 'Image Preview'


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    """Admin interface for blog images."""
    list_display = ['blog_post', 'caption', 'display_order', 'image_preview']
    list_filter = ['blog_post']
    search_fields = ['blog_post__title', 'caption', 'alt_text']
    list_editable = ['display_order']
    raw_id_fields = ['blog_post']
    
    def image_preview(self, obj):
        """Display image preview in admin list."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 75px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Preview'
