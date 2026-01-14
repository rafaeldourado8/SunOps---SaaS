"""
Django Admin para Orçamentos
"""
from django.contrib import admin
from contexts.orcamentos.infrastructure.django_models.orcamento_model import OrcamentoModel


@admin.register(OrcamentoModel)
class OrcamentoAdmin(admin.ModelAdmin):
    """Admin customizado para Orçamento"""
    
    list_display = ('id', 'kit_nome', 'valor_total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('kit_nome',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações', {
            'fields': ('cliente_id', 'vendedor_id', 'kit_nome', 'valor_total', 'status')
        }),
        ('Kit', {
            'fields': ('kit_itens',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
