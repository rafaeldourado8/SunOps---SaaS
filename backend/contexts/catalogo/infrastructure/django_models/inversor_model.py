"""
Django Model para Inversor
"""
from django.db import models
import uuid


class InversorModel(models.Model):
    """Model Django para Inversor"""
    
    TIPO_CHOICES = [
        ('STRING', 'String'),
        ('MICROINVERSOR', 'Microinversor'),
    ]
    
    FASES_CHOICES = [
        (1, 'Monofásico'),
        (3, 'Trifásico'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    marca_id = models.UUIDField()
    fornecedor_id = models.UUIDField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    potencia = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='STRING')
    fases = models.IntegerField(choices=FASES_CHOICES, default=1)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inversores'
        verbose_name = 'Inversor'
        verbose_name_plural = 'Inversores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['marca_id']),
            models.Index(fields=['fornecedor_id']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.potencia}kW"
