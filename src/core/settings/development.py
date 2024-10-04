from .base import *

SECRET_KEY = env("SECRET_KEY")

DEBUG = "DEBUG"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS_IN_DEV")

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASS"),
        "ATOMIC_REQUESTS": True,
        "CONN_HEALTH_CHECKS": True
    }
}

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST = env("EMAIL_HOST")