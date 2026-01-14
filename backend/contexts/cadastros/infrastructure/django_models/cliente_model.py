"""
Django Model para Cliente (Infrastructure Layer)

Adapter que mapeia Entity Cliente para PostgreSQL.
SOLID: Dependency Inversion - implementa persistência
"""
from django.db import models
import uuid


class ClienteModel(models.Model):
    """
    Model Django para persistir Cliente.
    
    Mapeia Entity Cliente → Tabela PostgreSQL
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=18, unique=True, db_index=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['documento']),
            models.Index(fields=['email']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.documento})"
