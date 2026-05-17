# lms_core/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy
from datetime import timedelta

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (only for local development)
load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: Keep secret key in environment variable for production
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "*+12kt-wep!d8t=n2p+s$o7l5bdru6jx7a^^(%wu&(4)hri3^&")
# DEBUG mode: True for development, False for production on Render
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
# ALLOWED_HOSTS: Include Render domain and localhost for development
_allowed_hosts_str = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [host.strip() for host in _allowed_hosts_str.split(",") if host.strip()]
# Ensure Render domain is always included in production
if not DEBUG:
    ALLOWED_HOSTS.extend([".onrender.com", "library-management-system-klgf.onrender.com"])

# Application definition
INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "whitenoise.runserver_nostatic",
    # Custom apps
    "apps.accounts",
    "apps.library",
    "apps.transactions",
    "apps.reports",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lms_core.urls"

# Template configuration (Jinja2 + Django)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.csrf",
            ],
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
            ],
            "environment": "lms_core.jinja.environment",
            "match_extension": ".jinja",
            "autoescape": True,
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csrf",
            ],
        },
    },
]

WSGI_APPLICATION = "lms_core.wsgi.application"
ASGI_APPLICATION = "lms_core.asgi.application"

# Database configuration for Render PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "lms_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "Password12345"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        # Render-specific: Use connection pooler if available
        "CONN_MAX_AGE": 600,  # Persistent connections for 10 minutes
        "OPTIONS": {
            "sslmode": "require" if not DEBUG else "disable",  # SSL only for production
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static files configuration for Render + WhiteNoise
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (user uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_URL = "login"

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Restrict in production
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]

# Security settings for production
if not DEBUG:
    # HTTPS redirect
    # SECURE_SSL_REDIRECT = False
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # Secure cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    # Browser security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# Unfold admin configuration
UNFOLD = {
    "SITE_TITLE": "Library Admin Dashboard",
    "SITE_HEADER": "Library Management Admin",
    "SHOW_HISTORY": True,
    "DARK_MODE": True,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Users & Access Control",
                "icon": "admin_panel_settings",
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:accounts_customuser_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "Library Catalog",
                "icon": "menu_book",
                "items": [
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:library_category_changelist"),
                    },
                    {
                        "title": "Books",
                        "icon": "book",
                        "link": reverse_lazy("admin:library_book_changelist"),
                    },
                ],
            },
            {
                "title": "Members",
                "icon": "badge",
                "items": [
                    {
                        "title": "Members List",
                        "icon": "people",
                        "link": reverse_lazy("admin:transactions_member_changelist"),
                    },
                ],
            },
            {
                "title": "Book Transactions",
                "icon": "swap_horiz",
                "items": [
                    {
                        "title": "Book Issues",
                        "icon": "assignment_turned_in",
                        "link": reverse_lazy("admin:transactions_bookissue_changelist"),
                    },
                    {
                        "title": "Reservations",
                        "icon": "event_available",
                        "link": reverse_lazy(
                            "admin:transactions_reservation_changelist"
                        ),
                    },
                    {
                        "title": "Fines",
                        "icon": "payments",
                        "link": reverse_lazy("admin:transactions_fine_changelist"),
                    },
                ],
            },
            {
                "title": "Notifications",
                "icon": "notifications",
                "items": [
                    {
                        "title": "Notifications Log",
                        "icon": "campaign",
                        "link": reverse_lazy(
                            "admin:transactions_notification_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}

# Logging configuration for Render
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["null"],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
