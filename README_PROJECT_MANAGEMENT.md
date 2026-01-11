# Project Management System

A Django-based project management application for Tawi Meridian LLC to manage business operations, projects, proposals, and client relationships.

## Current Status

**Foundation Phase** - Basic structure and authentication implemented.

### What's Implemented

1. ✅ **Authentication System**
   - Login/logout functionality
   - Protected views with `@login_required`
   - Login redirects to project management dashboard

2. ✅ **Basic App Structure**
   - Project Management app created
   - URL routing configured
   - Base templates created
   - Navigation structure in place

3. ✅ **Navigation Integration**
   - Login link in main navbar (shows "Login" if not authenticated, "Dashboard" if authenticated)
   - Logout functionality
   - Links to project management dashboard

### What's Coming Next

The full system will include:

1. **Opportunity & Proposal Management**
   - Track opportunities from identification to award
   - Proposal section tracking
   - Bid/no-bid decision tools
   - Win/loss analysis

2. **Project Management**
   - Project tracking
   - Task management (Kanban, list, Gantt views)
   - Deliverables tracking
   - Team assignments
   - Project health status

3. **Time Tracking**
   - Time entry interface
   - Timesheet submission and approval
   - Timer widget
   - Utilization reporting

4. **Client Relationship Management (CRM)**
   - Client organizations
   - Contact management
   - Communication history
   - Relationship tracking

5. **Financial Tracking**
   - Budgets and expenses
   - Invoice management
   - Profitability analysis
   - Financial reporting

6. **Document Management**
   - Centralized repository
   - Version control
   - Document organization

7. **Reporting & Analytics**
   - Business intelligence dashboards
   - Project reports
   - Financial reports
   - Performance metrics

## Usage

### Accessing the System

1. **Login**: Visit `/project-management/login/` or click "Login" in the navbar
2. **Dashboard**: After login, you'll be redirected to `/project-management/`
3. **Logout**: Click "Logout" in the navbar

### Authentication

- Uses Django's built-in authentication system
- Requires a user account (create via Django admin or management command)
- All project management pages require login (`@login_required`)

### Current Pages

- `/project-management/` - Dashboard (placeholder)
- `/project-management/projects/` - Projects list (placeholder)
- `/project-management/opportunities/` - Opportunities list (placeholder)
- `/project-management/login/` - Login page
- `/project-management/logout/` - Logout (redirects to home)

## Next Steps

To build out the full system, follow the detailed specifications in the requirements document. The foundation is in place:

1. Create models for each app (opportunities, projects, time_tracking, clients, financials, etc.)
2. Implement views and templates
3. Add forms for data entry
4. Build reporting and analytics
5. Add real-time features (optional - Django Channels)

## Technical Stack

- Django 5.0+
- Django Authentication (built-in)
- Tailwind CSS for UI
- PostgreSQL database (configured)
- Django REST Framework (for API - future)

## Development Notes

- All project management URLs are prefixed with `/project-management/`
- Authentication settings configured in `settings.py`:
  - `LOGIN_URL = '/project-management/login/'`
  - `LOGIN_REDIRECT_URL = '/project-management/'`
  - `LOGOUT_REDIRECT_URL = '/'`
