import os
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy, reverse

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-key-change-in-prod")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    # Custom Apps
    "apps.accounts",
    "apps.library",
    "apps.transactions",
    "apps.reports",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lms_core.urls"

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
            ],
            "environment": "lms_core.jinja.environment",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "lms_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "Password12345"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_URL = "login"

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

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CORS_ALLOW_ALL_ORIGINS = DEBUG
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


from django.urls import reverse_lazy

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
