"""
Django settings for hello project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
debug = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
DEBUG = debug

if debug:
    load_dotenv(os.path.expanduser("~/.ecfr/.env"))

ALLOWED_HOSTS = []
if debug:
    ALLOWED_HOSTS.append("localhost")
else:
    ALLOWED_HOSTS.extend(
        [
            os.getenv("RAILWAY_DOMAIN", ""),
            ".railway.app",
        ]
    )

INSTALLED_APPS = [
    # builtin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # dependencies
    "corsheaders",
    "django_extensions",
    "rest_framework",
    # ecfr
    "regulations",
]

MIDDLEWARE = [
    # builtin
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ecfr
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "ecfr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecfr.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# https://supabase.com/dashboard/project/vcvcjszyjpprefmherxt/settings/database?showConnect=true
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": os.getenv("SUPABASE_USER"),
        "PASSWORD": os.getenv("SUPABASE_PASSWORD"),
        "HOST": os.getenv("SUPABASE_HOST"),
        "PORT": os.getenv("SUPABASE_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = []
if debug:
    CORS_ALLOWED_ORIGINS.append("http://localhost:3000")
else:
    CORS_ALLOWED_ORIGINS.append(os.getenv("VERCEL_DOMAIN"))
