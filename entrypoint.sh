#!/bin/sh

# Wait for PostgreSQL to start
sleep 5
echo "Django Configuration"

# Prepare initial migration
echo "Prepare init migration"
python manage.py makemigrations

# Migrate database
echo "migrate db"
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8000
