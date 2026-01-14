"""
Django Model para Fornecedor
"""
from django.db import models
import uuid


class FornecedorModel(models.Model):
    """Model Django para Fornecedor"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True, db_index=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fornecedores'
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cnpj']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.cnpj}"
