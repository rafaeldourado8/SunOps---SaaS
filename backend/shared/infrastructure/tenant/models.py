from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """Modelo de Tenant no banco MASTER"""
    
    slug = models.SlugField(unique=True, max_length=50)
    nome = models.CharField(max_length=200)
    db_name = models.CharField(max_length=100, unique=True)
    db_host = models.CharField(max_length=255, default='postgres')
    db_port = models.IntegerField(default=5432)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'tenants'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.slug})"
