"""
Blog models for Tawi Meridian.

This module defines the BlogPost model for insights and articles.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation


# Blog categories
CATEGORIES = [
    ('engineering', 'Engineering'),
    ('data_science', 'Data Science'),
    ('climate', 'Climate & Sustainability'),
    ('government', 'Government Contracting'),
    ('international', 'International Development'),
    ('general', 'General'),
]


class BlogPost(models.Model):
    """
    Blog post / insight article.
    
    Used to publish thought leadership, technical insights, and industry news.
    """
    # Basic Information
    title = models.CharField(max_length=200, help_text='Post title')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='URL-friendly version of title'
    )
    
    # Author & Content
    author = models.CharField(
        max_length=100,
        help_text='Author name'
    )
    author_bio = models.TextField(
        blank=True,
        help_text='Brief author biography'
    )
    author_email = models.EmailField(
        blank=True,
        help_text='Author email (optional)'
    )
    
    # Content
    excerpt = models.TextField(
        max_length=500,
        help_text='Short excerpt for listings and previews (max 500 characters)'
    )
    content = models.TextField(
        help_text='Full post content (supports markdown or HTML)'
    )
    
    # Categorization
    category = models.CharField(
        max_length=50,
        choices=CATEGORIES,
        default='general',
        help_text='Post category'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated tags (e.g., "renewable energy, climate, Kenya")'
    )
    
    # Visual Elements
    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        help_text='Featured image for post'
    )
    
    # Status & Display
    is_published = models.BooleanField(
        default=False,
        help_text='Make visible on public site'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Show prominently on homepage or blog list'
    )
    published_date = models.DateTimeField(
        help_text='Date and time to publish (used for scheduling)'
    )
    
    # SEO & Metadata
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        help_text='SEO title (defaults to title if not set)'
    )
    meta_description = models.TextField(
        max_length=300,
        blank=True,
        help_text='SEO description (defaults to excerpt if not set)'
    )
    
    # Engagement Metrics
    view_count = models.IntegerField(
        default=0,
        help_text='Number of times post has been viewed'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['slug', 'is_published']),
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['is_featured', 'is_published']),
            models.Index(fields=['published_date', 'is_published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to blog post detail page."""
        return reverse('blog:blog_post_detail', kwargs={'slug': self.slug})

    @property
    def display_title(self):
        """Return meta_title if set, otherwise title."""
        return self.meta_title or self.title

    @property
    def display_description(self):
        """Return meta_description if set, otherwise excerpt."""
        return self.meta_description or self.excerpt

    @property
    def tags_list(self):
        """Return tags as a list."""
        if self.tags:
            return [t.strip() for t in self.tags.split(',')]
        return []

    def increment_view_count(self):
        """Increment view count (for analytics)."""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class BlogImage(models.Model):
    """
    Additional images for blog posts.
    
    Allows multiple images per post for galleries or inline images.
    """
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for accessibility'
    )
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Blog Image'
        verbose_name_plural = 'Blog Images'
        ordering = ['display_order']

    def __str__(self):
        return f'{self.blog_post.title} - Image {self.display_order}'

    def save(self, *args, **kwargs):
        """Auto-generate alt text if not provided."""
        if not self.alt_text and self.caption:
            self.alt_text = self.caption
        elif not self.alt_text:
            self.alt_text = f'{self.blog_post.title} - Image {self.display_order}'
        super().save(*args, **kwargs)
