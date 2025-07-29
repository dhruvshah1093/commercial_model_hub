#!/bin/bash

# Set the working directory to the root of the project
PROJECT_PATH="/workspaces/${WORKSPACE_NAME}"
cd "$PROJECT_PATH" || exit

echo "Working directory set to $(pwd)"

# Install Python dependencies
pip install --upgrade pip && pip install -r requirements.txt

echo "Copying env..."
cp .env.example .env

# Check if manage.py exists
if [ ! -f manage.py ]; then
  echo "manage.py not found. Initializing Django project..."
  django-admin startproject django_project .
fi

# Check if the app already exists
if [ ! -d core ]; then
  echo "App $REPO_NAME not found. Creating Django app..."
  python manage.py startapp core
fi

# check for the database is avaiable 
python manage.py wait_for_db

# Apply database migrations 
echo "Applying database migrations..."
python manage.py migrate

# Run the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
