"""
Django Model para Vendedor (Infrastructure Layer)
"""
from django.db import models
import uuid


class VendedorModel(models.Model):
    """Model Django para persistir Vendedor."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    telefone = models.CharField(max_length=20)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vendedores'
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.comissao_percentual}%)"
