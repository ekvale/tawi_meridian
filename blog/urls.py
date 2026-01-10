"""
URL configuration for blog app.
"""

from django.urls import path
from . import views
from .feeds import LatestBlogPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('feed/', LatestBlogPostsFeed(), name='blog_feed'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
]
