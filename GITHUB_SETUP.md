# GitHub Repository Setup Guide

This guide will help you set up the GitHub repository and push your code.

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Repository details:
   - **Repository name**: `tawimeridian`
   - **Description**: "Professional website for Tawi Meridian LLC - Engineering and data science consulting firm"
   - **Visibility**: Private (recommended) or Public
   - **Do NOT** check:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   - (We already have these files)
4. Click "Create repository"

## Step 2: Initialize Local Git Repository

If you haven't already initialized git (we did this earlier):

```bash
# Check if git is initialized
git status

# If not initialized, initialize it
git init
```

## Step 3: Add All Files to Git

```bash
# Add all files to staging
git add .

# Verify what will be committed
git status

# Make initial commit
git commit -m "Initial commit: Tawi Meridian website

- Django 5.0+ website with PostgreSQL
- Core pages: Home, About, Services, Portfolio, Blog, Contact
- Admin dashboard for content management
- SEO optimized with meta tags and sitemap
- Responsive design with Tailwind CSS
- Production-ready deployment configuration"
```

## Step 4: Add GitHub Remote

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/ekvale/tawi_meridian.git

# Verify remote was added
git remote -v
```

## Step 5: Push to GitHub

```bash
# Set main as default branch
git branch -M main

# Push to GitHub (first time)
git push -u origin main
```

You'll be prompted for your GitHub username and password/token. If you're using two-factor authentication, you'll need to use a Personal Access Token instead of your password.

### Creating a Personal Access Token (if needed)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Tawi Meridian Deployment"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)
7. Use this token as your password when pushing

## Step 6: Verify Upload

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/tawimeridian`
2. Verify all files are there
3. Check that `.env` is NOT in the repository (it should be in .gitignore)

## Step 7: Update Deployment Scripts

After pushing to GitHub, update the deployment scripts with your actual repository URL:

```bash
# Update deploy.sh
nano deployment/deploy.sh

# Change this line:
REPO_URL="https://github.com/YOUR_USERNAME/tawimeridian.git"
# To your actual repository URL

# Update DEPLOYMENT.md as well
nano DEPLOYMENT.md
# Replace all instances of YOUR_USERNAME with your actual GitHub username
```

Then commit and push these changes:

```bash
git add deployment/deploy.sh DEPLOYMENT.md
git commit -m "Update deployment scripts with repository URL"
git push
```

## Step 8: Set Up Branch Protection (Optional but Recommended)

1. Go to your repository on GitHub
2. Settings → Branches
3. Add branch protection rule for `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require conversation resolution before merging
   - ✅ Include administrators

## Future Updates

After making changes locally:

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## Working with the Deployment Server

When you set up your DigitalOcean droplet, you'll clone from GitHub:

```bash
# On the server
git clone https://github.com/YOUR_USERNAME/tawimeridian.git
```

Then for updates:

```bash
# Pull latest changes
git pull origin main

# Run deployment script
bash deployment/deploy.sh
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

1. Use Personal Access Token instead of password
2. Or set up SSH keys:
   ```bash
   # Generate SSH key (if you don't have one)
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Copy public key
   cat ~/.ssh/id_ed25519.pub
   
   # Add to GitHub: Settings → SSH and GPG keys → New SSH key
   
   # Change remote to SSH
   git remote set-url origin git@github.com:ekvale/tawi_meridian.git
   ```

### Large Files

If you have large files that shouldn't be in git:

```bash
# Remove from git (but keep local file)
git rm --cached path/to/large-file

# Add to .gitignore
echo "path/to/large-file" >> .gitignore

# Commit the change
git add .gitignore
git commit -m "Remove large file from repository"
git push
```

### Undo Last Commit (before pushing)

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Or undo commit and discard changes (CAREFUL!)
git reset --hard HEAD~1
```

## Next Steps

After setting up GitHub:

1. Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide to deploy to DigitalOcean
2. Set up CI/CD (GitHub Actions) for automated deployments (optional)
3. Configure domain name and SSL certificate
4. Set up monitoring and backups
