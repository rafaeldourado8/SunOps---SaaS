"""App config."""
from django.apps import AppConfig


class FinanceiroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared.infrastructure.financeiro'
    label = 'financeiro'
