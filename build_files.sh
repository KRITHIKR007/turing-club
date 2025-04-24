#!/bin/bash
# Build script for Vercel deployment

# Make script executable
chmod +x build_files.sh

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput