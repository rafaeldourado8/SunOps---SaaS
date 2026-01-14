"""
Django Admin para Cadastros
"""
from django.contrib import admin
from contexts.cadastros.infrastructure.django_models.cliente_model import ClienteModel
from contexts.cadastros.infrastructure.django_models.vendedor_model import VendedorModel
from contexts.cadastros.infrastructure.django_models.fornecedor_model import FornecedorModel


@admin.register(ClienteModel)
class ClienteAdmin(admin.ModelAdmin):
    """Admin customizado para Cliente"""
    
    list_display = ('nome', 'documento', 'email', 'telefone', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('nome', 'documento', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'documento', 'email', 'telefone')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VendedorModel)
class VendedorAdmin(admin.ModelAdmin):
    """Admin customizado para Vendedor"""
    
    list_display = ('nome', 'email', 'telefone', 'comissao_percentual', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('nome', 'email', 'telefone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Comissão', {
            'fields': ('comissao_percentual',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FornecedorModel)
class FornecedorAdmin(admin.ModelAdmin):
    """Admin customizado para Fornecedor"""
    
    list_display = ('nome', 'cnpj', 'email', 'telefone', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('nome', 'cnpj', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'email', 'telefone')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
