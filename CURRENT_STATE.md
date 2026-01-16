# Tawi Meridian - Current Application State

**Last Updated:** January 2026  
**Purpose:** Reference document for understanding the current state of the Tawi Meridian Django application

---

## Project Overview

Tawi Meridian LLC is a government contracting and consulting business with a focus on:
- Engineering & Energy Systems
- Data Science & Analytics
- Software Development
- International Development (specifically Solar Hybrid Mango Dehydration Project in Kenya)

The application is a Django-based website with multiple apps for managing business operations, content, and project tracking.

---

## Technology Stack

- **Framework:** Django 5.0+
- **Database:** PostgreSQL (production), SQLite (development)
- **Web Server:** Gunicorn + Nginx
- **Static Files:** WhiteNoise
- **Environment Management:** django-environ
- **Deployment:** DigitalOcean Ubuntu server
- **Version Control:** Git (GitHub)

---

## Installed Apps

### Core Apps (Built-in)
- `django.contrib.admin`
- `django.contrib.auth`
- `django.contrib.contenttypes`
- `django.contrib.sessions`
- `django.contrib.messages`
- `django.contrib.staticfiles`
- `django.contrib.sitemaps`
- `django.contrib.humanize`

### Third-Party Apps
- `rest_framework` - Django REST Framework
- `django_htmx` - HTMX integration
- `crispy_forms` & `crispy_bootstrap5` - Form styling
- `honeypot` - Spam protection
- `csp` - Content Security Policy middleware

### Custom Apps
1. **`core`** - Core functionality, site settings, office locations, certifications
2. **`services`** - Service offerings display
3. **`portfolio`** - Case studies/portfolio items
4. **`blog`** - Blog posts and insights
5. **`contact`** - Contact form and submissions
6. **`business_plan`** - Business plan tracking with milestones, tasks, financials
7. **`project_management`** - Comprehensive project management and contact management system

---

## Key Features by App

### Core App
- **Models:**
  - `SiteSetting` - Site-wide configurable settings
  - `OfficeLocation` - Office locations with addresses
  - `Certification` - Company certifications
- **Context Processor:** `site_settings` - Makes site settings available in all templates
- **Management Commands:**
  - `create_superuser` - Interactive superuser creation
  - `load_initial_data` - Loads initial services, certifications, office locations

### Services App
- **Models:**
  - `Service` - Service offerings with features, icons, display order
- **Views:** List and detail views for services
- **Features:** Featured services, service categories

### Portfolio App
- **Models:**
  - `CaseStudy` - Portfolio case studies with images and testimonials
- **Views:** List and detail views with filtering
- **Features:** Image galleries, testimonials, project filtering

### Blog App
- **Models:**
  - `BlogPost` - Blog posts with categories, tags, images
- **Views:** List and detail views
- **Features:** RSS feed, categories, tags, featured posts

### Contact App
- **Models:**
  - `ContactSubmission` - Contact form submissions
- **Forms:** `ContactForm` with honeypot spam protection
- **Features:**
  - Email notifications on form submission
  - Email backend: SendGrid SMTP (port 2525)
  - Test email management command: `python manage.py test_email --to email@example.com`
- **Email Configuration:**
  - Uses environment variables from `.env` file
  - SendGrid domain authentication configured for `tawimeridian.com`
  - Default from: `noreply@tawimeridian.com` (when domain verified)
  - Currently using `ekvale@gmail.com` for testing

### Business Plan App
- **Purpose:** Track business plan milestones, tasks, financial metrics, opportunities, and certifications
- **Models:**
  - `MilestonePeriod` - Time periods (90-Day, 6-Month, Year 1)
  - `Milestone` - Business plan milestones with status, priority, progress
  - `Task` - Tasks associated with milestones
  - `FinancialMetric` - Monthly financial tracking (revenue, expenses, etc.)
  - `Opportunity` - Sales pipeline opportunities
  - `CertificationTracking` - Certification application tracking
- **Views:**
  - Dashboard with KPIs, Gantt chart, completion percentages
  - Milestones list and detail
  - Financial dashboard with charts
  - Sales pipeline view
  - Certifications tracking
- **Features:**
  - User assignment (Sharon - CEO, Eric - CTO)
  - Filtering by user
  - Progress tracking and completion percentages
  - Gantt chart visualization (Frappe Gantt)
  - Circular progress indicators for KPIs
  - Revenue charts (Chart.js)
