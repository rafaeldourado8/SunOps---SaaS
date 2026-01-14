"""
Django Model para Painel
"""
from django.db import models
import uuid


class PainelModel(models.Model):
    """Model Django para Painel Solar"""
    
    TIPO_CHOICES = [
        ('MONOCRISTALINO', 'Monocristalino'),
        ('POLICRISTALINO', 'Policristalino'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    marca_id = models.UUIDField()
    fornecedor_id = models.UUIDField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    potencia = models.DecimalField(max_digits=10, decimal_places=2)
    eficiencia = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='MONOCRISTALINO')
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'paineis'
        verbose_name = 'Painel Solar'
        verbose_name_plural = 'Painéis Solares'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['marca_id']),
            models.Index(fields=['fornecedor_id']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.potencia}W"
