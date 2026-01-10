# Quick Start Guide: Tawi Meridian Website

This guide provides a quick overview of getting the Tawi Meridian website up and running.

## For Local Development

1. **Clone and set up**
   ```bash
   git clone <repository-url>
   cd tawimeridian
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Initialize database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_initial_data
   python manage.py collectstatic --noinput
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

Visit http://localhost:8000

## For Production Deployment (DigitalOcean)

1. **Follow GitHub setup**: See [GITHUB_SETUP.md](GITHUB_SETUP.md)
2. **Create DigitalOcean Droplet**: Ubuntu 22.04, minimum 1GB RAM
3. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)

### Quick Deployment Commands

```bash
# On server - initial setup
sudo bash deployment/setup_server.sh

# Configure environment
cd ~/tawimeridian
cp env.production.example .env
nano .env  # Edit with production values

# Install and configure
source ~/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py load_initial_data
python manage.py collectstatic --noinput

# Start services
sudo systemctl start tawimeridian
sudo systemctl reload nginx

# For updates
bash deployment/deploy.sh
```

## Important Files

- **Settings**: `tawimeridian/settings.py`
- **Environment**: `.env` (create from `.env.example` or `env.production.example`)
- **Deployment**: See `deployment/` directory
- **Nginx Config**: `nginx/tawimeridian.conf`
- **Gunicorn Config**: `gunicorn_config.py`

## Key Environment Variables

- `SECRET_KEY`: Django secret key (generate new for production)
- `DEBUG`: `False` in production, `True` in development
- `ALLOWED_HOSTS`: Comma-separated list of domains/IPs
- `DATABASE_URL`: PostgreSQL connection string
- `EMAIL_*`: Email service configuration

## Contact Form Emails

Contact form submissions are automatically sent to:
- ekvale@gmail.com
- memoi.e.sharon@gmail.com

## Need Help?

- **Local Development**: See [README.md](README.md)
- **GitHub Setup**: See [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
