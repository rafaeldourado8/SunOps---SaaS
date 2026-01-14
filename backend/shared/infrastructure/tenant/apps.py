from django.apps import AppConfig


class TenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared.infrastructure.tenant'
    verbose_name = 'Multi-Tenancy'
    
    def ready(self):
        # Import superadmin para registrar models
        import shared.infrastructure.tenant.superadmin
