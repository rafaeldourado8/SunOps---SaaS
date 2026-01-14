import redis
from typing import Optional
import json
from decouple import config


class CacheManager:
    """Gerencia cache Redis para tenant info e sessions"""
    
    _client: Optional[redis.Redis] = None
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.Redis(
                host=config('REDIS_HOST', default='redis'),
                port=config('REDIS_PORT', default=6379, cast=int),
                db=0,
                decode_responses=True
            )
        return cls._client
    
    @classmethod
    def get_tenant_info(cls, tenant_slug: str) -> Optional[dict]:
        client = cls.get_client()
        key = f"tenant:{tenant_slug}"
        data = client.get(key)
        return json.loads(data) if data else None
    
    @classmethod
    def set_tenant_info(cls, tenant_slug: str, tenant_data: dict, ttl: int = 3600):
        client = cls.get_client()
        key = f"tenant:{tenant_slug}"
        client.setex(key, ttl, json.dumps(tenant_data))
    
    @classmethod
    def delete_tenant_info(cls, tenant_slug: str):
        client = cls.get_client()
        key = f"tenant:{tenant_slug}"
        client.delete(key)
