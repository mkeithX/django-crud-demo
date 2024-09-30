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