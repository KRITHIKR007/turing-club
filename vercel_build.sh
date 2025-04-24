#!/bin/bash

# This is a simplified build script specifically for Vercel

echo "Installing dependencies..."
pip install -r requirements-vercel.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput