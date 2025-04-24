#!/bin/bash
# Build script for Vercel deployment

echo "Starting build process..."

# Make script executable (this is important for local testing)
chmod +x build_files.sh

echo "Installing Python dependencies..."
# Use Python 3 explicitly with requirements for Vercel
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-vercel.txt

echo "Collecting static files..."
# Use Python 3 explicitly
python3 manage.py collectstatic --noinput

echo "Build completed successfully!"