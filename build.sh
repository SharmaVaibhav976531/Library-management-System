#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (WhiteNoise will serve them)
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create superuser if not exists (idempotent - safe to run multiple times)
bash create_superuser.sh

# Compile static assets (if using any JS/CSS build tools)
# npm install && npm run build  # Uncomment if you have frontend build step