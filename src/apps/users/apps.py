from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    label = 'apps_users'

    verbose_name = 'Accounts'
    verbose_name_plural = verbose_name

    def ready(self):
        import apps.users.signals
