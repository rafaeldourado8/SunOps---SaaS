import redis
import os
from typing import Optional
import json

class RedisClient:
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            cls._instance = redis.from_url(redis_url, decode_responses=True)
        return cls._instance
    
    @classmethod
    def set_cache(cls, key: str, value: any, expire: int = 300):
        """Cache com expiração em segundos (padrão: 5 min)"""
        client = cls.get_instance()
        client.setex(key, expire, json.dumps(value))
    
    @classmethod
    def get_cache(cls, key: str) -> Optional[any]:
        """Recupera cache"""
        client = cls.get_instance()
        value = client.get(key)
        return json.loads(value) if value else None
    
    @classmethod
    def delete_cache(cls, key: str):
        """Remove cache"""
        client = cls.get_instance()
        client.delete(key)
    
    @classmethod
    def set_session(cls, session_id: str, data: dict, expire: int = 240):
        """Sessão com expiração em segundos (padrão: 4 min)"""
        cls.set_cache(f"session:{session_id}", data, expire)
    
    @classmethod
    def get_session(cls, session_id: str) -> Optional[dict]:
        """Recupera sessão"""
        return cls.get_cache(f"session:{session_id}")
    
    @classmethod
    def delete_session(cls, session_id: str):
        """Remove sessão"""
        cls.delete_cache(f"session:{session_id}")
