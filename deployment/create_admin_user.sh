#!/bin/bash
# Script to create a non-root admin user on DigitalOcean Droplet
# Run this FIRST as root before deploying the application
# Usage: sudo bash create_admin_user.sh

set -e  # Exit on error

echo "🔐 Creating non-root admin user..."

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

# Get username from user
read -p "Enter username for admin user (default: admin): " USERNAME
USERNAME=${USERNAME:-admin}

# Check if user already exists
if id "$USERNAME" &>/dev/null; then
    echo -e "${YELLOW}User '$USERNAME' already exists${NC}"
    read -p "Do you want to continue anyway? (y/N): " CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Create user
    echo -e "${YELLOW}Creating user '$USERNAME'...${NC}"
    adduser --disabled-password --gecos "" $USERNAME
    
    # Set password (user will be prompted)
    echo -e "${YELLOW}Setting password for $USERNAME...${NC}"
    passwd $USERNAME
    
    echo -e "${GREEN}✓ User '$USERNAME' created${NC}"
fi

# Add to sudo group
echo -e "${YELLOW}Adding '$USERNAME' to sudo group...${NC}"
usermod -aG sudo $USERNAME
echo -e "${GREEN}✓ Added to sudo group${NC}"

# Copy SSH keys (if they exist)
if [ -d "/root/.ssh" ] && [ -f "/root/.ssh/authorized_keys" ]; then
    echo -e "${YELLOW}Copying SSH keys...${NC}"
    mkdir -p /home/$USERNAME/.ssh
    cp /root/.ssh/authorized_keys /home/$USERNAME/.ssh/
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh
    chmod 700 /home/$USERNAME/.ssh
    chmod 600 /home/$USERNAME/.ssh/authorized_keys
    echo -e "${GREEN}✓ SSH keys copied${NC}"
fi

# Disable root login (optional - uncomment if you want)
# echo -e "${YELLOW}Disabling root SSH login...${NC}"
# sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
# sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
# systemctl restart sshd
# echo -e "${GREEN}✓ Root SSH login disabled (you can re-enable if needed)${NC}"

echo ""
echo -e "${GREEN}✅ Admin user '$USERNAME' created successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Exit this session: exit"
echo "2. Connect with new user: ssh $USERNAME@146.190.37.164"
echo "3. Verify sudo access: sudo whoami (should output 'root')"
echo "4. Continue with deployment setup"
echo ""
echo -e "${YELLOW}Note:${NC} The setup script will create a separate 'tawimeridian' user"
echo "for running the Django application. This admin user is for system management."
