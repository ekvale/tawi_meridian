"""
Views for Project Management app
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_http_methods


@login_required
def dashboard(request):
    """Main project management dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'project_management/dashboard.html', context)


@login_required
def projects_list(request):
    """List all projects"""
    context = {}
    return render(request, 'project_management/projects_list.html', context)


@login_required
def opportunities_list(request):
    """List all opportunities"""
    context = {}
    return render(request, 'project_management/opportunities_list.html', context)
