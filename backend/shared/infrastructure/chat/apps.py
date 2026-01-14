"""App config para chat."""
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared.infrastructure.chat'
    label = 'chat'
