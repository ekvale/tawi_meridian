# Tawi Meridian Website

Professional website for Tawi Meridian LLC, a women-owned engineering and data science consulting firm serving government agencies.

## Features

- **Home Page**: Hero section, impact metrics, service pillars, featured case studies
- **About Page**: Company story, mission, founders, values, locations
- **Services**: Detailed service pages for all offerings
- **Portfolio/Case Studies**: Showcase of projects with filtering and search
- **Blog/Insights**: Thought leadership articles with RSS feed
- **Contact Form**: With spam protection (honeypot + rate limiting) and email notifications
- **Capability Statements**: Downloadable PDFs with tracking
- **Admin Dashboard**: Custom admin interface for content management
- **SEO Optimized**: Meta tags, Open Graph, sitemap, structured data
- **Responsive Design**: Mobile-first with Tailwind CSS
- **Accessibility**: WCAG 2.1 AA compliant

## Technology Stack

- **Backend**: Django 5.0+
- **Database**: PostgreSQL (SQLite for development)
- **Frontend**: Tailwind CSS, HTMX (optional)
- **Static Files**: WhiteNoise
- **Email**: SendGrid or AWS SES (configurable)
- **Media Files**: Local (development) or S3 (production)

## Requirements

- Python 3.11+
- PostgreSQL 12+ (optional for development)
- pip and virtualenv

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd tawimeridian
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # or postgresql://user:password@localhost:5432/tawimeridian
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=info@tawimeridian.com
CONTACT_EMAIL=info@tawimeridian.com
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
# or use the custom command:
python manage.py create_superuser
```

### 7. Load initial data

```bash
python manage.py load_initial_data
```

This creates:
- Service offerings
- Certifications
- Office locations

### 8. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 9. Run the development server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the site.

## Project Structure

```
tawimeridian/
├── core/               # Core app (base templates, utilities, context processors)
├── services/           # Services app (service offerings)
├── portfolio/          # Portfolio app (case studies)
├── blog/               # Blog app (insights/articles)
├── contact/            # Contact app (contact form, submissions)
├── tawimeridian/       # Project settings
├── templates/          # Base templates
├── static/             # Static files (CSS, JS, images)
├── media/              # Media files (user uploads)
├── manage.py
└── requirements.txt
```

## Apps Overview

### Core App
- Base templates (base.html, navbar, footer)
- Site settings model
- Office locations model
- Certifications model
- Context processors

### Services App
- Service model with features
- Service list and detail views
- Admin interface

### Portfolio App
- CaseStudy model
- Case study images and testimonials
- Filtering and search
- Admin interface

### Blog App
- BlogPost model
- Blog images
- RSS feed
- Categories and tags
- Admin interface

### Contact App
- ContactSubmission model
- Contact form with spam protection
- CapabilityDownload tracking
- Email notifications
- Admin interface

## Management Commands

### Create Superuser

```bash
python manage.py create_superuser
```

### Load Initial Data

```bash
python manage.py load_initial_data
```

This command creates:
- 5 service offerings
- 4 certifications (8(a), WOSB, EDWOSB, MBE)
- 2 office locations (Minneapolis, Texas)

## Admin Interface

Access the admin at `/admin/` after creating a superuser.

Features:
- Custom admin interfaces for all models
- Inline editing for related models
- Search and filtering
- List display optimizations
- Image previews
- Bulk actions

## Adding Content

### Adding a Service

1. Go to Admin → Services → Add Service
2. Fill in title, description, icon, etc.
3. Set display_order to control position
4. Add features using inline editing
5. Save and publish

### Adding a Case Study

1. Go to Admin → Portfolio → Case Studies → Add Case Study
2. Fill in project details
3. Upload hero image
4. Add additional images using inline editing
5. Add testimonials if available
6. Set featured=True to show on homepage
7. Set published=True to make visible
8. Save

### Adding a Blog Post

1. Go to Admin → Blog → Posts → Add Post
2. Fill in title, author, content
3. Upload featured image
4. Add additional images using inline editing
5. Select category and add tags
6. Set published_date for scheduling
7. Set is_published=True to make visible
8. Save

## Deployment

### Heroku

1. Install Heroku CLI
2. Create Heroku app: `heroku create tawi-meridian`
3. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
4. Set environment variables in Heroku dashboard
5. Deploy: `git push heroku main`
6. Run migrations: `heroku run python manage.py migrate`
7. Collect static: `heroku run python manage.py collectstatic --noinput`
8. Load initial data: `heroku run python manage.py load_initial_data`
9. Create superuser: `heroku run python manage.py createsuperuser`

### Railway

1. Connect GitHub repository to Railway
2. Add PostgreSQL service
3. Set environment variables in Railway dashboard
4. Deploy automatically on push
5. Run migrations and collect static via Railway CLI

### DigitalOcean App Platform

1. Create new app from GitHub repository
2. Select PostgreSQL database
3. Configure environment variables
4. Set build and run commands
5. Deploy

## Environment Variables

Required environment variables (see `.env.example`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: True/False
- `ALLOWED_HOSTS`: Comma-separated list
- `DATABASE_URL`: Database connection string
- `EMAIL_BACKEND`: Email backend
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Email settings
- `DEFAULT_FROM_EMAIL`: Default sender email
- `CONTACT_EMAIL`: Contact form recipient
- `GOOGLE_ANALYTICS_ID`: Google Analytics tracking ID (optional)
- `LINKEDIN_URL`, `TWITTER_URL`, `FACEBOOK_URL`: Social media links (optional)

## Security Features

- CSRF protection (Django default)
- SQL injection protection (Django ORM)
- XSS protection
- Honeypot field for spam prevention
- Rate limiting on contact form (5 submissions/hour per IP)
- Secure password handling
- HTTPS enforcement in production
- Content Security Policy (CSP)

## Testing

Run tests:

```bash
python manage.py test
```

Or with coverage:

```bash
pytest --cov=. --cov-report=html
```

## Performance

- WhiteNoise for static file serving
- Database query optimization (select_related, prefetch_related)
- Image lazy loading
- Compressed static files
- Caching (can be added)

## SEO Features

- Meta titles and descriptions for all pages
- Open Graph tags for social sharing
- Twitter Card tags
- XML sitemap (when implemented)
- robots.txt
- Structured data (JSON-LD) - to be implemented
- Fast page load times
- Mobile-friendly design

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

### Database errors

```bash
python manage.py migrate
```

### Email not sending

Check email backend settings in `.env`:
- For development: `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`
- For production: Use SMTP or SendGrid

### Media files not accessible

Ensure `MEDIA_URL` and `MEDIA_ROOT` are set correctly in settings.py and that media files are served in development.

## Contributing

This is a proprietary project. For questions or issues, contact the development team.

## License

Proprietary - Tawi Meridian LLC

## Deployment

This project is configured for deployment to DigitalOcean Droplets. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deployment Steps

1. **Create DigitalOcean Droplet**: Ubuntu 22.04 LTS, minimum 1GB RAM
2. **Set up GitHub repository**: Push code to GitHub
3. **Run setup script**: Follow instructions in `DEPLOYMENT.md`
4. **Configure environment**: Set up `.env` with production values
5. **Deploy**: Use `deployment/deploy.sh` script for automated deployment

### Deployment Files

- `gunicorn_config.py` - Gunicorn WSGI server configuration
- `nginx/tawimeridian.conf` - Nginx reverse proxy configuration
- `deployment/tawimeridian.service` - Systemd service file
- `deployment/setup_server.sh` - Initial server setup script
- `deployment/deploy.sh` - Automated deployment script
- `env.production.example` - Production environment variables template

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Support

For technical support or questions:
- Email: info@tawimeridian.com
- Website: https://tawimeridian.com

## Acknowledgments

- Django framework
- Tailwind CSS
- HTMX
- Heroicons
- All open-source contributors
