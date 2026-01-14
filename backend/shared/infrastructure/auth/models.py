from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model com roles para multi-tenancy"""
    
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'Admin'
        VENDEDOR = 'VENDEDOR', 'Vendedor'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VENDEDOR
    )
    tenant_slug = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
