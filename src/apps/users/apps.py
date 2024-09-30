from django.apps import AppConfig


class UsersConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    label = 'apps_users'

    verbose_name = 'Accounts'
    verbose_name_plural = verbose_name

    def ready(self):
        import apps.users.signals
