"""
Django App Config
"""
from django.apps import AppConfig


class CadastrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contexts.cadastros.infrastructure.django_models'
    label = 'cadastros'
    verbose_name = 'Cadastros'
