"""
Business Plan Tracking Models

Models for tracking progress against the business plan including:
- Milestones and goals
- Tasks and activities
- Financial metrics (revenue, expenses, targets)
- Sales pipeline (opportunities, proposals)
- Certifications tracking
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class MilestonePeriod(models.Model):
    """
    Represents different time periods for milestones (90-day, 6-month, 12-month, etc.)
    """
    name = models.CharField(max_length=100, unique=True, help_text='e.g., "90-Day Plan", "Year 1"')
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Milestone Period'
        verbose_name_plural = 'Milestone Periods'
        ordering = ['display_order', 'start_date']
    
    def __str__(self):
        return self.name
    
    @property
    def progress_percentage(self):
        """Calculate completion percentage for this period"""
        total_milestones = self.milestones.count()
        if total_milestones == 0:
            return 0
        completed = self.milestones.filter(status='completed').count()
        return int((completed / total_milestones) * 100)


class Milestone(models.Model):
    """
    Major milestones from the business plan
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('at_risk', 'At Risk'),
        ('blocked', 'Blocked'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    period = models.ForeignKey(MilestonePeriod, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    target_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='milestones')
    notes = models.TextField(blank=True, help_text='Additional notes or updates')
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['period', 'display_order', 'target_date']
    
    def __str__(self):
        return f'{self.period.name}: {self.title}'
    
    def get_absolute_url(self):
        return reverse('business_plan:milestone_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        """Check if milestone is past target date and not completed"""
        if self.status == 'completed':
            return False
        return timezone.now().date() > self.target_date
    
    @property
    def progress_percentage(self):
        """Calculate progress based on completed tasks"""
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0 if self.status == 'not_started' else 50 if self.status == 'in_progress' else 100
        completed = self.tasks.filter(status='completed').count()
        return int((completed / total_tasks) * 100)


class Task(models.Model):
    """
    Individual tasks within milestones
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['milestone', 'display_order', 'due_date']
    
    def __str__(self):
        return f'{self.milestone.title}: {self.title}'


class FinancialMetric(models.Model):
    """
    Financial metrics tracking (revenue, expenses, targets)
    """
    METRIC_TYPE_CHOICES = [
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
        ('profit', 'Profit'),
        ('margin', 'Margin (%)'),
    ]
    
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPE_CHOICES)
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateField(help_text='Start of the period (e.g., first day of month)')
    target_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Target value for this period'
    )
    actual_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Actual value achieved'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Financial Metric'
        verbose_name_plural = 'Financial Metrics'
        ordering = ['-period_start', 'metric_type']
        unique_together = ['metric_type', 'period_type', 'period_start']
    
    def __str__(self):
        return f'{self.get_metric_type_display()} - {self.period_start.strftime("%Y-%m")}'
    
    @property
    def variance(self):
        """Calculate variance from target"""
        if self.target_value is None or self.actual_value is None:
            return None
        return self.actual_value - self.target_value
    
    @property
    def variance_percentage(self):
        """Calculate variance as percentage"""
        if self.target_value is None or self.actual_value is None or self.target_value == 0:
            return None
        return ((self.actual_value - self.target_value) / self.target_value) * 100
    
    @property
    def progress_percentage(self):
        """Calculate progress toward target"""
        if self.target_value is None or self.target_value == 0:
            return None
        if self.actual_value is None:
            return 0
        percentage = (self.actual_value / self.target_value) * 100
        return min(percentage, 100)  # Cap at 100%


class Opportunity(models.Model):
    """
    Sales opportunities in the pipeline
    """
    STATUS_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal Submitted'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    agency = models.CharField(max_length=200, blank=True, help_text='Government agency or organization')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospecting')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    estimated_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Estimated contract value'
    )
    win_probability = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Win probability percentage (0-100)'
    )
    expected_close_date = models.DateField(null=True, blank=True)
    proposal_submitted_date = models.DateField(null=True, blank=True)
    award_date = models.DateField(null=True, blank=True)
    actual_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Actual contract value if won'
    )
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
        ordering = ['-priority', '-expected_close_date', 'status']
    
    def __str__(self):
        return self.title
    
    @property
    def weighted_value(self):
        """Calculate weighted pipeline value (value * probability)"""
        if self.estimated_value is None:
            return None
        return self.estimated_value * (self.win_probability / 100)


class CertificationTracking(models.Model):
    """
    Extended tracking for certifications with status and timeline
    Extends the core.Certification model with business plan tracking
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('application_prep', 'Application Preparation'),
        ('application_submitted', 'Application Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    certification = models.OneToOneField(
        'core.Certification', 
        on_delete=models.CASCADE, 
        related_name='tracking',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, help_text='Certification name if not linked to core model')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    target_submission_date = models.DateField(null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    expected_approval_date = models.DateField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='certifications_tracking')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Certification Tracking'
        verbose_name_plural = 'Certifications Tracking'
        ordering = ['-priority', 'status', 'name']
    
    def __str__(self):
        cert_name = self.certification.name if self.certification else self.name
        return f'{cert_name} ({self.get_status_display()})'
    
    @property
    def is_overdue(self):
        """Check if submission is overdue"""
        if self.status in ['submitted', 'under_review', 'approved', 'active']:
            return False
        if self.target_submission_date is None:
            return False
        return timezone.now().date() > self.target_submission_date
