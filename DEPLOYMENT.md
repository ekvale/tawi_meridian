# Deployment Guide: Tawi Meridian to DigitalOcean Droplet

This guide walks you through deploying the Tawi Meridian website to a DigitalOcean Droplet.

## Prerequisites

- A DigitalOcean account
- A domain name (optional but recommended)
- GitHub account with repository access
- SSH key pair for server access

## Step 1: Create DigitalOcean Droplet

1. Log in to DigitalOcean
2. Click "Create" → "Droplets"
3. Choose configuration:
   - **Image**: Ubuntu 22.04 (LTS) x64
   - **Plan**: Basic, Regular Intel (at least 1GB RAM, 1 vCPU recommended)
   - **Region**: Choose closest to your users
   - **Authentication**: SSH keys (recommended) or root password
   - **Hostname**: tawimeridian (or your preferred name)
4. Click "Create Droplet"

## Step 2: Initial Server Setup

### Connect to your droplet

```bash
ssh root@146.190.37.164
```

### Run the setup script

```bash
# Download and run the setup script
curl -O https://raw.githubusercontent.com/ekvale/tawi_meridian/main/deployment/setup_server.sh
chmod +x setup_server.sh
sudo bash setup_server.sh
```

**Note**: Update the script with your actual database password before running, or change it later.

Alternatively, follow the manual setup steps in the script if you prefer.

## Step 3: Set Up GitHub Repository

### Create GitHub repository

1. Go to GitHub and create a new repository named `tawimeridian`
2. **Do NOT** initialize with README, .gitignore, or license (we already have these)

### Push local code to GitHub

On your local machine:

```bash
# Add remote
git remote add origin https://github.com/ekvale/tawi_meridian.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Tawi Meridian website"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Configure Server Environment

### Clone repository on server

```bash
# Switch to application user
sudo su - tawimeridian

# Clone repository
cd ~
git clone https://github.com/ekvale/tawi_meridian.git tawimeridian

# Or if you already have the directory from setup
cd ~/tawimeridian
git pull origin main
```

### Set up environment variables

```bash
cd ~/tawimeridian
cp .env.production.example .env
nano .env  # Edit with your production values
```

**Important variables to set:**
- `SECRET_KEY`: Generate a new secret key (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG=False`
- `ALLOWED_HOSTS`: Your domain and droplet IP (e.g., `tawimeridian.com,www.tawimeridian.com,146.190.37.164`)
- `DATABASE_URL`: PostgreSQL connection string
- `EMAIL_*`: Email service configuration
- `GOOGLE_ANALYTICS_ID`: Your Google Analytics ID

### Update database password

```bash
# Update PostgreSQL password
sudo -u postgres psql
ALTER USER tawimeridian_user WITH PASSWORD 'your-new-secure-password';
\q

# Update DATABASE_URL in .env file to match
```

## Step 5: Install Dependencies and Set Up Database

```bash
# Activate virtual environment
source ~/venv/bin/activate

# Install dependencies
cd ~/tawimeridian
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py load_initial_data

# Collect static files
python manage.py collectstatic --noinput
```

## Step 6: Configure Nginx

```bash
# Copy Nginx configuration
sudo cp ~/tawimeridian/nginx/tawimeridian.conf /etc/nginx/sites-available/tawimeridian

# Update the paths in the config if needed
sudo nano /etc/nginx/sites-available/tawimeridian

# Create symlink
sudo ln -sf /etc/nginx/sites-available/tawimeridian /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

**Update domain name**: Edit `/etc/nginx/sites-available/tawimeridian` and replace `tawimeridian.com` with your actual domain.

## Step 7: Configure Gunicorn Service

```bash
# Copy systemd service file
sudo cp ~/tawimeridian/deployment/tawimeridian.service /etc/systemd/system/

# Update paths in service file if needed
sudo nano /etc/systemd/system/tawimeridian.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable tawimeridian

# Start service
sudo systemctl start tawimeridian

