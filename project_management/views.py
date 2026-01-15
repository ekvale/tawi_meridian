"""
Views for Project Management app
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count, Max
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from .models import Organization, Contact, ContactInteraction, OrganizationType, ContactCategory


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('project_management:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('project_management:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'project_management/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('project_management:login')


@login_required
def dashboard(request):
    """Project Management Dashboard"""
    # Statistics
    total_organizations = Organization.objects.count()
    total_contacts = Contact.objects.count()
    active_organizations = Organization.objects.filter(status='active').count()
    
    # Recent interactions
    recent_interactions = ContactInteraction.objects.select_related(
        'organization', 'contact', 'created_by'
    ).order_by('-interaction_date')[:10]
    
    # Organizations by priority
    organizations_by_priority = Organization.objects.values('priority').annotate(
        count=Count('id')
    ).order_by('-priority')
    
    # Upcoming follow-ups
    today = timezone.now().date()
    next_month = today + timedelta(days=30)
    upcoming_follow_ups = ContactInteraction.objects.filter(
        next_action_date__gte=today,
        next_action_date__lte=next_month
    ).exclude(next_action='').select_related('organization', 'contact').order_by('next_action_date')[:10]
    
    # Recent organizations
    recent_organizations = Organization.objects.select_related(
        'type', 'category', 'assigned_to'
    ).order_by('-created_at')[:10]
    
    context = {
        'total_organizations': total_organizations,
        'total_contacts': total_contacts,
        'active_organizations': active_organizations,
        'recent_interactions': recent_interactions,
        'organizations_by_priority': organizations_by_priority,
        'upcoming_follow_ups': upcoming_follow_ups,
        'recent_organizations': recent_organizations,
    }
    
    return render(request, 'project_management/dashboard.html', context)


@login_required
def organizations_list(request):
    """List all organizations with filtering"""
    organizations = Organization.objects.select_related('type', 'category', 'assigned_to').annotate(
        contact_count=Count('contacts')
    ).all()
    
    # Filters
    type_filter = request.GET.get('type')
    if type_filter:
        organizations = organizations.filter(type_id=type_filter)
    
    category_filter = request.GET.get('category')
    if category_filter:
        organizations = organizations.filter(category_id=category_filter)
    
    priority_filter = request.GET.get('priority')
    if priority_filter:
        organizations = organizations.filter(priority=priority_filter)
    
    status_filter = request.GET.get('status')
    if status_filter:
        organizations = organizations.filter(status=status_filter)
    
    assigned_filter = request.GET.get('assigned')
    if assigned_filter:
        organizations = organizations.filter(assigned_to_id=assigned_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        organizations = organizations.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(organizations.order_by('-priority', 'name'), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    organization_types = OrganizationType.objects.all().order_by('display_order', 'name')
    contact_categories = ContactCategory.objects.all().order_by('display_order', 'name')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assigned_users = User.objects.filter(assigned_organizations__isnull=False).distinct().order_by('first_name', 'last_name', 'username')
    
    context = {
        'page_obj': page_obj,
        'organization_types': organization_types,
        'contact_categories': contact_categories,
        'assigned_users': assigned_users,
        'filters': {
            'type': type_filter,
            'category': category_filter,
            'priority': priority_filter,
            'status': status_filter,
            'assigned': assigned_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'project_management/organizations_list.html', context)


@login_required
def organization_detail(request, pk):
    """Detail view for an organization"""
    organization = get_object_or_404(
        Organization.objects.select_related('type', 'category', 'assigned_to', 'created_by'),
        pk=pk
    )
    
    contacts = organization.contacts.all().order_by('is_primary', 'last_name', 'first_name')
    interactions = organization.interactions.select_related('contact', 'created_by').order_by('-interaction_date')[:20]
    
    context = {
        'organization': organization,
        'contacts': contacts,
        'interactions': interactions,
    }
    
    return render(request, 'project_management/organization_detail.html', context)


@login_required
def contacts_list(request):
    """List all contacts with filtering"""
    contacts = Contact.objects.select_related('organization', 'organization__type', 'created_by').all()
    
    # Filters
    organization_filter = request.GET.get('organization')
    if organization_filter:
        contacts = contacts.filter(organization_id=organization_filter)
    
    role_filter = request.GET.get('role')
    if role_filter:
        contacts = contacts.filter(role=role_filter)
    
    is_primary_filter = request.GET.get('is_primary')
    if is_primary_filter == 'true':
        contacts = contacts.filter(is_primary=True)
    elif is_primary_filter == 'false':
        contacts = contacts.filter(is_primary=False)
    
    is_active_filter = request.GET.get('is_active')
    if is_active_filter == 'true':
        contacts = contacts.filter(is_active=True)
    elif is_active_filter == 'false':
        contacts = contacts.filter(is_active=False)
    
    search_query = request.GET.get('search')
    if search_query:
        contacts = contacts.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(organization__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(contacts.order_by('organization', 'last_name', 'first_name'), 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    organizations = Organization.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'organizations': organizations,
        'filters': {
            'organization': organization_filter,
            'role': role_filter,
            'is_primary': is_primary_filter,
            'is_active': is_active_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'project_management/contacts_list.html', context)


@login_required
def contact_detail(request, pk):
    """Detail view for a contact"""
    contact = get_object_or_404(
        Contact.objects.select_related('organization', 'created_by'),
        pk=pk
    )
    
    interactions = ContactInteraction.objects.filter(
        Q(contact=contact) | Q(organization=contact.organization)
    ).select_related('organization', 'created_by').order_by('-interaction_date')[:20]
    
    context = {
        'contact': contact,
        'interactions': interactions,
    }
    
    return render(request, 'project_management/contact_detail.html', context)


@login_required
def opportunities_list(request):
    """List opportunities (placeholder for now)"""
    # TODO: Implement opportunities model and logic
    return render(request, 'project_management/opportunities_list.html', {
        'message': 'Opportunities management coming soon'
    })


@login_required
def projects_list(request):
    """List projects (placeholder for now)"""
    # TODO: Implement projects model and logic
    return render(request, 'project_management/projects_list.html', {
        'message': 'Projects management coming soon'
    })
