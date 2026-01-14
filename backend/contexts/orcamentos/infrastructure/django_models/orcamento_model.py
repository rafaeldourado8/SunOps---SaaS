"""
Django Model para Orcamento
"""
from django.db import models
import uuid


class OrcamentoModel(models.Model):
    """Model Django para Orçamento"""
    
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('ENVIADO', 'Enviado'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente_id = models.UUIDField()
    vendedor_id = models.UUIDField()
    kit_nome = models.CharField(max_length=200)
    kit_itens = models.JSONField(default=list)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orcamentos'
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cliente_id']),
            models.Index(fields=['vendedor_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Orçamento {self.id} - R$ {self.valor_total}"
