from django.apps import AppConfig


class ThinkificConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thinkific'

    def ready(self):
        import thinkific.signals