- **Management Command:**
  - `populate_business_plan` - Populates initial milestones and tasks from business plan outline
  - Assigns tasks based on roles (CEO vs CTO responsibilities)

### Project Management App
- **Purpose:** Comprehensive CRM and project management system
- **Models:**
  - `OrganizationType` - Types of organizations (Farmer Cooperative, Government Agency, University, etc.)
  - `ContactCategory` - Priority categories (TOP PRIORITY, STRATEGIC PARTNER, etc.)
  - `Organization` - Organizations with contact info, priority, status, categories
  - `Contact` - Individual contacts associated with organizations
  - `ContactInteraction` - Track communications (emails, calls, meetings, notes)
- **Views:**
  - Dashboard with statistics and recent activity
  - Organizations list with filtering (type, category, priority, status, search)
  - Organization detail with contacts and interactions
  - Contacts list with filtering
  - Contact detail with interaction history
  - Projects and Opportunities (placeholders for future implementation)
- **Features:**
  - Comprehensive filtering and search
  - Priority and status tracking
  - Follow-up action tracking
  - Last contacted date auto-updates
  - Primary contact designation
  - Pagination for large lists
- **Management Command:**
  - `populate_contacts` - Bulk imports organizations and contacts from comprehensive contact list
  - Includes 30+ organizations and contacts for Solar Hybrid Mango Dehydration Project
  - Creates organization types and contact categories
- **Admin Interface:**
  - Full admin interface with inline editing
  - Custom list displays and filters
  - Contact count displays

---

## Authentication & Authorization

- **Login System:** Custom login/logout views in `project_management` app
- **Login URL:** `/project-management/login/`
- **Redirect After Login:** `/project-management/` (dashboard)
- **User Roles:**
  - Staff users can access project management and business plan dashboards
  - Sharon (CEO) - Assigned to business development, certifications, proposals
  - Eric (CTO) - Assigned to technical tasks, website, database

---

## Static Files & Media

- **Static Files Location:** `/static/` (source), `/staticfiles/` (collected)
- **Static Files Storage:** WhiteNoise with compression
- **Media Files Location:** `/media/`
- **Logo:** `static/images/logo.png` (tracked in Git)
- **Important:** `/static` is tracked in Git (source files), `/staticfiles` is ignored (collected output)

---

## Content Security Policy (CSP)

Configured in `tawimeridian/settings.py`:
- Allows `data:` URIs for fonts (for inline font data)
- Allows `https://cdn.jsdelivr.net` for scripts and styles (Gantt chart library)
- Allows Google Fonts and Google Analytics
- Allows inline scripts/styles (for Tailwind CSS CDN in development)

---

## Email Configuration

- **Backend:** SendGrid SMTP
- **Host:** `smtp.sendgrid.net`
- **Port:** `2525` (alternative port, less likely to be blocked)
- **TLS:** Enabled
- **Username:** `apikey`
- **Password:** SendGrid API key (in `.env`)
- **From Email:** `noreply@tawimeridian.com` (when domain verified) or `ekvale@gmail.com` (testing)
- **Domain Authentication:** SendGrid domain authentication configured for `tawimeridian.com`
  - DNS records configured for domain verification
  - CNAME records for email authentication
  - DKIM records for email signing
  - DMARC policy configured

---

## Database Configuration

- **Production:** PostgreSQL
  - Connection string in `.env`: `DATABASE_URL=postgresql://tawimeridian_user:PASSWORD@localhost:5432/tawimeridian`
- **Development:** SQLite (`db.sqlite3`)
- **Migrations:** All apps have migrations

---

## Deployment

### Server Details
- **Provider:** DigitalOcean
- **OS:** Ubuntu (Noble)
- **User:** `tawimeridian`
- **Service:** `tawimeridian.service` (systemd)
- **Web Server:** Gunicorn (managed by systemd)
- **Reverse Proxy:** Nginx
- **Domain:** `tawimeridian.com`, `www.tawimeridian.com`

### Deployment Process
1. Push changes to GitHub: `git push origin main`
2. SSH to server: `ssh tawimeridian@SERVER_IP`
3. Pull changes: `cd ~/tawimeridian && git pull origin main`
4. Activate venv: `source ~/venv/bin/activate`
5. Run migrations: `python manage.py migrate`
6. Collect static: `python manage.py collectstatic --noinput`
7. Restart service: `sudo systemctl restart tawimeridian`
8. Check status: `sudo systemctl status tawimeridian`

