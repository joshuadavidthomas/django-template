from __future__ import annotations

import multiprocessing
import socket
from pathlib import Path

import django_stubs_ext
import sentry_sdk
from django_flyio.db import get_db_config
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .core.sentry import sentry_traces_sampler

# 0. Setup

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = Env()
env.read_env(Path(BASE_DIR.parent, ".env").as_posix())

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# We should strive to only have two possible runtime scenarios: either `DEBUG`
# is True or it is False. `DEBUG` should be only true in development, and
# False when deployed, whether or not it's a production environment.
DEBUG = env.bool("DEBUG", default=False)

# `STAGING` is here to allow us to tweak things like urls, smtp servers, etc.
# between staging and production environments, **NOT** for anything that `DEBUG`
# would be used for.
STAGING = env.bool("STAGING", default=False)

# 1. Django Core Settings
# https://docs.djangoproject.com/en/4.0/ref/settings/

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"] if DEBUG else ["localhost"])

ASGI_APPLICATION = "django_project.asgi.application"

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

DATABASES = get_db_config()

DATABASE_ROUTERS = ["django_flyio.routers.FlyDBReplicaRouter"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = [
    # First Party
    "django_project.core",
    "django_project.django_project",
    "django_project.users",
    # Third Party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "anymail",
    "django_extensions",
    "django_htmx",
    "django_q",
    "django_vite",
    "django_watchfiles",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "simple_history",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]
if DEBUG:
    INSTALLED_APPS = [
        "debug_toolbar",
        "whitenoise.runserver_nostatic",
    ] + INSTALLED_APPS

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/topics/http/middleware/
# https://docs.djangoproject.com/en/dev/ref/middleware/#middleware-ordering
MIDDLEWARE = [
    # should be first
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # order doesn't matter
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_flyio.middleware.FlyResponseMiddleware",
    # should be last
    "django.middleware.cache.FetchFromCacheMiddleware",
]
if DEBUG:
    MIDDLEWARE.remove("django.middleware.cache.UpdateCacheMiddleware")
    MIDDLEWARE.remove("django.middleware.cache.FetchFromCacheMiddleware")

    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

ROOT_URLCONF = "django_project.urls"

SECRET_KEY = env(
    "SECRET_KEY",
    default="eZPdvuAaLrVY8Kj3DG2QNqJaJc4fPp6iDgYneKN3fkNmqgkcNnoNLkFe3NCRXqW",
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

SECURE_HSTS_PRELOAD = not DEBUG

# 10 minutes to start with, will increase as HSTS is tested
SECURE_HSTS_SECONDS = 0 if DEBUG else 600

# https://noumenal.es/notes/til/django/csrf-trusted-origins/
# https://fly.io/docs/reference/runtime-environment/#x-forwarded-proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = not DEBUG

SITE_ID = 1

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true
DEFAULT_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CACHED_LOADERS = [("django.template.loaders.cached.Loader", DEFAULT_LOADERS)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            Path(BASE_DIR, "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
            "loaders": DEFAULT_LOADERS if DEBUG else CACHED_LOADERS,
        },
    },
]

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "django_project.wsgi.application"

# 2. Django Contrib Settings

# django.contrib.auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


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

AUTH_USER_MODEL = "users.User"

# django.contrib.staticfiles
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static" / "dist",
    BASE_DIR / "static" / "public",
]

# 3. Third Party Settings

# django-anymail
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN", default=""),
}

# django-q2
Q_CLUSTER = {
    "name": "ORM",
    "workers": multiprocessing.cpu_count() * 2 + 1,
    "timeout": 90,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
}

# django-vite
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "static" / "dist"

DJANGO_VITE_DEV_MODE = DEBUG

DJANGO_VITE_DEV_SERVER_PORT = 5173

# sentry
if not DEBUG or env.bool("ENABLE_SENTRY", default=False):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=None),
        environment=env("SENTRY_ENV", default=None),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(event_level=None, level=None),
        ],
        traces_sampler=sentry_traces_sampler,
        send_default_pii=True,
    )

# 4. Project Settings
