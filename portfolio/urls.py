"""
URL configuration for portfolio app.
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.CaseStudyListView.as_view(), name='case_study_list'),
    path('<slug:slug>/', views.CaseStudyDetailView.as_view(), name='case_study_detail'),
]
