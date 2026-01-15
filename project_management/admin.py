"""
Admin configuration for Project Management app
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Organization, Contact, ContactInteraction, OrganizationType, ContactCategory


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    ordering = ['display_order', 'name']


@admin.register(ContactCategory)
class ContactCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'display_order']
    ordering = ['display_order', 'name']


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1
    fields = ['first_name', 'last_name', 'title', 'email', 'phone', 'is_primary', 'is_active']
    show_change_link = True


class ContactInteractionInline(admin.TabularInline):
    model = ContactInteraction
    extra = 0
    fields = ['interaction_type', 'subject', 'interaction_date', 'created_by']
    readonly_fields = ['created_by', 'created_at']
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'category', 'priority', 'status', 'location', 'contact_count_display', 'assigned_to', 'last_contacted']
    list_filter = ['type', 'category', 'priority', 'status', 'assigned_to']
    search_fields = ['name', 'description', 'location', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'last_contacted', 'created_by']
    inlines = [ContactInline, ContactInteractionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type', 'category', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone', 'address', 'location')
        }),
        ('Details', {
            'fields': ('key_notes', 'contact_strategy', 'tags')
        }),
        ('Status & Assignment', {
            'fields': ('priority', 'status', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at', 'last_contacted')
        }),
    )
    
    def contact_count_display(self, obj):
        count = obj.contact_count
        url = reverse('admin:project_management_contact_changelist') + f'?organization__id__exact={obj.id}'
        return format_html('<a href="{}">{} contacts</a>', url, count)
    contact_count_display.short_description = 'Contacts'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'organization', 'title', 'role', 'email', 'phone', 'is_primary', 'is_active', 'last_contacted']
    list_filter = ['organization', 'role', 'is_primary', 'is_active', 'organization__type', 'organization__category']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'title', 'organization__name']
    readonly_fields = ['created_at', 'updated_at', 'last_contacted', 'created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'title', 'role', 'organization', 'is_primary')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'mobile', 'office_location')
        }),
        ('Notes', {
            'fields': ('notes', 'key_info')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at', 'last_contacted')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
    get_full_name.admin_order_field = 'last_name'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactInteraction)
class ContactInteractionAdmin(admin.ModelAdmin):
    list_display = ['interaction_type', 'organization', 'contact', 'subject', 'interaction_date', 'next_action', 'created_by']
    list_filter = ['interaction_type', 'interaction_date', 'organization', 'created_by']
    search_fields = ['subject', 'notes', 'organization__name', 'contact__first_name', 'contact__last_name']
    readonly_fields = ['created_by', 'created_at']
    date_hierarchy = 'interaction_date'
    
    fieldsets = (
        ('Interaction Details', {
            'fields': ('organization', 'contact', 'interaction_type', 'subject', 'interaction_date', 'notes')
        }),
        ('Follow-up', {
            'fields': ('next_action', 'next_action_date')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
