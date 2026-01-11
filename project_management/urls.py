"""
URL configuration for project_management app
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'project_management'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='project_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects_list, name='projects_list'),
    path('opportunities/', views.opportunities_list, name='opportunities_list'),
]
