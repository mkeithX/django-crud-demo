from .base import *

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = "DEBUG"

# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS_IN_DEV")

ALLOWED_HOSTS = [
    os.getenv("ALLOWED_HOSTS_IN_DEV")
]

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "ATOMIC_REQUESTS": True,
        "CONN_HEALTH_CHECKS": True
    }
}

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")