"""
URL configuration for contact app.
"""

from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('success/', views.contact_success, name='contact_success'),
    path('capabilities/<str:doc_type>/', views.capability_download, name='capability_download'),
]
