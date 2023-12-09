from django.apps import AppConfig


class ApiMarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_market'

    def ready(self):
        import api_market.signals