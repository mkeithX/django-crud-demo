from pathlib import Path
import os
import environ
from django.contrib.messages import constants as messages

env = environ.Env(
    DEBUG=(bool, False),
    DB_ENGINE=(str, "django.db.backends.postgresql"),
    ADMIN_URL=(str, "admin/"),
    STATICFILES_DIRS=(str, "STATICFILES_DIRS"),
    STATIC_BACKEND=(str, "django.contrib.staticfiles.storage.StaticFilesStorage"),
)

CORE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = environ.Path(__file__) -4

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ADMIN_URL = env("ADMIN_URL")

INSTALLED_APPS = [
    "apps.users.apps.UsersConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.postgres',
    'django.contrib.sites',
    'crispy_forms',
    'django_bootstrap5',
    'django_cleanup',
    'django_countries',    
]

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'apps_users.User'

ROOT_URLCONF = 'core.urls'

TEMPLATE_DIR = os.path.join(CORE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "index"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(CORE_DIR, "media")

STATIC_URL = "static/"
STATICFILES_DIRS = env.list("STATICFILES_DIRS")