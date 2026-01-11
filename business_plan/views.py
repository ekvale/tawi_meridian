"""
Views for Business Plan Tracking Dashboard
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
from datetime import datetime, timedelta
from .models import (
    MilestonePeriod, Milestone, Task,
    FinancialMetric, Opportunity, CertificationTracking
)


@login_required
def dashboard(request):
    """
    Main dashboard showing overview of business plan progress
    """
    today = timezone.now().date()
    
    # Milestones data
    active_periods = MilestonePeriod.objects.filter(end_date__gte=today).order_by('start_date')
    milestones = Milestone.objects.all()
    milestone_stats = {
        'total': milestones.count(),
        'completed': milestones.filter(status='completed').count(),
        'in_progress': milestones.filter(status='in_progress').count(),
        'overdue': sum(1 for m in milestones if m.is_overdue),
    }
    
    # Tasks data
    tasks = Task.objects.all()
    task_stats = {
        'total': tasks.count(),
        'completed': tasks.filter(status='completed').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'not_started': tasks.filter(status='not_started').count(),
    }
    
    # Financial metrics
    current_year = today.year
    current_month = today.replace(day=1)
    revenue_metrics = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__gte=current_month - timedelta(days=365)
    ).order_by('period_start')
    
    monthly_revenue = []
    for i in range(12):
        month = current_month - timedelta(days=30*i)
        metric = revenue_metrics.filter(period_start__year=month.year, period_start__month=month.month).first()
        monthly_revenue.append({
            'month': month.strftime('%Y-%m'),
            'target': float(metric.target_value) if metric and metric.target_value else 0,
            'actual': float(metric.actual_value) if metric and metric.actual_value else 0,
        })
    
    # Year-to-date revenue
    ytd_revenue = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__year=current_year,
        period_start__month__lte=today.month
    ).aggregate(total=Sum('actual_value'))['total'] or 0
    
    ytd_target = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__year=current_year,
        period_start__month__lte=today.month
    ).aggregate(total=Sum('target_value'))['total'] or 0
    
    # Sales pipeline
    opportunities = Opportunity.objects.all()
    pipeline_stats = {
        'total': opportunities.count(),
        'active': opportunities.exclude(status__in=['won', 'lost', 'cancelled']).count(),
        'won': opportunities.filter(status='won').count(),
        'lost': opportunities.filter(status='lost').count(),
    }
    
    # Weighted pipeline value
    active_opps = opportunities.exclude(status__in=['won', 'lost', 'cancelled'])
    weighted_pipeline = sum(
        float(opp.weighted_value) for opp in active_opps if opp.weighted_value
    )
    total_pipeline_value = sum(
        float(opp.estimated_value) for opp in active_opps if opp.estimated_value
    )
    
    # Certifications
    certifications = CertificationTracking.objects.all()
    cert_stats = {
        'total': certifications.count(),
        'active': certifications.filter(status='active').count(),
        'approved': certifications.filter(status='approved').count(),
        'pending': certifications.filter(status__in=['not_started', 'application_prep', 'application_submitted', 'under_review']).count(),
    }
    
    context = {
        'active_periods': active_periods,
        'milestone_stats': milestone_stats,
        'task_stats': task_stats,
        'revenue_metrics': revenue_metrics[:12],  # Last 12 months
        'monthly_revenue': mark_safe(json.dumps(monthly_revenue)),
        'ytd_revenue': float(ytd_revenue),
        'ytd_target': float(ytd_target),
        'pipeline_stats': pipeline_stats,
        'weighted_pipeline': weighted_pipeline,
        'total_pipeline_value': total_pipeline_value,
        'cert_stats': cert_stats,
        'recent_milestones': milestones.select_related('assigned_to').order_by('-updated_at')[:5],
        'upcoming_opportunities': opportunities.filter(
            expected_close_date__gte=today
        ).exclude(status__in=['won', 'lost', 'cancelled']).select_related('assigned_to').order_by('expected_close_date')[:5],
    }
    
    return render(request, 'business_plan/dashboard.html', context)


@login_required
def milestones_list(request):
    """
    List all milestones with filtering
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    periods = MilestonePeriod.objects.all().order_by('display_order', 'start_date')
    period_id = request.GET.get('period')
    
    if period_id:
        milestones = Milestone.objects.filter(period_id=period_id).select_related('assigned_to').order_by('display_order', 'target_date')
        selected_period = get_object_or_404(MilestonePeriod, pk=period_id)
    else:
        milestones = Milestone.objects.all().select_related('assigned_to').order_by('period', 'display_order', 'target_date')
        selected_period = None
    
    status_filter = request.GET.get('status')
    if status_filter:
        milestones = milestones.filter(status=status_filter)
    
    user_filter = request.GET.get('user')
    if user_filter:
        milestones = milestones.filter(assigned_to_id=user_filter)
    
    # Get all users who have milestones assigned (for filter dropdown)
    users_with_milestones = User.objects.filter(milestones__isnull=False).distinct().order_by('first_name', 'last_name', 'username')
    
    context = {
        'periods': periods,
        'milestones': milestones,
        'selected_period': selected_period,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'users': users_with_milestones,
    }
    
    return render(request, 'business_plan/milestones_list.html', context)


