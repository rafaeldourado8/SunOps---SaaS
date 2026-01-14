"""
Value Object: Email
Complexidade Ciclomática: 2
"""
import re


class Email:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, valor: str):
        limpo = valor.strip().lower()
        self._validar(limpo)
        self._valor = limpo
    
    def _validar(self, email: str) -> None:
        if not email:
            raise ValueError("Email não pode ser vazio")
        
        if not self.EMAIL_REGEX.match(email):
            raise ValueError(f"Email inválido: {email}")
    
    @property
    def valor(self) -> str:
        return self._valor
    
    def __str__(self) -> str:
        return self._valor
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Email) and self._valor == other._valor
    
    def __hash__(self) -> int:
        return hash(self._valor)
