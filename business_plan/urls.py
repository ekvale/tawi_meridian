"""
URL configuration for business_plan app
"""

from django.urls import path
from . import views

app_name = 'business_plan'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('milestones/', views.milestones_list, name='milestones_list'),
    path('milestones/<int:pk>/', views.milestone_detail, name='milestone_detail'),
    path('financial/', views.financial_dashboard, name='financial_dashboard'),
    path('pipeline/', views.pipeline_view, name='pipeline'),
    path('certifications/', views.certifications_view, name='certifications'),
]
