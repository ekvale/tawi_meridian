# Deployment Instructions: Business Plan Tracking System

This guide covers deploying the new business plan tracking system to your production server.

## Step 1: Push Changes to GitHub (Already Done)

✅ Changes have been committed and pushed to GitHub.

## Step 2: Deploy to Server

### Option A: Using the Deployment Script (Recommended)

SSH into your server and run:

```bash
# SSH to your server
ssh admin@YOUR_SERVER_IP

# Navigate to project directory (or use the deployment script location)
cd /home/tawimeridian/tawimeridian

# Run the deployment script
bash /home/tawimeridian/tawimeridian/deployment/deploy.sh
```

### Option B: Manual Deployment Steps

If you prefer to deploy manually or the script doesn't work, follow these steps:

#### 1. SSH to Your Server

```bash
ssh admin@YOUR_SERVER_IP
```

#### 2. Navigate to Project Directory

```bash
cd /home/tawimeridian/tawimeridian
```

#### 3. Pull Latest Code from GitHub

```bash
git pull origin main
```

#### 4. Activate Virtual Environment

```bash
source /home/tawimeridian/venv/bin/activate
```

#### 5. Install/Update Dependencies (if needed)

```bash
pip install -r requirements.txt
```

**Note**: The new business_plan app doesn't require any additional dependencies - it uses Django core functionality and Chart.js (loaded from CDN).

#### 6. Run Database Migrations

**⚠️ IMPORTANT**: This creates new database tables for the business plan tracking system.

```bash
python manage.py makemigrations business_plan
python manage.py migrate
```

#### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 8. Restart Gunicorn Service

```bash
sudo systemctl restart tawimeridian
```

#### 9. Check Service Status

```bash
sudo systemctl status tawimeridian
```

If there are any errors, check the logs:

```bash
sudo journalctl -u tawimeridian -n 50
```

#### 10. Reload Nginx (if needed)

```bash
sudo systemctl reload nginx
```

## Step 3: Verify Deployment

### Check the Application

1. **Test the Dashboard**: Visit `https://your-domain.com/business-plan/`
   - You should see the login page (if not logged in)
   - After logging in, you should see the dashboard

2. **Check Admin Interface**: Visit `https://your-domain.com/admin/business_plan/`
   - Verify all models are accessible
   - You can start adding data here

### Verify Database Tables

```bash
# On the server, check that migrations ran successfully
python manage.py showmigrations business_plan
```

You should see all migrations marked with `[X]`.

## Step 4: Initial Setup (After Deployment)

### Create Initial Data

1. **Log in to Admin**: `https://your-domain.com/admin/`

2. **Create Milestone Periods**:
   - Go to `Business Plan` → `Milestone Periods`
   - Add periods like:
     - "90-Day Plan" (Months 1-3)
     - "6-Month Plan" (Months 1-6)
     - "Year 1" (Year 2026)
     - etc.

3. **Create Milestones**:
   - Go to `Business Plan` → `Milestones`
   - Add milestones from your business plan
   - Link them to the appropriate periods

4. **Add Tasks** (optional):
   - Go to `Business Plan` → `Tasks`
   - Add tasks to milestones

5. **Add Financial Metrics** (as you have data):
   - Go to `Business Plan` → `Financial Metrics`
   - Add monthly/quarterly revenue and expense targets
   - Update actual values as they come in

6. **Add Opportunities**:
   - Go to `Business Plan` → `Opportunities`
   - Add sales opportunities to track

7. **Add Certification Tracking**:
   - Go to `Business Plan` → `Certifications Tracking`
   - Link to existing certifications from the Core app or add new ones

## Troubleshooting

### Migration Errors

If migrations fail:

```bash
# Check for errors
python manage.py migrate --verbosity 2

# If you need to reset (⚠️ WARNING: This will delete data)
# Only do this in development or if you haven't added data yet
python manage.py migrate business_plan zero
python manage.py migrate business_plan
```

### Service Won't Start

```bash
# Check logs
sudo journalctl -u tawimeridian -n 100

# Check for Python errors
python manage.py check

# Verify settings
python manage.py check --deploy
```

### Static Files Not Loading

```bash
# Re-collect static files
python manage.py collectstatic --noinput --clear

# Check static files directory permissions
sudo chown -R tawimeridian:tawimeridian /home/tawimeridian/tawimeridian/staticfiles
```

### 404 Errors on Business Plan Pages

- Verify URLs are correctly included in `tawimeridian/urls.py`
- Check that `business_plan` is in `INSTALLED_APPS` in `settings.py`
- Verify migrations have run: `python manage.py showmigrations business_plan`

### Chart.js Not Loading

- Charts use Chart.js from CDN - ensure your server has internet access
- Check browser console for errors
- Verify Content Security Policy allows the Chart.js CDN (should already be configured)

## Quick Reference

**Most common deployment command sequence:**

```bash
cd /home/tawimeridian/tawimeridian
git pull origin main
source /home/tawimeridian/venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart tawimeridian
sudo systemctl reload nginx
```

## Next Steps

After deployment is complete:

1. ✅ Verify the dashboard loads correctly
2. ✅ Test adding data in the admin interface
3. ✅ Create initial milestone periods and milestones
4. ✅ Start tracking your business plan progress!

## Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u tawimeridian -n 100`
2. Check Django checks: `python manage.py check`
3. Review the README_BUSINESS_PLAN.md for usage instructions
