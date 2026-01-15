"""
URL configuration for project_management app
"""

from django.urls import path
from . import views

app_name = 'project_management'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Organizations
    path('organizations/', views.organizations_list, name='organizations_list'),
    path('organizations/<int:pk>/', views.organization_detail, name='organization_detail'),
    
    # Contacts
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    
    # Projects and Opportunities (placeholders for now)
    path('projects/', views.projects_list, name='projects_list'),
    path('opportunities/', views.opportunities_list, name='opportunities_list'),
]
