"""
Django settings for core project (Weekly Report Generator & Team Dashboard backend).
"""

import os
import re
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-change-me-in-production")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # local apps
    "accounts",
    "projects",
    "reports",
    "aiassistant",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

AUTH_USER_MODEL = "accounts.User"

# ---------------------------------------------------------------------------
# Database
# Uses MySQL by default, but falls back to SQLite automatically when the
# MySQL server or target database is unavailable (useful for local testing).
# ---------------------------------------------------------------------------
if config("DB_ENGINE", default="mysql") == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    import pymysql
    pymysql.install_as_MySQLdb()

    db_name: str = str(config("DB_NAME", default="weekly_reports"))
    db_user: str = str(config("DB_USER", default="root"))
    db_password: str = str(config("DB_PASSWORD", default=""))
    db_host: str = str(config("DB_HOST", default="127.0.0.1"))
    db_port: int = config("DB_PORT", default=3306, cast=int)

    try:
        import pymysql

        connection = pymysql.connect(
            host=str(db_host),
            user=str(db_user),
            password=str(db_password),
            port=int(db_port),
            database=str(db_name),
            charset="utf8mb4",
            autocommit=True,
        )

        version = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version_row = cursor.fetchone()
            if version_row:
                version = version_row[0]

        connection.close()

        version_match = re.search(r"(\d+\.\d+)(?:\.\d+)?", version or "") if version else None
        if version_match and float(version_match.group(1)) >= 10.5:
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.mysql",
                    "NAME": db_name,
                    "USER": db_user,
                    "PASSWORD": db_password,
                    "HOST": db_host,
                    "PORT": db_port,
                    "OPTIONS": {"charset": "utf8mb4"},
                }
            }
        else:
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }
    except Exception:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# REST Framework / JWT
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# ---------------------------------------------------------------------------
# CORS — allow the Next.js dev server (and configured origins) to call the API
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000,http://localhost:3001,http://127.0.0.1:3001",
    cast=Csv(),
)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
