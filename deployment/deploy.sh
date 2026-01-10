#!/bin/bash
# Deployment script for Tawi Meridian on DigitalOcean Droplet
# Run this script after initial server setup

set -e  # Exit on error

echo "🚀 Starting Tawi Meridian deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/tawimeridian/tawimeridian"
VENV_DIR="/home/tawimeridian/venv"
REPO_URL="https://github.com/ekvale/tawi_meridian.git"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Please do not run as root. Use a non-root user with sudo privileges.${NC}"
   exit 1
fi

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Creating project directory...${NC}"
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Pull latest code from GitHub
echo -e "${YELLOW}Pulling latest code from GitHub...${NC}"
if [ -d ".git" ]; then
    git pull origin main
else
    git clone "$REPO_URL" .
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Install/update dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

# Clear cache (if using caching)
# python manage.py clear_cache

# Restart Gunicorn service
echo -e "${YELLOW}Restarting Gunicorn service...${NC}"
sudo systemctl restart tawimeridian

# Check service status
if sudo systemctl is-active --quiet tawimeridian; then
    echo -e "${GREEN}✓ Gunicorn service is running${NC}"
else
    echo -e "${RED}✗ Gunicorn service failed to start. Check logs: sudo journalctl -u tawimeridian${NC}"
    exit 1
fi

# Reload Nginx
echo -e "${YELLOW}Reloading Nginx...${NC}"
sudo systemctl reload nginx

# Check Nginx status
if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx failed to reload. Check logs: sudo tail -f /var/log/nginx/error.log${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${GREEN}Your site should be live at http://$(hostname -I | awk '{print $1}')${NC}"
