from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from shared.infrastructure.tenant.models import Tenant
from shared.infrastructure.tenant.connection_manager import TenantConnectionManager
from shared.infrastructure.cache.cache_manager import CacheManager
from django.db import connection


class TenantMiddleware(BaseHTTPMiddleware):
    """Resolve tenant por subdomain ou header X-Tenant-Slug"""
    
    # Rotas que não precisam de tenant
    EXCLUDED_PATHS = [
        "/health",
        "/",
        "/docs",
        "/openapi.json",
        "/static",
        "/ws/chat",
        "/api/chat"
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Verifica se rota está excluída
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        tenant_slug = self._extract_tenant_slug(request)
        
        if not tenant_slug:
            raise HTTPException(status_code=400, detail="Tenant não identificado")
        
        # Busca tenant no cache
        tenant_data = CacheManager.get_tenant_info(tenant_slug)
        
        if not tenant_data:
            # Busca no banco MASTER
            tenant_data = self._get_tenant_from_db(tenant_slug)
            if tenant_data:
                CacheManager.set_tenant_info(tenant_slug, tenant_data)
        
        if not tenant_data or not tenant_data.get('ativo'):
            raise HTTPException(status_code=404, detail="Tenant não encontrado ou inativo")
        
        # Define tenant na thread atual
        TenantConnectionManager.set_tenant(tenant_slug, tenant_data)
        
        # Adiciona tenant ao request state
        request.state.tenant_slug = tenant_slug
        request.state.tenant_data = tenant_data
        
        response = await call_next(request)
        
        # Limpa tenant após request
        TenantConnectionManager.clear()
        
        return response
    
    def _extract_tenant_slug(self, request: Request) -> str:
        # Prioridade 1: Header X-Tenant-Slug
        tenant_slug = request.headers.get('X-Tenant-Slug')
        if tenant_slug:
            return tenant_slug
        
        # Prioridade 2: Subdomain (ex: solar-abc.ops-crm.com)
        host = request.headers.get('host', '')
        if '.' in host:
            return host.split('.')[0]
        
        return None
    
    def _get_tenant_from_db(self, tenant_slug: str) -> dict:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT slug, nome, db_name, db_host, db_port, ativo FROM tenants WHERE slug = %s",
                    [tenant_slug]
                )
                row = cursor.fetchone()
                if row:
                    return {
                        'slug': row[0],
                        'nome': row[1],
                        'db_name': row[2],
                        'db_host': row[3],
                        'db_port': row[4],
                        'ativo': row[5],
                        'db_user': 'postgres',
                        'db_password': 'postgres_dev_password'
                    }
        except Exception:
            pass
        return None
