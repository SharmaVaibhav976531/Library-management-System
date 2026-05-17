#!/usr/bin/env bash
# Create Django superuser if it doesn't already exist
# This script is idempotent and safe to run multiple times

set -o errexit

echo "Checking if superuser exists..."

# Use Django ORM to check if superuser exists and create if needed
python manage.py shell << END
from apps.accounts.models import CustomUser
import os

username = os.getenv('DJANGO_ADMIN_USERNAME', 'admin')
email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@admin.com')
password = os.getenv('DJANGO_ADMIN_PASSWORD', 'Admin@1234')

# Check if superuser already exists
if not CustomUser.objects.filter(username=username).exists():
    CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"✓ Superuser '{username}' created successfully")
else:
    print(f"✓ Superuser '{username}' already exists")
END
