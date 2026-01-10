#!/bin/bash
# Initial server setup script for DigitalOcean Droplet
# Run this script ONCE on a fresh Ubuntu 22.04 server
# Usage: bash setup_server.sh

set -e  # Exit on error

echo "🔧 Setting up DigitalOcean Droplet for Tawi Meridian..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# Install essential packages
echo -e "${YELLOW}Installing essential packages...${NC}"
apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    ufw \
    certbot \
    python3-certbot-nginx \
    build-essential \
    libpq-dev \
    python3-dev \
    supervisor

# Create application user
echo -e "${YELLOW}Creating application user...${NC}"
if id "tawimeridian" &>/dev/null; then
    echo -e "${BLUE}User 'tawimeridian' already exists${NC}"
else
    useradd -m -s /bin/bash tawimeridian
    usermod -aG www-data tawimeridian
    echo -e "${GREEN}✓ Created user 'tawimeridian'${NC}"
fi

# Set up directories
echo -e "${YELLOW}Setting up directories...${NC}"
mkdir -p /home/tawimeridian/tawimeridian
mkdir -p /home/tawimeridian/venv
mkdir -p /var/log/tawimeridian
mkdir -p /var/run/tawimeridian
mkdir -p /home/tawimeridian/tawimeridian/media
mkdir -p /home/tawimeridian/tawimeridian/staticfiles

# Set permissions
chown -R tawimeridian:www-data /home/tawimeridian
chown -R tawimeridian:www-data /var/log/tawimeridian
chown -R tawimeridian:www-data /var/run/tawimeridian
chmod -R 755 /home/tawimeridian
chmod -R 775 /home/tawimeridian/tawimeridian/media
chmod -R 755 /home/tawimeridian/tawimeridian/staticfiles

# Create Python virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
sudo -u tawimeridian python3.11 -m venv /home/tawimeridian/venv
sudo -u tawimeridian /home/tawimeridian/venv/bin/pip install --upgrade pip
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Set up PostgreSQL database
echo -e "${YELLOW}Setting up PostgreSQL database...${NC}"
sudo -u postgres psql << EOF
CREATE DATABASE tawimeridian;
CREATE USER tawimeridian_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
ALTER ROLE tawimeridian_user SET client_encoding TO 'utf8';
ALTER ROLE tawimeridian_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tawimeridian_user SET timezone TO 'America/Chicago';
GRANT ALL PRIVILEGES ON DATABASE tawimeridian TO tawimeridian_user;
\q
EOF
echo -e "${GREEN}✓ PostgreSQL database created${NC}"
echo -e "${YELLOW}⚠ IMPORTANT: Update the database password in .env file${NC}"

# Configure firewall
echo -e "${YELLOW}Configuring firewall...${NC}"
ufw --force enable
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw status
echo -e "${GREEN}✓ Firewall configured${NC}"

# Copy Nginx configuration
echo -e "${YELLOW}Setting up Nginx configuration...${NC}"
if [ -f "/home/tawimeridian/tawimeridian/nginx/tawimeridian.conf" ]; then
    cp /home/tawimeridian/tawimeridian/nginx/tawimeridian.conf /etc/nginx/sites-available/tawimeridian
    ln -sf /etc/nginx/sites-available/tawimeridian /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t
    systemctl enable nginx
    systemctl restart nginx
    echo -e "${GREEN}✓ Nginx configured${NC}"
else
    echo -e "${YELLOW}⚠ Nginx config file not found. You'll need to copy it manually after deploying code.${NC}"
fi

# Copy systemd service file
echo -e "${YELLOW}Setting up systemd service...${NC}"
if [ -f "/home/tawimeridian/tawimeridian/deployment/tawimeridian.service" ]; then
    cp /home/tawimeridian/tawimeridian/deployment/tawimeridian.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable tawimeridian
    echo -e "${GREEN}✓ Systemd service configured${NC}"
else
    echo -e "${YELLOW}⚠ Systemd service file not found. You'll need to copy it manually after deploying code.${NC}"
fi

echo -e "${GREEN}✅ Initial server setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Clone your GitHub repository to /home/tawimeridian/tawimeridian"
echo -e "2. Create .env file with production settings (see .env.example)"
echo -e "3. Install dependencies: cd /home/tawimeridian/tawimeridian && /home/tawimeridian/venv/bin/pip install -r requirements.txt"
echo -e "4. Run migrations: /home/tawimeridian/venv/bin/python manage.py migrate"
echo -e "5. Create superuser: /home/tawimeridian/venv/bin/python manage.py createsuperuser"
echo -e "6. Load initial data: /home/tawimeridian/venv/bin/python manage.py load_initial_data"
echo -e "7. Collect static files: /home/tawimeridian/venv/bin/python manage.py collectstatic --noinput"
echo -e "8. Copy Nginx config: sudo cp nginx/tawimeridian.conf /etc/nginx/sites-available/tawimeridian"
echo -e "9. Copy systemd service: sudo cp deployment/tawimeridian.service /etc/systemd/system/"
echo -e "10. Start services: sudo systemctl start tawimeridian && sudo systemctl reload nginx"
echo -e "11. Set up SSL certificate: sudo certbot --nginx -d tawimeridian.com -d www.tawimeridian.com"
