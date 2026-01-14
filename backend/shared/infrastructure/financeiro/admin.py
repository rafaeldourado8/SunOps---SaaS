"""Admin para configurações financeiras."""
from django.contrib import admin
from .models import ConfiguracaoFinanceira, AuditoriaFinanceira


@admin.register(ConfiguracaoFinanceira)
class ConfiguracaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ['id', 'margem_lucro_minima', 'comissao_percentual', 'imposto_percentual', 'ativo', 'atualizado_em']
    list_filter = ['ativo']
    readonly_fields = ['atualizado_em']
    
    fieldsets = (
        ('Percentuais', {
            'fields': ('comissao_percentual', 'imposto_percentual', 'margem_lucro_minima')
        }),
        ('Custos Fixos', {
            'fields': ('custo_montagem_por_painel', 'custo_operacional_fixo')
        }),
        ('Arredondamento', {
            'fields': ('arredondamento_multiplo',)
        }),
        ('Controle', {
            'fields': ('ativo', 'atualizado_por', 'atualizado_em')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.atualizado_por = request.user.username
        
        # Auditoria
        if change:
            for field in ['comissao_percentual', 'imposto_percentual', 'margem_lucro_minima']:
                if field in form.changed_data:
                    AuditoriaFinanceira.objects.create(
                        admin_nome=request.user.username,
                        acao='ALTEROU_' + field.upper(),
                        campo_alterado=field,
                        valor_anterior=str(form.initial.get(field)),
                        valor_novo=str(form.cleaned_data.get(field))
                    )
        
        super().save_model(request, obj, form, change)


@admin.register(AuditoriaFinanceira)
class AuditoriaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'admin_nome', 'acao', 'campo_alterado', 'valor_anterior', 'valor_novo']
    list_filter = ['admin_nome', 'acao', 'timestamp']
    readonly_fields = ['admin_nome', 'acao', 'campo_alterado', 'valor_anterior', 'valor_novo', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
