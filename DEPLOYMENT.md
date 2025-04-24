# TTC Portfolio - Deployment Checklist

## Pre-Deployment Preparation

- [x] Set up settings structure (development/production/vercel)
- [x] Configure secure settings for production
- [x] Create requirements.txt
- [x] Set up Procfile for Gunicorn
- [x] Configure .gitignore
- [x] Set up Vercel-specific config (vercel.json and build_files.sh)

## Deployment Steps

1. **Environment Variables Setup**
   - Create a `.env` file based on the `.env.example` template
   - Generate a secure Django secret key:
     ```python
     python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
     ```
   - Set `DJANGO_ENV=production` in your production environment

2. **Database Configuration**
   - Set up PostgreSQL database
   - Configure database credentials in `.env`

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Ensure your web server is configured to serve from `staticfiles` directory

4. **SSL/HTTPS Configuration**
   - Obtain SSL certificate (e.g., Let's Encrypt)
   - Configure web server for HTTPS

5. **Server Setup**
   - Install required packages: `pip install -r requirements.txt`
   - Configure Gunicorn to run with the Procfile
   - Set up a process manager (e.g., systemd, supervisor)

## Post-Deployment Checklist

- [ ] Verify that DEBUG is set to False
- [ ] Ensure all static files are being served correctly
- [ ] Check that HTTPS is working properly
- [ ] Test all forms and functionality
- [ ] Monitor the application logs for any errors

## Platform-Specific Instructions

### Vercel Deployment
The project is now configured to be deployed on Vercel with minimal setup:

1. **Connect your GitHub repository to Vercel**:
   - Go to https://vercel.com/new
   - Select your repository
   - Choose the "Python" framework preset

2. **Set environment variables in Vercel**:
   - `DJANGO_SECRET_KEY`: Your secret Django key
   - `DEBUG`: Set to 'False' for production
   - `DATABASE_URL`: If using an external database (optional)

3. **Deploy**:
   - Click "Deploy" and your application should be live
   - Vercel will use our vercel.json configuration and build_files.sh script

4. **Database considerations for Vercel**:
   - Vercel's filesystem is read-only (except for /tmp)
   - SQLite is configured in /tmp for simple deployments
   - For production, connect to a database service like:
     - Vercel Postgres (via Vercel integration)
     - Supabase
     - Railway
     - PlanetScale
     - ElephantSQL

5. **Media files on Vercel**:
   - Media files won't persist on Vercel due to the serverless architecture
   - For user-uploaded content, use a service like:
     - AWS S3
     - Cloudinary
     - Uploadcare

### Heroku Deployment
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create a Heroku app
heroku create ttcportfolio

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Push to Heroku
git push heroku main

# Set environment variables
heroku config:set DJANGO_ENV=production
heroku config:set DJANGO_SECRET_KEY=your_secret_key_here
heroku config:set ALLOWED_HOSTS=yourapp.herokuapp.com

# Run migrations
heroku run python manage.py migrate
```

### Traditional VPS/Dedicated Server
1. Set up Nginx/Apache as reverse proxy to Gunicorn
2. Configure a process manager to keep Gunicorn running
3. Sample Nginx configuration:
```nginx
server {
    listen 80;
    server_name yourwebsite.com www.yourwebsite.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/ttcportfolio/staticfiles;
    }
    
    location /media/ {
        root /path/to/ttcportfolio/media;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
    }
}