@login_required
def milestone_detail(request, pk):
    """
    Detail view for a milestone with tasks
    """
    milestone = get_object_or_404(Milestone.objects.select_related('assigned_to', 'period'), pk=pk)
    tasks = milestone.tasks.select_related('assigned_to').all().order_by('display_order', 'due_date')
    
    context = {
        'milestone': milestone,
        'tasks': tasks,
    }
    
    return render(request, 'business_plan/milestone_detail.html', context)


@login_required
def financial_dashboard(request):
    """
    Financial metrics dashboard
    """
    today = timezone.now().date()
    current_year = today.year
    
    # Revenue metrics
    revenue_metrics = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__year=current_year
    ).order_by('period_start')
    
    # Expense metrics
    expense_metrics = FinancialMetric.objects.filter(
        metric_type='expense',
        period_start__year=current_year
    ).order_by('period_start')
    
    # Year totals
    ytd_revenue = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__year=current_year,
        period_start__month__lte=today.month
    ).aggregate(total=Sum('actual_value'))['total'] or 0
    
    ytd_expenses = FinancialMetric.objects.filter(
        metric_type='expense',
        period_start__year=current_year,
        period_start__month__lte=today.month
    ).aggregate(total=Sum('actual_value'))['total'] or 0
    
    ytd_profit = float(ytd_revenue) - float(ytd_expenses)
    
    ytd_revenue_target = FinancialMetric.objects.filter(
        metric_type='revenue',
        period_start__year=current_year,
        period_start__month__lte=today.month
    ).aggregate(total=Sum('target_value'))['total'] or 0
    
    # Monthly data for charts
    monthly_data = []
    for month in range(1, 13):
        month_date = today.replace(month=month, day=1)
        revenue = revenue_metrics.filter(period_start__month=month).first()
        expense = expense_metrics.filter(period_start__month=month).first()
        
        monthly_data.append({
            'month': month_date.strftime('%b'),
            'revenue_target': float(revenue.target_value) if revenue and revenue.target_value else 0,
            'revenue_actual': float(revenue.actual_value) if revenue and revenue.actual_value else 0,
            'expense_target': float(expense.target_value) if expense and expense.target_value else 0,
            'expense_actual': float(expense.actual_value) if expense and expense.actual_value else 0,
        })
    
    context = {
        'revenue_metrics': revenue_metrics,
        'expense_metrics': expense_metrics,
        'ytd_revenue': float(ytd_revenue),
        'ytd_expenses': float(ytd_expenses),
        'ytd_profit': ytd_profit,
        'ytd_revenue_target': float(ytd_revenue_target),
        'monthly_data': mark_safe(json.dumps(monthly_data)),
        'current_year': current_year,
    }
    
    return render(request, 'business_plan/financial_dashboard.html', context)


@login_required
def pipeline_view(request):
    """
    Sales pipeline view
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    status_filter = request.GET.get('status')
    user_filter = request.GET.get('user')
    
    opportunities = Opportunity.objects.select_related('assigned_to').all()
    
    if status_filter:
        opportunities = opportunities.filter(status=status_filter)
    else:
        opportunities = opportunities.exclude(status__in=['won', 'lost', 'cancelled'])
    
    if user_filter:
        opportunities = opportunities.filter(assigned_to_id=user_filter)
    
    opportunities = opportunities.order_by('-priority', '-expected_close_date')
    
    # Get all users who have opportunities assigned (for filter dropdown)
    users_with_opportunities = User.objects.filter(opportunities__isnull=False).distinct().order_by('first_name', 'last_name', 'username')
    
    # Statistics
    stats = {
        'total_value': sum(float(opp.estimated_value) for opp in opportunities if opp.estimated_value),
        'weighted_value': sum(float(opp.weighted_value) for opp in opportunities if opp.weighted_value),
        'count': opportunities.count(),
    }
    
    # Group by status
    by_status = {}
    all_opps = Opportunity.objects.all()
    if user_filter:
        all_opps = all_opps.filter(assigned_to_id=user_filter)
    for opp in all_opps:
        status = opp.get_status_display()
        if status not in by_status:
            by_status[status] = {'count': 0, 'value': 0}
        by_status[status]['count'] += 1
        if opp.estimated_value:
            by_status[status]['value'] += float(opp.estimated_value)
    
    context = {
        'opportunities': opportunities,
        'stats': stats,
        'by_status': by_status,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'users': users_with_opportunities,
    }
    
    return render(request, 'business_plan/pipeline.html', context)


@login_required
def certifications_view(request):
    """
    Certifications tracking view
    """
    status_filter = request.GET.get('status')
    
    certifications = CertificationTracking.objects.all()
    
    if status_filter:
        certifications = certifications.filter(status=status_filter)
    
    certifications = certifications.order_by('-priority', 'status', 'name')
    
    context = {
        'certifications': certifications,
        'status_filter': status_filter,
    }
    
    return render(request, 'business_plan/certifications.html', context)
