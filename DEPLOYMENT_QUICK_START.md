# Quick Deployment Guide - Your DigitalOcean Droplet

**Your Droplet IP**: `146.190.37.164`  
**Repository**: https://github.com/ekvale/tawi_meridian.git

## Step 1: Connect to Your Droplet (Initial Root Access)

```bash
ssh root@146.190.37.164
```

## Step 2: Create Non-Root Admin User (Security Best Practice)

**⚠️ IMPORTANT**: Create a non-root user with sudo privileges for security.

**Option A: Use the automated script (recommended)**

```bash
# Download and run the admin user creation script
curl -O https://raw.githubusercontent.com/ekvale/tawi_meridian/main/deployment/create_admin_user.sh
chmod +x create_admin_user.sh
sudo bash create_admin_user.sh
```

**Option B: Manual creation**

```bash
# Create admin user (replace 'admin' with your preferred username)
adduser admin

# Add user to sudo group
usermod -aG sudo admin

# Copy SSH keys to new user (recommended)
mkdir -p /home/admin/.ssh
cp ~/.ssh/authorized_keys /home/admin/.ssh/
chown -R admin:admin /home/admin/.ssh
chmod 700 /home/admin/.ssh
chmod 600 /home/admin/.ssh/authorized_keys

# Exit and reconnect
exit
```

Now reconnect using your new user:
```bash
ssh admin@146.190.37.164
```

Verify sudo works:
```bash
sudo whoami  # Should output: root
```

**Note**: The setup script will create a separate `tawimeridian` user for running the Django application. The admin user is for system administration.

## Step 3: Run Initial Server Setup

```bash
# Download setup script
curl -O https://raw.githubusercontent.com/ekvale/tawi_meridian/main/deployment/setup_server.sh
chmod +x setup_server.sh
sudo bash setup_server.sh
```

This script will:
- Update system packages
- Install Python, PostgreSQL, Nginx, and required tools
- Create application user (`tawimeridian`)
- Set up database
- Configure firewall
- Create necessary directories

## Step 3: Clone Repository and Configure

```bash
# Switch to application user
sudo su - tawimeridian

# Clone repository
cd ~
git clone https://github.com/ekvale/tawi_meridian.git tawimeridian

# Create production .env file
cd ~/tawimeridian
cp env.production.example .env
nano .env
```

**Update these values in .env:**

```env
DEBUG=False
SECRET_KEY=hz5y($ruu6w&^@^=n6fyzw5aw7a!o#&r*%v#dug$4+dh=*zm0b
ALLOWED_HOSTS=tawimeridian.com,www.tawimeridian.com,146.190.37.164

# Database - UPDATE THE PASSWORD!
DATABASE_URL=postgresql://tawimeridian_user:YOUR_SECURE_PASSWORD@localhost:5432/tawimeridian

# Email - Configure with SendGrid or AWS SES
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@tawimeridian.com
```

**⚠️ IMPORTANT**: Change the database password! The setup script creates a user with a default password. Update it:

```bash
# As root or with sudo
sudo -u postgres psql
ALTER USER tawimeridian_user WITH PASSWORD 'your-new-secure-password';
\q

# Then update DATABASE_URL in .env to match
```

## Step 4: Install Dependencies and Set Up Application

```bash
# Activate virtual environment
source ~/venv/bin/activate

# Install dependencies
cd ~/tawimeridian
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser

# Load initial data
python manage.py load_initial_data

# Collect static files
python manage.py collectstatic --noinput
```

## Step 5: Configure Nginx

```bash
# Copy Nginx configuration
sudo cp ~/tawimeridian/nginx/tawimeridian.conf /etc/nginx/sites-available/tawimeridian

# Update domain name in config (if you have one)
sudo nano /etc/nginx/sites-available/tawimeridian
# Replace tawimeridian.com with your actual domain, or use the IP for now

# Create symlink and remove default
sudo ln -sf /etc/nginx/sites-available/tawimeridian /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Step 6: Configure and Start Gunicorn Service

```bash
# Copy systemd service file
sudo cp ~/tawimeridian/deployment/tawimeridian.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable tawimeridian

# Start service
sudo systemctl start tawimeridian

# Check status
sudo systemctl status tawimeridian
```

## Step 7: Verify Deployment

Visit your site:
- **By IP**: http://146.190.37.164
- **By domain**: http://your-domain.com (if configured)

Test:
- [ ] Homepage loads
- [ ] Static files (CSS, images) load correctly
- [ ] Contact form works
- [ ] Admin panel accessible at `/admin/`

## Step 8: Set Up SSL Certificate (After Domain is Configured)

Once your domain points to the droplet:

```bash
sudo certbot --nginx -d tawimeridian.com -d www.tawimeridian.com
```

This will:
- Obtain SSL certificate from Let's Encrypt
- Automatically configure Nginx for HTTPS
- Set up automatic renewal

## Useful Commands

### View Logs
```bash
# Gunicorn logs
sudo journalctl -u tawimeridian -f

# Nginx access logs
sudo tail -f /var/log/nginx/tawimeridian_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/tawimeridian_error.log
```

### Restart Services
```bash
# Restart Gunicorn
sudo systemctl restart tawimeridian

# Reload Nginx (no downtime)
sudo systemctl reload nginx
```

### Update Application
```bash
cd ~/tawimeridian
git pull origin main
source ~/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart tawimeridian
```

Or use the automated deployment script:
```bash
bash deployment/deploy.sh
```

## Troubleshooting

### 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status tawimeridian

# Check Gunicorn logs
sudo journalctl -u tawimeridian -n 50

# Test Gunicorn directly
curl http://127.0.0.1:8000
```

### Static Files Not Loading
```bash
# Recollect static files
cd ~/tawimeridian
source ~/venv/bin/activate
python manage.py collectstatic --noinput --clear

# Check permissions
sudo chown -R tawimeridian:www-data ~/tawimeridian/staticfiles
```

### Permission Errors
```bash
# Fix ownership
sudo chown -R tawimeridian:www-data ~/tawimeridian
sudo chmod -R 755 ~/tawimeridian
sudo chmod -R 775 ~/tawimeridian/media
```

## Security Checklist

- [x] Server setup completed
- [ ] Database password changed
- [ ] `SECRET_KEY` set in production `.env`
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured with IP and domain
- [ ] Firewall configured (UFW)
- [ ] SSL certificate installed (after domain setup)
- [ ] Regular backups configured
- [ ] Email service configured

## Next Steps

1. Configure your domain DNS to point to `146.190.37.164`
2. Set up SSL certificate with Let's Encrypt
3. Configure email service (SendGrid or AWS SES)
4. Set up automated backups
5. Configure monitoring and alerts

## Support

- Review full documentation: `DEPLOYMENT.md`
- Check logs for errors
- Contact: ekvale@gmail.com or memoi.e.sharon@gmail.com

---

**Your site should now be live at**: http://146.190.37.164 🚀
