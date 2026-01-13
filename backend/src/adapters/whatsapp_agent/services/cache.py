import redis.asyncio as redis
import json
import hashlib
from typing import Optional, Any


class CacheService:
    """Serviço de cache Redis para economia de tokens"""
    
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    async def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache"""
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Armazena valor no cache com TTL"""
        await self.redis.setex(key, ttl, json.dumps(value))
    
    async def get_or_compute(self, key: str, compute_fn, ttl: int = 3600) -> Any:
        """Busca no cache ou computa se não existir"""
        cached = await self.get(key)
        if cached:
            return cached
        
        value = await compute_fn()
        await self.set(key, value, ttl)
        return value
    
    def generate_key(self, *args) -> str:
        """Gera chave de cache baseada em argumentos"""
        content = "|".join(str(arg) for arg in args)
        return hashlib.md5(content.encode()).hexdigest()
