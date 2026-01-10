# Manual Admin User Setup (Quick Fix)

If the automated script fails, use these commands manually:

## Step 1: Create Admin User (as root)

```bash
# Create user manually (works even if admin group exists)
useradd -m -s /bin/bash admin

# Set password for admin user
passwd admin
# (Enter password when prompted)

# Add to sudo group
usermod -aG sudo admin
```

## Step 2: Copy SSH Keys

```bash
# Copy SSH keys from root to admin user
mkdir -p /home/admin/.ssh
cp /root/.ssh/authorized_keys /home/admin/.ssh/
chown -R admin:admin /home/admin/.ssh
chmod 700 /home/admin/.ssh
chmod 600 /home/admin/.ssh/authorized_keys
```

## Step 3: Verify Setup

```bash
# Check user was created
id admin

# Check sudo group
groups admin

# Check SSH keys
ls -la /home/admin/.ssh/
cat /home/admin/.ssh/authorized_keys
```

## Step 4: Exit and Test Connection

```bash
exit
ssh admin@146.190.37.164
```

## Step 5: Verify Sudo Access

Once connected as admin:
```bash
sudo whoami  # Should output: root
```

If all works, continue with deployment setup!
