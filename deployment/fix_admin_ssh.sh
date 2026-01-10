#!/bin/bash
# Script to fix SSH access for admin user
# Run this as root if admin user can't SSH in
# Usage: sudo bash fix_admin_ssh.sh

set -e  # Exit on error

echo "🔧 Fixing SSH access for admin user..."

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

# Get username
read -p "Enter admin username (default: admin): " USERNAME
USERNAME=${USERNAME:-admin}

# Check if user exists
if ! id "$USERNAME" &>/dev/null; then
    echo -e "${RED}User '$USERNAME' does not exist!${NC}"
    echo -e "${YELLOW}Creating user first...${NC}"
    
    # Create user (handle case where group already exists)
    if getent group "$USERNAME" > /dev/null 2>&1; then
        # Group exists, create user without creating group
        useradd -m -s /bin/bash $USERNAME
    else
        # Create user normally
        adduser --disabled-password --gecos "" $USERNAME
    fi
    
    # Set password
    passwd $USERNAME
    
    # Add to sudo group
    usermod -aG sudo $USERNAME
    echo -e "${GREEN}✓ User '$USERNAME' created${NC}"
fi

# Copy SSH keys from root
echo -e "${YELLOW}Copying SSH keys from root to $USERNAME...${NC}"

if [ -d "/root/.ssh" ] && [ -f "/root/.ssh/authorized_keys" ]; then
    mkdir -p /home/$USERNAME/.ssh
    cp /root/.ssh/authorized_keys /home/$USERNAME/.ssh/
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh
    chmod 700 /home/$USERNAME/.ssh
    chmod 600 /home/$USERNAME/.ssh/authorized_keys
    echo -e "${GREEN}✓ SSH keys copied successfully${NC}"
else
    echo -e "${RED}No SSH keys found in /root/.ssh/authorized_keys${NC}"
    echo -e "${YELLOW}You may need to add your SSH public key manually${NC}"
    
    # Create .ssh directory anyway
    mkdir -p /home/$USERNAME/.ssh
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh
    chmod 700 /home/$USERNAME/.ssh
    
    echo -e "${BLUE}To add your SSH key manually:${NC}"
    echo "1. Copy your public key (usually ~/.ssh/id_rsa.pub on your local machine)"
    echo "2. Run: nano /home/$USERNAME/.ssh/authorized_keys"
    echo "3. Paste your public key"
    echo "4. Save and exit (Ctrl+X, Y, Enter)"
    echo "5. Run: chmod 600 /home/$USERNAME/.ssh/authorized_keys"
    echo "6. Run: chown $USERNAME:$USERNAME /home/$USERNAME/.ssh/authorized_keys"
fi

echo ""
echo -e "${GREEN}✅ SSH setup complete!${NC}"
echo -e "${BLUE}You can now try: ssh $USERNAME@146.190.37.164${NC}"
