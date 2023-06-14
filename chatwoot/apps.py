from django.apps import AppConfig


class ChatwootConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatwoot'

    def ready(self):
        import chatwoot.signals
    
    
