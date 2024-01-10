from django.apps import AppConfig


class AgentsCommissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents_commissions'
    def ready(self):
        import agents_commissions.signals