# Check status
sudo systemctl status tawimeridian
```

## Step 8: Configure Domain and SSL (Optional but Recommended)

### Point domain to droplet

1. Go to your domain registrar
2. Create an A record pointing to your droplet IP (146.190.37.164):
   - Type: A
   - Name: @ (or blank)
   - Value: 146.190.37.164
   - TTL: 3600
3. Create another A record for www:
   - Type: A
   - Name: www
   - Value: 146.190.37.164
   - TTL: 3600

Wait for DNS propagation (can take up to 48 hours, usually much faster).

### Set up SSL with Let's Encrypt

```bash
# Install Certbot (if not already installed)
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d tawimeridian.com -d www.tawimeridian.com

# Follow the prompts
# Certbot will automatically configure Nginx for HTTPS

# Test auto-renewal
sudo certbot renew --dry-run
```

After SSL is set up, update your Nginx configuration to use the HTTPS server block and redirect HTTP to HTTPS.

## Step 9: Verify Deployment

1. Visit `http://146.190.37.164` or `https://your-domain.com`
2. Check that all pages load correctly
3. Test the contact form
4. Verify static files are loading (CSS, images)
5. Check admin panel: `https://your-domain.com/admin/`

## Step 10: Set Up Automated Deployment

Update the `deploy.sh` script with your repository URL, then:

```bash
# Make script executable
chmod +x ~/tawimeridian/deployment/deploy.sh

# Run deployment
cd ~/tawimeridian
bash deployment/deploy.sh
```

You can set up a cron job or GitHub Actions to automatically deploy on push to main branch.

## Ongoing Maintenance

### View logs

```bash
# Gunicorn logs
sudo journalctl -u tawimeridian -f

# Nginx access logs
sudo tail -f /var/log/nginx/tawimeridian_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/tawimeridian_error.log

# Application logs
tail -f /var/log/tawimeridian/error.log
```

### Restart services

```bash
# Restart Gunicorn
sudo systemctl restart tawimeridian

# Reload Nginx (no downtime)
sudo systemctl reload nginx

# Restart Nginx (full restart)
sudo systemctl restart nginx
```

### Update application

```bash
# SSH into server
ssh tawimeridian@146.190.37.164

# Run deployment script
cd ~/tawimeridian
bash deployment/deploy.sh

# Or manually:
git pull origin main
source ~/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart tawimeridian
```

### Backup database

```bash
# Create backup
sudo -u postgres pg_dump tawimeridian > ~/backups/tawimeridian_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
sudo -u postgres psql tawimeridian < ~/backups/tawimeridian_backup.sql
```

### Monitor server resources

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check running processes
ps aux | grep gunicorn
```

## Troubleshooting

### Service won't start

```bash
# Check service status
sudo systemctl status tawimeridian

# Check logs
sudo journalctl -u tawimeridian -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### Static files not loading

```bash
# Recollect static files
source ~/venv/bin/activate
cd ~/tawimeridian
python manage.py collectstatic --noinput --clear

# Check permissions
ls -la ~/tawimeridian/staticfiles/
sudo chown -R tawimeridian:www-data ~/tawimeridian/staticfiles
```

### Database connection errors

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -U tawimeridian_user -d tawimeridian

# Check .env file has correct DATABASE_URL
cat ~/tawimeridian/.env | grep DATABASE_URL
```

### 502 Bad Gateway

- Check Gunicorn is running: `sudo systemctl status tawimeridian`
- Check Gunicorn logs: `sudo journalctl -u tawimeridian -n 50`
- Verify Nginx can reach Gunicorn: `curl http://127.0.0.1:8000`

### Permission errors

```bash
# Fix ownership
sudo chown -R tawimeridian:www-data ~/tawimeridian
sudo chmod -R 755 ~/tawimeridian
sudo chmod -R 775 ~/tawimeridian/media
```

## Security Checklist

- [ ] Changed default database password
- [ ] Set `DEBUG=False` in production
- [ ] Generated new `SECRET_KEY`
- [ ] Configured firewall (UFW)
- [ ] Set up SSL/HTTPS
- [ ] Enabled security headers in Nginx
- [ ] Restricted SSH access (optional: disable password authentication)
- [ ] Set up regular backups
- [ ] Installed fail2ban (optional but recommended)
- [ ] Configured log rotation
- [ ] Set up monitoring/alerts

## Additional Resources

- [DigitalOcean Django Deployment Guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## Support

For issues or questions, contact the development team or refer to the project README.
