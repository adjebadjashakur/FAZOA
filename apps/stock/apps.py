from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'apps.stock'
    verbose_name = 'Stock Management'

    def ready(self):
        """Register signals when app is ready."""
        import apps.stock.signals