### Environment Variables
- Stored in `~/tawimeridian/.env` (not in Git)
- Template: `env.production.example`
- Key variables:
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS`
  - `DATABASE_URL`
  - `EMAIL_*` settings
  - `DEFAULT_FROM_EMAIL`
  - `CONTACT_EMAIL`

---

## Recent Major Implementations

### 1. Business Plan Tracking System
- **Date:** January 2026
- **Features:**
  - Milestone and task tracking
  - Financial metrics dashboard
  - Sales pipeline management
  - Certification tracking
  - Gantt chart visualization
  - KPI completion percentages
  - User assignment and filtering

### 2. Contact Management System
- **Date:** January 2026
- **Features:**
  - Organization and contact database
  - Interaction tracking
  - Priority and category management
  - Follow-up action tracking
  - Bulk import from comprehensive contact list
  - 30+ organizations and contacts for Kenya mango project

### 3. Email System
- **Date:** January 2026
- **Features:**
  - Contact form email notifications
  - SendGrid integration
  - Domain authentication setup
  - Test email command for debugging

### 4. Dashboard Enhancements
- **Date:** January 2026
- **Features:**
  - Gantt chart for milestone timeline
  - Circular progress indicators
  - Revenue and milestone charts
  - KPI cards with completion percentages

---

## Known Issues & Notes

### Fixed Issues
1. ✅ Logo not showing - Fixed by removing `/static` from `.gitignore`
2. ✅ CSP font violation - Fixed by adding `data:` to `font-src`
3. ✅ Database connection error - Fixed by correcting PostgreSQL password in `.env`
4. ✅ Contact unique constraint error - Fixed by using conditional UniqueConstraint for emails

### Current Configuration
- **Email:** Using SendGrid with domain authentication (some DNS records may still be propagating)
- **Static Files:** Source files in `/static` are tracked in Git
- **Database:** PostgreSQL in production
- **CSP:** Configured to allow necessary external resources

---

## Management Commands

### Available Commands
1. `python manage.py create_superuser` - Create superuser interactively
2. `python manage.py load_initial_data` - Load initial services, certifications, locations
3. `python manage.py populate_business_plan` - Populate business plan milestones and tasks
4. `python manage.py populate_contacts` - Bulk import organizations and contacts
5. `python manage.py test_email --to EMAIL` - Test email configuration

---

## URL Structure

- `/` - Home page
- `/about/` - About page
- `/services/` - Services list
- `/portfolio/` - Portfolio/case studies
- `/insights/` - Blog posts
- `/contact/` - Contact form
- `/business-plan/` - Business plan dashboard (login required)
- `/project-management/` - Project management dashboard (login required)
- `/admin/` - Django admin

---

## Key Files to Reference

### Settings
- `tawimeridian/settings.py` - Main Django settings
- `.env` - Environment variables (not in Git)
- `env.production.example` - Environment variable template

### Models
- `business_plan/models.py` - Business plan models
- `project_management/models.py` - Contact management models
- `core/models.py` - Core models (settings, locations, certifications)

### Views
- `business_plan/views.py` - Business plan views with dashboard logic
- `project_management/views.py` - Contact management views

### Templates
- `templates/base.html` - Base template
- `templates/partials/navbar.html` - Navigation bar
- `templates/business_plan/dashboard.html` - Business plan dashboard
- `templates/project_management/dashboard.html` - Project management dashboard

### Management Commands
- `business_plan/management/commands/populate_business_plan.py`
- `project_management/management/commands/populate_contacts.py`
- `contact/management/commands/test_email.py`

---

## Next Steps / TODOs

### Potential Enhancements
1. Complete Projects and Opportunities models in `project_management` app
2. Add time tracking functionality
3. Add document management
4. Add team collaboration features
5. Add reporting and analytics
6. Complete SendGrid domain authentication (verify all DNS records)
7. Add export functionality for contacts and organizations
8. Add bulk actions for contacts and organizations

### Maintenance
- Regular database backups
- Monitor email delivery rates
- Update dependencies periodically
- Review and optimize database queries

---

## Contact Information

- **Company:** Tawi Meridian LLC
- **Website:** https://tawimeridian.com
- **Email:** info@tawimeridian.com
- **Support Email:** ekvale@gmail.com (for testing)

---

## Git Repository

- **Repository:** GitHub (ekvale/tawi_meridian)
- **Branch:** `main`
- **Recent Commits:**
  - Contact management system implementation
  - Business plan dashboard enhancements
  - Email system configuration
  - Static files fixes

---

**Note:** This document should be updated whenever major features are added or significant changes are made to the application architecture.
