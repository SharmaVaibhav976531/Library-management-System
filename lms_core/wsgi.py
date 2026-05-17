# lms_core/wsgi.py
"""
WSGI config for lms_core project.
"""
import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_core.settings")

# WhiteNoise wrapper for static files (must wrap Django app)
from whitenoise import WhiteNoise

application = get_wsgi_application()
application = WhiteNoise(application, root="staticfiles", index_file=True)