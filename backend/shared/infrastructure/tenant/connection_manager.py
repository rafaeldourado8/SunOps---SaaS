from typing import Optional
from django.db import connections
from django.conf import settings
import threading


class TenantConnectionManager:
    """Gerencia conexões database-per-tenant"""
    
    _local = threading.local()
    
    @classmethod
    def set_tenant(cls, tenant_slug: str, db_config: dict):
        """Define tenant atual e configura conexão"""
        cls._local.tenant_slug = tenant_slug
        cls._local.db_config = db_config
        
        # Adiciona database ao settings do Django
        if tenant_slug not in settings.DATABASES:
            settings.DATABASES[tenant_slug] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_config['db_name'],
                'USER': db_config.get('db_user', 'postgres'),
                'PASSWORD': db_config.get('db_password', 'postgres_dev_password'),
                'HOST': db_config.get('db_host', 'postgres'),
                'PORT': db_config.get('db_port', 5432),
            }
    
    @classmethod
    def get_tenant_slug(cls) -> Optional[str]:
        """Retorna slug do tenant atual"""
        return getattr(cls._local, 'tenant_slug', None)
    
    @classmethod
    def get_connection(cls):
        """Retorna conexão do tenant atual"""
        tenant_slug = cls.get_tenant_slug()
        if not tenant_slug:
            raise ValueError("Tenant não definido")
        return connections[tenant_slug]
    
    @classmethod
    def clear(cls):
        """Limpa tenant atual"""
        cls._local.tenant_slug = None
        cls._local.db_config = None
