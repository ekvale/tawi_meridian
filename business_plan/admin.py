"""
Admin interface for Business Plan Tracking
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    MilestonePeriod, Milestone, Task,
    FinancialMetric, Opportunity, CertificationTracking
)


@admin.register(MilestonePeriod)
class MilestonePeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'progress_display', 'display_order']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name', 'description']
    ordering = ['display_order', 'start_date']
    
    def progress_display(self, obj):
        progress = obj.progress_percentage
        color = 'green' if progress >= 80 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            progress
        )
    progress_display.short_description = 'Progress'


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'period', 'status', 'priority', 'target_date', 'is_overdue_display', 'progress_display']
    list_filter = ['status', 'priority', 'period', 'target_date']
    search_fields = ['title', 'description', 'notes']
    date_hierarchy = 'target_date'
    ordering = ['period', 'display_order', 'target_date']
    filter_horizontal = []
    raw_id_fields = ['assigned_to']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('period', 'title', 'description', 'priority')
        }),
        ('Status', {
            'fields': ('status', 'target_date', 'completed_date', 'assigned_to')
        }),
        ('Additional Information', {
            'fields': ('notes', 'display_order')
        }),
    )
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠ Overdue</span>')
        return 'On Time'
    is_overdue_display.short_description = 'Status'
    
    def progress_display(self, obj):
        progress = obj.progress_percentage
        color = 'green' if progress >= 80 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            progress
        )
    progress_display.short_description = 'Progress'


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ['title', 'status', 'due_date', 'assigned_to', 'display_order']
    ordering = ['display_order', 'due_date']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone', 'status', 'due_date', 'assigned_to']
    list_filter = ['status', 'milestone', 'due_date']
    search_fields = ['title', 'description']
    raw_id_fields = ['milestone', 'assigned_to']
    ordering = ['milestone', 'display_order', 'due_date']


@admin.register(FinancialMetric)
class FinancialMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'period_type', 'period_start', 'target_value', 'actual_value', 'variance_display', 'progress_display']
    list_filter = ['metric_type', 'period_type', 'period_start']
    search_fields = ['notes']
    date_hierarchy = 'period_start'
    ordering = ['-period_start', 'metric_type']
    
    fieldsets = (
        ('Period', {
            'fields': ('metric_type', 'period_type', 'period_start')
        }),
        ('Values', {
            'fields': ('target_value', 'actual_value', 'notes')
        }),
    )
    
    def variance_display(self, obj):
        variance = obj.variance
        if variance is None:
            return '-'
        color = 'green' if variance >= 0 else 'red'
        sign = '+' if variance >= 0 else ''
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{:,.2f}</span>',
            color,
            sign,
            float(variance)
        )
    variance_display.short_description = 'Variance'
    
    def progress_display(self, obj):
        progress = obj.progress_percentage
        if progress is None:
            return '-'
        color = 'green' if progress >= 90 else 'orange' if progress >= 70 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            int(progress)
        )
    progress_display.short_description = 'Progress'


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'agency', 'status', 'priority', 'estimated_value', 'win_probability', 'expected_close_date']
    list_filter = ['status', 'priority', 'agency', 'expected_close_date']
    search_fields = ['title', 'description', 'client_name', 'agency', 'notes']
    date_hierarchy = 'expected_close_date'
    ordering = ['-priority', '-expected_close_date', 'status']
    raw_id_fields = ['assigned_to']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'client_name', 'agency', 'priority', 'assigned_to')
        }),
        ('Status & Timeline', {
            'fields': ('status', 'expected_close_date', 'proposal_submitted_date', 'award_date')
        }),
        ('Financial', {
            'fields': ('estimated_value', 'actual_value', 'win_probability', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('assigned_to')


@admin.register(CertificationTracking)
class CertificationTrackingAdmin(admin.ModelAdmin):
    list_display = ['name_display', 'status', 'priority', 'target_submission_date', 'submission_date', 'approval_date', 'is_overdue_display']
    list_filter = ['status', 'priority', 'target_submission_date', 'approval_date']
    search_fields = ['certification__name', 'name', 'notes']
    date_hierarchy = 'target_submission_date'
    ordering = ['-priority', 'status', 'name']
    raw_id_fields = ['certification', 'assigned_to']
    
    fieldsets = (
        ('Certification', {
            'fields': ('certification', 'name', 'priority', 'assigned_to')
        }),
        ('Status & Timeline', {
            'fields': ('status', 'target_submission_date', 'submission_date', 'expected_approval_date', 'approval_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def name_display(self, obj):
        return str(obj)
    name_display.short_description = 'Certification'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠ Overdue</span>')
        return 'On Time'
    is_overdue_display.short_description = 'Status'
