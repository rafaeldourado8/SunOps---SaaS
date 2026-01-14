from django.contrib import admin
from config.admin import superadmin_site
from shared.infrastructure.tenant.models import Tenant


@admin.register(Tenant, site=superadmin_site)
class TenantSuperAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nome', 'db_name', 'db_host', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('slug', 'nome', 'db_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações do Tenant', {
            'fields': ('slug', 'nome', 'ativo')
        }),
        ('Configuração Database', {
            'fields': ('db_name', 'db_host', 'db_port')
        }),
        ('Metadados', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
