# Business Plan Tracking System

A comprehensive Django application for tracking and visualizing progress against the Tawi Meridian business plan.

## Features

- **Dashboard**: Overview of key metrics, milestones, revenue, and pipeline
- **Milestones Tracking**: Track milestones by period (90-day, 6-month, 12-month, etc.) with tasks
- **Financial Dashboard**: Track revenue, expenses, and targets with visual charts
- **Sales Pipeline**: Manage opportunities with weighted pipeline values
- **Certifications Tracking**: Track certification applications and status

## Models

### MilestonePeriod
Represents time periods for milestones (e.g., "90-Day Plan", "Year 1")

### Milestone
Major milestones with status, priority, target dates, and tasks

### Task
Individual tasks within milestones

### FinancialMetric
Track revenue, expenses, and targets by period (monthly, quarterly, yearly)

### Opportunity
Sales opportunities with estimated values, win probabilities, and status

### CertificationTracking
Track certification applications and status, linked to core.Certification

## Views

- `/business-plan/` - Main dashboard
- `/business-plan/milestones/` - List all milestones
- `/business-plan/milestones/<id>/` - Milestone detail with tasks
- `/business-plan/financial/` - Financial dashboard with charts
- `/business-plan/pipeline/` - Sales pipeline view
- `/business-plan/certifications/` - Certifications tracking

## Admin Interface

All models are registered in the Django admin interface. Access at `/admin/business_plan/`

## Setup

1. The app is already registered in `settings.py`
2. Run migrations:
   ```bash
   python manage.py makemigrations business_plan
   python manage.py migrate
   ```
3. Create a superuser if needed:
   ```bash
   python manage.py createsuperuser
   ```
4. Access the dashboard at `/business-plan/` (requires login)

## Usage

1. Create milestone periods in the admin
2. Add milestones to periods
3. Add tasks to milestones
4. Enter financial metrics monthly/quarterly
5. Add sales opportunities
6. Track certifications

The dashboard will automatically calculate progress percentages and visualize data with Chart.js.

## Templates

- `business_plan/base.html` - Base template with navigation
- `business_plan/dashboard.html` - Main dashboard
- `business_plan/milestones_list.html` - Milestones list
- `business_plan/milestone_detail.html` - Milestone detail
- `business_plan/financial_dashboard.html` - Financial charts
- `business_plan/pipeline.html` - Sales pipeline
- `business_plan/certifications.html` - Certifications list

## Charts

The system uses Chart.js (loaded from CDN) for visualizations:
- Revenue charts (line and bar)
- Milestone status (doughnut)
- Financial metrics (bar charts)

## Authentication

All views require login (`@login_required`). Users need to be logged in to access the business plan tracking system.
