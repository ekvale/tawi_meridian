"""
Django settings for Tawi Meridian project.

This configuration supports both development and production environments
using django-environ for environment variable management.
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
)

# Read .env file if it exists
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    
    # Third-party apps
    'rest_framework',
    'django_htmx',
    'crispy_forms',
    'crispy_bootstrap5',
    'honeypot',
    'csp',
    
    # Local apps
    'core',
    'services',
    'portfolio',
    'blog',
    'contact',
    'business_plan',
    'project_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'tawimeridian.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',  # Custom context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'tawimeridian.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='info@tawimeridian.com')
CONTACT_EMAIL = env('CONTACT_EMAIL', default='info@tawimeridian.com')

# Crispy Forms configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# CSRF settings
# IMPORTANT: In production, set CSRF_TRUSTED_ORIGINS in .env file
# Example: CSRF_TRUSTED_ORIGINS=https://tawimeridian.com,https://www.tawimeridian.com
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Security settings (enable in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Content Security Policy
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://www.googletagmanager.com", "https://unpkg.com", "https://cdn.tailwindcss.com", "https://cdn.jsdelivr.net"),
        'style-src': ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"),
        'img-src': ("'self'", "data:", "https:", "http:"),
        'font-src': ("'self'", "data:", "https://fonts.gstatic.com"),
        'connect-src': ("'self'", "https://www.google-analytics.com"),
    }
}

# Honeypot settings (spam protection)
HONEYPOT_FIELD_NAME = 'website_url'
HONEYPOT_VALUE = ''

# Rate limiting (configure per view)
RATELIMIT_ENABLE = True

# Site settings (used in context processor)
SITE_NAME = 'Tawi Meridian'
SITE_DESCRIPTION = 'Engineering Climate Solutions, Building Community Resilience'

# Google Analytics
GOOGLE_ANALYTICS_ID = env('GOOGLE_ANALYTICS_ID', default='')

# Social Media Links
SOCIAL_LINKS = {
    'linkedin': env('LINKEDIN_URL', default=''),
    'twitter': env('TWITTER_URL', default=''),
    'facebook': env('FACEBOOK_URL', default=''),
}

# Impact metrics - Mango Project Statistics
IMPACT_METRICS = {
    # The Problem
    'post_harvest_loss_percent': 45,  # 40-50% average
    'current_processing_percent': 1,  # <1% currently processed
    'kitui_waste_tonnes': 70000,  # 40,000-100,000 tonnes wasted annually (using midpoint)
    'value_lost_millions': 10.5,  # $6-15 million in lost income (using midpoint)
    
    # The Solution (per facility)
    'farmers_per_facility': 350,  # 200-500 farmers
    'waste_prevented_tonnes': 60,  # 60 tonnes per season
    'income_increase_percent': 98,  # 50-147% average (using midpoint)
    'jobs_per_facility': 8,  # 6-10 direct jobs
    
    # At Scale (10 facilities)
    'farmers_at_scale': 3500,  # 2,000-5,000 farmers
    'waste_prevented_at_scale': 600,  # 600 tonnes
    'economic_impact_millions': 1.5,  # $1-2M county economic impact
    
    # Technology Advantages
    'throughput_increase': 250,  # 2-3x more than solar-only
    'season_extension_months': 8,  # 8-10 months vs 4 months
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# Authentication settings
LOGIN_URL = '/project-management/login/'
LOGIN_REDIRECT_URL = '/project-management/'
LOGOUT_REDIRECT_URL = '/'
