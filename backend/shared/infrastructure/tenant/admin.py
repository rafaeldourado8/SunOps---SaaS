from django.contrib import admin
from shared.infrastructure.tenant.models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nome', 'db_name', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('slug', 'nome', 'db_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
