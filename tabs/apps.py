from django.apps import AppConfig


class TabsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # type: ignore
    name = 'tabs'

    def ready(self):
        import tabs.signals