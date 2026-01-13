from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

class PasswordHasher:
    """SRP: Responsável apenas por hash de senhas"""
    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256", "django_pbkdf2_sha256"], deprecated="auto")
    
    def hash(self, password: str) -> str:
        return self._context.hash(password)
    
    def verify(self, plain: str, hashed: str) -> bool:
        return self._context.verify(plain, hashed)

class TokenGenerator:
    """SRP: Responsável apenas por geração de tokens JWT"""
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self._secret = secret_key
        self._algorithm = algorithm
    
    def create_access_token(self, subject: str, expires_minutes: int = 30) -> str:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        payload = {"sub": subject, "exp": expire, "type": "access"}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
    
    def create_refresh_token(self, subject: str, expires_days: int = 7) -> str:
        expire = datetime.utcnow() + timedelta(days=expires_days)
        payload = {"sub": subject, "exp": expire, "type": "refresh"}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
    
    def decode(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])
