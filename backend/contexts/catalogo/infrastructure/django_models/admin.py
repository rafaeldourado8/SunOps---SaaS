"""
Django Admin para Catálogo
"""
from django.contrib import admin
from contexts.catalogo.infrastructure.django_models.marca_model import MarcaModel
from contexts.catalogo.infrastructure.django_models.painel_model import PainelModel
from contexts.catalogo.infrastructure.django_models.inversor_model import InversorModel


@admin.register(MarcaModel)
class MarcaAdmin(admin.ModelAdmin):
    """Admin customizado para Marca"""
    
    list_display = ('nome', 'ativo', 'created_at')
    list_filter = ('ativo', 'created_at')
    search_fields = ('nome',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações', {
            'fields': ('nome', 'ativo')
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PainelModel)
class PainelAdmin(admin.ModelAdmin):
    """Admin customizado para Painel"""
    
    list_display = ('nome', 'potencia', 'tipo', 'preco', 'ativo', 'created_at')
    list_filter = ('ativo', 'tipo', 'created_at')
    search_fields = ('nome',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'marca_id', 'fornecedor_id', 'preco')
        }),
        ('Especificações', {
            'fields': ('potencia', 'eficiencia', 'tipo')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InversorModel)
class InversorAdmin(admin.ModelAdmin):
    """Admin customizado para Inversor"""
    
    list_display = ('nome', 'potencia', 'tipo', 'fases', 'preco', 'ativo', 'created_at')
    list_filter = ('ativo', 'tipo', 'fases', 'created_at')
    search_fields = ('nome',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'marca_id', 'fornecedor_id', 'preco')
        }),
        ('Especificações', {
            'fields': ('potencia', 'tipo', 'fases')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
